FROM python:{{ cookiecutter.app_lang_version }}-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
# Pull official base image
FROM python:{{ cookiecutter.app_lang_version }}-slim

# Set work directory
WORKDIR /usr/src/app

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

# Publish network port
EXPOSE 5000

# Execute script to start the application web server
ENTRYPOINT ["./entrypoint.sh"]
