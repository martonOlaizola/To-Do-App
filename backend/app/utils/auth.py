from fastapi import Depends, HTTPException
from typing import Annotated
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.core.database import get_db
from app.core.config import settings
from app.models.user_models import User

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def authenticate_user(user_email: str, user_password: str, db: Session = Depends(get_db)):
  user  = db.query(User).filter(User.email == user_email).first()
  if user is None:
    return False
  if bcrypt_context.verify(user_password, user.hashed_password) is None:
    return False
  return user

def create_token(user_email: str, user_id: int, expires_delta = timedelta):
  encode = {'sub': user_email, 'id': user_id}
  expires = datetime.now(timezone.utc) + expires_delta
  encode.update({'exp': expires})
  return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_email = payload.get('sub')
    user_id = payload.get('id')
    if user_email is None or user_id is None:
      raise HTTPException(
        status_code=401,
        detail='El usuario no se pudo validar'
      )
    return {'user_email': user_email, 'user_id': user_id}
  except JWTError:
    raise HTTPException(
        status_code=401,
        detail='El usuario no se pudo validar'
      )