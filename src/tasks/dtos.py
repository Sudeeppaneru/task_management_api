
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.models import TaskStatus


class TaskCreate(BaseModel):
    task_description: str = Field(min_length=1, max_length=500)
    task_status: TaskStatus = TaskStatus.todo
    deadline: datetime | None = None
    start_date: datetime | None = None


class TaskUpdate(BaseModel):
    task_description: str | None = Field(
        default=None,
        min_length=1,
        max_length=500,
    )
    task_status: TaskStatus | None = None
    deadline: datetime | None = None
    start_date: datetime | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    task_description: str
    task_status: TaskStatus
    deadline: datetime | None
    start_date: datetime | None
    created_on: datetime
    deleted_on: datetime | None
    completed_on: datetime | None
