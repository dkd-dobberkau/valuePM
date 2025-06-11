# Value-Based IT Project Management System
# Foundation structure for development with Claude Code

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Dict, List, Optional, Union
import uuid


class ProjectType(Enum):
    INFRASTRUCTURE = "infrastructure"
    SOFTWARE_DEVELOPMENT = "software_development"
    DIGITAL_TRANSFORMATION = "digital_transformation"


class ValueCategory(Enum):
    COST_REDUCTION = "cost_reduction"
    REVENUE_INCREASE = "revenue_increase"
    EFFICIENCY_GAIN = "efficiency_gain"
    QUALITY_IMPROVEMENT = "quality_improvement"
    RISK_MITIGATION = "risk_mitigation"
    USER_SATISFACTION = "user_satisfaction"


class MetricType(Enum):
    CURRENCY = "currency"
    PERCENTAGE = "percentage"
    TIME = "time"
    COUNT = "count"
    SCORE = "score"


@dataclass
class ValueMetric:
    """Defines a measurable value metric"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    category: ValueCategory = ValueCategory.EFFICIENCY_GAIN
    metric_type: MetricType = MetricType.PERCENTAGE
    target_value: float = 0.0
    baseline_value: float = 0.0
    current_value: Optional[float] = None
    measurement_frequency: str = "monthly"  # daily, weekly, monthly, quarterly
    is_active: bool = True


@dataclass
class Measurement:
    """Individual measurement of a metric"""
    metric_id: str
    value: float
    measured_at: datetime
    notes: str = ""
    confidence_level: float = 1.0  # 0.0 to 1.0


@dataclass
class Stakeholder:
    """Project stakeholder with value expectations"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    role: str = ""
    department: str = ""
    primary_value_interest: List[ValueCategory] = field(default_factory=list)
    influence_level: int = 1  # 1-5 scale


