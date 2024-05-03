import sentry_sdk
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware

from src.api import v1_routes
from .config import config, EnvironmentEnum
from .logging import init_logging
from .errors.handlers import ExceptionsHandler
from .middlewares.error_handling import error_handler, COMMON_ERROR_HANDLERS
from .middlewares.trace_id import CorrelationIdMiddleware

healthcheck_route = APIRouter()


@healthcheck_route.get('/health')
def health_check():
    return {'status': 'ok'}


def create_app():
    init_logging()

    if config.ENVIRONMENT == EnvironmentEnum.PROD:
        sentry_sdk.init(dsn=config.SENTRY_DSN, enable_tracing=True)

    app = FastAPI(
        title='{{ cookiecutter.project_name }}',
        description="{{ cookiecutter.project_description }}",
        middleware=[Middleware(CorrelationIdMiddleware),],
        exception_handlers={
            HTTPException: error_handler(ExceptionsHandler(*COMMON_ERROR_HANDLERS)),
            RequestValidationError: error_handler(ExceptionsHandler(*COMMON_ERROR_HANDLERS)),
            Exception: error_handler(ExceptionsHandler(*COMMON_ERROR_HANDLERS)),
        },
    )

    app.include_router(healthcheck_route, tags=['service'])
    app.include_router(v1_routes)

    return app
