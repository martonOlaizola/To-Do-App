from app.core.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Relationship

class User(Base):
  """
  Clase que representa a los usuarios en la base de datos.

  **Atributos**
  
  - **__tablename__**: nombre de la tabla.

  - **id**(int): id del usuario.

  - **email**(str): Email del usuario.

  - **hashed_password**(str): Contraseña encriptada
  """

  __tablename__='users'

  id=Column(
    Integer,
    primary_key=True,
    index=True
  )
  email=Column(
    String(30),
    nullable=False
  )
  hashed_password=Column(
    String(60),
    nullable=False
  )

  tasks=Relationship('Task', back_populates="owner", cascade="all, delete")