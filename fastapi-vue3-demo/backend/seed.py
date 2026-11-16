import json
from pathlib import Path

from sqlalchemy import func, select

from backend.database import SessionLocal
from backend.modules.task import TaskModel

SEED_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"


def seed_tasks() -> None:
    records = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    with SessionLocal() as db:
        count = db.scalar(select(func.count()).select_from(TaskModel))
        if count:
            return
        db.add_all(TaskModel(**record) for record in records)
        db.commit()
