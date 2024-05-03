import logging
from abc import ABC, abstractmethod
from typing import Type

from fastapi.exceptions import RequestValidationError
from inflection import underscore, parameterize
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from ..errors.constants import Error, ErrorType
from ..errors.exceptions import OtherError

logger = logging.getLogger()


class BaseErrorHandler(ABC):
    handle_exception = None

    def __init__(self):
        if not self.handle_exception:
            raise NotImplementedError()

    @abstractmethod
    def get_error(self, exc: Exception) -> Error:
        pass


class FastAPIErrorHandler(BaseErrorHandler):
    handle_exception = HTTPException

    def get_error(self, exception: HTTPException) -> Error:
        logger.debug(f'Handling exception: {type(exception)}: {exception}')
        return Error(
            code=exception.status_code,
            error=underscore(parameterize(exception.detail)).upper(),
            message=exception.detail,
        )


class ValidationErrorHandler(BaseErrorHandler):
    handle_exception = RequestValidationError

    def get_error(self, exception: RequestValidationError) -> Error:
        logger.debug(f'Handling exception: {type(exception)}: {exception}')
        return Error(
            code=HTTP_422_UNPROCESSABLE_ENTITY,
            error=ErrorType.VALIDATION_ERROR,
            message=ErrorType.VALIDATION_ERROR,
        )


class OurErrorHandler(BaseErrorHandler):
    handle_exception = OtherError

    def get_error(self, exc: OtherError) -> Error:
        logger.debug(f'Handling exception: {type(exc)}: {exc}')
        return Error(code=exc.code, error=exc.error, message=exc.message)


class ExceptionsHandler:
    def __init__(self, *args: Type[BaseErrorHandler]):
        self.handlers = []
        self.add_handlers(*args)

    def add_handlers(self, *args: Type[BaseErrorHandler]):
        self.handlers.extend([h if isinstance(h, BaseErrorHandler) else h() for h in args])

    def get_error(self, exc: Exception) -> Error:
        for handler in self.handlers:
            if isinstance(exc, handler.handle_exception):
                err = handler.get_error(exc)
                logger.warning(f'Application error: {err}')
                return err

        logger.exception(exc)
        return Error(code=500, error='INTERNAL_ERROR', message=str(exc))
