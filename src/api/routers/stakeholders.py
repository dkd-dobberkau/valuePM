"""Stakeholders API router"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.api import schemas
from src.services.stakeholder_service import StakeholderService
from src.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.Stakeholder)
async def create_stakeholder(
    stakeholder: schemas.StakeholderCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Create a new stakeholder"""
    service = StakeholderService(db)
    return service.create_stakeholder(stakeholder)


@router.get("/", response_model=List[schemas.Stakeholder])
async def list_stakeholders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """List all stakeholders"""
    service = StakeholderService(db)
    return service.get_stakeholders(skip=skip, limit=limit)


@router.get("/{stakeholder_id}", response_model=schemas.Stakeholder)
async def get_stakeholder(
    stakeholder_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get stakeholder details"""
    service = StakeholderService(db)
    stakeholder = service.get_stakeholder(stakeholder_id)
    if not stakeholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stakeholder not found"
        )
    return stakeholder


@router.put("/{stakeholder_id}", response_model=schemas.Stakeholder)
async def update_stakeholder(
    stakeholder_id: str,
    stakeholder_update: schemas.StakeholderUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Update stakeholder"""
    service = StakeholderService(db)
    stakeholder = service.update_stakeholder(stakeholder_id, stakeholder_update)
    if not stakeholder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stakeholder not found"
        )
    return stakeholder


@router.delete("/{stakeholder_id}")
async def delete_stakeholder(
    stakeholder_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Delete stakeholder"""
    service = StakeholderService(db)
    if not service.delete_stakeholder(stakeholder_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stakeholder not found"
        )
    return {"detail": "Stakeholder deleted successfully"}


@router.post("/{stakeholder_id}/projects/{project_id}")
async def assign_to_project(
    stakeholder_id: str,
    project_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Assign stakeholder to project"""
    service = StakeholderService(db)
    if not service.assign_to_project(stakeholder_id, project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to assign stakeholder to project"
        )
    return {"detail": "Stakeholder assigned to project successfully"}


@router.delete("/{stakeholder_id}/projects/{project_id}")
async def remove_from_project(
    stakeholder_id: str,
    project_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Remove stakeholder from project"""
    service = StakeholderService(db)
    if not service.remove_from_project(stakeholder_id, project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to remove stakeholder from project"
        )
    return {"detail": "Stakeholder removed from project successfully"}