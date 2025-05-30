from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas
from db.database import get_db
from passlib.context import CryptContext
from typing import List


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
@router.post("/interactions")
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
@router.get("/interactions/{user_id}",response_model=List[schemas.Interaction])
def get_user_interactions(user:schemas.UserBase,db:Session = Depends(get_db)):
    db_interaction = db.query(models.Interaction).filter(user.id == models.Interaction.user_id).all()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="No interactions found for this user")
    return db_interaction


