"""Metrics API router"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.api import schemas
from src.services.metric_service import MetricService
from src.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.ValueMetric)
async def create_metric(
    metric: schemas.ValueMetricCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Create a new metric for a project"""
    service = MetricService(db)
    return service.create_metric(metric)


@router.get("/project/{project_id}", response_model=List[schemas.ValueMetric])
async def list_project_metrics(
    project_id: str,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """List all metrics for a project"""
    service = MetricService(db)
    return service.get_project_metrics(project_id, active_only)


@router.get("/{metric_id}", response_model=schemas.ValueMetric)
async def get_metric(
    metric_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get metric details"""
    service = MetricService(db)
    metric = service.get_metric(metric_id)
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metric not found"
        )
    return metric


@router.put("/{metric_id}", response_model=schemas.ValueMetric)
async def update_metric(
    metric_id: str,
    metric_update: schemas.ValueMetricUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Update metric"""
    service = MetricService(db)
    metric = service.update_metric(metric_id, metric_update)
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metric not found"
        )
    return metric


@router.delete("/{metric_id}")
async def delete_metric(
    metric_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Delete metric (soft delete by setting is_active=False)"""
    service = MetricService(db)
    if not service.delete_metric(metric_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metric not found"
        )
    return {"detail": "Metric deleted successfully"}