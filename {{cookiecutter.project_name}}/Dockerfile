FROM python:3.12-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY pyproject.toml ./poetry.lock /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Pull official base image
FROM python:3.12-slim

# Set work directory
WORKDIR /usr/src/app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt
RUN apt update && apt install -y --no-install-recommends gcc python3-dev \
    && pip install --no-cache-dir -U pip setuptools wheel && pip install --no-cache-dir -r requirements.txt \
    && apt purge -y --auto-remove gcc python3-dev

# Copy project files
COPY . .

# Make entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

# Switch to the non-privileged user to run the application.
USER appuser

# Publish network port
EXPOSE 5000

# Execute script to start the application web server
ENTRYPOINT ["./entrypoint.sh"]
