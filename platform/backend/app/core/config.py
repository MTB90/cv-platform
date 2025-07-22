from pydantic_settings import BaseSettings


class Settings(BaseSettings):
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

    # API
    API_V1: str = "/api/v1"
    API_PRIVATE: str = "/api/private"


settings = Settings()  # type: ignore
