import json
import typing as t
import logging
from functools import wraps

import httpx

logger = logging.getLogger(__name__)

Middleware = t.Optional[
    list[t.Callable[[dict, t.Callable[..., t.Awaitable[httpx.Response]]], t.Awaitable[httpx.Response]]]
]


class HttpClient:
    def __init__(
        self, base_url: str, query_params: dict = None, headers: dict = None, verify: bool = False, **session_params
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._query_params = query_params or {}
        self._headers = headers or {}
        self._verify = verify
        self._session_params = session_params
        self._session: t.Optional[httpx.AsyncClient] = httpx.AsyncClient(
                base_url=self._base_url,
                params=self._query_params,
                headers=self._headers,
                verify=self._verify,
                **self._session_params,
            )

    async def __aenter__(self) -> t.Self:
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def close(self) -> None:
        await self._session.aclose()

    async def call(
        self,
        path: str = "",
        method: str = "GET",
        data: t.Optional[dict] = None,
        json_data: t.Optional[t.Any] = None,
        params: t.Optional[dict] = None,
        headers: t.Optional[dict] = None,
        timeout: t.Optional[int] = None,
        files: t.Optional[bytes] = None,
        **kwargs,
    ) -> httpx.Response:
        headers = {**self._headers, **(headers or {})}
        if json_data is not None:
            json_data = json.dumps(json_data, ensure_ascii=False) if not isinstance(json_data, str) else json_data
            headers.setdefault("Content-Type", "application/json")
            data = json_data

        url = f"{self._base_url}/{path.lstrip('/')}"
        logger.debug(
            json.dumps(
                {"method": method, "url": url, "params": params, "headers": headers, "data": data},
                default=str,
                indent=2,
            )
        )

        response = await self._session.request(
            method=method, url=url, data=data, headers=headers, params=params, timeout=timeout, files=files, **kwargs
        )

        logger.debug(json.dumps({"status": response.status_code, "response": response.text}, default=str, indent=2))
        response.raise_for_status()
        return response


class ApiCall:
    def __init__(self, client: HttpClient, path: str = "", method: str = "GET", middleware: Middleware = None) -> None:
        self._client = client
        self._path = path
        self._method = method
        self._handler = self._compose_middleware(middleware)

    def _compose_middleware(self, middleware: Middleware) -> t.Callable[[dict], t.Awaitable[httpx.Response]]:
        handler = self._call
        if middleware:
            for mw in reversed(middleware):
                handler = self._wrap_middleware(mw, handler)
        return handler

    @staticmethod
    def _wrap_middleware(
        middleware: t.Callable, handler: t.Callable[[dict], t.Awaitable[httpx.Response]]
    ) -> t.Callable[[dict], t.Awaitable[httpx.Response]]:
        @wraps(handler)
        async def wrapped(parameters: dict) -> httpx.Response:
            return await middleware(parameters, handler)

        return wrapped

    async def _call(self, parameters: dict) -> httpx.Response:
        path_params = parameters.pop("path_params", {})
        path = self._path.format(**path_params) if path_params else self._path

        parameters["headers"] = {**self._client._headers, **parameters.get("headers", {})}
        parameters["method"] = self._method

        return await self._client.call(path=path, **parameters)

    async def __call__(self, **kwargs) -> t.Any:
        return await self._handler({k: v for k, v in kwargs.items() if v is not None})
