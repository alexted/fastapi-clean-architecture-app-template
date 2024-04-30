from dataclasses import dataclass
from typing import Any


class ErrorType:
    VALIDATION_ERROR = 'VALIDATION_ERROR'
    INTERNAL_ERROR = 'INTERNAL_ERROR'
    EXTERNAL_SERVICE_ERROR = 'EXTERNAL_SERVICE_ERROR'
    BAD_REQUEST = 'BAD_REQUEST'
    NOT_FOUND = 'NOT_FOUND'
    EXPIRED_TOKEN = 'EXPIRED_TOKEN'
    BAD_TOKEN = 'BAD_TOKEN'
    ACCESS_DENIED = 'ACCESS_DENIED'


@dataclass
class Error:
    status: int = None
    error: str = None
    message: str = None
    detail: Any = None
