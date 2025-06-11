"""SQLAlchemy database models for Value-Based IT Project Management System"""

from datetime import datetime, date
from typing import Optional, List
from uuid import uuid4

from sqlalchemy import (
    Column, String, Float, Boolean, DateTime, Date, ForeignKey,
    Integer, Text, Enum as SQLEnum, JSON, Table
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum

from src.core.enums import ProjectType, ValueCategory, MetricType

Base = declarative_base()


def generate_uuid():
    return str(uuid4())


# Association tables
project_stakeholders = Table(
    'project_stakeholders',
    Base.metadata,
    Column('project_id', String, ForeignKey('projects.id'), primary_key=True),
    Column('stakeholder_id', String, ForeignKey('stakeholders.id'), primary_key=True)
)


class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    project_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(50), default="planning", nullable=False)
    business_case = Column(Text, nullable=True)
    estimated_total_value = Column(Float, default=0.0, nullable=False)
    
    # Relationships
    metrics = relationship("ValueMetric", back_populates="project", cascade="all, delete-orphan")
    measurements = relationship("Measurement", back_populates="project", cascade="all, delete-orphan")
    deliverables = relationship("Deliverable", back_populates="project", cascade="all, delete-orphan")
    stakeholders = relationship("Stakeholder", secondary=project_stakeholders, back_populates="projects")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, type={self.project_type})>"


class ValueMetric(Base):
    __tablename__ = 'value_metrics'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)
    metric_type = Column(String(50), nullable=False)
    target_value = Column(Float, nullable=False)
    baseline_value = Column(Float, nullable=False)
    current_value = Column(Float, nullable=True)
    measurement_frequency = Column(String(50), default="monthly", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="metrics")
    measurements = relationship("Measurement", back_populates="metric", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ValueMetric(id={self.id}, name={self.name}, type={self.metric_type})>"


class Measurement(Base):
    __tablename__ = 'measurements'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    metric_id = Column(String, ForeignKey('value_metrics.id'), nullable=False)
    project_id = Column(String, ForeignKey('projects.id'), nullable=False)
    value = Column(Float, nullable=False)
    measured_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)
    confidence_level = Column(Float, default=1.0, nullable=False)
    created_by = Column(String(255), nullable=True)
    
    # Relationships
    metric = relationship("ValueMetric", back_populates="measurements")
    project = relationship("Project", back_populates="measurements")
    
    def __repr__(self):
        return f"<Measurement(id={self.id}, metric_id={self.metric_id}, value={self.value})>"


class Stakeholder(Base):
    __tablename__ = 'stakeholders'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    role = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    primary_value_interests = Column(JSON, default=list)  # List of ValueCategory values
    influence_level = Column(Integer, default=1, nullable=False)  # 1-5 scale
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    projects = relationship("Project", secondary=project_stakeholders, back_populates="stakeholders")
    
    def __repr__(self):
        return f"<Stakeholder(id={self.id}, name={self.name}, role={self.role})>"


class Deliverable(Base):
    __tablename__ = 'deliverables'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    project_id = Column(String, ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    expected_completion = Column(Date, nullable=False)
    actual_completion = Column(Date, nullable=True)
    value_contribution = Column(JSON, default=dict)  # metric_id -> expected value mapping
    status = Column(String(50), default="planned", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="deliverables")
    
    def __repr__(self):
        return f"<Deliverable(id={self.id}, name={self.name}, status={self.status})>"


class User(Base):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"


class AuditLog(Base):
    """Audit log for tracking changes"""
    __tablename__ = 'audit_logs'
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String, nullable=False)
    changes = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", backref="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, resource={self.resource_type})>"