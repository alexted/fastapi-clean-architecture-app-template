import sentry_sdk
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from markdown2 import markdown_path
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from src import api
from src.app.config import config, EnvironmentEnum
from src.app.logging import init_logging
from src.utils.errors.handlers import ExceptionsHandler
from src.utils.middlewares.error_handling import error_handler, COMMON_ERROR_HANDLERS, error_handling_middleware
from src.utils.middlewares.request_id import handle_request_id

healthcheck_route = APIRouter()


@healthcheck_route.get('/health')
def health_check():
    return {'status': 'ok'}


def create_app():
    init_logging()

    app = FastAPI(title='{{ cookiecutter.project_name }}', description=markdown_path(config.README_PATH))

    app.include_router(healthcheck_route, tags=['system'])
    app.include_router(api.sum_routes, prefix='/v1', tags=['v1'])
    {% if cookiecutter.use_postgresql|lower == 'y' -%}
    app.include_router(api.items_routes, prefix='/v1', tags=['v1'])
    {% endif %}

    app.exception_handlers[HTTPException] = error_handler(ExceptionsHandler(*COMMON_ERROR_HANDLERS))
    app.exception_handlers[RequestValidationError] = error_handler(ExceptionsHandler(*COMMON_ERROR_HANDLERS))

    if config.ENVIRONMENT == EnvironmentEnum.PROD:
        sentry_sdk.init(environment=config.ENVIRONMENT, dsn=config.SENTRY_DSN)
        app.add_middleware(SentryAsgiMiddleware)
    app.add_middleware(
        BaseHTTPMiddleware, dispatch=error_handling_middleware(ExceptionsHandler(*COMMON_ERROR_HANDLERS)),
    )
    app.add_middleware(BaseHTTPMiddleware, dispatch=handle_request_id)

    return app
