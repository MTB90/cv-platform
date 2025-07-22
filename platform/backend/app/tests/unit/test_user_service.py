from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from core.exceptions import UserNotFound
from models import User
from schema.user import UserCreate
from services.user_service import UserService


@pytest.mark.anyio
async def test_given_not_existing_user_when_get_user_then_raise_404():
    db = AsyncMock()

    with patch('services.user_service.UserRepository', return_value=AsyncMock()) as mock_user_repo:
        mock_user_repo.return_value.get_by_id.return_value = None
        service = UserService(db)

        with pytest.raises(UserNotFound):
            await service.get_user_by_id(UUID("2a7156db-0bae-4bc5-9bd5-f7f6d977fe34"))

@pytest.mark.anyio
async def test_given_new_user_when_create_user_then_return_correct_respond(mock_user_create, mock_user_response):
    db = AsyncMock()

    with patch('services.user_service.UserRepository', return_value=AsyncMock()) as mock_user_repo:
        mock_user_repo.return_value.create.return_value = mock_user_create
        service = UserService(db)
        result = await service.create_user(UserCreate(
            name=mock_user_create.name,
            email=mock_user_create.email
        ))

        assert result.__dict__ == mock_user_response.__dict__

