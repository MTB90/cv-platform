from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from core.exceptions import NotFoundError
from schema.job import JobCreate, JobType
from services.job_service import JobService
from tests.conftest import patch_async_cls


@pytest.mark.anyio
async def test_create_job_when_no_user_raise_404():
    mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
    job_create = JobCreate(
        type=JobType.FORMATING, source_id=UUID("5e029eea-5df0-4b48-9e6f-6d47f574c9fa")
    )

    with patch_async_cls("services.job_service.UserRepository") as mock_user_repo:
        mock_user_repo.get_by_id.return_value = None

        service = JobService(AsyncMock())
        with pytest.raises(NotFoundError):
            await service.create(mock_user_id, job_create)


@pytest.mark.anyio
async def test_create_job_when_no_source_doc_raise_404():
    mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
    job_create = JobCreate(
        type=JobType.FORMATING, source_id=UUID("5e029eea-5df0-4b48-9e6f-6d47f574c9fa")
    )

    with patch_async_cls("services.job_service.UserRepository"):
        with patch_async_cls("services.job_service.DocRepository") as mock_doc_repo:
            mock_doc_repo.get_by_id.return_value = None

            with pytest.raises(NotFoundError):
                service = JobService(AsyncMock())
                await service.create(mock_user_id, job_create)


@pytest.mark.anyio
async def test_create_job_when_doc_found_execute_workflow():
    pass
