import datetime
import logging
from uuid import UUID, uuid4

from core.exceptions import UserNotFoundError, DocNotFoundError
from domain.doc import Doc, DocStatus, DocType
from infra.repo.doc import DocRepository
from infra.repo.job import JobRepository
from infra.repo.user import UserRepository
from schema.job import JobCreate, JobResponse

logger = logging.getLogger(__name__)


class JobService:
    def __init__(self, user_repo: UserRepository, doc_repo: DocRepository, job_repo: JobRepository):
        self._user_repo = user_repo
        self._doc_repo = doc_repo
        self._job_repo = job_repo

    async def list_jobs(self, user_id: UUID):
        logger.info("list all users")
        jobs = await self._job_repo.get_all(user_id)
        return [JobResponse(**job.__dict__) for job in jobs]

    async def create_job(self, user_id: UUID, data: JobCreate):
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
            format=source_doc.format,
            status=DocStatus.PROCESSING,
            created_at=datetime.datetime.now(datetime.UTC),
            updated_at=datetime.datetime.now(datetime.UTC),
        )

        logger.info("create result document entity", extra={"data": result_doc})
        result_doc = await self._doc_repo.create(result_doc)

        logger.info("creating processing job", extra={"user_id": user_id, "data": data})
