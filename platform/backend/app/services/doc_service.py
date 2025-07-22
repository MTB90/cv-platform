from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFound
from repository.doc import DocRepository
from repository.user import UserRepository
from schema.doc import CVCreate, CVResponse
from utils.storage import Storage


class DocService:
    def __init__(self, db: AsyncSession, storage: Storage):
        self._db = db
        self._storage = storage
        self._user_repo = UserRepository(db)
        self._doc_repo = DocRepository(db)

    async def create_cv(self, user_id: UUID, doc_data: CVCreate) -> CVResponse:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound()

        doc = await self._doc_repo.create(user_id, doc_data)

        object_name = f"{user_id}/{doc.id}.{doc.format.value}"
        presigned_url = await self._storage.presigned_put_object(object_name)

        return CVResponse(**doc.__dict__, presigned_url=presigned_url)
