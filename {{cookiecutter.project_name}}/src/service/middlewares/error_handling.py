import logging
from datetime import datetime

from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from ..errors.handlers import (
    FastAPIErrorHandler,
    ValidationErrorHandler,
    ExceptionsHandler,
    OurErrorHandler,
)

COMMON_ERROR_HANDLERS = [
    FastAPIErrorHandler,
    ValidationErrorHandler,
    OurErrorHandler,
]

logger = logging.getLogger(__name__)


def error_handler(exceptions_handler: ExceptionsHandler):
    async def handle_errors(request: Request, exc) -> Response:
        return _make_response(exceptions_handler, exc)

    return handle_errors


def error_handling_middleware(exceptions_handler: ExceptionsHandler):
    async def handle_errors(request: Request, call_next) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            return _make_response(exceptions_handler, exc)

    return handle_errors


def _make_response(exceptions_handler: ExceptionsHandler, exc) -> JSONResponse:
    error = exceptions_handler.get_error(exc)
    data = {
        'code': error.code,
        'error': error.error,
        'message': error.message,
        'trace_id': error.trace_id,
        'timestamp': datetime.utcnow().isoformat()
    }

    return JSONResponse(status_code=error.code, content=data)
