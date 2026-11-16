from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.api.tasks import router as task_router
from backend.seed import seed_tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_tasks()
    yield


app = FastAPI(title="Task Manager API", version="1.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)


@app.get("/")
async def root():
    return {"message": "欢迎使用任务中枢"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
