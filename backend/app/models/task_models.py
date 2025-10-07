from app.core.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Relationship
from .user_models import User


class Task(Base):
  """SQLAlchemy model describing a task owned by a user.

  Attributes:
    __tablename__ (str): Name of the table managed by SQLAlchemy.
    id (Column[int]): Auto incremented identifier for the task.
    title (Column[str]): Short label supplied by the user.
    description (Column[str]): Optional details that expand on the task.
    task_type (Column[str]): Category tag such as work, personal, or study.
    completed (Column[bool]): Flag that indicates whether the task is done.
    user_id (Column[int]): Foreign key referencing the owning user.
    owner (Relationship[User]): SQLAlchemy relationship back to the user.
  """

  __tablename__ = 'tasks'
  id = Column(
    Integer,
    primary_key=True,
    index=True,
  )
  title = Column(
    String(30),
    nullable=False,
  )
  description = Column(
    String(50),
    nullable=True,
  )
  task_type = Column(
    String(50),
    nullable=False,
  )
  completed = Column(
    Boolean,
    nullable=False,
  )
  user_id = Column(
    Integer,
    ForeignKey('users.id', ondelete='CASCADE'),
  )

  owner = Relationship('User', back_populates='tasks')
