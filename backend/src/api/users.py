"""
Users API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..services import UserService
from ..models.user import User

router = APIRouter()


@router.get("/", response_model=List[dict])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users."""
    users = UserService.get_users(db, skip=skip, limit=limit)
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at
        }
        for user in users
    ]


@router.post("/", response_model=dict)
def create_user(
    username: str,
    email: str, 
    password: str,
    first_name: str = None,
    last_name: str = None,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    try:
        user = UserService.create_user(
            db=db,
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID."""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "bio": user.bio,
        "spotify_id": user.spotify_id,
        "created_at": user.created_at,
        "last_login": user.last_login
    }