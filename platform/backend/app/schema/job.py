from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class JobType(str, Enum):
    FORMATING = "formating"


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobBase(BaseModel):
    type: JobType
    status: JobStatus = JobStatus.PENDING
    source_id: UUID


class JobCreate(JobBase):
    pass
