from fastapi import APIRouter

{% if cookiecutter.use_postgresql | lower == 'y' -%}
from src.api.items import routes as items_routes
{% endif -%}
from src.api.numbers import routes as numbers_routes

v1_routes: APIRouter = APIRouter(prefix="/v1")

v1_routes.include_router(numbers_routes)
{% if cookiecutter.use_postgresql | lower == 'y' -%}
v1_routes.include_router(items_routes)
{% endif -%}

__all__ = ("v1_routes",)
