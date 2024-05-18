from enum import StrEnum
from pathlib import Path

from pydantic import ConfigDict, HttpUrl, PostgresDsn, RedisDsn, KafkaDsn
from pydantic_settings import BaseSettings

CONFIG_FILE = Path('.env').as_posix() if Path('.env').exists() else None


class EnvironmentEnum(StrEnum):
    LOCAL = 'LOCAL'
    TESTING = 'TESTING'
    TEST = 'TEST'
    DEV = 'DEV'
    STAGE = 'STAGE'
    PROD = 'PROD'


class LoggingLevelEnum(StrEnum):
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'


class AppConfig(BaseSettings):
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL
    APP_NAME: str = "{{ cookiecutter.project_name|lower|replace(' ', '_')|replace('-', '_') }}"

    SENTRY_DSN: HttpUrl = "https://omg.wtf/"

    LOG_LEVEL: LoggingLevelEnum = LoggingLevelEnum.INFO

    {% if cookiecutter.use_postgresql | lower == 'y' -%}
    POSTGRES_DSN: PostgresDsn
    POSTGRES_MAX_CONNECTIONS: int = 20
    {% endif %}
    {% if cookiecutter.use_redis | lower == 'y' -%}
    REDIS_DSN: RedisDsn
    {% endif %}
    {% if cookiecutter.use_kafka | lower == 'y' -%}
    KAFKA_DSN: KafkaDsn | str
    {% endif %}

    model_config = ConfigDict(use_enum_values=True)



config: AppConfig = AppConfig(_env_file=CONFIG_FILE, _env_file_encoding='utf-8')
