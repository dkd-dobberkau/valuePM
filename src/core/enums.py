"""Enumerations for the Value-Based IT Project Management System"""

from enum import Enum


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


class ProjectStatus(Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DeliverableStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MeasurementFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"