from granian import Granian
from granian.constants import Interfaces
from granian.log import LogLevels

if __name__ == "__main__":
    Granian(
        "src.service.application:create_app",
        factory=True,
        reload=True,
        port=5000,
        interface=Interfaces.ASGI,
        log_level=LogLevels.debug,
    ).serve()
