from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, constr


class UserCreate(BaseModel):
    name: constr(max_length=255)
    email: constr(max_length=255)


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime
