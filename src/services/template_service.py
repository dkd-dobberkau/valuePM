"""Template service for project metrics"""

from typing import List, Dict, Any
from src.core.enums import ProjectType, ValueCategory, MetricType, MeasurementFrequency


class TemplateService:
    """Service for managing project templates"""
    
    def get_template_metrics(self, project_type: ProjectType) -> List[Dict[str, Any]]:
        """Get template metrics for a project type"""
        if project_type == ProjectType.INFRASTRUCTURE:
            return self._infrastructure_metrics()
        elif project_type == ProjectType.SOFTWARE_DEVELOPMENT:
            return self._software_development_metrics()
        elif project_type == ProjectType.DIGITAL_TRANSFORMATION:
            return self._digital_transformation_metrics()
        else:
            return []
    
    def _infrastructure_metrics(self) -> List[Dict[str, Any]]:
        """Infrastructure project metrics template"""
        return [
            {
                "name": "System Availability",
                "description": "Uptime percentage",
                "category": ValueCategory.QUALITY_IMPROVEMENT,
                "metric_type": MetricType.PERCENTAGE,
                "target_value": 99.9,
                "baseline_value": 95.0,
                "measurement_frequency": MeasurementFrequency.WEEKLY
            },
            {
                "name": "Response Time",
                "description": "Average response time in milliseconds",
                "category": ValueCategory.EFFICIENCY_GAIN,
                "metric_type": MetricType.TIME,
                "target_value": 200,
                "baseline_value": 500,
                "measurement_frequency": MeasurementFrequency.DAILY
            },
            {
                "name": "Infrastructure Cost",
                "description": "Monthly infrastructure costs",
                "category": ValueCategory.COST_REDUCTION,
                "metric_type": MetricType.CURRENCY,
                "target_value": 8000,
                "baseline_value": 10000,
                "measurement_frequency": MeasurementFrequency.MONTHLY
            }
        ]
    
    def _software_development_metrics(self) -> List[Dict[str, Any]]:
        """Software development project metrics template"""
        return [
            {
                "name": "User Adoption Rate",
                "description": "Percentage of target users actively using the software",
                "category": ValueCategory.USER_SATISFACTION,
                "metric_type": MetricType.PERCENTAGE,
                "target_value": 80.0,
                "baseline_value": 0.0,
                "measurement_frequency": MeasurementFrequency.WEEKLY
            },
            {
                "name": "Development Velocity",
                "description": "Story points completed per sprint",
                "category": ValueCategory.EFFICIENCY_GAIN,
                "metric_type": MetricType.COUNT,
                "target_value": 50,
                "baseline_value": 30,
                "measurement_frequency": MeasurementFrequency.WEEKLY
            },
            {
                "name": "Bug Resolution Time",
                "description": "Average time to resolve bugs in hours",
                "category": ValueCategory.QUALITY_IMPROVEMENT,
                "metric_type": MetricType.TIME,
                "target_value": 24,
                "baseline_value": 72,
                "measurement_frequency": MeasurementFrequency.DAILY
            }
        ]
    
    def _digital_transformation_metrics(self) -> List[Dict[str, Any]]:
        """Digital transformation project metrics template"""
        return [
            {
                "name": "Process Automation Rate",
                "description": "Percentage of manual processes automated",
                "category": ValueCategory.EFFICIENCY_GAIN,
                "metric_type": MetricType.PERCENTAGE,
                "target_value": 70.0,
                "baseline_value": 10.0,
                "measurement_frequency": MeasurementFrequency.MONTHLY
            },
            {
                "name": "Employee Productivity",
                "description": "Tasks completed per day per employee",
                "category": ValueCategory.EFFICIENCY_GAIN,
                "metric_type": MetricType.COUNT,
                "target_value": 15,
                "baseline_value": 10,
                "measurement_frequency": MeasurementFrequency.WEEKLY
            },
            {
                "name": "Data Quality Score",
                "description": "Data quality index (0-100)",
                "category": ValueCategory.QUALITY_IMPROVEMENT,
                "metric_type": MetricType.SCORE,
                "target_value": 90,
                "baseline_value": 60,
                "measurement_frequency": MeasurementFrequency.MONTHLY
            }
        ]