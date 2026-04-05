FROM python:3.14-slim AS requirements-stage

WORKDIR /tmp

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry poetry-plugin-export

COPY pyproject.toml poetry.lock* ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid 10001 \
    svc-my-app

COPY --from=requirements-stage /tmp/requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

COPY --chown=svc-my-app:svc-my-app . .

USER svc-my-app

EXPOSE 5000

ENTRYPOINT ["sh", "./entrypoint.sh"]
