from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.deps import get_current_user, require_permissions
from backend.database import get_db
from backend.modules.user import UserModel
from backend.schemas.task import Task
from backend.services import task_service

router = APIRouter(tags=["tasks"])


@router.get("/tasks", response_model=list[Task])
def get_tasks(
    db: Session = Depends(get_db),
    user: UserModel = Depends(require_permissions("task:read")),
):
    return task_service.list_tasks(db, user)


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(require_permissions("task:read")),
):
    task = task_service.get_task(db, task_id, user)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=Task)
def create_task(
    task: Task,
    db: Session = Depends(get_db),
    user: UserModel = Depends(require_permissions("task:create")),
):
    return task_service.create_task(db, task, user)


@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    updated_task: Task,
    db: Session = Depends(get_db),
    user: UserModel = Depends(require_permissions("task:update", "task:change_status")),
):
    task = task_service.update_task(db, task_id, updated_task, user)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(require_permissions("task:delete")),
):
    deleted = task_service.delete_task(db, task_id, user)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}