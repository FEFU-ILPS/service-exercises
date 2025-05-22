from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import disconnect_db
from routers import exercises_router, health_router
from service_logging import logger
from fastapi import Request

import hashlib
from random import randbytes
from typing import Callable


@asynccontextmanager
async def lifespan(_: FastAPI):
    # on_startup
    logger.info("FastAPI application starting up...")
    yield

    # on_shutdown
    logger.info("FastAPI application shutting down...")
    await disconnect_db()


service = FastAPI(lifespan=lifespan)


@service.middleware("http")
async def add_request_hash(request: Request, call_next: Callable):
    request_hash = hashlib.sha1(randbytes(32)).hexdigest()[:10]
    with logger.contextualize(request_hash=request_hash):
        response = await call_next(request)
        return response


service.include_router(health_router)
service.include_router(exercises_router)
