from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.modules.task import TaskModel
from backend.schemas.task import Task

STATUSES = {"pending", "in_progress", "review", "completed"}
PRIORITIES = {"low", "medium", "high", "urgent"}


def prepare(task: Task) -> Task:
    if task.status not in STATUSES:
        task.status = "completed" if task.completed else "pending"
    if task.completed and task.status == "pending":
        task.status = "completed"
    task.completed = task.status == "completed"
    if task.priority not in PRIORITIES:
        task.priority = "medium"
    task.assignee = (task.assignee or "未分配").strip() or "未分配"
    task.department = (task.department or "综合部").strip() or "综合部"
    task.description = task.description or ""
    task.due_date = task.due_date or None
    return task


def list_tasks(db: Session) -> list[TaskModel]:
    return list(db.scalars(select(TaskModel)).all())


def get_task(db: Session, task_id: int) -> TaskModel | None:
    return db.get(TaskModel, task_id)


def create_task(db: Session, task: Task) -> TaskModel:
    prepare(task)
    row = TaskModel(**task.model_dump(exclude={"id"}))
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update_task(db: Session, task_id: int, task: Task) -> TaskModel | None:
    row = db.get(TaskModel, task_id)
    if row is None:
        return None
    prepare(task)
    for key, value in task.model_dump(exclude={"id"}).items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


def delete_task(db: Session, task_id: int) -> bool:
    row = db.get(TaskModel, task_id)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True
