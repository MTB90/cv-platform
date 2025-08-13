from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from deps import JobServiceDep
from schema.doc import DocCreate, DocPresignedUrl
from schema.job import JobResponse

router = APIRouter(prefix="/users", tags=["jobs"])


@router.post("/{user_id}/jobs", response_model=DocPresignedUrl, status_code=status.HTTP_201_CREATED)
async def create_job(user_id: UUID, data: DocCreate, service: JobServiceDep):
    return await service.create_job(user_id, data)


@router.get("/{user_id}/jobs", response_model=List[JobResponse])
async def list_jobs(user_id: UUID, service: JobServiceDep):
    return await service.list_jobs(user_id)
