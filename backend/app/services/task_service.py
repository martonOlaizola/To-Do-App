from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.task_models import Task
from app.schemas.task_schemas import TaskCreate, TaskOut, TaskUpdate


def create_task(task: TaskCreate, user_id: int, db: Session = Depends(get_db)) -> TaskOut:
  """Persist a new task belonging to the provided user.

  Args:
    task (TaskCreate): Validated payload with task attributes.
    user_id (int): Identifier of the user that will own the task.
    db (Session): Database session injected by FastAPI.

  Returns:
    TaskOut: ORM instance refreshed with its database identifier.
  """
  new_task = Task(
    **task.model_dump(),
    user_id=user_id,
  )
  db.add(new_task)
  db.commit()
  db.refresh(new_task)
  return new_task


def get_all_tasks(db: Session = Depends(get_db)) -> List[TaskOut]:
  """Retrieve every task stored in the database.

  Args:
    db (Session): Database session injected by FastAPI.

  Returns:
    List[TaskOut]: Collection of persisted tasks.
  """
  tasks = db.query(Task).all()
  return tasks


def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
  """Load a specific task by its primary key.

  Args:
    task_id (int): Identifier of the task to retrieve.
    db (Session): Database session injected by FastAPI.

  Returns:
    Task | None: Matching task instance or None when it does not exist.
  """
  return db.query(Task).filter(Task.id == task_id).first()


def get_all_tasks_from_user(user_id: int, db: Session = Depends(get_db)):
  """Return every task assigned to a given user.

  Args:
    user_id (int): Identifier of the task owner.
    db (Session): Database session injected by FastAPI.

  Returns:
    List[Task]: Tasks that belong to the requested user.
  """
  return db.query(Task).filter(Task.user_id == user_id).all()


def update_task(task: TaskUpdate, task_id: int, user_id, db: Session = Depends(get_db)):
  """Modify the stored attributes of an existing task.

  Args:
    task (TaskUpdate): Partial payload with the desired changes.
    task_id (int): Identifier of the task to update.
    db (Session): Database session injected by FastAPI.

  Returns:
    Task: Updated ORM entity synced with the database.
  """
  task_db = db.query(Task).filter(Task.id == task_id and task.user_id == user_id).first()
  task_db.title = task.title if task.title else task_db.title
  task_db.description = task.description if task.description else task_db.description
  task_db.task_type = task.task_type if task.task_type else task_db.task_type
  task_db.completed = task.completed if task.completed is not None else task_db.completed
  db.commit()
  db.refresh(task_db)
  return task_db


def delete_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
  """Remove a task owned by the provided user.

  Args:
    task_id (int): Identifier of the task to delete.
    user_id (int): Identifier of the authenticated user.
    db (Session): Database session injected by FastAPI.

  Raises:
    HTTPException: When the task does not exist for that user.
  """
  task_db = db.query(Task).filter(Task.id == task_id and Task.user_id == user_id).first()
  if task_db is None:
    raise HTTPException(
      status_code=404,
      detail="Tarea no encontrada.",
    )
  db.delete(task_db)
  db.commit()


def delete_completed_tasks(user_id: int, db: Session = Depends(get_db)):
  """Delete every completed task that belongs to the given user.

  Args:
    user_id (int): Identifier of the authenticated user.
    db (Session): Database session injected by FastAPI.

  Raises:
    HTTPException: When no completed tasks exist for the user.
  """
  task_db = db.query(Task).filter(Task.completed == True and Task.user_id == user_id).all()
  if task_db is None:
    raise HTTPException(
      status_code=404,
      detail="El usuario no tiene tareas completadas",
    )
  for task in task_db:
    db.delete(task)
    db.commit()
