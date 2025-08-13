from fastapi import APIRouter
from fastapi import status

from deps import DocServiceDep
from schema.doc import DocEvent

router = APIRouter(prefix="/webhooks", tags=["webhooks", "docs"])


@router.post("/docs/status", status_code=status.HTTP_204_NO_CONTENT)
async def doc_status_event(data: DocEvent, service: DocServiceDep):
    return await service.update_doc_status(data)
