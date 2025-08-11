from uuid import UUID

from pydantic import BaseModel

from domain.job import JobType


class JobCreate(BaseModel):
    type: JobType
    source_id: UUID
