from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, constr

from domain.job import JobType, JobStatus


class JobCreate(BaseModel):
    name: constr(max_length=255)
    type: JobType
    source_id: UUID


class JobResponse(BaseModel):
    id: UUID
    type: JobType
    status: JobStatus
    source_id: UUID
    result_id: UUID
    created_at: datetime
    updated_at: datetime
