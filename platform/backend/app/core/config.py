from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Base
    LOG_LEVEL: str = "INFO"

    # API
    API_V1: str = "/api/v1"
    API_PRIVATE: str = "/api/private"

    # Database connection
    CV_BACKEND_DB_HOST: str
    CV_BACKEND_DB_NAME: str
    CV_BACKEND_DB_PASS: str
    CV_BACKEND_DB_USER: str

    CV_BACKEND_MINIO_ENDPOINT: str
    CV_BACKEND_MINIO_SERVER_URL: str
    CV_BACKEND_MINIO_ACCESS_KEY: str
    CV_BACKEND_MINIO_SECRET_KEY: str
    CV_BACKEND_MINIO_BUCKET_NAME: str


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()  # type: ignore
    return _settings
