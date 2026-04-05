from __future__ import annotations

from logging import Logger, getLogger
from time import time
from typing import TYPE_CHECKING

from fastapi.concurrency import iterate_in_threadpool

if TYPE_CHECKING:
    from collections.abc import Callable

    from fastapi import Request, Response

logger: Logger = getLogger("fastapi-app")


async def log_requests(request: Request, call_next: Callable) -> Response:
    if request.url.path in ("/health", "/metrics"):
        return await call_next(request)
    request.state.start_time = time()

    if (
        "multipart/form-data" not in request.headers.get("content-type", "")
        and int(request.headers.get("content-length", "0")) <= 512000
    ):
        request_body: bytes = await request.body()
    else:
        request_body: bytes = b"file"

    response: Response = await call_next(request)

    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))

    logger.info(
        {
            "method": request.method,
            "resource": request.url.path,
            "query_params": request.query_params,
            "headers": dict(request.headers),
            "correlation_id": request.headers.get("X-Request-ID", request.state.correlation_id),
            "client_ip": request.client.host,
            "execution_duration": round(time() - request.state.start_time, 3),
            "response_status": response.status_code,
            "request_body": request_body.decode(),
            "response_body": (b"".join(response_body)).decode(),
        }
    )
    # NOTE: It may make sense to move data logging to a background task to reduce endpoint response time.
    # See the example here: https://stackoverflow.com/a/73464007/8791187
    return response
