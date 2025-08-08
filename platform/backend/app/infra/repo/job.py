import logging
from uuid import UUID

from infra.models import JobModel
from infra.repo.base import BaseRepository
from schema.job import JobCreate

logger = logging.getLogger(__name__)


class JobRepository(BaseRepository):
    async def create(self, source_id: UUID, result_id: UUID, data: JobCreate) -> JobModel:
        job = JobModel(**data.__dict__, source_id=source_id, result_id=result_id)

        await self.add_and_commit(job)
        await self.db.refresh(job)
        return job
