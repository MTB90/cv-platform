from contextlib import contextmanager
from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from core.config import Settings
from models import User, Doc
from schema.doc import DocFormat, DocType, DocStatus
from schema.user import UserResponse


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def mock_settings() -> Settings:
    return Settings(
        CV_BACKEND_DB_HOST="db:5432",
        CV_BACKEND_DB_NAME="platform",
        CV_BACKEND_DB_USER="platform",
        CV_BACKEND_DB_PASS="password",
        CV_BACKEND_MINIO_SERVER_URL="http://localhost:9000",
        CV_BACKEND_MINIO_ENDPOINT="minio:9000",
        CV_BACKEND_MINIO_ACCESS_KEY="minioAccessKey",
        CV_BACKEND_MINIO_SECRET_KEY="minioSecretKey",
        CV_BACKEND_MINIO_BUCKET_NAME="minio-platform-docs",
    )


@contextmanager
def patch_async_cls(patch_path: str):
    with patch(patch_path) as mock_cls:
        mock_instance = AsyncMock()
        mock_cls.return_value = mock_instance
        yield mock_instance


@pytest.fixture()
def mock_user():
    date_string = "2024-09-19 15:45:30"

    return User(
        id=UUID("16229579-de59-44a6-9b51-dec60bd50680"),
        name="user",
        email="user@email.com",
        created_at=datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S"),
    )


@pytest.fixture()
def mock_cv():
    date_string = "2024-09-19 15:45:30"

    return Doc(
        id=UUID("a75c7d8a-d306-4b2f-8b09-35e3a903471f"),
        name="CV",
        user_id=UUID("16229579-de59-44a6-9b51-dec60bd50680"),
        type=DocType.CV,
        status=DocStatus.PENDING,
        format=DocFormat.PDF,
        created_at=datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S"),
        updated_at=datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S"),
    )


@pytest.fixture()
def mock_user_response():
    date_string = "2024-09-19 15:45:30"

    return UserResponse(
        id=UUID("16229579-de59-44a6-9b51-dec60bd50680"),
        name="user",
        email="user@email.com",
        created_at=datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S"),
    )
