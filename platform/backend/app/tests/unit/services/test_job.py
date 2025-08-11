from unittest.mock import AsyncMock
from uuid import UUID

import pytest

from core.exceptions import NotFoundError
from schema.job import JobCreate, JobType
from services.job_service import JobService


@pytest.mark.anyio
async def test_create_job_when_no_user_raise_404():
    mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
    job_create = JobCreate(
        name="formated cv",
        type=JobType.FORMATING,
        source_id=UUID("5e029eea-5df0-4b48-9e6f-6d47f574c9fa"),
    )

    mock_user_repo = AsyncMock()
    mock_user_repo.get_by_id.return_value = None

    service = JobService(AsyncMock(), mock_user_repo, AsyncMock(), AsyncMock())
    with pytest.raises(NotFoundError):
        await service.create(mock_user_id, job_create)


@pytest.mark.anyio
async def test_create_job_when_no_source_doc_raise_404():
    mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
    job_create = JobCreate(
        name="formated cv",
        type=JobType.FORMATING,
        source_id=UUID("5e029eea-5df0-4b48-9e6f-6d47f574c9fa"),
    )

    mock_doc_repo = AsyncMock()
    mock_doc_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service = JobService(AsyncMock(), AsyncMock(), mock_doc_repo, AsyncMock())
        await service.create(mock_user_id, job_create)


@pytest.mark.anyio
async def test_create_job_when_doc_found_execute_workflow():
    mock_user_id = UUID("a32ec7b9-9d23-4b21-bfe4-3c3762116332")
    job_create = JobCreate(
        name="formated cv",
        type=JobType.FORMATING,
        source_id=UUID("5e029eea-5df0-4b48-9e6f-6d47f574c9fa"),
    )

    mock_doc_repo = AsyncMock()
    mock_job_repo = AsyncMock()

    service = JobService(AsyncMock(), AsyncMock(), mock_doc_repo, mock_job_repo)
    await service.create(mock_user_id, job_create)

    mock_doc_repo.create.assert_called()
