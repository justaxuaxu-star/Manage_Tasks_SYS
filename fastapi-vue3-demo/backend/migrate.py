from sqlalchemy import inspect, text

from backend.database import engine


def ensure_task_columns() -> None:
    with engine.begin() as conn:
        inspector = inspect(conn)
        if "tasks" not in inspector.get_table_names():
            return
        columns = {col["name"] for col in inspector.get_columns("tasks")}
        if "created_by_id" not in columns:
            conn.execute(text("ALTER TABLE tasks ADD COLUMN created_by_id INTEGER REFERENCES users(id)"))
        if "assignee_user_id" not in columns:
            conn.execute(text("ALTER TABLE tasks ADD COLUMN assignee_user_id INTEGER REFERENCES users(id)"))