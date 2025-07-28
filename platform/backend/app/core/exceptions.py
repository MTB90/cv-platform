from typing import List, Tuple, Any
from uuid import UUID

from fastapi import HTTPException
from pydantic_core import ErrorDetails
from starlette import status


class AppException(HTTPException):
    def __init__(
        self,
        message: str,
        status_code: int,
        detail: ErrorDetails = None,
    ):
        self.status_code = status_code
        self.message = message
        self.detail = [] if detail is None else detail
        super().__init__(status_code=status_code, detail=detail)


class InternalServiceError(AppException):
    def __init__(self, message: str = "Internal Server Error"):
        detail = ErrorDetails(
            type=type(self).__name__,
            loc=("body",),
            msg=message,
            input=None,
        )

        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, detail)


class ServiceUnavailableError(AppException):
    def __init__(self, message: str = "Service Unavailable"):
        detail = ErrorDetails(
            type=type(self).__name__,
            loc=("",),
            msg=message,
            input=None,
        )

        super().__init__(message, status.HTTP_503_SERVICE_UNAVAILABLE, detail)


class NotFoundError(AppException):
    def __init__(self, message="Not Found", keys: Tuple[str] = None, values: List[str] = None):
        detail = ErrorDetails(
            type=type(self).__name__,
            loc=keys,
            msg=message,
            input=values,
        )
        super().__init__(message, status.HTTP_404_NOT_FOUND, detail)


class UserNotFoundError(NotFoundError):
    def __init__(self, user_id: UUID):
        super().__init__(message="User Not Found", keys=("user.id",), values=[str(user_id)])


class DocNotFoundError(NotFoundError):
    def __init__(self, doc_id: UUID):
        super().__init__(message="Doc Not Found", keys=("doc.id",), values=[str(doc_id)])


class ConflictError(AppException):
    def __init__(self, message="Conflict", field: str = None, expected: str = None):
        detail = ErrorDetails(
            type=type(self).__name__,
            loc=(field,),
            msg=message,
            input=None,
            ctx={"expected": expected} if expected else None,
        )
        super().__init__(message, status.HTTP_409_CONFLICT, detail)
