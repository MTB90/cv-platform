import logging

from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from domain.job import Job
from infra.mapper import JobMapper
from infra.repo.base import BaseRepository

logger = logging.getLogger(__name__)


class JobRepository(BaseRepository):
    async def create(self, job: Job) -> Job:
        job_record = JobMapper.from_domain(job)

        try:
            await self.add_and_commit(job_record)
        except IntegrityError:
            raise ConflictError("Doc Creation Failed")

        return job
