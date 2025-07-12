from fastapi import APIRouter

from api.resources import health

private_api_router = APIRouter()
private_api_router.include_router(health.router)
