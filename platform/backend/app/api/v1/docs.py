from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from deps import DocServiceDep
from schema.doc import DocCreate, DocPresignedUrl, DocResponse

router = APIRouter(prefix="/users", tags=["docs"])


@router.post("/{user_id}/docs", response_model=DocPresignedUrl, status_code=status.HTTP_201_CREATED)
async def create_doc(user_id: UUID, data: DocCreate, service: DocServiceDep):
    return await service.create_doc(user_id, data)


@router.get("/{user_id}/docs", response_model=List[DocResponse])
async def list_docs(user_id: UUID, service: DocServiceDep):
    return await service.list_docs(user_id)
