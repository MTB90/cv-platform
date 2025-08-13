import logging
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.exceptions import ConflictError
from domain.job import Job
from infra.mapper import JobMapper
from infra.models import JobModel
from infra.repo.base import BaseRepository

logger = logging.getLogger(__name__)


class JobRepository(BaseRepository):
    async def get_all(self, user_id: UUID) -> Sequence[Job]:
        result = await self.db.execute(select(JobModel).where(JobModel.user_id == user_id))
        job_records = result.scalars().all()

        return [JobMapper.to_domain(job_record) for job_record in job_records]

    async def get_by_id(self, job_id: UUID) -> Optional[Job]:
        result = await self.db.execute(select(JobModel).where(JobModel.id == job_id))
        job_record = result.scalar_one_or_none()

        if job_record is None:
            return None

        return JobMapper.to_domain(job_record)

    async def create(self, job: Job) -> Job:
        job_record = JobMapper.from_domain(job)

        try:
            await self.add_and_commit(job_record)
        except IntegrityError:
            raise ConflictError("Job Creation Failed")

        return job
