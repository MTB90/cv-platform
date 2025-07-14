from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CV_BACKEND_PROJECT_NAME: str

    # Database connection
    CV_BACKEND_DB_HOST: str
    CV_BACKEND_DB_PASS: str
    CV_BACKEND_DB_USER: str

    # API
    API_V1: str = "/api/v1"
    API_PRIVATE: str = "/api/private"


settings = Settings()  # type: ignore
