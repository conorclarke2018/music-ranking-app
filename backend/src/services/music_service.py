"""
Music service for artist, album, and song CRUD operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, func

from ..models.music import Artist, Album, Song


class MusicService:
    """Service class for music-related operations."""
    
    # Artist operations
    @staticmethod
    def create_artist(
        db: Session,
        name: str,
        spotify_id: Optional[str] = None,
        **additional_data
    ) -> Artist:
        """Create a new artist."""
        db_artist = Artist(
            name=name,
            spotify_id=spotify_id,
            **additional_data
        )
        
        try:
            db.add(db_artist)
            db.commit()
            db.refresh(db_artist)
            return db_artist
        except IntegrityError:
            db.rollback()
            raise ValueError("Artist with this Spotify ID already exists")
    
    @staticmethod
    def get_artist_by_id(db: Session, artist_id: int) -> Optional[Artist]:
        """Get artist by ID."""
        return db.query(Artist).filter(Artist.id == artist_id).first()
    
    @staticmethod
    def get_artist_by_spotify_id(db: Session, spotify_id: str) -> Optional[Artist]:
        """Get artist by Spotify ID."""
        return db.query(Artist).filter(Artist.spotify_id == spotify_id).first()
    
    @staticmethod
    def search_artists(db: Session, query: str, limit: int = 20) -> List[Artist]:
        """Search artists by name."""
        return (
            db.query(Artist)
            .filter(Artist.name.ilike(f"%{query}%"))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_popular_artists(db: Session, limit: int = 50) -> List[Artist]:
        """Get popular artists ordered by popularity."""
        return (
            db.query(Artist)
            .filter(Artist.popularity.isnot(None))
            .order_by(Artist.popularity.desc())
            .limit(limit)
            .all()
        )
    
    # Album operations
    @staticmethod
    def create_album(
        db: Session,
        title: str,
        artist_id: int,
        spotify_id: Optional[str] = None,
        **additional_data
    ) -> Album:
        """Create a new album."""
        db_album = Album(
            title=title,
            artist_id=artist_id,
            spotify_id=spotify_id,
            **additional_data
        )
        
        try:
            db.add(db_album)
            db.commit()
            db.refresh(db_album)
            return db_album
        except IntegrityError:
            db.rollback()
            raise ValueError("Album with this Spotify ID already exists")
    
    @staticmethod
    def get_album_by_id(db: Session, album_id: int) -> Optional[Album]:
        """Get album by ID."""
        return db.query(Album).filter(Album.id == album_id).first()
    
    @staticmethod
    def get_album_by_spotify_id(db: Session, spotify_id: str) -> Optional[Album]:
        """Get album by Spotify ID."""
        return db.query(Album).filter(Album.spotify_id == spotify_id).first()
    
    @staticmethod
    def get_albums_by_artist(db: Session, artist_id: int) -> List[Album]:
        """Get all albums by an artist."""
        return (
            db.query(Album)
            .filter(Album.artist_id == artist_id)
            .order_by(Album.release_date.desc())
            .all()
        )
    
    @staticmethod
    def search_albums(db: Session, query: str, limit: int = 20) -> List[Album]:
        """Search albums by title or artist name."""
        return (
            db.query(Album)
            .join(Artist)
            .filter(
                or_(
                    Album.title.ilike(f"%{query}%"),
                    Artist.name.ilike(f"%{query}%")
                )
            )
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_popular_albums(db: Session, limit: int = 50) -> List[Album]:
        """Get popular albums ordered by popularity."""
        return (
            db.query(Album)
            .filter(Album.popularity.isnot(None))
            .order_by(Album.popularity.desc())
            .limit(limit)
            .all()
        )
    
    # Song operations
    @staticmethod
    def create_song(
        db: Session,
        title: str,
        artist_id: int,
        album_id: Optional[int] = None,
        spotify_id: Optional[str] = None,
        **additional_data
    ) -> Song:
        """Create a new song."""
        db_song = Song(
            title=title,
            artist_id=artist_id,
            album_id=album_id,
            spotify_id=spotify_id,
            **additional_data
        )
        
        try:
            db.add(db_song)
            db.commit()
            db.refresh(db_song)
            return db_song
        except IntegrityError:
            db.rollback()
            raise ValueError("Song with this Spotify ID already exists")
    
    @staticmethod
    def get_song_by_id(db: Session, song_id: int) -> Optional[Song]:
        """Get song by ID."""
        return db.query(Song).filter(Song.id == song_id).first()
    
    @staticmethod
    def get_song_by_spotify_id(db: Session, spotify_id: str) -> Optional[Song]:
        """Get song by Spotify ID."""
        return db.query(Song).filter(Song.spotify_id == spotify_id).first()
    
    @staticmethod
    def get_songs_by_artist(db: Session, artist_id: int, limit: int = 100) -> List[Song]:
        """Get all songs by an artist."""
        return (
            db.query(Song)
            .filter(Song.artist_id == artist_id)
            .order_by(Song.popularity.desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_songs_by_album(db: Session, album_id: int) -> List[Song]:
        """Get all songs from an album."""
        return (
            db.query(Song)
            .filter(Song.album_id == album_id)
            .order_by(Song.track_number)
            .all()
        )
    
    @staticmethod
    def search_songs(db: Session, query: str, limit: int = 50) -> List[Song]:
        """Search songs by title or artist name."""
        return (
            db.query(Song)
            .join(Artist)
            .filter(
                or_(
                    Song.title.ilike(f"%{query}%"),
                    Artist.name.ilike(f"%{query}%")
                )
            )
            .order_by(Song.popularity.desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_popular_songs(db: Session, limit: int = 50) -> List[Song]:
        """Get popular songs ordered by popularity."""
        return (
            db.query(Song)
            .filter(Song.popularity.isnot(None))
            .order_by(Song.popularity.desc())
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_songs_by_audio_features(
        db: Session,
        min_danceability: Optional[float] = None,
        max_danceability: Optional[float] = None,
        min_energy: Optional[float] = None,
        max_energy: Optional[float] = None,
        min_valence: Optional[float] = None,
        max_valence: Optional[float] = None,
        limit: int = 50
    ) -> List[Song]:
        """Get songs filtered by audio features."""
        query = db.query(Song)
        
        if min_danceability is not None:
            query = query.filter(Song.danceability >= min_danceability)
        if max_danceability is not None:
            query = query.filter(Song.danceability <= max_danceability)
        if min_energy is not None:
            query = query.filter(Song.energy >= min_energy)
        if max_energy is not None:
            query = query.filter(Song.energy <= max_energy)
        if min_valence is not None:
            query = query.filter(Song.valence >= min_valence)
        if max_valence is not None:
            query = query.filter(Song.valence <= max_valence)
        
        return query.limit(limit).all()
    
    # Utility methods
    @staticmethod
    def get_or_create_artist(db: Session, name: str, spotify_id: Optional[str] = None) -> Artist:
        """Get existing artist or create new one."""
        if spotify_id:
            artist = MusicService.get_artist_by_spotify_id(db, spotify_id)
            if artist:
                return artist
        
        # Try to find by name if no spotify_id match
        existing = db.query(Artist).filter(Artist.name == name).first()
        if existing:
            # Update spotify_id if provided
            if spotify_id and not existing.spotify_id:
                existing.spotify_id = spotify_id
                db.commit()
                db.refresh(existing)
            return existing
        
        # Create new artist
        return MusicService.create_artist(db, name=name, spotify_id=spotify_id)
    
    @staticmethod
    def get_or_create_album(
        db: Session,
        title: str,
        artist_id: int,
        spotify_id: Optional[str] = None,
        **additional_data
    ) -> Album:
        """Get existing album or create new one."""
        if spotify_id:
            album = MusicService.get_album_by_spotify_id(db, spotify_id)
            if album:
                return album
        
        # Try to find by title and artist
        existing = (
            db.query(Album)
            .filter(Album.title == title, Album.artist_id == artist_id)
            .first()
        )
        if existing:
            # Update spotify_id if provided
            if spotify_id and not existing.spotify_id:
                existing.spotify_id = spotify_id
                db.commit()
                db.refresh(existing)
            return existing
        
        # Create new album
        return MusicService.create_album(
            db, title=title, artist_id=artist_id, spotify_id=spotify_id, **additional_data
        )