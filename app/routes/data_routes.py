from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import json
import os
from app.models.schemas import (
    PortfolioProfile, ExperienceList, ProjectList,
    CertificationData, APIResponse, FilterOptions,
    PaginatedProjectsResponse, PaginatedJobsResponse,
    PaginatedCertificatesResponse
)
from app.config.settings import app_settings
from app.utils.logger import logger

router = APIRouter()

def load_json_data(filename: str):
    """Load data from JSON file"""
    file_path = app_settings.data_dir / filename
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Data file not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file {file_path}: {str(e)}")
        return None

@router.get("/profile", response_model=APIResponse)
async def get_profile():
    """Get portfolio profile information"""
    data = load_json_data("page.json")
    if data is None:
        raise HTTPException(status_code=404, detail="Profile data not found")

    return APIResponse(
        success=True,
        message="Profile retrieved successfully",
        data=data
    )

@router.get("/intro", response_model=APIResponse)
async def get_intro():
    """Get introduction information"""
    data = load_json_data("intro.json")
    if data is None:
        raise HTTPException(status_code=404, detail="Intro data not found")

    return APIResponse(
        success=True,
        message="Introduction retrieved successfully",
        data=data
    )

@router.get("/layout", response_model=APIResponse)
async def get_layout():
    """Get layout configuration"""
    data = load_json_data("layout.json")
    if data is None:
        raise HTTPException(status_code=404, detail="Layout data not found")

    return APIResponse(
        success=True,
        message="Layout retrieved successfully",
        data=data
    )

@router.get("/projects", response_model=APIResponse)
async def get_projects(
    category: Optional[str] = Query(None, description="Filter by category"),
    featured: Optional[bool] = Query(None, description="Filter featured projects"),
    limit: int = Query(50, description="Limit number of results")
):
    """Get projects data with optional filtering"""
    data = load_json_data("projects.json")
    if data is None:
        raise HTTPException(status_code=404, detail="Projects data not found")

    projects = data if isinstance(data, list) else []

    # Apply filters
    if category:
        projects = [p for p in projects if p.get("category", "").lower() == category.lower()]

    if featured is not None:
        projects = [p for p in projects if p.get("featured", False) == featured]

    # Apply limit
    projects = projects[:limit]

    return APIResponse(
        success=True,
        message=f"Retrieved {len(projects)} projects",
        data=projects
    )

@router.get("/experience", response_model=APIResponse)
async def get_experience():
    """Get work experience data"""
    data = load_json_data("jobs.json")
    if data is None:
        raise HTTPException(status_code=404, detail="Experience data not found")

    return APIResponse(
        success=True,
        message="Experience data retrieved successfully",
        data=data
    )

@router.get("/certificates", response_model=APIResponse)
async def get_certificates():
    """Get certificates data"""
    data = load_json_data("certificates.json")
    if data is None:
        raise HTTPException(status_code=404, detail="Certificates data not found")

    return APIResponse(
        success=True,
        message="Certificates retrieved successfully",
        data=data
    )

@router.get("/projects/{project_id}", response_model=APIResponse)
async def get_project_by_id(project_id: str):
    """Get specific project by ID"""
    data = load_json_data("projects.json")
    if data is None:
        raise HTTPException(status_code=404, detail="Projects data not found")

    projects = data if isinstance(data, list) else []
    project = next((p for p in projects if p.get("id") == project_id), None)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return APIResponse(
        success=True,
        message="Project retrieved successfully",
        data=project
    )