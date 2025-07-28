from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest

from core.exceptions import ServiceUnavailableError, NotFoundError
from schema.doc import DocCreate, DocFormat, DocType, DocEventStatus
from services.doc_service import DocService
from tests.conftest import patch_async_cls
from utils.storage import MinioClient


@pytest.mark.anyio
async def test_create_when_no_user_then_raise_404():
    mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
    doc_create = DocCreate(name="MyCV", format=DocFormat.PDF, type=DocType.CV)

    with patch_async_cls("services.doc_service.UserRepository") as mock_user_repo:
        mock_user_repo.get_by_id.return_value = None

        service = DocService(AsyncMock(), AsyncMock())
        with pytest.raises(NotFoundError):
            await service.create(mock_user_id, doc_create)


@pytest.mark.anyio
async def test_create_when_no_errors_then_call_pre_signed_url(mock_user, mock_cv):
    mock_storage = AsyncMock()
    mock_storage.presigned_put_object.return_value = (
        f"http://mino.com/{mock_user.id}/{mock_cv.id}.{mock_cv.format}"
    )

    doc_create = DocCreate(name=mock_cv.name, type=mock_cv.type, format=mock_cv.format)

    with patch_async_cls("services.doc_service.UserRepository") as mock_user_repo:
        with patch_async_cls("services.doc_service.DocRepository") as mock_doc_repo:
            mock_user_repo.get_by_id.return_value = mock_user
            mock_doc_repo.create.return_value = mock_cv

            service = DocService(AsyncMock(), mock_storage)
            await service.create(mock_user.id, doc_create)
            mock_storage.presigned_put_object.assert_called_once()


@pytest.mark.anyio
@patch("utils.storage.Minio", return_value=AsyncMock())
async def test_create_when_storage_client_error_then_raise_storage_error(
    mock_mino, mock_settings, mock_user, mock_cv
):
    mock_mino.return_value.presigned_put_object.side_effect = Exception()
    doc_create = DocCreate(name=mock_cv.name, type=mock_cv.type, format=mock_cv.format)

    with patch_async_cls("services.doc_service.UserRepository") as mock_user_repo:
        with patch_async_cls("services.doc_service.DocRepository") as mock_doc_repo:
            with pytest.raises(ServiceUnavailableError):
                service = DocService(AsyncMock(), MinioClient(mock_settings))
                await service.create(mock_user.id, doc_create)

            mock_user_repo.get_by_id.assert_called_once()
            mock_doc_repo.create.assert_not_called()


@pytest.mark.anyio
async def test_update_status_when_doc_not_exist_then_raise_404(mock_user, mock_cv):
    doc_update_status = DocEventStatus(
        user_id=mock_user.id, doc_id=mock_cv.id, EventName="s3:ObjectCreated:Put"
    )
    with patch_async_cls("services.doc_service.UserRepository"):
        with patch_async_cls("services.doc_service.DocRepository") as mock_doc_repo:
            mock_doc_repo.get_by_id.return_value = None

            with pytest.raises(NotFoundError):
                service = DocService(AsyncMock(), AsyncMock())
                await service.update_status(doc_update_status)
