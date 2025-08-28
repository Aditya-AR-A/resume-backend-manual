"""
Data Service Module

Handles data loading and retrieval operations for portfolio data.
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

from app.config.settings import app_settings
from app.utils.logger import logger


class DataService:
    """Service for loading and managing portfolio data"""

    def __init__(self):
        self.data_dir = app_settings.data_dir
        self._cache = {}  # Simple in-memory cache

    def _load_json_file(self, filename: str) -> Optional[Any]:
        """Load data from a JSON file with caching"""
        if filename in self._cache:
            return self._cache[filename]

        file_path = self.data_dir / filename

        try:
            if not file_path.exists():
                logger.error(f"Data file not found: {file_path}")
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache[filename] = data
                logger.debug(f"Loaded data from {filename}")
                return data

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON file {file_path}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error loading file {file_path}: {str(e)}")
            return None

    def get_profile_data(self) -> Optional[Dict[str, Any]]:
        """Get portfolio profile data"""
        return self._load_json_file("page.json")

    def get_intro_data(self) -> Optional[Dict[str, Any]]:
        """Get introduction data"""
        return self._load_json_file("intro.json")

    def get_layout_data(self) -> Optional[Dict[str, Any]]:
        """Get layout configuration"""
        return self._load_json_file("layout.json")

    def get_projects_data(self, category: Optional[str] = None,
                         featured: Optional[bool] = None,
                         limit: int = 50) -> Optional[List[Dict[str, Any]]]:
        """Get projects data with optional filtering"""
        data = self._load_json_file("projects.json")

        if data is None:
            return None

        if not isinstance(data, list):
            logger.error("Projects data is not a list")
            return None

        projects = data

        # Apply filters
        if category:
            projects = [p for p in projects if p.get("category", "").lower() == category.lower()]

        if featured is not None:
            projects = [p for p in projects if p.get("featured", False) == featured]

        # Apply limit
        projects = projects[:limit]

        return projects

    def get_project_by_id(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific project by ID"""
        data = self._load_json_file("projects.json")

        if data is None or not isinstance(data, list):
            return None

        for project in data:
            if project.get("id") == project_id:
                return project

        return None

    def get_experience_data(self) -> Optional[List[Dict[str, Any]]]:
        """Get work experience data"""
        data = self._load_json_file("jobs.json")
        return data if isinstance(data, list) else None

    def get_certificates_data(self) -> Optional[List[Dict[str, Any]]]:
        """Get certificates data"""
        data = self._load_json_file("certificates.json")
        return data if isinstance(data, list) else None

    def clear_cache(self):
        """Clear the data cache"""
        self._cache.clear()
        logger.info("Data cache cleared")

    def get_data_stats(self) -> Dict[str, Any]:
        """Get statistics about the loaded data"""
        stats = {
            "data_directory": str(self.data_dir),
            "cached_files": list(self._cache.keys()),
            "cache_size": len(self._cache)
        }

        # Try to get actual data counts
        projects = self.get_projects_data()
        experience = self.get_experience_data()
        certificates = self.get_certificates_data()

        stats.update({
            "projects_count": len(projects) if projects else 0,
            "experience_count": len(experience) if experience else 0,
            "certificates_count": len(certificates) if certificates else 0
        })

        return stats


# Create global data service instance
data_service = DataService()
