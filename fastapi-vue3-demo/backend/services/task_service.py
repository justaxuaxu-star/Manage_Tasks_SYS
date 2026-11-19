from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.modules.task import TaskModel
from backend.modules.user import UserModel
from backend.schemas.task import Task
from backend.services import rbac_service

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


def can_read_all(user: UserModel) -> bool:
    return rbac_service.is_admin(user) or rbac_service.has_permission(user, "task:read_all")


def is_task_visible(user: UserModel, row: TaskModel) -> bool:
    if can_read_all(user):
        return True
    return (
        row.assignee_user_id == user.id
        or row.created_by_id == user.id
        or row.department == user.department
        or row.assignee == user.display_name
    )


def list_tasks(db: Session, user: UserModel) -> list[TaskModel]:
    if can_read_all(user):
        return list(db.scalars(select(TaskModel)).all())
    stmt = select(TaskModel).where(
        or_(
            TaskModel.assignee_user_id == user.id,
            TaskModel.created_by_id == user.id,
            TaskModel.department == user.department,
            TaskModel.assignee == user.display_name,
        )
    )
    return list(db.scalars(stmt).all())


def get_task(db: Session, task_id: int, user: UserModel) -> TaskModel | None:
    row = db.get(TaskModel, task_id)
    if row is None or not is_task_visible(user, row):
        return None
    return row


def create_task(db: Session, task: Task, user: UserModel) -> TaskModel:
    prepare(task)
    data = task.model_dump(exclude={"id"})
    data["created_by_id"] = user.id
    if data.get("assignee_user_id") is None and data.get("assignee") == user.display_name:
        data["assignee_user_id"] = user.id
    row = TaskModel(**data)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update_task(db: Session, task_id: int, task: Task, user: UserModel) -> TaskModel | None:
    row = get_task(db, task_id, user)
    if row is None:
        return None
    prepare(task)
    data = task.model_dump(exclude={"id"})
    if data.get("assignee_user_id") != row.assignee_user_id or data.get("assignee") != row.assignee:
        if not rbac_service.has_permission(user, "task:assign"):
            data["assignee_user_id"] = row.assignee_user_id
            data["assignee"] = row.assignee
    row.created_by_id = row.created_by_id or user.id
    for key, value in data.items():
        setattr(row, key, value)
    db.commit()
    db.refresh(row)
    return row


def delete_task(db: Session, task_id: int, user: UserModel) -> bool:
    row = get_task(db, task_id, user)
    if row is None:
        return False
    db.delete(row)
    db.commit()
    return True