from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from deps import DocServiceDep
from schema.doc import DocUpdateStatus

router = APIRouter(prefix="/webhooks", tags=["webhooks", "docs"])


@router.patch("/docs/{doc_id}/status", status_code=status.HTTP_204_NO_CONTENT)
async def update_doc_status(doc_id: UUID, data: DocUpdateStatus, service: DocServiceDep):
    return await service.update_status(doc_id, data)
