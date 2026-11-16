from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware  


app = FastAPI(title="Task Manager API123", version="1.0.1")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app = FastAPI(title="Task Manager API", docs_url=None, redoc_url=None)

# 数据模型定义
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# 模拟数据库（实际项目中应使用真实数据库）
tasks = [
    Task(id=1, title="学习FastAPI", description="掌握FastAPI基础知识", completed=True),
    Task(id=2, title="学习Vue3", description="了解Vue3 Composition API", completed=False)
]
next_id = 3

# API路由实现
@app.get("/")
async def root():
    return {"message": "欢迎使用Task Manager API"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    global next_id
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id
            tasks[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)