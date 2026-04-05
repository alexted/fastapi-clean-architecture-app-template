from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import UTC, datetime
import logging
from typing import TYPE_CHECKING, Any

from fastapi import Request, Response
from pydantic import BaseModel
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT

from ..errors.constants import ErrorType
from .correlation_id import CORRELATION_ID

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine

    from fastapi.exceptions import HTTPException, RequestValidationError

    from ..errors.exceptions import OtherError

logger = logging.getLogger()


class ErrorSchema(BaseModel):
    error: str
    message: str | list[dict[str, Any]]
    correlation_id: str | None
    timestamp: datetime


class Error(BaseModel):
    status_code: int
    data: ErrorSchema


class BaseErrorHandler(ABC):
    @abstractmethod
    def _get_error(self, request: Request, exc: Exception) -> Error: ...

    @classmethod
    def get_handler(cls) -> Callable[[Request, Exception], Coroutine]:
        instance = cls()

        async def handler(request: Request, exception: Exception) -> Response:
            logger.debug(f"Handling exception: {type(exception)}: {exception}")

            error = instance._get_error(request, exception)
            return Response(status_code=error.status_code, content=error.data.model_dump())

        return handler


class FastAPIErrorHandler(BaseErrorHandler):
    def _get_error(self, request: Request, exception: HTTPException) -> Error:
        return Error(
            status_code=exception.status_code,
            data=ErrorSchema(
                error=ErrorType.INTERNAL_ERROR,
                message=exception.detail,
                correlation_id=CORRELATION_ID.get(),
                timestamp=datetime.now(UTC).isoformat(),
            ),
        )


class ValidationErrorHandler(BaseErrorHandler):
    def _get_error(self, request: Request, exception: RequestValidationError) -> Error:
        return Error(
            status_code=HTTP_422_UNPROCESSABLE_CONTENT,
            data=ErrorSchema(
                error=ErrorType.VALIDATION_ERROR,
                message=exception.errors(),
                correlation_id=CORRELATION_ID.get(),
                timestamp=datetime.now(UTC).isoformat(),
            ),
        )


class OtherErrorHandler(BaseErrorHandler):
    def _get_error(self, request: Request, exception: OtherError) -> Error:
        return Error(
            status_code=exception.code,
            data=ErrorSchema(
                error=exception.type or exception.__class__.__name__,
                message=exception.message,
                correlation_id=CORRELATION_ID.get(),
                timestamp=datetime.now(UTC).isoformat(),
            ),
        )


class ExceptionHandler(BaseErrorHandler):
    def _get_error(self, request: Request, exception: Exception) -> Error:
        logger.exception(f"Unhandled exception: {type(exception)}")
        return Error(
            status_code=500,
            data=ErrorSchema(
                error=ErrorType.INTERNAL_ERROR,
                message=exception.__repr__(),
                correlation_id=CORRELATION_ID.get(),
                timestamp=datetime.now(UTC).isoformat(),
            ),
        )
