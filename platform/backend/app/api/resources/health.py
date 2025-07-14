from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import db_session

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health():
    return {"message": "ok"}
