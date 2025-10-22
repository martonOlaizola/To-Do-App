from pydantic import BaseModel, field_validator
from typing import Optional


class TaskBase(BaseModel):
  """Shared attributes for task payloads exchanged with the API.

  Attributes:
    title (str): Short label that identifies the task.
    description (Optional[str]): Optional text with additional details.
    task_type (str): Category such as work, personal, or study.
    completed (bool): Indicator showing whether the task is complete.
  """

  title: str
  description: Optional[str] = None
  task_type: str
  completed: bool = False

  @field_validator("task_type")
  def validate_task_type(value: str) -> str:
    valid_types = ['trabajo', 'personal', 'estudio']
    if value.lower() not in valid_types:
      raise ValueError(f'{value} is not a valid type')
    return value
  
  @field_validator("title")
  def validate_title(value: str) -> str:
    if len(value) > 30:
      raise ValueError('Title too long, 30 characters max')
    return value

  @field_validator("description")
  def validate_description(value: str) -> str:
    if len(value) > 50:
      raise ValueError('Description too long, 50 characters max')
    return value

class TaskCreate(TaskBase):
  """Payload used when creating a new task."""
  pass

class TaskUpdate(BaseModel):
  """Partial payload that conveys task updates.

  Attributes:
    title (Optional[str]): Updated title if provided.
    description (Optional[str]): Updated description if provided.
    task_type (Optional[str]): Updated category if provided.
    completed (Optional[bool]): Updated completion flag if provided.
  """

  title: Optional[str] = None
  description: Optional[str] = None
  task_type: Optional[str] = None
  completed: Optional[bool] = None

  @field_validator("task_type")
  def validate_task_type(value: str) -> str:
    valid_types = ['trabajo', 'personal', 'estudio']
    if value not in valid_types:
      raise ValueError(f'{value} is not a valid type')
    return value
  
  @field_validator("title")
  def validate_title(value: str) -> str:
    if len(value) > 30:
      raise ValueError('Title too long')
    return value
  @field_validator("description")
  def validate_description(value: str) -> str:
    if len(value) > 50:
      raise ValueError('Description too long')

class TaskOut(TaskBase):
  """Representation of a task returned to the client.

  Attributes:
    id (int): Identifier assigned by the database.
  """

  id: int

  class Config:
    """Allow conversion from SQLAlchemy objects."""

    from_attributes = True
