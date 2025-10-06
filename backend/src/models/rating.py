"""
Rating and Review models for the Music Ranking App.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base


class Rating(Base):
    """Rating model for numerical ratings of songs and albums."""
    
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # What is being rated (one of these will be set)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=True)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    
    # Rating value (1-10 scale)
    rating = Column(Float, nullable=False)
    
    # Optional context
    context = Column(String(100), nullable=True)  # "first_listen", "after_month", etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    song = relationship("Song", back_populates="ratings")
    album = relationship("Album", back_populates="ratings")
    
    # Ensure a user can only rate the same item once per context
    __table_args__ = (
        UniqueConstraint('user_id', 'song_id', 'context', name='uq_user_song_context'),
        UniqueConstraint('user_id', 'album_id', 'context', name='uq_user_album_context'),
    )
    
    def __repr__(self):
        item_type = "song" if self.song_id else "album"
        item_id = self.song_id or self.album_id
        return f"<Rating(id={self.id}, user_id={self.user_id}, {item_type}_id={item_id}, rating={self.rating})>"
    
    @property
    def item_type(self):
        """Return the type of item being rated."""
        if self.song_id:
            return "song"
        elif self.album_id:
            return "album"
        return None
    
    @property
    def item_id(self):
        """Return the ID of the item being rated."""
        return self.song_id or self.album_id


class Review(Base):
    """Review model for written reviews of songs and albums."""
    
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # What is being reviewed (one of these will be set)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=True)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=True)
    
    # Review content
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    
    # Optional numerical rating (1-10)
    rating = Column(Float, nullable=True)
    
    # Review metadata
    is_public = Column(Integer, default=1)  # 1 = public, 0 = private
    word_count = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    song = relationship("Song", back_populates="reviews")
    album = relationship("Album", back_populates="reviews")
    
    def __repr__(self):
        item_type = "song" if self.song_id else "album"
        item_id = self.song_id or self.album_id
        return f"<Review(id={self.id}, user_id={self.user_id}, {item_type}_id={item_id})>"
    
    @property
    def item_type(self):
        """Return the type of item being reviewed."""
        if self.song_id:
            return "song"
        elif self.album_id:
            return "album"
        return None
    
    @property
    def item_id(self):
        """Return the ID of the item being reviewed."""
        return self.song_id or self.album_id
    
    def update_word_count(self):
        """Update the word count based on content."""
        if self.content:
            self.word_count = len(self.content.split())
        else:
            self.word_count = 0