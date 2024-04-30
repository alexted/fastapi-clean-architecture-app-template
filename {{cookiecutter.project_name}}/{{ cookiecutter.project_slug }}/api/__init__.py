{% if cookiecutter.use_postgresql | lower == 'y' -%}
from {{ cookiecutter.project_slug }}.api.endpoints.items import routes as items_routes
{% endif %}
from {{ cookiecutter.project_slug }}.api.endpoints.sum import routes as sum_routes

__all__ = (
    'sum_routes',
{% if cookiecutter.use_postgresql | lower == 'y' -%}
    'items_routes'
{% endif %}
)
