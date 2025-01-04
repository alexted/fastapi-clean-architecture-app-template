#!/bin/bash

[ -v ENVIRONMENT ] && export ENVIRONMENT=${ENVIRONMENT:-'LOCAL'}

if [[ ${ENVIRONMENT} = 'LOCAL' ]]; then
    exec granian --interface asgi --process-name {{cookiecutter.project_name}} --host 0.0.0.0 --port 5000 --log-level debug --factory --reload "src.service.application:create_app()"
else
    echo "Running database migrations..."
    alembic upgrade head
    echo "Starting application..."
    exec granian --interface asgi --process-name {{cookiecutter.project_name}} --host 0.0.0.0 --port 5000  --workers "${CONCURRENCY:-8}" --factory "src.service.application:create_app"
fi
