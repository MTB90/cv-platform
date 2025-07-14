from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CV_BACKEND_PROJECT_NAME: str
    CV_BACKEND_DATABASE_URL: str

    API_V1: str = "/api/v1"
    API_PRIVATE: str = "/api/private"


settings = Settings()  # type: ignore
