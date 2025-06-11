"""Projects API router"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.api import schemas
from src.services.project_service import ProjectService
from src.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.Project)
async def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Create a new project"""
    service = ProjectService(db)
    return service.create_project(project, current_user.id)


@router.get("/", response_model=List[schemas.Project])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """List all projects"""
    service = ProjectService(db)
    return service.get_projects(skip=skip, limit=limit)


@router.get("/{project_id}", response_model=schemas.ProjectWithMetrics)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get project details"""
    service = ProjectService(db)
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


@router.put("/{project_id}", response_model=schemas.Project)
async def update_project(
    project_id: str,
    project_update: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Update project"""
    service = ProjectService(db)
    project = service.update_project(project_id, project_update)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Delete project"""
    service = ProjectService(db)
    if not service.delete_project(project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return {"detail": "Project deleted successfully"}


@router.get("/{project_id}/dashboard", response_model=schemas.ProjectDashboard)
async def get_project_dashboard(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get project dashboard data"""
    service = ProjectService(db)
    dashboard = service.get_project_dashboard(project_id)
    if not dashboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return dashboard


@router.get("/portfolio/overview", response_model=schemas.PortfolioOverview)
async def get_portfolio_overview(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get portfolio overview"""
    service = ProjectService(db)
    return service.get_portfolio_overview()