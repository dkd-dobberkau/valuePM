"""Project service"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from src.db.models import Project, ValueMetric, Measurement, Stakeholder, Deliverable
from src.api import schemas
from src.core.enums import ProjectType, ProjectStatus
from src.services.template_service import TemplateService


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.template_service = TemplateService()
    
    def create_project(self, project_create: schemas.ProjectCreate, user_id: str) -> Project:
        """Create new project"""
        db_project = Project(
            name=project_create.name,
            project_type=project_create.project_type.value if hasattr(project_create.project_type, 'value') else project_create.project_type,
            start_date=project_create.start_date,
            end_date=project_create.end_date,
            status=project_create.status.value if hasattr(project_create.status, 'value') else project_create.status,
            business_case=project_create.business_case,
            estimated_total_value=project_create.estimated_total_value
        )
        self.db.add(db_project)
        self.db.flush()
        
        # Add template metrics if requested
        if project_create.use_template:
            template_metrics = self.template_service.get_template_metrics(project_create.project_type)
            for metric_data in template_metrics:
                metric = ValueMetric(
                    project_id=db_project.id,
                    **metric_data
                )
                self.db.add(metric)
        
        self.db.commit()
        self.db.refresh(db_project)
        return db_project
    
    def get_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        """Get all projects"""
        return self.db.query(Project).offset(skip).limit(limit).all()
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get project by ID with related data"""
        return self.db.query(Project).options(
            joinedload(Project.metrics),
            joinedload(Project.stakeholders),
            joinedload(Project.deliverables)
        ).filter(Project.id == project_id).first()
    
    def update_project(self, project_id: str, project_update: schemas.ProjectUpdate) -> Optional[Project]:
        """Update project"""
        db_project = self.db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return None
        
        update_data = project_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        self.db.commit()
        self.db.refresh(db_project)
        return db_project
    
    def delete_project(self, project_id: str) -> bool:
        """Delete project"""
        db_project = self.db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return False
        
        self.db.delete(db_project)
        self.db.commit()
        return True
    
    def get_project_dashboard(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Generate project dashboard data"""
        project = self.get_project(project_id)
        if not project:
            return None
        
        # Get recent measurements
        recent_measurements = self.db.query(Measurement).filter(
            Measurement.project_id == project_id
        ).order_by(Measurement.measured_at.desc()).limit(5).all()
        
        # Calculate metrics summary
        metrics_summary = {}
        roi_summary = {}
        
        for metric in project.metrics:
            if not metric.is_active:
                continue
            
            # Get current value from latest measurement
            latest_measurement = self.db.query(Measurement).filter(
                Measurement.metric_id == metric.id
            ).order_by(Measurement.measured_at.desc()).first()
            
            current_value = latest_measurement.value if latest_measurement else None
            metric.current_value = current_value
            
            # Calculate progress
            progress = 0.0
            if current_value is not None and metric.target_value != metric.baseline_value:
                progress = (current_value - metric.baseline_value) / (metric.target_value - metric.baseline_value)
            
            metrics_summary[metric.name] = schemas.MetricSummary(
                name=metric.name,
                current=current_value,
                target=metric.target_value,
                baseline=metric.baseline_value,
                progress_percent=min(100, max(0, progress * 100))
            )
            
            # Calculate ROI
            if current_value is not None:
                if metric.metric_type.value == "currency":
                    roi_summary[metric.name] = current_value
                elif metric.metric_type.value == "percentage" and metric.baseline_value > 0:
                    improvement = (current_value - metric.baseline_value) / metric.baseline_value
                    roi_summary[metric.name] = improvement
        
        # Count deliverables by status
        deliverables_status = self.db.query(
            Deliverable.status, func.count(Deliverable.id)
        ).filter(
            Deliverable.project_id == project_id
        ).group_by(Deliverable.status).all()
        
        deliverables_status_dict = {status: count for status, count in deliverables_status}
        
        # Build dashboard
        dashboard = schemas.ProjectDashboard(
            project_info={
                "name": project.name,
                "type": project.project_type.value,
                "status": project.status,
                "duration_days": (datetime.now().date() - project.start_date).days if project.start_date else 0
            },
            metrics_summary=metrics_summary,
            recent_measurements=[{
                "metric": m.metric.name,
                "value": m.value,
                "date": m.measured_at.date(),
                "notes": m.notes
            } for m in recent_measurements],
            roi_summary=roi_summary,
            deliverables_status=deliverables_status_dict
        )
        
        return dashboard
    
    def get_portfolio_overview(self) -> schemas.PortfolioOverview:
        """Get portfolio overview"""
        projects = self.db.query(Project).all()
        
        by_type = {}
        by_status = {}
        total_estimated_value = 0.0
        project_summaries = []
        
        for project in projects:
            # Count by type
            type_key = project.project_type.value
            by_type[type_key] = by_type.get(type_key, 0) + 1
            
            # Count by status
            by_status[project.status] = by_status.get(project.status, 0) + 1
            
            # Sum estimated value
            total_estimated_value += project.estimated_total_value
            
            # Calculate current ROI
            roi_total = 0.0
            for metric in project.metrics:
                if metric.current_value is not None:
                    if metric.metric_type.value == "currency":
                        roi_total += metric.current_value
            
            project_summaries.append({
                "id": project.id,
                "name": project.name,
                "type": project.project_type.value,
                "status": project.status,
                "estimated_value": project.estimated_total_value,
                "current_roi": roi_total
            })
        
        return schemas.PortfolioOverview(
            total_projects=len(projects),
            by_type=by_type,
            by_status=by_status,
            total_estimated_value=total_estimated_value,
            projects=project_summaries
        )