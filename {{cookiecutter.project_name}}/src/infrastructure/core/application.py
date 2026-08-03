from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator
import sentry_sdk
from sentry_sdk.integrations.otlp import OTLPIntegration
from starlette.middleware.base import BaseHTTPMiddleware

from api.health import health_routes
from src.api import v1_routes

from ..clients.postgres.engine import init_database
from .constants import responses
from .errors.exceptions import OtherError
from .log_config import init_logging
from .middlewares.trace_id import handle_trace_id
from .middlewares.error_handling import ExceptionHandler, FastAPIErrorHandler, OtherErrorHandler, ValidationErrorHandler
from .middlewares.log_requests import log_requests
from .settings import AppConfig, EnvironmentEnum, get_config
from .telemetry import setup_otel


def create_app() -> FastAPI:
    config: AppConfig = get_config()

    init_logging(config)
    init_database(config)

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
        responses=responses,
        swagger_ui_init_oauth={
            "clientId": config.APP_NAME.lower(),
            "appName": config.APP_NAME.lower(),
            "scopes": ("openid", "email"),
            "usePkceWithAuthorizationCodeGrant": False,
        },
    )

    setup_otel(config, app)

    app.add_middleware(BaseHTTPMiddleware, dispatch=handle_trace_id)
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

    if config.ENVIRONMENT == EnvironmentEnum.PROD:
        sentry_sdk.init(
            dsn=config.SENTRY_DSN, integrations=[OTLPIntegration()], send_default_pii=True, enable_logs=True
        )
        Instrumentator(
            excluded_handlers=["/health/live", "/health/ready", "/metrics"]
        ).instrument(app).expose(app, include_in_schema=False)

    app.include_router(health_routes)
    app.include_router(v1_routes)

    return app
