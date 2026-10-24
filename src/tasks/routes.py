from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.models import User
from src.auth.dependencies import get_current_active_user
from src.tasks.dtos import TaskCreate, TaskUpdate, TaskResponse
from src.tasks.controller import (
    create_task,
    list_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)

task = APIRouter(prefix="/tasks", tags=["Tasks"])


@task.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_new_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return create_task(db, current_user, task_data)


@task.get("", response_model=list[TaskResponse])
def get_user_tasks(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return list_tasks(db, current_user, limit=limit, offset=offset)


@task.get("/{task_id}", response_model=TaskResponse)
def get_single_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return get_task_by_id(db, current_user, task_id)


@task.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int,
    update_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return update_task(db, current_user, task_id, update_data)


@task.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    delete_task(db, current_user, task_id)
    return None
