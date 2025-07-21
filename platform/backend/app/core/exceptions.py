class PlatformBackendApiError(Exception):
    status_code = 500
    message = "Service is unavailable"

    def __init__(self):
        super().__init__(self.message, self.status_code)


class EntityDoesNotExistError(PlatformBackendApiError):
    status_code = 404
    message = "Entity does not exist"
