from __future__ import annotations

from granian import Granian
from granian.constants import Interfaces
from granian.log import LogLevels

from src.infrastructure.core.settings  import get_config, EnvironmentEnum

def main():
    # Инициализируем конфиг ОДИН РАЗ на старте процесса.
    # Все последующие вызовы get_config() в приложении вернут этот же объект из кэша.
    config = get_config()

    # Динамическая настройка на основе строго типизированного окружения
    if config.ENVIRONMENT == EnvironmentEnum.LOCAL:
        # Локально: дебаг, 1 воркер, горячая перезагрузка
        log_level = LogLevels.debug
        workers = 1
        reload = True
    else:
        # Продакшен/Стейджинг: берем настройки из конфига Pydantic
        # getattr безопасно сопоставляет твой LoggingLevelEnum с энумом Granian
        log_level = getattr(LogLevels, config.LOG_LEVEL.lower(), LogLevels.info)
        workers = config.SERVER_WORKERS
        reload = False

    print(f"Starting Granian server in {config.ENVIRONMENT} mode...", flush=True)

    Granian(
        target="src.infrastructure.core.application:create_app", # Убедись, что путь корректный
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
