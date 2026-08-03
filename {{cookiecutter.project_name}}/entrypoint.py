from __future__ import annotations

from granian import Granian
from granian.constants import Interfaces
from granian.log import LogLevels

from src.infrastructure.core.settings import EnvironmentEnum, get_config


def main():
    config = get_config()

    if config.ENVIRONMENT == EnvironmentEnum.LOCAL:
        log_level = LogLevels.debug
        workers = 1
        reload = True
    else:
        log_level = getattr(LogLevels, config.LOG_LEVEL.lower(), LogLevels.info)
        workers = config.SERVER_WORKERS
        reload = False

    print(f"Starting Granian server in {config.ENVIRONMENT} mode...", flush=True)

    Granian(
        target="src.infrastructure.core.application:create_app",
        address=config.SERVER_HOST,
        port=config.SERVER_PORT,
        workers=workers,
        factory=True,
        reload=reload,
        interface=Interfaces.ASGI,
        log_level=log_level,
    ).serve()

if __name__ == "__main__":
    main()
