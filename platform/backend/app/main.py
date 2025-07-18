from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import health, user

from core.config import settings
from database import DB


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start up logic
    app.state.DB = DB(settings)
    yield
    # Clean up logic


def build_app() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # add here all private routes
    application.include_router(health.router, prefix=settings.API_PRIVATE)

    # add here all public routes
    application.include_router(user.router, prefix=settings.API_V1)
    return application


app = build_app()
