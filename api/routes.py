from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas
from db.database import get_db
from passlib.context import CryptContext


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(user: schemas.UserLogin,db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"message": "Login successful", "user": user.username}    

