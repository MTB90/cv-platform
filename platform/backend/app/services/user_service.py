from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFound
from repository.user import UserRepository
from schema.user import UserCreate, UserResponse


class UserService:
    def __init__(self, db: AsyncSession):
        self._user_repo = UserRepository(db)

    async def create_user(self, data: UserCreate) -> UserResponse:
        user = await self._user_repo.create(data)
        return UserResponse(**user.__dict__)

    async def list_all_users(self):
        users = await self._user_repo.get_all()
        return [UserResponse(**user.__dict__) for user in users]

    async def get_user_by_id(self, user_id: UUID):
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFound()

        return UserResponse(**user.__dict__)
