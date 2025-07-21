from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import api

from core.config import settings
from core.exceptions import PlatformBackendApiError
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

    application.include_router(api.router)
    return application


app = build_app()


@app.exception_handler(PlatformBackendApiError)
async def unicorn_exception_handler(request: Request, exc: PlatformBackendApiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
