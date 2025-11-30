from fastapi import FastAPI, Response, APIRouter, HTTPException
import sentry_sdk
from starlette.status import HTTP_200_OK
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from src.api import v1_routes
from src.service.errors.exceptions import OtherError
from src.service.middlewares.error_handling import (
    ExceptionHandler,
    OtherErrorHandler,
    FastAPIErrorHandler,
    ValidationErrorHandler,
)

from .config import AppConfig, EnvironmentEnum, get_config
from .logging_config import init_logging
from .telemetry import setup_otel
from .constants import responses
from .middlewares.log_requests import log_requests
from .middlewares.correlation_id import handle_correlation_id

healthcheck_route = APIRouter(include_in_schema=False)


@healthcheck_route.get("/health", description="liveness probe")
def health_check() -> Response:
    return Response(status_code=HTTP_200_OK)


def create_app() -> FastAPI:
    config: AppConfig = get_config()
    init_logging(config)

    app = FastAPI(
        title=config.APP_NAME,
        description="{{ cookiecutter.project_description }}",
        version="{{ cookiecutter.project_release }}",
        exception_handlers={
            HTTPException: FastAPIErrorHandler.get_handler(),
            RequestValidationError: ValidationErrorHandler.get_handler(),
            OtherError: OtherErrorHandler.get_handler(),
            Exception: ExceptionHandler.get_handler(),
        },
        default_response_class=ORJSONResponse,
        responses=responses,
        swagger_ui_init_oauth={
            "clientId": config.APP_NAME.lower(),
            "appName": config.APP_NAME.lower(),
            "scopes": ("openid", "email"),
            "usePkceWithAuthorizationCodeGrant": False,
        },
        license_info={"name": "Proprietary Software License", "url": "https://{{ cookiecutter.project_name }}.com/license"},
    )

    app.add_middleware(BaseHTTPMiddleware, dispatch=handle_correlation_id)
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)  # Note: logs request and response bodies

    setup_otel(config)

    if config.ENVIRONMENT == EnvironmentEnum.PROD:
        sentry_sdk.init(dsn=config.SENTRY_URL, enable_tracing=True)
        Instrumentator(excluded_handlers=["/health", "/metrics"]).instrument(app).expose(app, include_in_schema=False)

    app.include_router(healthcheck_route, tags=["service"])
    app.include_router(v1_routes)

    return app
