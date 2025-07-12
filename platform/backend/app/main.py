from fastapi import FastAPI
from fastapi.routing import APIRoute

from api import private_api_router
from core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(private_api_router, prefix=settings.API_PRIVATE)
