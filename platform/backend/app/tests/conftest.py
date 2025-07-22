from datetime import datetime
from uuid import UUID

import pytest

from models import User
from schema.user import UserResponse


@pytest.fixture()
def mock_user_create():
    date_string = "2024-09-19 15:45:30"

    return User(
        id=UUID("16229579-de59-44a6-9b51-dec60bd50680"),
        name="user",
        email="user@email.com",
        created_at=datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    )

@pytest.fixture()
def mock_user_response():
    date_string = "2024-09-19 15:45:30"

    return UserResponse(
        name="user",
        email="user@email.com",
        created_at=datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    )
