"""
User service for CRUD operations and business logic.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from ..models.user import User

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def create_user(
        db: Session,
        username: str,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> User:
        """Create a new user."""
        hashed_password = pwd_context.hash(password)
        
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name
        )
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            db.rollback()
            if "username" in str(e.orig):
                raise ValueError("Username already exists")
            elif "email" in str(e.orig):
                raise ValueError("Email already exists")
            else:
                raise ValueError("User creation failed")
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_spotify_id(db: Session, spotify_id: str) -> Optional[User]:
        """Get user by Spotify ID."""
        return db.query(User).filter(User.spotify_id == spotify_id).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(
        db: Session,
        user_id: int,
        **update_data
    ) -> Optional[User]:
        """Update user information."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))
        
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as e:
            db.rollback()
            if "username" in str(e.orig):
                raise ValueError("Username already exists")
            elif "email" in str(e.orig):
                raise ValueError("Email already exists")
            else:
                raise ValueError("User update failed")
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Soft delete user (deactivate)."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        user.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username and password."""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        
        if not UserService.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    @staticmethod
    def update_spotify_tokens(
        db: Session,
        user_id: int,
        spotify_id: str,
        access_token: str,
        refresh_token: Optional[str] = None
    ) -> Optional[User]:
        """Update user's Spotify integration tokens."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        user.spotify_id = spotify_id
        user.spotify_access_token = access_token
        if refresh_token:
            user.spotify_refresh_token = refresh_token
        
        db.commit()
        db.refresh(user)
        return user