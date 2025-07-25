from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from core.exceptions import UserNotFoundError, StorageServiceError
from schema.doc import CVCreate, DocFormat
from services.doc_service import DocService
from tests.conftest import patch_async_cls
from utils.storage import MinioClient


@pytest.mark.anyio
async def test_create_cv_when_no_user_then_raise_404():
    mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
    mock_cv_data = CVCreate(name="MyCV", format=DocFormat.PDF)

    with patch_async_cls("services.doc_service.UserRepository") as mock_user_repo:
        mock_user_repo.get_by_id.return_value = None

        service = DocService(AsyncMock(), AsyncMock())
        with pytest.raises(UserNotFoundError):
            await service.create_cv(mock_user_id, mock_cv_data)


@pytest.mark.anyio
async def test_create_cv_when_no_errors_then_call_pre_signed_url(mock_user, mock_cv):
    mock_storage = AsyncMock()
    mock_storage.presigned_put_object.return_value = (
        f"http://mino.com/{mock_user.id}/{mock_cv.id}.{mock_cv.format}"
    )

    doc_cv = CVCreate(name=mock_cv.name, type=mock_cv.type, format=mock_cv.format)

    with patch_async_cls("services.doc_service.UserRepository") as mock_user_repo:
        with patch_async_cls("services.doc_service.DocRepository") as mock_doc_repo:
            mock_user_repo.get_by_id.return_value = mock_user
            mock_doc_repo.create.return_value = mock_cv

            service = DocService(AsyncMock(), mock_storage)
            await service.create_cv(mock_user.id, doc_cv)
            mock_storage.presigned_put_object.assert_called_once()


@pytest.mark.anyio
@patch("utils.storage.Minio", return_value=AsyncMock())
async def test_create_cv_when_storage_client_error_then_raise_storage_error(
    mock_mino, mock_settings, mock_user, mock_cv
):
    mock_mino.return_value.presigned_put_object.side_effect = Exception()

    doc_cv = CVCreate(name=mock_cv.name, type=mock_cv.type, format=mock_cv.format)

    with patch_async_cls("services.doc_service.UserRepository") as mock_user_repo:
        with patch_async_cls("services.doc_service.DocRepository") as mock_doc_repo:
            with pytest.raises(StorageServiceError):

                service = DocService(AsyncMock(), MinioClient(mock_settings))
                await service.create_cv(mock_user.id, doc_cv)

            mock_user_repo.get_by_id.assert_called_once()
            mock_doc_repo.create.assert_not_called()
