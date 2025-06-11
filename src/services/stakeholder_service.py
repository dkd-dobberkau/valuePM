"""Stakeholder service"""

from typing import List, Optional
from sqlalchemy.orm import Session

from src.db.models import Stakeholder, Project
from src.api import schemas


class StakeholderService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_stakeholder(self, stakeholder_create: schemas.StakeholderCreate) -> Stakeholder:
        """Create new stakeholder"""
        # Convert ValueCategory enums to strings for JSON storage
        value_interests = [v.value if hasattr(v, 'value') else v for v in stakeholder_create.primary_value_interests]
        
        db_stakeholder = Stakeholder(
            name=stakeholder_create.name,
            email=stakeholder_create.email,
            role=stakeholder_create.role,
            department=stakeholder_create.department,
            primary_value_interests=value_interests,
            influence_level=stakeholder_create.influence_level
        )
        self.db.add(db_stakeholder)
        self.db.commit()
        self.db.refresh(db_stakeholder)
        return db_stakeholder
    
    def get_stakeholder(self, stakeholder_id: str) -> Optional[Stakeholder]:
        """Get stakeholder by ID"""
        return self.db.query(Stakeholder).filter(Stakeholder.id == stakeholder_id).first()
    
    def get_stakeholders(self, skip: int = 0, limit: int = 100) -> List[Stakeholder]:
        """Get all stakeholders"""
        return self.db.query(Stakeholder).offset(skip).limit(limit).all()
    
    def update_stakeholder(
        self, 
        stakeholder_id: str, 
        stakeholder_update: schemas.StakeholderUpdate
    ) -> Optional[Stakeholder]:
        """Update stakeholder"""
        db_stakeholder = self.get_stakeholder(stakeholder_id)
        if not db_stakeholder:
            return None
        
        update_data = stakeholder_update.dict(exclude_unset=True)
        
        # Handle value interests conversion
        if 'primary_value_interests' in update_data:
            update_data['primary_value_interests'] = [
                v.value if hasattr(v, 'value') else v for v in update_data['primary_value_interests']
            ]
        
        for field, value in update_data.items():
            setattr(db_stakeholder, field, value)
        
        self.db.commit()
        self.db.refresh(db_stakeholder)
        return db_stakeholder
    
    def delete_stakeholder(self, stakeholder_id: str) -> bool:
        """Delete stakeholder"""
        db_stakeholder = self.get_stakeholder(stakeholder_id)
        if not db_stakeholder:
            return False
        
        self.db.delete(db_stakeholder)
        self.db.commit()
        return True
    
    def assign_to_project(self, stakeholder_id: str, project_id: str) -> bool:
        """Assign stakeholder to project"""
        stakeholder = self.get_stakeholder(stakeholder_id)
        project = self.db.query(Project).filter(Project.id == project_id).first()
        
        if not stakeholder or not project:
            return False
        
        if project not in stakeholder.projects:
            stakeholder.projects.append(project)
            self.db.commit()
        
        return True
    
    def remove_from_project(self, stakeholder_id: str, project_id: str) -> bool:
        """Remove stakeholder from project"""
        stakeholder = self.get_stakeholder(stakeholder_id)
        project = self.db.query(Project).filter(Project.id == project_id).first()
        
        if not stakeholder or not project:
            return False
        
        if project in stakeholder.projects:
            stakeholder.projects.remove(project)
            self.db.commit()
        
        return True