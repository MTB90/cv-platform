from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from core.exceptions import UserNotFound
from services.user_service import UserService


@pytest.mark.anyio
async def test_given_not_existing_user_when_get_user_then_raise_404():
    db = AsyncMock()

    with patch('services.user_service.UserRepository', return_value=AsyncMock()) as mock_user_repo:
        mock_user_repo.return_value.get_by_id.return_value = None
        service = UserService(db)

        with pytest.raises(UserNotFound):
            await service.get_user_by_id(UUID("2a7156db-0bae-4bc5-9bd5-f7f6d977fe34"))
