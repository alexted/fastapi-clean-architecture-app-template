from enum import Enum
from functools import lru_cache

from pydantic import HttpUrl, KafkaDsn, RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentEnum(str, Enum):
    LOCAL = "LOCAL"
    TESTING = "TESTING"
    TEST = "TEST"
    DEV = "DEV"
    STAGE = "STAGE"
    PROD = "PROD"


class LoggingLevelEnum(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class AppConfig(BaseSettings):
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL
    APP_NAME: str = "HRM-Core"

    # Logging
    SENTRY_DSN: HttpUrl | None = None
    LOG_LEVEL: LoggingLevelEnum = LoggingLevelEnum.INFO

    # Postgres
    POSTGRES_DSN: PostgresDsn
    POSTGRES_MAX_CONNECTIONS: int = 10

    # Redis
    REDIS_DSN: RedisDsn

    # Kafka
    KAFKA_DSN: KafkaDsn | str

    # S3
    S3_DOCS_BUCKET: str = "documents"
    S3_IMAGES_BUCKET: str = "images"
    S3_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    AWS_REGION_NAME: str | None = None

    # Identity provider
    IDP_URL: HttpUrl
    IDP_CLIENT_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", use_enum_values=True, extra="ignore", frozen=True
    )


@lru_cache(maxsize=1)
def get_config() -> AppConfig:
    return AppConfig()
