class BaseError(Exception):
    status_code = None
    message = None

    def __init__(self):
        super().__init__(self.message, self.status_code)


class ServiceError(BaseError):
    status_code = 500
    message = "Internal server error"


class StorageServiceError(BaseError):
    status_code = 503
    message = "Storage service unavailable"


class ValidationError(BaseError):
    status_code = 400
    message = "Bad Request"


class UserIntegrityError(ValidationError):
    message = "Invalid user data"


class DocIntegrityError(ValidationError):
    message = "Invalid doc data"


class NotFoundError(BaseError):
    status_code = 404
    message = "Resource not found"


class UserNotFoundError(NotFoundError):
    message = "User not found"


class DocNotFoundError(NotFoundError):
    message = "Doc not found"
