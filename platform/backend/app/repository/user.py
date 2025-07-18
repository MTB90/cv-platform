from typing import Optional, Sequence

from sqlalchemy import select

from models import User, UserCreate
from repository.base import BaseRepository


class UserRepository(BaseRepository):
    async def get_all(self) -> Sequence[User]:
        result = await self.db_session.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: str) -> Optional[User]:
        result = await self.db_session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        user = User(
            name=user_data.name,
            email=user_data.email,
        )
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user
