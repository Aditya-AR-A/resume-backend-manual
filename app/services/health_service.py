"""
Health Service Module

Handles system health checks, status monitoring, and diagnostics.
"""

import time
import os
from typing import Dict, Any, Optional

from app.config.settings import app_settings
from app.services.data_service import data_service
from app.services.ai_service import ai_service
from app.utils.logger import logger

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.warning("psutil not available - system monitoring features will be limited")


class HealthService:
    """Service for system health monitoring and diagnostics"""

    def __init__(self):
        self.start_time = time.time()

    def get_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        try:
            return {
                "status": "healthy",
                "timestamp": time.time(),
                "version": app_settings.app_version,
                "uptime": self._get_uptime(),
                "system": self._get_system_info(),
                "services": self._get_services_status(),
                "data": self._get_data_status()
            }
        except Exception as e:
            logger.error(f"Error getting health status: {str(e)}")
            return {
                "status": "unhealthy",
                "timestamp": time.time(),
                "error": str(e)
            }

    def get_system_status(self) -> Dict[str, Any]:
        """Get basic system status"""
        try:
            return {
                "version": app_settings.app_version,
                "debug": app_settings.debug,
                "host": app_settings.host,
                "port": app_settings.port,
                "uptime": self._get_uptime(),
                "environment": os.getenv("ENVIRONMENT", "development")
            }
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {"error": str(e)}

    def get_config_status(self) -> Dict[str, Any]:
        """Get configuration status (without sensitive data)"""
        try:
            return {
                "app_name": app_settings.app_name,
                "version": app_settings.app_version,
                "debug": app_settings.debug,
                "cors_origins": app_settings.cors_origins,
                "data_directory": str(app_settings.data_dir),
                "log_level": app_settings.log_level,
                "cache_enabled": app_settings.cache_enabled,
                "ai_providers_configured": self._count_configured_providers()
            }
        except Exception as e:
            logger.error(f"Error getting config status: {str(e)}")
            return {"error": str(e)}

    def _get_uptime(self) -> float:
        """Get system uptime in seconds"""
        return time.time() - self.start_time

    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        if not PSUTIL_AVAILABLE:
            return {
                "cpu_percent": "unavailable",
                "memory": "unavailable",
                "disk": "unavailable",
                "note": "Install psutil for detailed system monitoring"
            }

        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory": {
                    "total": psutil.virtual_memory().total,
                    "available": psutil.virtual_memory().available,
                    "percent": psutil.virtual_memory().percent
                },
                "disk": {
                    "total": psutil.disk_usage('/').total,
                    "free": psutil.disk_usage('/').free,
                    "percent": psutil.disk_usage('/').percent
                }
            }
        except Exception as e:
            logger.warning(f"Could not get system info: {str(e)}")
            return {"error": "System info unavailable"}

    def _get_services_status(self) -> Dict[str, str]:
        """Get status of various services"""
        services = {}

        try:
            # Check data service
            data_stats = data_service.get_data_stats()
            services["data_service"] = "operational" if data_stats else "error"
        except Exception as e:
            logger.warning(f"Data service check failed: {str(e)}")
            services["data_service"] = "error"

        try:
            # Check AI service
            ai_status = ai_service.get_ai_status()
            services["ai_service"] = ai_status.status
        except Exception as e:
            logger.warning(f"AI service check failed: {str(e)}")
            services["ai_service"] = "error"

        # Check database (placeholder)
        services["database"] = "not_configured"  # Since we don't have a real DB

        # Check cache (placeholder)
        services["cache"] = "operational" if app_settings.cache_enabled else "disabled"

        return services

    def _get_data_status(self) -> Dict[str, Any]:
        """Get data loading status"""
        try:
            stats = data_service.get_data_stats()
            return {
                "data_directory": stats.get("data_directory"),
                "cached_files": stats.get("cached_files", []),
                "projects_count": stats.get("projects_count", 0),
                "experience_count": stats.get("experience_count", 0),
                "certificates_count": stats.get("certificates_count", 0)
            }
        except Exception as e:
            logger.warning(f"Could not get data status: {str(e)}")
            return {"error": "Data status unavailable"}

    def _count_configured_providers(self) -> int:
        """Count configured AI providers"""
        count = 0
        if app_settings.groq_api_key:
            count += 1
        if app_settings.openai_api_key:
            count += 1
        if app_settings.anthropic_api_key:
            count += 1
        return count

    def perform_diagnostics(self) -> Dict[str, Any]:
        """Perform comprehensive system diagnostics"""
        diagnostics = {
            "timestamp": time.time(),
            "checks": []
        }

        # Data directory check
        data_dir_check = {
            "name": "Data Directory",
            "status": "pass" if app_settings.data_dir.exists() else "fail",
            "details": f"Directory: {app_settings.data_dir}"
        }
        diagnostics["checks"].append(data_dir_check)

        # Configuration check
        config_check = {
            "name": "Configuration",
            "status": "pass",
            "details": f"App: {app_settings.app_name} v{app_settings.app_version}"
        }
        diagnostics["checks"].append(config_check)

        # AI providers check
        ai_providers = self._count_configured_providers()
        ai_check = {
            "name": "AI Providers",
            "status": "pass" if ai_providers > 0 else "warning",
            "details": f"Configured providers: {ai_providers}"
        }
        diagnostics["checks"].append(ai_check)

        # Services check
        services = self._get_services_status()
        operational_count = sum(1 for status in services.values() if status == "operational")
        services_check = {
            "name": "Services",
            "status": "pass" if operational_count > 0 else "warning",
            "details": f"Operational services: {operational_count}/{len(services)}"
        }
        diagnostics["checks"].append(services_check)

        # Overall status
        failed_checks = sum(1 for check in diagnostics["checks"] if check["status"] == "fail")
        diagnostics["overall_status"] = "fail" if failed_checks > 0 else "pass"

        return diagnostics


# Create global health service instance
health_service = HealthService()
