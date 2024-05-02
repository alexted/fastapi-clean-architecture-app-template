from dataclasses import dataclass
from typing import Any

from pydantic import UUID4


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
    code: int = None
    error: str = None
    message: str = None
    trace_id: UUID4 = None