@dataclass
class Deliverable:
    """Project deliverable with value contribution"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    expected_completion: date = field(default_factory=date.today)
    actual_completion: Optional[date] = None
    value_contribution: Dict[str, float] = field(default_factory=dict)  # metric_id -> expected value
    status: str = "planned"  # planned, in_progress, completed, cancelled


class Project:
    """Main project class"""
    
    def __init__(self, name: str, project_type: ProjectType):
        self.id = str(uuid.uuid4())
        self.name = name
        self.project_type = project_type
        self.created_at = datetime.now()
        self.start_date: Optional[date] = None
        self.end_date: Optional[date] = None
        self.status = "planning"
        
        # Core components
        self.metrics: Dict[str, ValueMetric] = {}
        self.measurements: List[Measurement] = []
        self.stakeholders: Dict[str, Stakeholder] = {}
        self.deliverables: Dict[str, Deliverable] = {}
        
        # Business case
        self.business_case: str = ""
        self.estimated_total_value: float = 0.0
        
    def add_metric(self, metric: ValueMetric) -> str:
        """Add a value metric to track"""
        self.metrics[metric.id] = metric
        return metric.id
    
    def record_measurement(self, metric_id: str, value: float, notes: str = "") -> None:
        """Record a measurement for a metric"""
        if metric_id not in self.metrics:
            raise ValueError(f"Metric {metric_id} not found in project")
        
        measurement = Measurement(
            metric_id=metric_id,
            value=value,
            measured_at=datetime.now(),
            notes=notes
        )
        self.measurements.append(measurement)
    
    def get_current_value(self, metric_id: str) -> Optional[float]:
        """Get the most recent measurement for a metric"""
        metric_measurements = [m for m in self.measurements if m.metric_id == metric_id]
        if not metric_measurements:
            return None
        return max(metric_measurements, key=lambda m: m.measured_at).value
    
    def calculate_roi(self) -> Dict[str, float]:
        """Calculate current ROI based on measurements"""
        roi_data = {}
        
        for metric_id, metric in self.metrics.items():
            current_value = self.get_current_value(metric_id)
            if current_value is not None:
                if metric.metric_type == MetricType.CURRENCY:
                    # For currency metrics, ROI is straightforward
                    roi_data[metric.name] = current_value
                elif metric.metric_type == MetricType.PERCENTAGE and metric.baseline_value > 0:
                    # For percentage improvements
                    improvement = (current_value - metric.baseline_value) / metric.baseline_value
                    roi_data[metric.name] = improvement
        
        return roi_data
    
    def get_value_dashboard(self) -> Dict:
        """Generate dashboard data"""
        dashboard = {
            "project_info": {
                "name": self.name,
                "type": self.project_type.value,
                "status": self.status,
                "duration_days": (datetime.now().date() - self.start_date).days if self.start_date else 0
            },
            "metrics_summary": {},
            "recent_measurements": [],
            "roi_summary": self.calculate_roi(),
            "deliverables_status": {}
        }
        
        # Metrics summary
        for metric_id, metric in self.metrics.items():
            current_value = self.get_current_value(metric_id)
            progress = 0.0
            if current_value is not None and metric.target_value != metric.baseline_value:
                progress = (current_value - metric.baseline_value) / (metric.target_value - metric.baseline_value)
            
            dashboard["metrics_summary"][metric.name] = {
                "current": current_value,
                "target": metric.target_value,
                "baseline": metric.baseline_value,
                "progress_percent": min(100, max(0, progress * 100))
            }
        
        # Recent measurements (last 5)
        recent_measurements = sorted(self.measurements, key=lambda m: m.measured_at, reverse=True)[:5]
        for measurement in recent_measurements:
            metric_name = self.metrics[measurement.metric_id].name
            dashboard["recent_measurements"].append({
                "metric": metric_name,
                "value": measurement.value,
                "date": measurement.measured_at.date(),
                "notes": measurement.notes
            })
        
        # Deliverables status
        status_counts = {}
        for deliverable in self.deliverables.values():
            status_counts[deliverable.status] = status_counts.get(deliverable.status, 0) + 1
        dashboard["deliverables_status"] = status_counts
        
        return dashboard


class ProjectTemplateFactory:
    """Factory for creating project templates with predefined metrics"""
    
    @staticmethod
    def create_infrastructure_template() -> List[ValueMetric]:
        """Template for infrastructure projects"""
        return [
            ValueMetric(
                name="System Availability",
                description="Uptime percentage",
                category=ValueCategory.QUALITY_IMPROVEMENT,
                metric_type=MetricType.PERCENTAGE,
                target_value=99.9,
                baseline_value=95.0
            ),
            ValueMetric(
                name="Response Time",
                description="Average response time in milliseconds",
                category=ValueCategory.EFFICIENCY_GAIN,
                metric_type=MetricType.TIME,
                target_value=200,
                baseline_value=500
            ),
            ValueMetric(
                name="Infrastructure Cost",
                description="Monthly infrastructure costs",
                category=ValueCategory.COST_REDUCTION,
                metric_type=MetricType.CURRENCY,
                target_value=8000,
                baseline_value=10000
            )
        ]
    
    @staticmethod
    def create_software_development_template() -> List[ValueMetric]:
        """Template for software development projects"""
        return [
            ValueMetric(
                name="User Adoption Rate",
                description="Percentage of target users actively using the software",
                category=ValueCategory.USER_SATISFACTION,
                metric_type=MetricType.PERCENTAGE,
                target_value=80.0,
                baseline_value=0.0
            ),
            ValueMetric(
                name="Development Velocity",
                description="Story points completed per sprint",
                category=ValueCategory.EFFICIENCY_GAIN,
                metric_type=MetricType.COUNT,
                target_value=50,
                baseline_value=30
            ),
            ValueMetric(
                name="Bug Resolution Time",
                description="Average time to resolve bugs in hours",
                category=ValueCategory.QUALITY_IMPROVEMENT,
                metric_type=MetricType.TIME,
                target_value=24,
                baseline_value=72
            )
        ]
    
    @staticmethod
    def create_digital_transformation_template() -> List[ValueMetric]:
        """Template for digital transformation projects"""
        return [
            ValueMetric(
                name="Process Automation Rate",
                description="Percentage of manual processes automated",
                category=ValueCategory.EFFICIENCY_GAIN,
                metric_type=MetricType.PERCENTAGE,
                target_value=70.0,
                baseline_value=10.0
            ),
            ValueMetric(
                name="Employee Productivity",
                description="Tasks completed per day per employee",
                category=ValueCategory.EFFICIENCY_GAIN,
                metric_type=MetricType.COUNT,
                target_value=15,
                baseline_value=10
            ),
            ValueMetric(
                name="Data Quality Score",
                description="Data quality index (0-100)",
                category=ValueCategory.QUALITY_IMPROVEMENT,
                metric_type=MetricType.SCORE,
                target_value=90,
                baseline_value=60
            )
        ]


class ValueProjectManager:
    """Main manager class for handling multiple projects"""
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
    
    def create_project(self, name: str, project_type: ProjectType, use_template: bool = True) -> str:
        """Create a new project with optional template"""
        project = Project(name, project_type)
        
        if use_template:
            if project_type == ProjectType.INFRASTRUCTURE:
                template_metrics = ProjectTemplateFactory.create_infrastructure_template()
            elif project_type == ProjectType.SOFTWARE_DEVELOPMENT:
                template_metrics = ProjectTemplateFactory.create_software_development_template()
            elif project_type == ProjectType.DIGITAL_TRANSFORMATION:
                template_metrics = ProjectTemplateFactory.create_digital_transformation_template()
            else:
                template_metrics = []
            
            for metric in template_metrics:
                project.add_metric(metric)
        
        self.projects[project.id] = project
        return project.id
    
    def get_portfolio_overview(self) -> Dict:
        """Get overview of all projects"""
        overview = {
            "total_projects": len(self.projects),
            "by_type": {},
            "by_status": {},
            "total_estimated_value": 0.0,
            "projects": []
        }
        
        for project in self.projects.values():
            # Count by type
            type_key = project.project_type.value
            overview["by_type"][type_key] = overview["by_type"].get(type_key, 0) + 1
            
            # Count by status
            overview["by_status"][project.status] = overview["by_status"].get(project.status, 0) + 1
            
            # Sum estimated value
            overview["total_estimated_value"] += project.estimated_total_value
            
            # Project summary
            roi_summary = project.calculate_roi()
            overview["projects"].append({
                "id": project.id,
                "name": project.name,
                "type": project.project_type.value,
                "status": project.status,
                "estimated_value": project.estimated_total_value,
                "current_roi": sum(roi_summary.values()) if roi_summary else 0.0
            })
        
        return overview


# Example usage and testing
if __name__ == "__main__":
    # Create project manager
    pm = ValueProjectManager()
    
    # Create sample projects
    infra_project_id = pm.create_project("Cloud Migration", ProjectType.INFRASTRUCTURE)
    dev_project_id = pm.create_project("Customer Portal", ProjectType.SOFTWARE_DEVELOPMENT)
    transform_project_id = pm.create_project("Digital Workflow", ProjectType.DIGITAL_TRANSFORMATION)
    
    # Get infrastructure project and add some measurements
    infra_project = pm.projects[infra_project_id]
    infra_project.start_date = date(2025, 1, 1)
    infra_project.estimated_total_value = 50000
    
    # Record some measurements
    for metric_id, metric in infra_project.metrics.items():
        if "Availability" in metric.name:
            infra_project.record_measurement(metric_id, 99.5, "Current uptime measurement")
        elif "Response Time" in metric.name:
            infra_project.record_measurement(metric_id, 300, "Average response time this week")
        elif "Cost" in metric.name:
            infra_project.record_measurement(metric_id, 9000, "Current monthly costs")
    
    # Generate dashboard
    dashboard = infra_project.get_value_dashboard()
    print("Infrastructure Project Dashboard:")
    print(f"Project: {dashboard['project_info']['name']}")
    print(f"Status: {dashboard['project_info']['status']}")
    print("\nMetrics Progress:")
    for metric_name, data in dashboard['metrics_summary'].items():
        print(f"  {metric_name}: {data['current']} (Target: {data['target']}) - {data['progress_percent']:.1f}% complete")
    
    print(f"\nROI Summary: {dashboard['roi_summary']}")
    
    # Portfolio overview
    portfolio = pm.get_portfolio_overview()
    print(f"\nPortfolio Overview:")
    print(f"Total Projects: {portfolio['total_projects']}")
    print(f"By Type: {portfolio['by_type']}")
    print(f"Total Estimated Value: ${portfolio['total_estimated_value']:,.2f}")
