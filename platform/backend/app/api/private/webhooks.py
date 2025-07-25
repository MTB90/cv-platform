from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from deps import DocServiceDep
from schema.doc import DocCreate, CVResponse

router = APIRouter(prefix="/webhooks", tags=["docs"])


@router.patch(
    "/docs/{docs_id}/status",
    response_model=CVResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_docs(user_id: UUID, data: DocCreate, service: DocServiceDep):
    return await service.create_cv(user_id, data)
