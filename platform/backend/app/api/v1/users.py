from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import status

from deps import UserServiceDep
from schema.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def list_users(service: UserServiceDep):
    return await service.list_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserServiceDep):
    return await service.get_user_by_id(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep):
    return await service.create_user(data)
