from datetime import datetime
from uuid import UUID

import pytest

from models import User, Doc
from schema.doc import DocFormat, DocType
from schema.user import UserResponse


@pytest.fixture
def anyio_backend():
    return "asyncio"


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
