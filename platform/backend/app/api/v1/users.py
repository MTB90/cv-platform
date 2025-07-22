from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status

from deps import get_user_service
from schema.user import UserCreate, UserResponse
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def list_users(service: UserService = Depends(get_user_service)):
    return await service.list_all_users()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate, service: UserService = Depends(get_user_service)
):
    return await service.create_user(data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    return await service.get_user_by_id(user_id)
