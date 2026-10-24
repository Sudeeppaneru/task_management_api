from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class MilestoneCreate(BaseModel):
    milestone_description: str = Field(min_length=1, max_length=500)
    deadline: datetime | None = None
    start_date: datetime | None = None


class MilestoneUpdate(BaseModel):
    milestone_description: str | None = Field(default=None, min_length=1, max_length=500)
    deadline: datetime | None = None
    start_date: datetime | None = None


class MilestoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    milestone_description: str
    deadline: datetime | None
    start_date: datetime | None
    created_on: datetime
    deleted_on: datetime | None
    completed_on: datetime | None
