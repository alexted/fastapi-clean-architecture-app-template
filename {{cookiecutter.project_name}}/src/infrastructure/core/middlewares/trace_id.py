from __future__ import annotations

from typing import TYPE_CHECKING
from opentelemetry import trace
import sentry_sdk

if TYPE_CHECKING:
    from collections.abc import Callable
    from fastapi import Request, Response


def get_current_trace_id() -> str | None:
    """
    Extracts a 32-character hex trace_id from the current OpenTelemetry context.
    Returns None if there is no valid context.
    """
    span = trace.get_current_span()
    span_context = span.get_span_context()

    if span_context.is_valid:
        return format(span_context.trace_id, "032x")
    return None


async def handle_trace_id(request: Request, call_next: Callable) -> Response:
    response = await call_next(request)

    trace_id = get_current_trace_id()

    if trace_id:
        sentry_sdk.set_tag("trace_id", trace_id)
        response.headers["X-Trace-Id"] = trace_id

    return response
