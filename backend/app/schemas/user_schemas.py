from pydantic import BaseModel, EmailStr
from typing import Optional, List
from .task_schemas import TaskOut

class UserBase(BaseModel):
  email: EmailStr

class UserCreate(UserBase):
  password: str

class UserOut(UserBase):
  id: int
  class Config:
    from_attributes=True

class Token(BaseModel):
  access_token: str
  token_type: str