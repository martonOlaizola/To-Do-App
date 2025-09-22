from app.core.database import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Relationship
from .user_models import User

class Task(Base):
  """
  Clase que representa a las tareas en la base de datos

  **Atributos**
  
  - **__tablename__**(str): Nombre de la tabla.

  - **id**(int): ID de la tarea.

  - **title**(str): Nombre de la tarea.

  - **description**(str): Descripción de la tarea.

  - **completed**(bool): Estado de la tarea. True si está completa, False si está incompleta.
  """

  __tablename__='tasks'
  id=Column(
    Integer,
    primary_key=True,
    index=True
  )
  title=Column(
    String(30),
    nullable=False
  )
  description=Column(
    String(50),
    nullable=True
  )
  completed=Column(
    Boolean,
    nullable=False
  )
  user_id=Column(
    Integer,
    ForeignKey('users.id', ondelete='CASCADE')
  )

  owner=Relationship('User', back_populates='tasks')