from fastapi import APIRouter, HTTPException
from app.models.schemas import HealthResponse, APIResponse
from app.services import health_service
from app.utils.logger import logger

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    health_data = health_service.get_health_status()

    return HealthResponse(
        status=health_data.get("status", "unknown"),
        version=health_data.get("version", "unknown"),
        uptime=health_data.get("uptime"),
        timestamp=health_data.get("timestamp")
    )

@router.get("/status")
async def get_status():
    """Get application status"""
    status_data = health_service.get_system_status()

    return APIResponse(
        success=True,
        message="Application is running",
        data=status_data
    )

@router.get("/config")
async def get_config():
    """Get application configuration (without sensitive data)"""
    config_data = health_service.get_config_status()

    return APIResponse(
        success=True,
        message="Configuration retrieved",
        data=config_data
    )