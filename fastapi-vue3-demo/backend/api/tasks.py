from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.deps import get_current_user, require_permissions
from backend.database import get_db
from backend.modules.user import UserModel
from backend.schemas.task import Task
from backend.schemas.task_workflow import (
    StatusTransitionOption,
    TaskStatusHistoryOut,
    TaskStatusTransitionsOut,
)
from backend.services import task_service, task_workflow
from backend.services.task_status_history_service import list_history_for_task
from backend.services.workflow_errors import WorkflowError

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
    try:
        task = task_service.update_task(db, task_id, updated_task, user)
    except WorkflowError as exc:
        raise HTTPException(status_code=422, detail=exc.message) from exc
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/tasks/{task_id}/status-transitions", response_model=TaskStatusTransitionsOut)
def get_status_transitions(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(require_permissions("task:read")),
):
    row = task_service.get_task(db, task_id, user)
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    allowed = task_workflow.allowed_targets(row.status, user)
    options = [
        StatusTransitionOption(value=code, label=task_workflow.STATUS_LABELS[code])
        for code in allowed
    ]
    return TaskStatusTransitionsOut(task_id=task_id, current_status=row.status, allowed=options)


@router.get("/tasks/{task_id}/status-history", response_model=list[TaskStatusHistoryOut])
def get_status_history(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(require_permissions("task:read")),
):
    row = task_service.get_task(db, task_id, user)
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return list_history_for_task(db, task_id)


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