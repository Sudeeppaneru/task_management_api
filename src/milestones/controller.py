from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models import Milestone, User
from src.tasks.controller import get_task_by_id
from src.milestones.dtos import MilestoneCreate, MilestoneUpdate


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def validate_milestone_dates(start_date: datetime | None, deadline: datetime | None):
    if start_date and deadline and start_date > deadline:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="start_date must not be later than deadline"
        )


def create_milestone(db: Session, user: User, task_id: int, milestone_data: MilestoneCreate) -> Milestone:
    # Ensure task exists and belongs to user
    task = get_task_by_id(db, user, task_id)
    validate_milestone_dates(milestone_data.start_date, milestone_data.deadline)

    db_milestone = Milestone(
        task_id=task.id,
        milestone_description=milestone_data.milestone_description,
        deadline=milestone_data.deadline,
        start_date=milestone_data.start_date,
    )
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone


def list_milestones(db: Session, user: User, task_id: int, limit: int = 20, offset: int = 0) -> list[Milestone]:
    task = get_task_by_id(db, user, task_id)
    return (
        db.query(Milestone)
        .filter(Milestone.task_id == task.id, Milestone.deleted_on.is_(None))
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_milestone_by_id(db: Session, user: User, task_id: int, milestone_id: int) -> Milestone:
    task = get_task_by_id(db, user, task_id)
    milestone = (
        db.query(Milestone)
        .filter(
            Milestone.id == milestone_id,
            Milestone.task_id == task.id,
            Milestone.deleted_on.is_(None),
        )
        .first()
    )
    if not milestone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Milestone not found"
        )
    return milestone


def update_milestone(
    db: Session, user: User, task_id: int, milestone_id: int, update_data: MilestoneUpdate
) -> Milestone:
    milestone = get_milestone_by_id(db, user, task_id, milestone_id)
    update_dict = update_data.model_dump(exclude_unset=True)

    new_start = update_dict.get("start_date", milestone.start_date)
    new_deadline = update_dict.get("deadline", milestone.deadline)
    validate_milestone_dates(new_start, new_deadline)

    for field, value in update_dict.items():
        setattr(milestone, field, value)

    db.commit()
    db.refresh(milestone)
    return milestone


def complete_milestone(db: Session, user: User, task_id: int, milestone_id: int) -> Milestone:
    milestone = get_milestone_by_id(db, user, task_id, milestone_id)
    if milestone.completed_on is None:
        milestone.completed_on = utc_now()
        db.commit()
        db.refresh(milestone)
    return milestone


def delete_milestone(db: Session, user: User, task_id: int, milestone_id: int):
    milestone = get_milestone_by_id(db, user, task_id, milestone_id)
    milestone.deleted_on = utc_now()
    db.commit()
