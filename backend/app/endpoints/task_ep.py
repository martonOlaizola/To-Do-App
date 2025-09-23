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
  tags=['Tasks']
)

@router.post(
  "/create",
  response_model=TaskOut,
  status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: dict =  Depends(auth.get_current_user)):
  user_id = int(current_user['user_id'])
  task_db = task_crud.create_task(task, user_id, db)
  return task_db

@router.get(
  "/",
  response_model=List[TaskOut],
  status_code=status.HTTP_200_OK
)
def get_all_task(db: Session = Depends(get_db)):
  task_db = task_crud.get_all_tasks(db)
  return task_db

@router.get(
  "/{task_id}",
  status_code=status.HTTP_200_OK,
  response_model=TaskOut
)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
  task_db = task_crud.get_task_by_id(task_id, db)
  if task_db is None:
    raise HTTPException(
      status_code=400,
      detail="Tarea no encontrada."
    )
  return task_db

@router.get(
    "/get-from-user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[TaskOut]
)
def get_all_tasks_from_user(user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
  user_id = int(user['user_id'])
  task_db = task_crud.get_all_tasks_from_user(user_id, db)
  return task_db

@router.put(
  "/update/{task_id}",
  status_code=status.HTTP_200_OK,
  response_model=TaskOut
)
def update_task(task: TaskUpdate, task_id: int, db: Session = Depends(get_db)):
  task_db = task_crud.get_task_by_id(task_id, db)
  if task_db is None:
    raise HTTPException(
      status_code=404,
      detail="Tarea no encontrada."
    )
  return task_crud.update_task(task, task_id, db)

@router.delete(
  '/delete/{task_id}',
  status_code=status.HTTP_200_OK
)
def delete_task(task_id: int, user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
  user_id = int(user['user_id'])
  task_db = task_crud.delete_task(task_id, user_id, db)
  return task_db
