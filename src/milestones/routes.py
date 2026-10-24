from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.models import User
from src.auth.dependencies import get_current_active_user
from src.milestones.dtos import MilestoneCreate, MilestoneUpdate, MilestoneResponse
from src.milestones.controller import (
    create_milestone,
    list_milestones,
    get_milestone_by_id,
    update_milestone,
    complete_milestone,
    delete_milestone,
)

milestones_router = APIRouter(prefix="/tasks/{task_id}/milestones", tags=["Milestones"])


@milestones_router.post("", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED)
def create_new_milestone(
    task_id: int,
    milestone_data: MilestoneCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return create_milestone(db, current_user, task_id, milestone_data)


@milestones_router.get("", response_model=list[MilestoneResponse])
def get_task_milestones(
    task_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return list_milestones(db, current_user, task_id, limit=limit, offset=offset)


@milestones_router.get("/{milestone_id}", response_model=MilestoneResponse)
def get_single_milestone(
    task_id: int,
    milestone_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return get_milestone_by_id(db, current_user, task_id, milestone_id)


@milestones_router.patch("/{milestone_id}", response_model=MilestoneResponse)
def patch_milestone(
    task_id: int,
    milestone_id: int,
    update_data: MilestoneUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return update_milestone(db, current_user, task_id, milestone_id, update_data)


@milestones_router.post("/{milestone_id}/complete", response_model=MilestoneResponse)
def mark_milestone_completed(
    task_id: int,
    milestone_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return complete_milestone(db, current_user, task_id, milestone_id)


@milestones_router.delete("/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_milestone(
    task_id: int,
    milestone_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    delete_milestone(db, current_user, task_id, milestone_id)
    return None
