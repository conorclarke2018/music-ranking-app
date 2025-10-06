"""
Playlist service for playlist and playlist song CRUD operations.
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..models.playlist import Playlist, PlaylistSong


class PlaylistService:
    """Service class for playlist operations."""
    
    # Playlist operations
    @staticmethod
    def create_playlist(
        db: Session,
        user_id: int,
        name: str,
        description: Optional[str] = None,
        is_public: bool = False,
        is_collaborative: bool = False,
        is_ai_generated: bool = False,
        ai_prompt: Optional[str] = None,
        ai_model: Optional[str] = None
    ) -> Playlist:
        """Create a new playlist."""
        db_playlist = Playlist(
            user_id=user_id,
            name=name,
            description=description,
            is_public=is_public,
            is_collaborative=is_collaborative,
            is_ai_generated=is_ai_generated,
            ai_prompt=ai_prompt,
            ai_model=ai_model
        )
        
        db.add(db_playlist)
        db.commit()
        db.refresh(db_playlist)
        return db_playlist
    
    @staticmethod
    def get_playlist_by_id(db: Session, playlist_id: int) -> Optional[Playlist]:
        """Get playlist by ID."""
        return db.query(Playlist).filter(Playlist.id == playlist_id).first()
    
    @staticmethod
    def get_user_playlists(db: Session, user_id: int) -> List[Playlist]:
        """Get all playlists created by a user."""
        return (
            db.query(Playlist)
            .filter(Playlist.user_id == user_id)
            .order_by(desc(Playlist.updated_at))
            .all()
        )
    
    @staticmethod
    def get_public_playlists(db: Session, limit: int = 50) -> List[Playlist]:
        """Get public playlists."""
        return (
            db.query(Playlist)
            .filter(Playlist.is_public == True)
            .order_by(desc(Playlist.updated_at))
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def update_playlist(
        db: Session,
        playlist_id: int,
        user_id: int,  # For authorization
        **update_data
    ) -> Optional[Playlist]:
        """Update a playlist (only by owner or if collaborative)."""
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        
        if not playlist:
            return None
        
        # Check permissions
        if playlist.user_id != user_id and not playlist.is_collaborative:
            return None
        
        for key, value in update_data.items():
            if hasattr(playlist, key):
                setattr(playlist, key, value)
        
        db.commit()
        db.refresh(playlist)
        return playlist
    
    @staticmethod
    def delete_playlist(db: Session, playlist_id: int, user_id: int) -> bool:
        """Delete a playlist (only by owner)."""
        playlist = (
            db.query(Playlist)
            .filter(Playlist.id == playlist_id, Playlist.user_id == user_id)
            .first()
        )
        
        if not playlist:
            return False
        
        db.delete(playlist)
        db.commit()
        return True
    
    # Playlist song operations
    @staticmethod
    def add_song_to_playlist(
        db: Session,
        playlist_id: int,
        song_id: int,
        user_id: int,
        position: Optional[int] = None,
        added_from_source: Optional[str] = None
    ) -> Optional[PlaylistSong]:
        """Add a song to a playlist."""
        # Check if playlist exists and user has permission
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if not playlist:
            return None
        
        if playlist.user_id != user_id and not playlist.is_collaborative:
            return None
        
        # Check if song is already in playlist
        existing = (
            db.query(PlaylistSong)
            .filter(PlaylistSong.playlist_id == playlist_id, PlaylistSong.song_id == song_id)
            .first()
        )
        if existing:
            return existing
        
        # Determine position if not provided
        if position is None:
            last_position = (
                db.query(PlaylistSong.position)
                .filter(PlaylistSong.playlist_id == playlist_id)
                .order_by(desc(PlaylistSong.position))
                .first()
            )
            position = (last_position[0] + 1) if last_position else 0
        
        # Create playlist song entry
        db_playlist_song = PlaylistSong(
            playlist_id=playlist_id,
            song_id=song_id,
            position=position,
            added_by_user_id=user_id,
            added_from_source=added_from_source
        )
        
        db.add(db_playlist_song)
        db.commit()
        
        # Update playlist stats
        playlist.update_stats()
        db.commit()
        
        db.refresh(db_playlist_song)
        return db_playlist_song
    
    @staticmethod
    def remove_song_from_playlist(
        db: Session,
        playlist_id: int,
        song_id: int,
        user_id: int
    ) -> bool:
        """Remove a song from a playlist."""
        # Check permissions
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if not playlist:
            return False
        
        if playlist.user_id != user_id and not playlist.is_collaborative:
            return False
        
        # Find and remove the playlist song
        playlist_song = (
            db.query(PlaylistSong)
            .filter(PlaylistSong.playlist_id == playlist_id, PlaylistSong.song_id == song_id)
            .first()
        )
        
        if not playlist_song:
            return False
        
        db.delete(playlist_song)
        db.commit()
        
        # Update playlist stats
        playlist.update_stats()
        db.commit()
        
        return True
    
    @staticmethod
    def reorder_playlist_songs(
        db: Session,
        playlist_id: int,
        user_id: int,
        song_positions: List[tuple[int, int]]  # [(song_id, new_position), ...]
    ) -> bool:
        """Reorder songs in a playlist."""
        # Check permissions
        playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if not playlist:
            return False
        
        if playlist.user_id != user_id and not playlist.is_collaborative:
            return False
        
        # Update positions
        for song_id, new_position in song_positions:
            playlist_song = (
                db.query(PlaylistSong)
                .filter(PlaylistSong.playlist_id == playlist_id, PlaylistSong.song_id == song_id)
                .first()
            )
            if playlist_song:
                playlist_song.position = new_position
        
        db.commit()
        return True
    
    @staticmethod
    def get_playlist_songs(db: Session, playlist_id: int) -> List[PlaylistSong]:
        """Get all songs in a playlist ordered by position."""
        return (
            db.query(PlaylistSong)
            .filter(PlaylistSong.playlist_id == playlist_id)
            .order_by(PlaylistSong.position)
            .all()
        )
    
    @staticmethod
    def duplicate_playlist(
        db: Session,
        playlist_id: int,
        user_id: int,
        new_name: Optional[str] = None
    ) -> Optional[Playlist]:
        """Create a copy of a playlist."""
        original = db.query(Playlist).filter(Playlist.id == playlist_id).first()
        if not original:
            return None
        
        # Check if playlist is public or user has access
        if not original.is_public and original.user_id != user_id:
            return None
        
        # Create new playlist
        new_playlist = PlaylistService.create_playlist(
            db=db,
            user_id=user_id,
            name=new_name or f"{original.name} (Copy)",
            description=original.description,
            is_public=False,  # Copies are private by default
            is_collaborative=False
        )
        
        # Copy songs
        original_songs = PlaylistService.get_playlist_songs(db, playlist_id)
        for ps in original_songs:
            PlaylistService.add_song_to_playlist(
                db=db,
                playlist_id=new_playlist.id,
                song_id=ps.song_id,
                user_id=user_id,
                position=ps.position,
                added_from_source="duplicate"
            )
        
        return new_playlist
    
    @staticmethod
    def search_playlists(db: Session, query: str, limit: int = 20) -> List[Playlist]:
        """Search public playlists by name."""
        return (
            db.query(Playlist)
            .filter(
                Playlist.is_public == True,
                Playlist.name.ilike(f"%{query}%")
            )
            .order_by(desc(Playlist.updated_at))
            .limit(limit)
            .all()
        )