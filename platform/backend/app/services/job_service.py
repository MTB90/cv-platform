import logging
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFoundError, DocNotFoundError
from infra.repo.doc import DocRepository
from infra.repo.job import JobRepository
from infra.repo.user import UserRepository
from schema.job import JobCreate

logger = logging.getLogger(__name__)


class JobService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._user_repo = UserRepository(db)
        self._doc_repo = DocRepository(db)
        self._job_repo = JobRepository(db)

    async def create(self, user_id: UUID, data: JobCreate):
        logger.info("creating job", extra={"user_id": user_id, "data": data})

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        source_doc = await self._doc_repo.get_by_id(data.source_id)
        if source_doc is None:
            raise DocNotFoundError(data.source_id)

        # result_doc_id = uuid4()
        # result_object_name = f"{user_id}/{result_doc_id}.{source_doc.format.value}"
        #
        # result_doc = await self._doc_repo.create(result_doc_id, user_id, )
