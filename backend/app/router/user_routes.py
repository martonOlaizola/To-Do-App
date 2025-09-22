from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
from typing import List, Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schemas import UserCreate, UserOut, Token
from app.core.database import get_db
from app.crud import user_crud
from app.utils import auth as user_auth

router = APIRouter(
  prefix='/auth',
  tags=['Auth']
)

@router.post(
  "/create",
  response_model=UserOut,
  status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  user_db = user_crud.get_user_by_email(user.email, db)
  if user_db:
    raise HTTPException(
      status_code=400,
      detail="El usuario ya existe."
    )
  return user_crud.create_user(user, db)

@router.post(
  "/token",
  status_code=status.HTTP_200_OK,
  response_model=Token
)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
  user = user_auth.authenticate_user(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(
    status_code=401,
    detail="El usuario no se pudo validar."
    )
  token = user_auth.create_token(user.email, user.id, timedelta(minutes=20))
  return {'access_token': token, 'token_type': 'bearer'}

@router.get(
  '/{user_id}',
  response_model=UserOut,
  status_code=status.HTTP_200_OK,
  )
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
  user_db = user_crud.get_user_by_id(user_id, db)
  if user_db is None:
    raise HTTPException(
      status_code=404,
      detail="Usuario no encontrado."
    )
  return user_db

@router.get(
  '/email/{user_email}',
  response_model=UserOut,
  status_code=status.HTTP_200_OK
)
def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
  user_db = user_crud.get_user_by_email(user_email, db)
  if user_db is None:
    raise HTTPException(
      status_code=404,
      detail="Usuario no encontrado."
    )
  return user_db