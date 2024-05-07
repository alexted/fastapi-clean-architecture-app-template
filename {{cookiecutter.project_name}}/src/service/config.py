from enum import Enum
from pathlib import Path

from pydantic import HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings

CONFIG_FILE = Path('.env').as_posix() if Path('.env').exists() else None


class EnvironmentEnum(str, Enum):
    LOCAL = 'LOCAL'
    TESTING = 'TESTING'
    TEST = 'TEST'
    DEV = 'DEV'
    STAGE = 'STAGE'
    PROD = 'PROD'


class LoggingLevelEnum(str, Enum):
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'


class AppConfig(BaseSettings):
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL
    APP_NAME: str = "{{ cookiecutter.project_slug }}"

    SENTRY_DSN: HttpUrl = "https://omg.wtf/"

    LOG_LEVEL: LoggingLevelEnum = LoggingLevelEnum.INFO

    {% if cookiecutter.use_postgresql | lower == 'y' -%}
    POSTGRES_DSN: PostgresDsn
    POSTGRES_MAX_CONNECTIONS: int = 20

    {% endif %}

    class Config:
        use_enum_values = True


config: AppConfig = AppConfig(_env_file=CONFIG_FILE, _env_file_encoding='utf-8')
