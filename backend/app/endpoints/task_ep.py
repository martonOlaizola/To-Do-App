from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.task_models import Task
from app.schemas.task_schemas import TaskCreate, TaskOut, TaskUpdate
from app.crud import task_crud
from app.utils import auth

router = APIRouter(
  prefix='/tasks',
  tags=['Tasks'],
)


@router.post(
  "/create",
  response_model=TaskOut,
  status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: dict = Depends(auth.get_current_user)):
  """Create a new task owned by the authenticated user.

  Args:
    task (TaskCreate): Payload with the task details.
    db (Session): Database session injected by FastAPI.
    current_user (dict): Authenticated principal info provided by the token.

  Returns:
    TaskOut: Newly created task serialized for the response.
  """
  user_id = int(current_user['user_id'])
  task_db = task_crud.create_task(task, user_id, db)
  return task_db


@router.get(
  "/",
  response_model=List[TaskOut],
  status_code=status.HTTP_200_OK,
)
def get_all_task(db: Session = Depends(get_db)):
  """Fetch every task stored in the system.

  Args:
    db (Session): Database session injected by FastAPI.

  Returns:
    List[TaskOut]: All persisted tasks regardless of owner.
  """
  task_db = task_crud.get_all_tasks(db)
  return task_db


@router.get(
  "/{task_id}",
  status_code=status.HTTP_200_OK,
  response_model=TaskOut,
)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
  """Retrieve a task by identifier.

  Args:
    task_id (int): Primary key of the task to load.
    db (Session): Database session injected by FastAPI.

  Raises:
    HTTPException: When the task does not exist.

  Returns:
    TaskOut: Task that matches the provided identifier.
  """
  task_db = task_crud.get_task_by_id(task_id, db)
  if task_db is None:
    raise HTTPException(
      status_code=400,
      detail="Tarea no encontrada.",
    )
  return task_db


@router.get(
  "/get-from-user/{user_id}",
  status_code=status.HTTP_200_OK,
  response_model=List[TaskOut],
)
def get_all_tasks_from_user(user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
  """Return the tasks that belong to the authenticated user.

  Args:
    user (dict): Authenticated principal info provided by the token.
    db (Session): Database session injected by FastAPI.

  Returns:
    List[TaskOut]: Tasks linked to the requesting user.
  """
  user_id = int(user['user_id'])
  task_db = task_crud.get_all_tasks_from_user(user_id, db)
  return task_db


@router.put(
  "/update/{task_id}",
  status_code=status.HTTP_200_OK,
  response_model=TaskOut,
)
def update_task(task: TaskUpdate, task_id: int, db: Session = Depends(get_db)):
  """Update an existing task with the provided changes.

  Args:
    task (TaskUpdate): Partial payload describing the update.
    task_id (int): Identifier of the task to modify.
    db (Session): Database session injected by FastAPI.

  Raises:
    HTTPException: When the target task does not exist.

  Returns:
    TaskOut: Updated task data serialized for the response.
  """
  task_db = task_crud.get_task_by_id(task_id, db)
  if task_db is None:
    raise HTTPException(
      status_code=404,
      detail="Tarea no encontrada.",
    )
  return task_crud.update_task(task, task_id, db)


@router.delete(
  '/delete/{task_id}',
  status_code=status.HTTP_200_OK,
)
def delete_task(task_id: int, user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
  """Delete a task owned by the authenticated user.

  Args:
    task_id (int): Identifier of the task to delete.
    user (dict): Authenticated principal info provided by the token.
    db (Session): Database session injected by FastAPI.

  Returns:
    None: The deletion is performed for its side effects.
  """
  user_id = int(user['user_id'])
  task_db = task_crud.delete_task(task_id, user_id, db)
  return task_db


@router.delete(
  '/delete_completed',
  status_code=status.HTTP_200_OK,
)
def delete_completed_tasks(user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
  """Erase every completed task associated with the authenticated user.

  Args:
    user (dict): Authenticated principal info provided by the token.
    db (Session): Database session injected by FastAPI.

  Returns:
    None: The deletion is performed for its side effects.
  """
  user_id = int(user['user_id'])
  task_db = task_crud.delete_completed_tasks(user_id, db)
  return task_db
