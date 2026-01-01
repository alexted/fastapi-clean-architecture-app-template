from uuid import uuid4
from contextvars import ContextVar
from collections.abc import Callable

from fastapi import Request, Response

CORRELATION_ID: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def set_transaction_id(correlation_id: str) -> None:
    """
    Set Sentry's event transaction ID as the current correlation ID.

    The transaction ID is displayed in a Sentry event's detail view,
    which makes it easier to correlate logs to specific events.
    """
    from sentry_sdk import configure_scope

    with configure_scope() as scope:
        scope.set_tag("transaction_id", correlation_id)


def get_sentry_extension() -> Callable[[str], None]:
    """
    Return set_transaction_id, if the Sentry-sdk is installed.
    """
    try:
        import sentry_sdk  # noqa: F401, TC002

        return set_transaction_id
    except ImportError:  # pragma: no cover
        return lambda correlation_id: None


sentry_extension = get_sentry_extension()


async def handle_correlation_id(request: Request, call_next: Callable) -> Response:
    correlation_id: str = request.headers.get("X-Request-ID", str(uuid4()))
    request.state.correlation_id = correlation_id
    CORRELATION_ID.set(correlation_id)
    sentry_extension(correlation_id)
    response: Response = await call_next(request)
    response.headers["X-Request-ID"] = correlation_id
    CORRELATION_ID.set(None)
    return response
