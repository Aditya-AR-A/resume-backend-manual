from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.utils.logger import logger
from app.config.settings import app_settings
from app.middleware.custom import LoggingMiddleware
from app.routes import main_routes, ai_routes, data_routes

logger.info("Logger initialized")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.debug("Application shutdown")

# Create FastAPI app
app = FastAPI(
    title=app_settings.app_name,
    version=app_settings.app_version,
    debug=app_settings.debug,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(main_routes.router, prefix="/api/v1", tags=["main"])
app.include_router(ai_routes.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(data_routes.router, prefix="/api/v1/data", tags=["data"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Resume Backend API",
        "version": app_settings.app_version,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": app_settings.app_version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=app_settings.host,
        port=app_settings.port,
        reload=app_settings.reload
    )
