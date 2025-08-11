from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
from sqlalchemy.exc import IntegrityError

from core.exceptions import NotFoundError, ConflictError
from infra.repo.user import UserRepository
from schema.user import UserCreate
from services.user_service import UserService


@pytest.mark.anyio
async def test_get_user_by_id_when_user_not_exist_then_raise_404():
    mock_user_repo = AsyncMock()

    mock_user_repo.get_by_id.return_value = None
    service = UserService(mock_user_repo)

    with pytest.raises(NotFoundError):
        await service.get_user_by_id(UUID("2a7156db-0bae-4bc5-9bd5-f7f6d977fe34"))


@pytest.mark.anyio
async def test_create_user_when_email_not_exist_then_return_user(mock_user, mock_user_response):
    create_user = UserCreate(name=mock_user.name, email=mock_user.email)

    mock_user_repo = AsyncMock()
    mock_user_repo.create.return_value = mock_user

    service = UserService(mock_user_repo)
    result = await service.create_user(create_user)

    assert result.__dict__ == mock_user_response.__dict__


@pytest.mark.anyio
async def test_get_user_when_user_exist_then_return_user(mock_user, mock_user_response):
    mock_user_repo = AsyncMock()
    mock_user_repo.get_by_id.return_value = mock_user

    service = UserService(mock_user_repo)
    result = await service.get_user_by_id(mock_user.id)

    assert result.__dict__ == mock_user_response.__dict__


@pytest.mark.anyio
async def test_create_user_when_email_already_exist_then_raise_bad_request(mock_user):
    db = AsyncMock()
    db.add = Mock()
    db.commit.side_effect = IntegrityError(orig=Exception(), statement=None, params=None)

    service = UserService(UserRepository(db))
    create_user = UserCreate(name=mock_user.name, email=mock_user.email)

    with pytest.raises(ConflictError):
        await service.create_user(create_user)
