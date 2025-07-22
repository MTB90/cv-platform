from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from core.exceptions import UserNotFound
from schema.doc import CreateCV
from services.doc_service import DocService


@pytest.mark.anyio
async def test_given_no_existing_user_when_create_cv_then_raise_404():
    db = AsyncMock()

    with patch('services.doc_service.UserRepository', return_value=AsyncMock()) as mock_user_repo:
        mock_user_repo.return_value.get_by_id.return_value = None
        mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
        mock_cv_data = CreateCV(name="MyCV")

        service = DocService(db)
        with pytest.raises(UserNotFound):
            await service.create_cv(mock_user_id, mock_cv_data)
