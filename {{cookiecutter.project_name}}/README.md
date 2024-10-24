# hrm-core

Our alternative to PeopleForce

## Authors

Uplatform team

## Implementation language

python 3.12

## Deployment environment

Kubernetes

## Service description

Implements the main business logic of the HRM system.

## Documentation

https://plab.atlassian.net/wiki/spaces/AI/pages/87425051/HRM

## Interaction with 3rd party services

* Passport (IdP)

## Scalability

Scalability is done by `Kubernetes` tools, by adding additional pods.
It is possible to scale by `gunicorn`, by adding additional workers.

## Dependencies

pre-requisites:

```bash
$ poetry new hrm-core && cd $_        // create a project virtual environment
```

Install the necessary packages:

```bash
(hrm-core)$ poetry install                // install all project dependencies
(hrm-core)$ poetry install --only main    // install only main project dependencies
```

**Important**:
before running in a container, be sure to execute the ``poetry install'' command,
command to generate poetry.lock - this is the file from which information about dependencies is to be taken when
building the image.
You must also add this file to the git index.

## Startup inside Docker

```bash
$ docker compose up
```

## Run tests

```bash
$ python -m pytest -vvs
```

## Linter

```bash
$ python -m ruff format && python -m ruff check --fix --unsafe-fixes
```

## Set pre-commit hook

```bash
$ pre-commit install
```

## Environment variables

These are the environment variables that you can set for the app to configure it and their default values:

#### `ENVIRONMENT`

String value which defines the runtime environment in which the application runs.

Can have the following values:

* `LOCAL`  *default*
* `TESTING`
* `TEST`
* `STAGE`
* `PROD`

#### `APP_NAME`

The string variable defining the service name.

By default: `HRM-Core`

### Logging

#### `LOG_LEVEL`

String value which defines the logging severity.

Can have the following values:

* `CRITICAL`
* `ERROR`
* `WARNING`
* `INFO`  *default*
* `DEBUG`

#### `SENTRY_URL`

The url that defines address of the Sentry service.

By default, it's not set.

### IdP

#### `IDP_URL`

The url of the Identity and Access Management (IDP) service.

By default, it's not set.

#### `IDP_PUBLIC_KEY`

The public key of the Identity and Access Management (IdP) service.

By default, it's not set.

#### `IDP_CLIENT_SECRET`

The credentials secret of the client (service).

By default, it's not set.

### Databases, MessageBrokers

#### `POSTGRES_DSN`

The dsn that defines connection string to of the PostgreSQL.

By default, it's not set.

#### `POSTGRES_MAX_CONNECTIONS`

The int value to setting to limit the number of connections (and resources that are consumed by connections) to the
PostgreSQL.

By default, it's `10`.

#### `REDIS_DSN`

The dsn that defines connection string to of the Redis.

By default, it's not set.

#### `KAFKA_DSN`

The dsn that defines connection string to of the Kafka.

By default, it's not set.

### S3

#### `S3_URL`

The string that defines url for S3.

By default, it's not set.

#### `S3_ACCESS_KEY`

The string that defines key ID for AWS access.

By default, it's not set.

#### `S3_SECRET_KEY`

The string that defines secret key of AWS account.

By default, it's not set.

#### `AWS_REGION_NAME`

The string that defines region of AWS.

By default, it's not set.

#### `S3_DOCS_BUCKET`

The string that defines S3 bucket name.

By default, it's not set.

#### `S3_IMAGES_BUCKET`

The string that defines S3 bucket name.

By default, it's not set.
