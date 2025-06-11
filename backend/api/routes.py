from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas
from db.database import get_db
from passlib.context import CryptContext
from typing import List
from backend.elasticsearch.indexing import get_recommendations, search_songs_es


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(user: schemas.UserLogin,db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"status": "ok", "message": "Login successful", "user": user.username}    
@router.post("/interactions" , response_model=schemas.Interaction)
def interaction_liked(interaction:schemas.InteractionCreate,db:Session= Depends(get_db)):
    db_interaction = db.query(models.Interaction).filter(
        models.Interaction.user_id == interaction.user_id,
        models.Interaction.song_id == interaction.song_id
    ).first()
    if db_interaction:
        db_interaction.liked = interaction.liked
        db_interaction.interaction_time = interaction.interaction_time
    else:
        db_interaction=models.Interaction(**interaction.dict())
        db.add(db_interaction)  
    db.commit()
    db.refresh(db_interaction) 
    return db_interaction
@router.get("/interactions/{user_id}",response_model=List[schemas.Interaction])
def get_user_interactions(user_id: int ,db:Session = Depends(get_db)):
    db_interaction = db.query(models.Interaction).filter( models.Interaction.user_id==user_id).all()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="No interactions found for this user")
    return db_interaction

@router.get("/recommendations/{user_id}")
def get_user_recommendations(user_id: int):
    songs = get_recommendations(user_id)
    return {"user_id": user_id, "recommended_songs": songs}

@router.get("/songs", response_model=List[schemas.Song])
def get_all_songs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Song).offset(skip).limit(limit).all()

@router.get("/users")
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return {"id": user.id, "username": user.username}
    return {}

@router.delete("/interactions/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(models.Interaction).filter(models.Interaction.id == interaction_id).first()
    if interaction:
        db.delete(interaction)
        db.commit()
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Interaction not found")

@router.get("/songs/search", response_model=List[schemas.Song])
def search_songs(q: str, skip: int = 0, limit: int = 10):
    try:
        return search_songs_es(q, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching songs: {str(e)}")
