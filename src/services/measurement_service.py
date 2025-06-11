"""Measurement service"""

from datetime import date, datetime
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from src.db.models import Measurement, ValueMetric
from src.api import schemas


class MeasurementService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_measurement(self, measurement_create: schemas.MeasurementCreate, user_id: str) -> Measurement:
        """Create new measurement"""
        db_measurement = Measurement(
            **measurement_create.dict(),
            created_by=user_id
        )
        self.db.add(db_measurement)
        
        # Update metric's current value
        metric = self.db.query(ValueMetric).filter(
            ValueMetric.id == measurement_create.metric_id
        ).first()
        if metric:
            metric.current_value = measurement_create.value
        
        self.db.commit()
        self.db.refresh(db_measurement)
        return db_measurement
    
    def get_measurement(self, measurement_id: str) -> Optional[Measurement]:
        """Get measurement by ID"""
        return self.db.query(Measurement).options(
            joinedload(Measurement.metric)
        ).filter(Measurement.id == measurement_id).first()
    
    def get_metric_measurements(
        self, 
        metric_id: str, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 100
    ) -> List[Measurement]:
        """Get measurements for a specific metric"""
        query = self.db.query(Measurement).filter(Measurement.metric_id == metric_id)
        
        if start_date:
            query = query.filter(Measurement.measured_at >= datetime.combine(start_date, datetime.min.time()))
        if end_date:
            query = query.filter(Measurement.measured_at <= datetime.combine(end_date, datetime.max.time()))
        
        return query.order_by(Measurement.measured_at.desc()).limit(limit).all()
    
    def get_project_measurements(
        self,
        project_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: int = 100
    ) -> List[Measurement]:
        """Get all measurements for a project"""
        query = self.db.query(Measurement).options(
            joinedload(Measurement.metric)
        ).filter(Measurement.project_id == project_id)
        
        if start_date:
            query = query.filter(Measurement.measured_at >= datetime.combine(start_date, datetime.min.time()))
        if end_date:
            query = query.filter(Measurement.measured_at <= datetime.combine(end_date, datetime.max.time()))
        
        return query.order_by(Measurement.measured_at.desc()).limit(limit).all()
    
    def delete_measurement(self, measurement_id: str) -> bool:
        """Delete measurement"""
        db_measurement = self.get_measurement(measurement_id)
        if not db_measurement:
            return False
        
        self.db.delete(db_measurement)
        self.db.commit()
        return True