"""
Rating service for rating and review CRUD operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from ..models.rating import Rating, Review


class RatingService:
    """Service class for rating and review operations."""
    
    # Rating operations
    @staticmethod
    def create_rating(
        db: Session,
        user_id: int,
        rating: float,
        song_id: Optional[int] = None,
        album_id: Optional[int] = None,
        context: Optional[str] = None
    ) -> Rating:
        """Create or update a rating."""
        # Check if rating already exists for this user/item/context combination
        existing = (
            db.query(Rating)
            .filter(
                Rating.user_id == user_id,
                Rating.song_id == song_id,
                Rating.album_id == album_id,
                Rating.context == context
            )
            .first()
        )
        
        if existing:
            # Update existing rating
            existing.rating = rating
            db.commit()
            db.refresh(existing)
            return existing
        
        # Create new rating
        db_rating = Rating(
            user_id=user_id,
            song_id=song_id,
            album_id=album_id,
            rating=rating,
            context=context
        )
        
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating
    
    @staticmethod
    def get_rating_by_id(db: Session, rating_id: int) -> Optional[Rating]:
        """Get rating by ID."""
        return db.query(Rating).filter(Rating.id == rating_id).first()
    
    @staticmethod
    def get_user_ratings(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Rating]:
        """Get all ratings by a user."""
        return (
            db.query(Rating)
            .filter(Rating.user_id == user_id)
            .order_by(desc(Rating.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_song_ratings(db: Session, song_id: int) -> List[Rating]:
        """Get all ratings for a song."""
        return db.query(Rating).filter(Rating.song_id == song_id).all()
    
    @staticmethod
    def get_album_ratings(db: Session, album_id: int) -> List[Rating]:
        """Get all ratings for an album."""
        return db.query(Rating).filter(Rating.album_id == album_id).all()
    
    @staticmethod
    def get_average_rating(db: Session, song_id: Optional[int] = None, album_id: Optional[int] = None) -> Optional[float]:
        """Get average rating for a song or album."""
        query = db.query(func.avg(Rating.rating))
        
        if song_id:
            query = query.filter(Rating.song_id == song_id)
        elif album_id:
            query = query.filter(Rating.album_id == album_id)
        else:
            return None
        
        result = query.scalar()
        return float(result) if result else None
    
    # Review operations
    @staticmethod
    def create_review(
        db: Session,
        user_id: int,
        content: str,
        song_id: Optional[int] = None,
        album_id: Optional[int] = None,
        title: Optional[str] = None,
        rating: Optional[float] = None,
        is_public: bool = True
    ) -> Review:
        """Create a new review."""
        db_review = Review(
            user_id=user_id,
            song_id=song_id,
            album_id=album_id,
            title=title,
            content=content,
            rating=rating,
            is_public=1 if is_public else 0
        )
        
        # Update word count
        db_review.update_word_count()
        
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
    
    @staticmethod
    def get_review_by_id(db: Session, review_id: int) -> Optional[Review]:
        """Get review by ID."""
        return db.query(Review).filter(Review.id == review_id).first()
    
    @staticmethod
    def get_user_reviews(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> List[Review]:
        """Get all reviews by a user."""
        return (
            db.query(Review)
            .filter(Review.user_id == user_id)
            .order_by(desc(Review.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_song_reviews(db: Session, song_id: int, public_only: bool = True) -> List[Review]:
        """Get all reviews for a song."""
        query = db.query(Review).filter(Review.song_id == song_id)
        if public_only:
            query = query.filter(Review.is_public == 1)
        return query.order_by(desc(Review.created_at)).all()
    
    @staticmethod
    def get_album_reviews(db: Session, album_id: int, public_only: bool = True) -> List[Review]:
        """Get all reviews for an album."""
        query = db.query(Review).filter(Review.album_id == album_id)
        if public_only:
            query = query.filter(Review.is_public == 1)
        return query.order_by(desc(Review.created_at)).all()
    
    @staticmethod
    def update_review(
        db: Session,
        review_id: int,
        user_id: int,  # For authorization
        **update_data
    ) -> Optional[Review]:
        """Update a review (only by the owner)."""
        review = (
            db.query(Review)
            .filter(Review.id == review_id, Review.user_id == user_id)
            .first()
        )
        
        if not review:
            return None
        
        for key, value in update_data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        
        # Update word count if content changed
        if 'content' in update_data:
            review.update_word_count()
        
        db.commit()
        db.refresh(review)
        return review
    
    @staticmethod
    def delete_review(db: Session, review_id: int, user_id: int) -> bool:
        """Delete a review (only by the owner)."""
        review = (
            db.query(Review)
            .filter(Review.id == review_id, Review.user_id == user_id)
            .first()
        )
        
        if not review:
            return False
        
        db.delete(review)
        db.commit()
        return True
    
    @staticmethod
    def get_recent_reviews(db: Session, limit: int = 20) -> List[Review]:
        """Get recent public reviews."""
        return (
            db.query(Review)
            .filter(Review.is_public == 1)
            .order_by(desc(Review.created_at))
            .limit(limit)
            .all()
        )