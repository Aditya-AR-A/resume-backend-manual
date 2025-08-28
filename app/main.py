from fastapi import FastAPI
from fastapi.middlewares.cors import CORSMiddleware

from contextlib import asynccontextmanager

from .utils.logger import get_logger

logger = get_logger()

logger.info("Logger initialized")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")
