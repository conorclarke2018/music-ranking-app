"""
Music API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..services import MusicService

router = APIRouter()


@router.get("/search")
def search_music(q: str, limit: int = 20, db: Session = Depends(get_db)):
    """Search for artists, albums, and songs."""
    artists = MusicService.search_artists(db, q, limit)
    albums = MusicService.search_albums(db, q, limit)
    songs = MusicService.search_songs(db, q, limit)
    
    return {
        "artists": [{"id": a.id, "name": a.name, "spotify_id": a.spotify_id} for a in artists],
        "albums": [{"id": a.id, "title": a.title, "artist_id": a.artist_id, "spotify_id": a.spotify_id} for a in albums],
        "songs": [{"id": s.id, "title": s.title, "artist_id": s.artist_id, "album_id": s.album_id, "spotify_id": s.spotify_id} for s in songs]
    }


@router.get("/artists/{artist_id}")
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    """Get artist by ID."""
    artist = MusicService.get_artist_by_id(db, artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    return {
        "id": artist.id,
        "name": artist.name,
        "spotify_id": artist.spotify_id,
        "bio": artist.bio,
        "image_url": artist.image_url,
        "genres": artist.genres,
        "popularity": artist.popularity
    }


@router.get("/albums/{album_id}")
def get_album(album_id: int, db: Session = Depends(get_db)):
    """Get album by ID."""
    album = MusicService.get_album_by_id(db, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    return {
        "id": album.id,
        "title": album.title,
        "artist_id": album.artist_id,
        "spotify_id": album.spotify_id,
        "description": album.description,
        "release_date": album.release_date,
        "album_type": album.album_type,
        "image_url": album.image_url,
        "total_tracks": album.total_tracks,
        "popularity": album.popularity
    }


@router.get("/songs/{song_id}")
def get_song(song_id: int, db: Session = Depends(get_db)):
    """Get song by ID."""
    song = MusicService.get_song_by_id(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    return {
        "id": song.id,
        "title": song.title,
        "artist_id": song.artist_id,
        "album_id": song.album_id,
        "spotify_id": song.spotify_id,
        "duration_ms": song.duration_ms,
        "duration_formatted": song.duration_formatted,
        "track_number": song.track_number,
        "popularity": song.popularity,
        "danceability": song.danceability,
        "energy": song.energy,
        "valence": song.valence
    }


@router.post("/artists")
def create_artist(name: str, spotify_id: Optional[str] = None, db: Session = Depends(get_db)):
    """Create a new artist."""
    try:
        artist = MusicService.create_artist(db, name=name, spotify_id=spotify_id)
        return {
            "id": artist.id,
            "name": artist.name,
            "spotify_id": artist.spotify_id,
            "created_at": artist.created_at
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))