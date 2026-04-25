FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app

ENV PATH="/home/nonroot/.local/bin:$PATH"

RUN pip install --no-cache-dir poetry poetry-plugin-export

COPY pyproject.toml poetry.lock* ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY --from=builder /app/venv /app/venv

ENV PATH="/app/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY . .

EXPOSE 5000

ENTRYPOINT ["python", "entrypoint.py"]
