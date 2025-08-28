from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import (
    PortfolioProfile, ExperienceList, ProjectList,
    CertificationData, APIResponse, FilterOptions,
    PaginatedProjectsResponse, PaginatedJobsResponse,
    PaginatedCertificatesResponse
)
from app.services import data_service
from app.utils.logger import logger

router = APIRouter()

@router.get("/profile", response_model=APIResponse)
async def get_profile():
    """Get portfolio profile information"""
    data = data_service.get_profile_data()
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
    data = data_service.get_intro_data()
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
    data = data_service.get_layout_data()
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
    projects = data_service.get_projects_data(
        category=category,
        featured=featured,
        limit=limit
    )

    if projects is None:
        raise HTTPException(status_code=404, detail="Projects data not found")

    return APIResponse(
        success=True,
        message=f"Retrieved {len(projects)} projects",
        data=projects
    )

@router.get("/experience", response_model=APIResponse)
async def get_experience():
    """Get work experience data"""
    data = data_service.get_experience_data()
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
    data = data_service.get_certificates_data()
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
    project = data_service.get_project_by_id(project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return APIResponse(
        success=True,
        message="Project retrieved successfully",
        data=project
    )