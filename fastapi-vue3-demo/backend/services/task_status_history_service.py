from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.modules.task_status_history import TaskStatusHistoryModel
from backend.modules.user import UserModel
from backend.schemas.task_workflow import TaskStatusHistoryOut
from backend.services.task_workflow import STATUS_LABELS


def record_status_change(
    db: Session,
    *,
    task_id: int,
    from_status: str | None,
    to_status: str,
    user: UserModel,
) -> None:
    if from_status == to_status:
        return
    row = TaskStatusHistoryModel(
        task_id=task_id,
        from_status=from_status or None,
        to_status=to_status,
        changed_by_id=user.id,
    )
    db.add(row)


def list_history_for_task(db: Session, task_id: int) -> list[TaskStatusHistoryOut]:
    stmt = (
        select(TaskStatusHistoryModel)
        .where(TaskStatusHistoryModel.task_id == task_id)
        .order_by(TaskStatusHistoryModel.created_at.desc(), TaskStatusHistoryModel.id.desc())
    )
    rows = list(db.scalars(stmt).all())
    user_ids = {r.changed_by_id for r in rows if r.changed_by_id}
    names: dict[int, str] = {}
    if user_ids:
        users = db.scalars(select(UserModel).where(UserModel.id.in_(user_ids))).all()
        names = {u.id: u.display_name or u.username for u in users}

    return [
        TaskStatusHistoryOut(
            id=r.id,
            task_id=r.task_id,
            from_status=r.from_status,
            to_status=r.to_status,
            changed_by_id=r.changed_by_id,
            changed_by_name=names.get(r.changed_by_id) if r.changed_by_id else None,
            created_at=r.created_at,
        )
        for r in rows
    ]


def status_label(code: str | None) -> str:
    if not code:
        return "（新建）"
    return STATUS_LABELS.get(code, code)