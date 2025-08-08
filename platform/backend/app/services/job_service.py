import logging
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFoundError
from repository.doc import DocRepository
from repository.user import UserRepository
from schema.job import JobCreate

logger = logging.getLogger(__name__)


class JobService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._user_repo = UserRepository(db)
        self._doc_repo = DocRepository(db)

    async def create(self, user_id: UUID, data: JobCreate):
        logger.info("creating job", extra={"user_id": user_id, "data": data})

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
