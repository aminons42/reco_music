from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, schemas
from app.db.database import get_db

router = APIRouter()
