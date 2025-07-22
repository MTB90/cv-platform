from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from core.exceptions import UserNotFound
from schema.doc import CVCreate
from services.doc_service import DocService


@pytest.mark.anyio
@patch("services.doc_service.UserRepository")
async def test_given_no_existing_user_when_create_cv_then_raise_404(mock_user_repo_cls):
    mock_db = AsyncMock()
    mock_storage = AsyncMock()
    mock_user_repo = AsyncMock()

    # Configure class patches to return mock instances
    mock_user_repo_cls.return_value = mock_user_repo

    mock_user_repo.get_by_id.return_value = None
    mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
    mock_cv_data = CVCreate(name="MyCV", format="txt")

    service = DocService(mock_db, mock_storage)
    with pytest.raises(UserNotFound):
        await service.create_cv(mock_user_id, mock_cv_data)


@pytest.mark.anyio
@patch("services.doc_service.UserRepository")
@patch("services.doc_service.DocRepository")
async def test_given_existing_user_when_create_cv_then_create_pre_signed_url(
    mock_doc_repo_class, mock_user_repo_class, mock_user, mock_cv
):
    # Create mock instances
    mock_db = AsyncMock()
    mock_storage = AsyncMock()
    mock_user_repo = AsyncMock()
    mock_doc_repo = AsyncMock()

    # Configure class patches to return mock instances
    mock_user_repo_class.return_value = mock_user_repo
    mock_doc_repo_class.return_value = mock_doc_repo

    mock_user_repo.get_by_id.return_value = mock_user
    mock_doc_repo.create.return_value = mock_cv
    mock_storage.presigned_put_object.return_value = (
        f"http://mino.com/{mock_user.id}/{mock_cv.id}.{mock_cv.format}"
    )

    service = DocService(mock_db, mock_storage)

    user_id = mock_user.id
    doc_cv = CVCreate(name=mock_cv.name, type=mock_cv.type, format=mock_cv.format)
    await service.create_cv(user_id, doc_cv)

    mock_storage.presigned_put_object.assert_called_once()
