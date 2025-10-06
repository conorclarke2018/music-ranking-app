"""
Playlist models for the Music Ranking App.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Playlist(Base):
    """Playlist model for user-created playlists."""
    
    __tablename__ = "playlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Playlist information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    
    # Playlist settings
    is_public = Column(Boolean, default=False)
    is_collaborative = Column(Boolean, default=False)
    is_ai_generated = Column(Boolean, default=False)
    
    # AI generation metadata (if applicable)
    ai_prompt = Column(Text, nullable=True)
    ai_model = Column(String(100), nullable=True)
    
    # Spotify integration
    spotify_id = Column(String(255), nullable=True)
    spotify_url = Column(String(500), nullable=True)
    
    # Stats
    total_duration_ms = Column(Integer, default=0)
    track_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_played = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="playlists")
    playlist_songs = relationship("PlaylistSong", back_populates="playlist", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Playlist(id={self.id}, name='{self.name}', user_id={self.user_id})>"
    
    def update_stats(self):
        """Update playlist statistics based on songs."""
        if self.playlist_songs:
            self.track_count = len(self.playlist_songs)
            total_duration = sum(
                (ps.song.duration_ms or 0) for ps in self.playlist_songs if ps.song
            )
            self.total_duration_ms = total_duration
        else:
            self.track_count = 0
            self.total_duration_ms = 0
    
    @property
    def duration_formatted(self):
        """Return total duration in hours and minutes format."""
        if not self.total_duration_ms:
            return "0:00"
        
        total_seconds = self.total_duration_ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:00"
        else:
            return f"{minutes}:{(total_seconds % 60):02d}"


class PlaylistSong(Base):
    """Association model for songs in playlists."""
    
    __tablename__ = "playlist_songs"
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    
    # Position in playlist
    position = Column(Integer, nullable=False, default=0)
    
    # Metadata about when/how song was added
    added_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    added_from_source = Column(String(100), nullable=True)  # "search", "recommendation", "ai"
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    playlist = relationship("Playlist", back_populates="playlist_songs")
    song = relationship("Song", back_populates="playlist_songs")
    added_by = relationship("User", foreign_keys=[added_by_user_id])
    
    # Ensure a song can't be added to the same playlist multiple times
    __table_args__ = (
        UniqueConstraint('playlist_id', 'song_id', name='uq_playlist_song'),
    )
    
    def __repr__(self):
        return f"<PlaylistSong(playlist_id={self.playlist_id}, song_id={self.song_id}, position={self.position})>"