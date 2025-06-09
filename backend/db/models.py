from sqlalchemy import String, Integer, Column, ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ ="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(100))
    password=Column(String(255))
    created_at=Column(DateTime)
    interactions=relationship("Interaction",back_populates="user")

class Song(Base):
    __tablename__="songs"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(255))
    artist=Column(String(255))
    genre=Column(String(100))
    release_year=Column(Integer)
    created_at=Column(DateTime)
    interactions=relationship("Interaction",back_populates="song")

class Interaction(Base):
    __tablename__="interactions"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    song_id=Column(Integer,ForeignKey("songs.id"))
    liked=Column(Boolean)
    interaction_time=Column(DateTime)
    user=relationship("User",back_populates="interactions")
    song=relationship("Song",back_populates="interactions")

    
    
    