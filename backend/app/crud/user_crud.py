from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
from app.models.user_models import User
from app.core.database import get_db
from app.utils.auth import bcrypt_context as bc

def create_user(user: UserCreate, db: Session = Depends(get_db)):
  new_user = User(
    email= user.email,
    hashed_password = bc.hash(user.password)
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
  return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
  return db.query(User).filter(User.email == user_email).first()