{% if cookiecutter.use_postgresql | lower == 'y' -%}
from src.api.endpoints.items import routes as items_routes
{% endif -%}
from src.api.endpoints.sum import routes as sum_routes

__all__ = (
    'sum_routes',
{% if cookiecutter.use_postgresql | lower == 'y' -%}
    'items_routes'
{% endif -%}
)
