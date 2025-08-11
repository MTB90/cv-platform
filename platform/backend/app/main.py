import logging
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import api
from core.config import get_settings
from core.context import context_request_id
from core.exceptions import AppException
from core.logging import setup_logging

settings = get_settings()
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def build_app() -> FastAPI:
    application = FastAPI()
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


@app.get("/healthz")
async def health():
    return {"message": "ok"}


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    # Ignore specific endpoints
    if request.url.path in ["/healthz", "/healthz/"]:
        return await call_next(request)

    # Save to context var and request.state
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    context_request_id.set(request_id)
    request.state.request_id = request_id

    logger.info(
        "request",
        extra={
            "client": request.client,
            "method": request.method,
            "path": request.url.path,
            "path_params": request.path_params,
            "query_params": request.query_params,
        },
    )

    response = await call_next(request)

    if response.status_code < 400:
        logger.info("response", extra={"status_code": response.status_code})
    else:
        logger.error("response", extra={"status_code": response.status_code})

    # Add to response headers
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(AppException)
async def business_error_handler(request: Request, exc: AppException):
    logger.error(exc.message.lower(), extra={"exc": str(exc)})
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": [exc.detail]},
    )

    # Also add it to headers for consistency
    response.headers["X-Request-ID"] = getattr(request.state, "request_id", None)
    return response


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
    logger.error("unexpected error", extra={"type": type(exc).__name__, "exc": str(exc)})
    response = JSONResponse(
        status_code=500,
        content={"detail": [{"type": type(exc).__name__, "msg": "Internal server error"}]},
    )

    # Also add it to headers for consistency
    response.headers["X-Request-ID"] = getattr(request.state, "request_id", None)
    return response
