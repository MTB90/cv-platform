from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database connection
    CV_BACKEND_DB_HOST: str
    CV_BACKEND_DB_NAME: str
    CV_BACKEND_DB_PASS: str
    CV_BACKEND_DB_USER: str

    # API
    API_V1: str = "/api/v1"
    API_PRIVATE: str = "/api/private"


settings = Settings()  # type: ignore
