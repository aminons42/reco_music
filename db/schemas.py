from pydantic import BaseModel
from typing import Optional,List 

class UserLogin(BaseModel):
    password: str
    username: Optional[str]
    class Config:
        orm_mode = True
class UserBase(UserLogin):
    id: int        
class SongBase(BaseModel):
    title: str
    artist: Optional[str]
    genre: Optional[str]
    release_year: Optional[int]
class Song(SongBase):
    id: int

    class Config:
        orm_mode = True
class InteractionBase(BaseModel):
    liked: bool
class InteractionCreate(InteractionBase):
    user_id: int
    song_id: int
class Interaction(InteractionBase):
    id: int
    user_id: int
    song_id: int

    class Config:
        orm_mode = True
