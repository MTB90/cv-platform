import logging
from uuid import UUID, uuid4

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFoundError, DocNotFoundError
from domain.doc import Doc, DocStatus, DocType
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
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        source_doc = await self._doc_repo.get_by_id(data.source_id)
        if source_doc is None:
            raise DocNotFoundError(data.source_id)

        result_doc = Doc(
            id=uuid4(),
            user_id=user_id,
            name=data.name,
            type=DocType.CV,
            format=data.format,
            status=DocStatus.PROCESSING,
        )

        logger.info("create result document entity", extra={"data": result_doc})
        result_doc = await self._doc_repo.create(result_doc)

        logger.info("creating processing job", extra={"user_id": user_id, "data": data})
