from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Task Manager API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATUSES = {"pending", "in_progress", "review", "completed"}
PRIORITIES = {"low", "medium", "high", "urgent"}


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    completed: bool = False
    status: str = "pending"
    priority: str = "medium"
    assignee: str = "未分配"
    department: str = "综合部"
    due_date: Optional[str] = None


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


tasks = [
    Task(
        id=1,
        title="季度经营分析报告",
        description="汇总各业务线收入、成本与风险，输出管理层可读的季度结论。",
        completed=True,
        status="completed",
        priority="high",
        assignee="林晓晨",
        department="运营部",
        due_date="2026-11-12",
    ),
    Task(
        id=2,
        title="客户门户改版评审",
        description="确认信息架构、关键路径和上线范围，冻结本迭代评审意见。",
        status="in_progress",
        priority="urgent",
        assignee="周予安",
        department="产品部",
        due_date="2026-11-17",
    ),
    Task(
        id=3,
        title="权限中心接口联调",
        description="打通角色、数据范围和审计日志接口，补齐异常码说明。",
        status="pending",
        priority="high",
        assignee="陈可",
        department="研发部",
        due_date="2026-11-19",
    ),
    Task(
        id=4,
        title="供应商对账流程优化",
        description="把月结对账从邮件往来改为系统内确认，减少漏单。",
        status="review",
        priority="medium",
        assignee="赵启明",
        department="综合部",
        due_date="2026-11-18",
    ),
    Task(
        id=5,
        title="新员工入职清单",
        description="整理账号、设备、权限和导师安排，形成可复用清单。",
        status="pending",
        priority="low",
        assignee="苏晚",
        department="综合部",
        due_date="2026-11-25",
    ),
    Task(
        id=6,
        title="移动端任务提醒方案",
        description="定义站内信、邮件和截止日前提醒的触发规则。",
        status="in_progress",
        priority="medium",
        assignee="林晓晨",
        department="产品部",
        due_date="2026-11-21",
    ),
    Task(
        id=7,
        title="数据看板指标口径对齐",
        description="统一完成率、逾期率和在办量的统计口径。",
        status="review",
        priority="high",
        assignee="周予安",
        department="运营部",
        due_date="2026-11-16",
    ),
    Task(
        id=8,
        title="生产环境发布检查单",
        description="核对迁移、回滚、监控告警和值班人，发布前逐项勾选。",
        completed=True,
        status="completed",
        priority="urgent",
        assignee="陈可",
        department="研发部",
        due_date="2026-11-10",
    ),
    Task(
        id=9,
        title="合同归档补录",
        description="补齐第三季度已签署合同的扫描件、编号和归档位置。",
        status="pending",
        priority="medium",
        assignee="赵启明",
        department="综合部",
        due_date="2026-11-13",
    ),
    Task(
        id=10,
        title="视觉规范抽检",
        description="抽查最近上线页面的字体、间距和状态色是否符合规范。",
        status="pending",
        priority="low",
        assignee="苏晚",
        department="设计部",
        due_date="2026-11-27",
    ),
]
next_id = 11


@app.get("/")
async def root():
    return {"message": "欢迎使用任务中枢"}


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
    prepare(task)
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            prepare(updated_task)
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
