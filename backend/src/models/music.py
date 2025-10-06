"""
Music-related models for the Music Ranking App.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Artist(Base):
    """Artist model for music artists."""
    
    __tablename__ = "artists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    spotify_id = Column(String(255), unique=True, nullable=True, index=True)
    
    # Artist information
    bio = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    genres = Column(String(500), nullable=True)  # JSON string of genres
    popularity = Column(Integer, nullable=True)  # Spotify popularity score
    followers = Column(Integer, nullable=True)   # Spotify follower count
    
    # External links
    spotify_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    albums = relationship("Album", back_populates="artist", cascade="all, delete-orphan")
    songs = relationship("Song", back_populates="artist", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Artist(id={self.id}, name='{self.name}')>"


class Album(Base):
    """Album model for music albums."""
    
    __tablename__ = "albums"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    spotify_id = Column(String(255), unique=True, nullable=True, index=True)
    
    # Album information
    description = Column(Text, nullable=True)
    release_date = Column(String(50), nullable=True)  # Store as string for flexibility
    album_type = Column(String(50), nullable=True)    # album, single, compilation
    image_url = Column(String(500), nullable=True)
    total_tracks = Column(Integer, nullable=True)
    
    # Music details
    genres = Column(String(500), nullable=True)       # JSON string of genres
    label = Column(String(255), nullable=True)
    popularity = Column(Integer, nullable=True)       # Spotify popularity score
    
    # External links
    spotify_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="album", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="album", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Album(id={self.id}, title='{self.title}', artist_id={self.artist_id})>"


class Song(Base):
    """Song model for individual tracks."""
    
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    spotify_id = Column(String(255), unique=True, nullable=True, index=True)
    
    # Song information
    duration_ms = Column(Integer, nullable=True)      # Duration in milliseconds
    track_number = Column(Integer, nullable=True)
    disc_number = Column(Integer, nullable=True)
    explicit = Column(Boolean, default=False)
    preview_url = Column(String(500), nullable=True)  # 30-second preview URL
    
    # Audio features (from Spotify API)
    danceability = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    key = Column(Integer, nullable=True)
    loudness = Column(Float, nullable=True)
    mode = Column(Integer, nullable=True)
    speechiness = Column(Float, nullable=True)
    acousticness = Column(Float, nullable=True)
    instrumentalness = Column(Float, nullable=True)
    liveness = Column(Float, nullable=True)
    valence = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)
    time_signature = Column(Integer, nullable=True)
    
    # Spotify metrics
    popularity = Column(Integer, nullable=True)
    
    # External links
    spotify_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    artist = relationship("Artist", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    ratings = relationship("Rating", back_populates="song", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="song", cascade="all, delete-orphan")
    playlist_songs = relationship("PlaylistSong", back_populates="song", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Song(id={self.id}, title='{self.title}', artist_id={self.artist_id})>"
    
    @property
    def duration_formatted(self):
        """Return duration in MM:SS format."""
        if not self.duration_ms:
            return None
        total_seconds = self.duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"