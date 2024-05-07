from .constants import ErrorType


class OtherError(Exception):
    """Base class for custom errors"""

    error_id: str = None
    code = 500

    def __init__(self, message=None, detail=None, error_id=None, code=None):
        """
        :param message: Error message
        :param detail: Detailed information about the error
        :param error_id: Error id
        :param code: Error code
        """
        super().__init__(message)

        self.error_id = error_id or self.error_id
        self.message = message
        self.detail = detail
        self.code = code or self.code

    def __str__(self):
        """ String representation of the error """
        return f'message: {self.message}, code: {self.code}, detail: {self.detail}'

    @property
    def error(self):
        return self.error_id


class InternalError(OtherError):
    """ Internal service error """

    error_id = ErrorType.INTERNAL_ERROR


class ExternalServiceError(OtherError):
    """ External service error """

    error_id = ErrorType.EXTERNAL_SERVICE_ERROR


class NotFoundError(OtherError):
    """ Resource not found """

    error_id = ErrorType.NOT_FOUND
    code = 404


class BadRequest(OtherError):
    """ Request is incorrect"""

    error_id = ErrorType.BAD_REQUEST
    code = 400


class AccessDeniedError(OtherError):
    """ Access to the resource is denied """

    error_id = ErrorType.ACCESS_DENIED
    code = 403
