"""
Playlists API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..services import PlaylistService

router = APIRouter()


@router.post("/")
def create_playlist(
    user_id: int,
    name: str,
    description: Optional[str] = None,
    is_public: bool = False,
    db: Session = Depends(get_db)
):
    """Create a new playlist."""
    playlist = PlaylistService.create_playlist(
        db=db,
        user_id=user_id,
        name=name,
        description=description,
        is_public=is_public
    )
    
    return {
        "id": playlist.id,
        "user_id": playlist.user_id,
        "name": playlist.name,
        "description": playlist.description,
        "is_public": playlist.is_public,
        "track_count": playlist.track_count,
        "created_at": playlist.created_at
    }


@router.get("/{playlist_id}")
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    """Get playlist by ID."""
    playlist = PlaylistService.get_playlist_by_id(db, playlist_id)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    return {
        "id": playlist.id,
        "user_id": playlist.user_id,
        "name": playlist.name,
        "description": playlist.description,
        "is_public": playlist.is_public,
        "is_collaborative": playlist.is_collaborative,
        "is_ai_generated": playlist.is_ai_generated,
        "track_count": playlist.track_count,
        "total_duration_ms": playlist.total_duration_ms,
        "duration_formatted": playlist.duration_formatted,
        "created_at": playlist.created_at,
        "updated_at": playlist.updated_at
    }


@router.get("/user/{user_id}")
def get_user_playlists(user_id: int, db: Session = Depends(get_db)):
    """Get all playlists for a user."""
    playlists = PlaylistService.get_user_playlists(db, user_id)
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "is_public": p.is_public,
            "track_count": p.track_count,
            "duration_formatted": p.duration_formatted,
            "updated_at": p.updated_at
        }
        for p in playlists
    ]


@router.post("/{playlist_id}/songs")
def add_song_to_playlist(
    playlist_id: int,
    song_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Add a song to a playlist."""
    playlist_song = PlaylistService.add_song_to_playlist(
        db=db,
        playlist_id=playlist_id,
        song_id=song_id,
        user_id=user_id
    )
    
    if not playlist_song:
        raise HTTPException(status_code=400, detail="Failed to add song to playlist")
    
    return {
        "playlist_id": playlist_song.playlist_id,
        "song_id": playlist_song.song_id,
        "position": playlist_song.position,
        "added_at": playlist_song.added_at
    }