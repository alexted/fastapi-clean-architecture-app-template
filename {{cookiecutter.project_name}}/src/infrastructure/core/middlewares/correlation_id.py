from __future__ import annotations

from uuid import uuid7
from typing import TYPE_CHECKING
from contextvars import ContextVar

import sentry_sdk
from opentelemetry import trace

if TYPE_CHECKING:
    from collections.abc import Callable

    from fastapi import Request, Response


CORRELATION_ID: ContextVar[str | None] = ContextVar("correlation_id", default=None)


async def handle_correlation_id(request: Request, call_next: Callable) -> Response:
    correlation_id = request.headers.get("X-Request-ID", str(uuid7()))
    request.state.correlation_id = correlation_id
    CORRELATION_ID.set(correlation_id)

    span = trace.get_current_span()
    if span.is_recording():
        span.set_attribute("correlation_id", correlation_id)

    sentry_sdk.set_tag("correlation_id", correlation_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = correlation_id
    CORRELATION_ID.set(None)
    return response
