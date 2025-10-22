from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.user_schemas import UserCreate
from app.models.user_models import User
from app.core.database import get_db
from app.utils.auth import bcrypt_context as bc


def create_user(user: UserCreate, db: Session = Depends(get_db)):
  """Persist a new user with a hashed password.

  Args:
    user (UserCreate): Validated payload with registration details.
    db (Session): Database session injected by FastAPI.

  Returns:
    User: Newly saved user entity.
  """
  new_user = User(
    email=user.email,
    hashed_password=bc.hash(user.password),
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
  """Load a user by primary key.

  Args:
    user_id (int): Identifier of the user to fetch.
    db (Session): Database session injected by FastAPI.

  Returns:
    User | None: Matching user instance or None when it does not exist.
  """
  return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
  """Find a user using the email address.

  Args:
    user_email (str): Email credential used for lookup.
    db (Session): Database session injected by FastAPI.

  Returns:
    User | None: Matching user instance or None when it does not exist.
  """
  return db.query(User).filter(User.email == user_email).first()
