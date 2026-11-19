from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.api.auth import router as auth_router
from backend.api.roles import router as roles_router
from backend.api.tasks import router as task_router
from backend.api.users import router as users_router
from backend.migrate import ensure_task_columns
from backend.seed import seed_tasks
from backend.seed_rbac import seed_rbac

# noqa: F401 - register models on metadata
from backend.modules import rbac, task, user  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_task_columns()
    seed_rbac()
    seed_tasks()
    yield


app = FastAPI(title="Task Manager API", version="1.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(task_router)


@app.get("/")
async def root():
    return {"message": "欢迎使用任务中枢"}


if __name__ == "__main__":
    import os
    from pathlib import Path
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    port = int(os.getenv("API_PORT", "8001"))
    uvicorn.run("backend.main:app", host="127.0.0.1", port=port, reload=True)