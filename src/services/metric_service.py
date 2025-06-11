"""Metric service"""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.db.models import ValueMetric
from src.api import schemas


class MetricService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_metric(self, metric_create: schemas.ValueMetricCreate) -> ValueMetric:
        """Create new metric"""
        db_metric = ValueMetric(**metric_create.dict())
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric
    
    def get_metric(self, metric_id: str) -> Optional[ValueMetric]:
        """Get metric by ID"""
        return self.db.query(ValueMetric).filter(ValueMetric.id == metric_id).first()
    
    def get_project_metrics(self, project_id: str, active_only: bool = True) -> List[ValueMetric]:
        """Get all metrics for a project"""
        query = self.db.query(ValueMetric).filter(ValueMetric.project_id == project_id)
        if active_only:
            query = query.filter(ValueMetric.is_active == True)
        return query.all()
    
    def update_metric(self, metric_id: str, metric_update: schemas.ValueMetricUpdate) -> Optional[ValueMetric]:
        """Update metric"""
        db_metric = self.get_metric(metric_id)
        if not db_metric:
            return None
        
        update_data = metric_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_metric, field, value)
        
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric
    
    def delete_metric(self, metric_id: str) -> bool:
        """Soft delete metric by setting is_active=False"""
        db_metric = self.get_metric(metric_id)
        if not db_metric:
            return False
        
        db_metric.is_active = False
        self.db.commit()
        return True