from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, constr


class UserBase(BaseModel):
    name: constr(max_length=255)
    email: constr(max_length=255)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
