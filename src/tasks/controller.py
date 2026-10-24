from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models import Task, Milestone, TaskStatus, User
from src.tasks.dtos import TaskCreate, TaskUpdate


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def validate_dates(start_date: datetime | None, deadline: datetime | None):
    if start_date and deadline and start_date > deadline:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="start_date must not be later than deadline"
        )


def create_task(db: Session, user: User, task_data: TaskCreate) -> Task:
    validate_dates(task_data.start_date, task_data.deadline)

    completed_on = utc_now() if task_data.task_status == TaskStatus.completed else None

    db_task = Task(
        user_id=user.id,
        task_description=task_data.task_description,
        task_status=task_data.task_status,
        deadline=task_data.deadline,
        start_date=task_data.start_date,
        completed_on=completed_on,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def list_tasks(db: Session, user: User, limit: int = 20, offset: int = 0) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.user_id == user.id, Task.deleted_on.is_(None))
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_task_by_id(db: Session, user: User, task_id: int) -> Task:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user.id, Task.deleted_on.is_(None))
        .first()
    )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


def update_task(db: Session, user: User, task_id: int, update_data: TaskUpdate) -> Task:
    task = get_task_by_id(db, user, task_id)
    update_dict = update_data.model_dump(exclude_unset=True)

    # Determine resulting start_date and deadline for validation
    new_start = update_dict.get("start_date", task.start_date)
    new_deadline = update_dict.get("deadline", task.deadline)
    validate_dates(new_start, new_deadline)

    if "task_status" in update_dict:
        new_status = update_dict["task_status"]
        if new_status == TaskStatus.completed and task.task_status != TaskStatus.completed:
            task.completed_on = utc_now()
        elif new_status != TaskStatus.completed and task.task_status == TaskStatus.completed:
            task.completed_on = None

    for field, value in update_dict.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, user: User, task_id: int):
    task = get_task_by_id(db, user, task_id)
    now = utc_now()
    task.deleted_on = now
    # Soft delete associated active milestones
    for milestone in task.milestones:
        if milestone.deleted_on is None:
            milestone.deleted_on = now
    db.commit()
