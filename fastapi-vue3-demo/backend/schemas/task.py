from typing import Optional

from pydantic import BaseModel, ConfigDict


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    completed: bool = False
    status: str = "pending"
    priority: str = "medium"
    assignee: str = "未分配"
    department: str = "综合部"
    due_date: Optional[str] = None
    created_by_id: Optional[int] = None
    assignee_user_id: Optional[int] = None
