from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from deps import DocServiceDep
from schema.doc import DocCreate, DocResponse

router = APIRouter(prefix="/users", tags=["jobs"])


@router.post("/{user_id}/jobs", response_model=DocResponse, status_code=status.HTTP_201_CREATED)
async def create_job(user_id: UUID, data: DocCreate, service: DocServiceDep):
    return await service.create(user_id, data)
