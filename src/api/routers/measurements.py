"""Measurements API router"""

from typing import List
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.api import schemas
from src.services.measurement_service import MeasurementService
from src.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.Measurement)
async def create_measurement(
    measurement: schemas.MeasurementCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Record a new measurement"""
    service = MeasurementService(db)
    return service.create_measurement(measurement, current_user.id)


@router.get("/metric/{metric_id}", response_model=List[schemas.Measurement])
async def list_metric_measurements(
    metric_id: str,
    start_date: date = Query(None),
    end_date: date = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """List measurements for a specific metric"""
    service = MeasurementService(db)
    return service.get_metric_measurements(
        metric_id, 
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )


@router.get("/project/{project_id}", response_model=List[schemas.Measurement])
async def list_project_measurements(
    project_id: str,
    start_date: date = Query(None),
    end_date: date = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """List all measurements for a project"""
    service = MeasurementService(db)
    return service.get_project_measurements(
        project_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )


@router.get("/{measurement_id}", response_model=schemas.Measurement)
async def get_measurement(
    measurement_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get measurement details"""
    service = MeasurementService(db)
    measurement = service.get_measurement(measurement_id)
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )
    return measurement


@router.delete("/{measurement_id}")
async def delete_measurement(
    measurement_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Delete measurement"""
    service = MeasurementService(db)
    if not service.delete_measurement(measurement_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found"
        )
    return {"detail": "Measurement deleted successfully"}