from typing import List

from fastapi import HTTPException
from pydantic_core import ErrorDetails
from starlette import status


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: ErrorDetails = None,
    ):
        self.status_code = status_code
        self.detail = [] if detail is None else detail
        super().__init__(status_code=status_code, detail=detail)


class InternalServiceError(AppException):
    def __init__(self, message: str = "Internal Server Error"):
        error_detail = ErrorDetails(
            type=type(self).__name__,
            loc=("body",),
            msg=message,
            input=None,
        )

        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)


class ServiceUnavailableError(AppException):
    def __init__(self, message: str = "Service Unavailable"):
        error_detail = ErrorDetails(
            type=type(self).__name__,
            loc=("body",),
            msg=message,
            input=None,
        )

        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=error_detail)


class NotFoundError(AppException):
    def __init__(self, message="Not Found", field: str = None, expected: str = None, input=None):
        error_detail = ErrorDetails(
            type=type(self).__name__,
            loc=("body", field) if field else ("body",),
            msg=message,
            input=input,
            ctx={"expected": expected} if expected else None,
        )
        super().__init__(status_code=409, detail=error_detail)


class ConflictError(AppException):
    def __init__(self, message="Conflict", field: str = None, expected: str = None, input=None):
        error_detail = ErrorDetails(
            type=type(self).__name__,
            loc=("body", field) if field else ("body",),
            msg=message,
            input=input,
            ctx={"expected": expected} if expected else None,
        )
        super().__init__(status_code=409, detail=error_detail)
