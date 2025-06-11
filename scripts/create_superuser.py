#!/usr/bin/env python3
"""Script to create a superuser"""

import sys
from pathlib import Path
from getpass import getpass

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.database import SessionLocal
from src.services.auth_service import AuthService
from src.api.schemas import UserCreate


def create_superuser():
    """Create a superuser interactively"""
    print("Create Superuser")
    print("-" * 50)
    
    # Get user input
    username = input("Username: ").strip()
    if not username:
        print("Error: Username is required")
        return
    
    email = input("Email: ").strip()
    if not email:
        print("Error: Email is required")
        return
    
    full_name = input("Full Name (optional): ").strip()
    
    # Get password
    while True:
        password = getpass("Password: ")
        password_confirm = getpass("Confirm Password: ")
        
        if password != password_confirm:
            print("Error: Passwords do not match")
            continue
        
        if len(password) < 8:
            print("Error: Password must be at least 8 characters")
            continue
        
        break
    
    # Create user
    db = SessionLocal()
    try:
        auth_service = AuthService(db)
        
        # Check if user exists
        if auth_service.get_user_by_username(username):
            print(f"Error: Username '{username}' already exists")
            return
        
        if auth_service.get_user_by_email(email):
            print(f"Error: Email '{email}' already exists")
            return
        
        # Create superuser
        user_create = UserCreate(
            username=username,
            email=email,
            full_name=full_name or None,
            password=password,
            is_active=True,
            is_superuser=True
        )
        
        user = auth_service.create_user(user_create)
        print(f"\nSuperuser '{user.username}' created successfully!")
        
    except Exception as e:
        print(f"Error creating superuser: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_superuser()