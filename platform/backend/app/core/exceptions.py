class BaseApiError(Exception):
    status_code = 500
    message = "Service is unavailable"

    def __init__(self):
        super().__init__(self.message, self.status_code)


class NotFoundError(BaseApiError):
    status_code = 404
    message = "Entity does not exist"


class UserNotFound(NotFoundError):
    message = "User does not exist"


class DocNotFound(NotFoundError):
    message = "Doc does not exist"
