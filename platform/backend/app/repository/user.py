from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select

from models import User
from repository.base import BaseRepository
from schema.user import UserCreate


class UserRepository(BaseRepository):
    async def get_all(self) -> Sequence[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        user = User(
            name=user_data.name,
            email=user_data.email,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
