import logging
from uuid import UUID, uuid4

from sqlmodel.ext.asyncio.session import AsyncSession

from core.exceptions import UserNotFoundError
from domain.models import User
from infra.repo.user import UserRepository
from schema.user import UserCreate, UserResponse

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: AsyncSession):
        self._user_repo = UserRepository(db)

    async def create_user(self, data: UserCreate) -> UserResponse:
        logger.info("creating new user", extra={"user_name": data.name})
        user = User(
            id=uuid4(),
            name=data.name,
            email=data.email,
        )

        user = await self._user_repo.create(user)
        logger.info("user created", extra={"user_name": data.name})
        return UserResponse(**user.__dict__)

    async def list_all_users(self):
        logger.info("list all users")
        users = await self._user_repo.get_all()
        return [UserResponse(**user.__dict__) for user in users]

    async def get_user_by_id(self, user_id: UUID):
        logger.info("get user", extra={"user_id": user_id})

        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)

        return UserResponse(**user.__dict__)
