from enum import Enum

from pydantic import BaseModel, constr


class JobType(str, Enum):
    FORMATING = "formating"


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobBase(BaseModel):
    name: constr(max_length=255)
    type: JobType
    status: JobStatus = JobStatus.PENDING


class JobCreate(JobBase):
    pass
