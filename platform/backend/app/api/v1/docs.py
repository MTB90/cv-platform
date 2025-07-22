from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from deps import DocServiceDep
from schema.doc import CVCreate, CVResponse

router = APIRouter(prefix="/users", tags=["docs"])


@router.post(
    "/{user_id}/docs", response_model=CVResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user_id: UUID, data: CVCreate, service: DocServiceDep):
    return await service.create_cv(user_id, data)
