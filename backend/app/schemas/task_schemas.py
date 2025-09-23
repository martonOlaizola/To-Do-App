from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
  title:str
  description: Optional[str]=None
  task_type: str
  completed: bool=False

class TaskCreate(TaskBase):
  pass

class TaskUpdate(BaseModel):
  title: Optional[str] = None
  description: Optional[str] = None
  task_type: Optional[str] = None
  completed: Optional[bool] = None

class TaskOut(TaskBase):
  id: int
  class Config:
    from_attributes=True