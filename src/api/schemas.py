"""Pydantic schemas for API validation"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field

from src.core.enums import (
    ProjectType, ValueCategory, MetricType, 
    ProjectStatus, DeliverableStatus, MeasurementFrequency
)


# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        use_enum_values = True


# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class User(UserBase):
    id: str
    created_at: datetime
    last_login: Optional[datetime] = None


# Auth schemas
class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    username: Optional[str] = None


# Project schemas
class ProjectBase(BaseSchema):
    name: str
    project_type: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "planning"
    business_case: Optional[str] = None
    estimated_total_value: float = 0.0


class ProjectCreate(ProjectBase):
    use_template: bool = True


class ProjectUpdate(BaseSchema):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    business_case: Optional[str] = None
    estimated_total_value: Optional[float] = None


class Project(ProjectBase):
    id: str
    created_at: datetime
    updated_at: datetime


class ProjectWithMetrics(Project):
    metrics: List["ValueMetric"] = []
    recent_measurements: List["Measurement"] = []
    stakeholders: List["Stakeholder"] = []
    deliverables: List["Deliverable"] = []


# Value Metric schemas
class ValueMetricBase(BaseSchema):
    name: str
    description: Optional[str] = None
    category: str
    metric_type: str
    target_value: float
    baseline_value: float
    current_value: Optional[float] = None
    measurement_frequency: str = "monthly"
    is_active: bool = True


class ValueMetricCreate(ValueMetricBase):
    project_id: str


class ValueMetricUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    target_value: Optional[float] = None
    baseline_value: Optional[float] = None
    current_value: Optional[float] = None
    measurement_frequency: Optional[str] = None
    is_active: Optional[bool] = None


class ValueMetric(ValueMetricBase):
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime


# Measurement schemas
class MeasurementBase(BaseSchema):
    metric_id: str
    value: float
    notes: Optional[str] = None
    confidence_level: float = Field(1.0, ge=0.0, le=1.0)


class MeasurementCreate(MeasurementBase):
    project_id: str


class Measurement(MeasurementBase):
    id: str
    project_id: str
    measured_at: datetime
    created_by: Optional[str] = None


# Stakeholder schemas
class StakeholderBase(BaseSchema):
    name: str
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    primary_value_interests: List[ValueCategory] = []
    influence_level: int = Field(1, ge=1, le=5)


class StakeholderCreate(StakeholderBase):
    pass


class StakeholderUpdate(BaseSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    department: Optional[str] = None
    primary_value_interests: Optional[List[ValueCategory]] = None
    influence_level: Optional[int] = Field(None, ge=1, le=5)


class Stakeholder(StakeholderBase):
    id: str
    created_at: datetime
    updated_at: datetime


# Deliverable schemas
class DeliverableBase(BaseSchema):
    name: str
    description: Optional[str] = None
    expected_completion: date
    actual_completion: Optional[date] = None
    value_contribution: Dict[str, float] = {}
    status: str = "planned"


class DeliverableCreate(DeliverableBase):
    project_id: str


class DeliverableUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    expected_completion: Optional[date] = None
    actual_completion: Optional[date] = None
    value_contribution: Optional[Dict[str, float]] = None
    status: Optional[DeliverableStatus] = None


class Deliverable(DeliverableBase):
    id: str
    project_id: str
    created_at: datetime
    updated_at: datetime


# Dashboard schemas
class MetricSummary(BaseSchema):
    name: str
    current: Optional[float]
    target: float
    baseline: float
    progress_percent: float


class ProjectDashboard(BaseSchema):
    project_info: Dict[str, Any]
    metrics_summary: Dict[str, MetricSummary]
    recent_measurements: List[Dict[str, Any]]
    roi_summary: Dict[str, float]
    deliverables_status: Dict[str, int]


class PortfolioOverview(BaseSchema):
    total_projects: int
    by_type: Dict[str, int]
    by_status: Dict[str, int]
    total_estimated_value: float
    projects: List[Dict[str, Any]]


# Update forward references
ProjectWithMetrics.model_rebuild()
ValueMetric.model_rebuild()
Measurement.model_rebuild()
Stakeholder.model_rebuild()
Deliverable.model_rebuild()