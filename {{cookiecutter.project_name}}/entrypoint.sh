#!/bin/bash

[ -v ENVIRONMENT ] && export ENVIRONMENT=${ENVIRONMENT:-'LOCAL'}

if [[ ${ENVIRONMENT} = 'LOCAL' ]]; then
    exec gunicorn asgi:app -n {{cookiecutter.project_name}} -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000 --log-level=debug
else
    exec gunicorn asgi:app -n {{cookiecutter.project_name}} -k uvicorn.workers.UvicornWorker -w "${CONCURRENCY:-8}" -b 0.0.0.0:5000 --timeout=600
fi
