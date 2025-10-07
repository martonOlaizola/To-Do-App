from app.core.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Relationship


class User(Base):
  """SQLAlchemy model describing an authenticated user.

  Attributes:
    __tablename__ (str): Name of the table managed by SQLAlchemy.
    id (Column[int]): Auto incremented identifier for each user.
    email (Column[str]): Unique email address used for login.
    hashed_password (Column[str]): Bcrypt hashed password for authentication.
    tasks (Relationship['Task']): Reverse relationship to managed tasks.
  """

  __tablename__ = 'users'

  id = Column(
    Integer,
    primary_key=True,
    index=True,
  )
  email = Column(
    String(30),
    nullable=False,
  )
  hashed_password = Column(
    String(60),
    nullable=False,
  )

  tasks = Relationship('Task', back_populates="owner", cascade="all, delete")
