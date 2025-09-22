from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.task_models import Task
from app.schemas.task_schemas import TaskCreate, TaskOut, TaskUpdate

def create_task(task: TaskCreate, user_id: int , db: Session = Depends(get_db)) -> TaskOut:
  """
  Crea una tarea en la base de datos

  **Recibe:**

  - **task** (TaskCreate): Tarea a añadir.

  - **db**: Base de datos.

  **Retorna:**

  - **TaskOut**: Tarea con id asociado
  """
  new_task = Task(
    **task.model_dump(),
    user_id = user_id
    )
  db.add(new_task)
  db.commit()
  db.refresh(new_task)
  return new_task

def get_all_tasks(db: Session = Depends(get_db)) -> List[TaskOut]:
  """
  Devuelve todas las tareas de la base de datos

  **Recibe:**

  - **db**: Base de datos.

  **Retorna:**
  Lista de tareas
  """
  tasks = db.query(Task).all()
  return tasks

def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
  """
  Devuelve una tarea que coincida con el id buscado

  **Recibe:**

  - **task_id** (int): ID de la tarea.

  - **db**: Base de datos.

  **Retorna:**

  - **TaskOut**
  """
  return db.query(Task).filter(Task.id == task_id).first()

def get_all_tasks_from_user(user_id: int, db: Session = Depends(get_db)):
  return db.query(Task).filter(Task.user_id == user_id).all()

def update_task(task: TaskUpdate, task_id: int, db: Session = Depends(get_db)):
  task_db = db.query(Task).filter(Task.id == task_id).first()
  task_db.title = task.title if task.title else task_db.title
  task_db.description = task.description if task.description else task_db.description
  task_db.completed = task.completed if task.completed else task_db.completed
  db.commit()
  db.refresh(task_db)
  return task_db

def delete_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
  task_db = db.query(Task).filter(Task.id == task_id and Task.user_id == user_id).first()
  if task_db is None:
    raise HTTPException(
      status_code=404,
      detail="Tarea no encontrada."
    )
  db.delete(task_db)
  db.commit()