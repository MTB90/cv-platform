from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "cv-platform-backend"
    ENVIRONMENT: Literal["dev", "staging", "production"] = "dev"

    API_V1: str = "/api/v1"
    API_PRIVATE: str = "/api/private"


settings = Settings()  # type: ignore
