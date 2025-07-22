from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFound
from repository.doc import DocRepository
from repository.user import UserRepository
from schema.doc import CreateCV


class DocService:
    def __init__(self, db: AsyncSession):
        self._user_repo = UserRepository(db)
        self._doc_repo = DocRepository(db)

    async def create_cv(self, user_id: UUID, doc_data: CreateCV):
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound()
