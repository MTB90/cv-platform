from uuid import UUID

from pydantic import BaseModel, constr

from domain.job import JobType


class JobCreate(BaseModel):
    name: constr(max_length=255)
    type: JobType
    source_id: UUID
