#!/bin/bash

[ -v ENVIRONMENT ] && export ENVIRONMENT=${ENVIRONMENT:-'LOCAL'}

if [[ ${ENVIRONMENT} = 'LOCAL' ]]; then
    exec gunicorn "src.service.application:create_app()" -n {{cookiecutter.project_name}} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 --log-level=debug
else
    echo "Running database migrations..."
    alembic upgrade head
    echo "Starting application..."
    exec gunicorn "src.service.application:create_app()" -n {{cookiecutter.project_name}} -k uvicorn.workers.UvicornWorker -w "${CONCURRENCY:-8}" -b 0.0.0.0:5000
fi
