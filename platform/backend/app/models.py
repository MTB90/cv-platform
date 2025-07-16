from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    pass


class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
