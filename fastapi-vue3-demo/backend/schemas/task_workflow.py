from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StatusTransitionOption(BaseModel):
    value: str
    label: str


class TaskStatusTransitionsOut(BaseModel):
    task_id: int
    current_status: str
    allowed: list[StatusTransitionOption]


class TaskStatusHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    from_status: str | None
    to_status: str
    changed_by_id: int | None
    changed_by_name: str | None = None
    created_at: datetime