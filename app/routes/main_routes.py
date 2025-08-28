from fastapi import APIRouter, HTTPException
from app.models.schemas import HealthResponse, APIResponse
from app.config.settings import app_settings
from app.utils.logger import logger
import time

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    start_time = time.time()
    uptime = time.time() - start_time  # This would be more sophisticated in production

    return HealthResponse(
        status="healthy",
        version=app_settings.app_version,
        uptime=uptime
    )

@router.get("/status")
async def get_status():
    """Get application status"""
    return APIResponse(
        success=True,
        message="Application is running",
        data={
            "version": app_settings.app_version,
            "debug": app_settings.debug,
            "host": app_settings.host,
            "port": app_settings.port
        }
    )

@router.get("/config")
async def get_config():
    """Get application configuration (without sensitive data)"""
    return APIResponse(
        success=True,
        message="Configuration retrieved",
        data={
            "app_name": app_settings.app_name,
            "version": app_settings.app_version,
            "debug": app_settings.debug,
            "cors_origins": app_settings.cors_origins
        }
    )