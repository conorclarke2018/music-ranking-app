"""
Ratings API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..services import RatingService

router = APIRouter()


@router.post("/")
def create_rating(
    user_id: int,
    rating: float,
    song_id: Optional[int] = None,
    album_id: Optional[int] = None,
    context: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create or update a rating."""
    if not song_id and not album_id:
        raise HTTPException(status_code=400, detail="Either song_id or album_id must be provided")
    
    if song_id and album_id:
        raise HTTPException(status_code=400, detail="Cannot rate both song and album in same request")
    
    if rating < 1 or rating > 10:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
    
    db_rating = RatingService.create_rating(
        db=db,
        user_id=user_id,
        rating=rating,
        song_id=song_id,
        album_id=album_id,
        context=context
    )
    
    return {
        "id": db_rating.id,
        "user_id": db_rating.user_id,
        "song_id": db_rating.song_id,
        "album_id": db_rating.album_id,
        "rating": db_rating.rating,
        "context": db_rating.context,
        "created_at": db_rating.created_at
    }


@router.get("/song/{song_id}/average")
def get_song_average_rating(song_id: int, db: Session = Depends(get_db)):
    """Get average rating for a song."""
    avg_rating = RatingService.get_average_rating(db, song_id=song_id)
    ratings = RatingService.get_song_ratings(db, song_id)
    
    return {
        "song_id": song_id,
        "average_rating": avg_rating,
        "total_ratings": len(ratings)
    }


@router.get("/album/{album_id}/average")
def get_album_average_rating(album_id: int, db: Session = Depends(get_db)):
    """Get average rating for an album."""
    avg_rating = RatingService.get_average_rating(db, album_id=album_id)
    ratings = RatingService.get_album_ratings(db, album_id)
    
    return {
        "album_id": album_id,
        "average_rating": avg_rating,
        "total_ratings": len(ratings)
    }