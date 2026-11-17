# 任务中枢

一个前后端分离的企业任务管理系统。用来查看交付压力、分派工作项，并按阶段推进任务。

前端是工作台，后端提供任务接口，数据保存在 PostgreSQL。适合作为可运行的全栈示例：有列表、看板、筛选，也有清晰的接口分层。

## 它能做什么

打开前端后有三个页面：

| 页面 | 路径 | 作用 |
| --- | --- | --- |
| 工作台 | `/` | 查看未完成数量、完成率、逾期、三日内到期、优先级分布和部门在办量 |
| 任务中心 | `/tasks` | 搜索、筛选、排序，并直接修改状态、编辑或删除 |
| 进度看板 | `/board` | 按「待处理 / 进行中 / 待验收 / 已完成」分列，拖拽卡片改变阶段 |

新建和编辑使用右侧表单，字段包括标题、说明、状态、优先级、负责人、部门和截止日期。页面上的「系统管理员」只是界面身份，当前没有登录。

## 技术组成

- 前端：Vue 3、Vue Router、Vite、Axios
- 后端：FastAPI、SQLAlchemy、Pydantic
- 数据库：PostgreSQL（通过 `psycopg` 连接）

后端按职责拆开：

- `api/tasks.py`：HTTP 路由
- `schemas/task.py`：请求和响应字段
- `modules/task.py`：数据库表
- `services/task_service.py`：查询、保存，以及状态和优先级的整理规则
- `database.py`：连接和会话
- `seed.py`：空库时写入示例任务

## 目录

```text
manage_tasks_sys/
├── frontend/                  Vue 3 工作台
└── fastapi-vue3-demo/
    └── backend/
        ├── main.py            应用入口
        ├── api/               路由
        ├── schemas/           数据契约
        ├── modules/           表模型
        ├── services/          业务逻辑
        ├── data/tasks.json    示例任务
        ├── database.py
        └── seed.py
```

## 本地运行

需要 Python 3.12、Node.js，以及本机可连接的 PostgreSQL。先建库 `taskdb`。

### 1. 后端

在 `fastapi-vue3-demo` 下创建虚拟环境并安装依赖：

```powershell
cd fastapi-vue3-demo
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv "psycopg[binary]"
```

同目录新建 `.env`（该文件已被 git 忽略，不要提交密码）：

```text
DATABASE_URL=postgresql+psycopg://postgres:你的密码@localhost:5432/taskdb
```

启动接口。工作目录必须是 `fastapi-vue3-demo`，这样 `backend` 才能被导入：

```powershell
uvicorn backend.main:app --reload
```

- 接口：http://localhost:8000
- 交互文档：http://localhost:8000/docs

首次启动会建表。`tasks` 表为空时，会从 `backend/data/tasks.json` 写入示例数据；表里已有数据时不会覆盖。

### 2. 前端

另开一个终端：

```powershell
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173 。前端请求发往 `http://localhost:8000`，后端只允许这个来源跨域访问。

## 接口

| 方法 | 路径 | 作用 |
| --- | --- | --- |
| `GET` | `/tasks` | 任务列表 |
| `GET` | `/tasks/{id}` | 单条任务 |
| `POST` | `/tasks` | 新建 |
| `PUT` | `/tasks/{id}` | 更新 |
| `DELETE` | `/tasks/{id}` | 删除 |

一条任务的主要字段：

| 字段 | 含义 |
| --- | --- |
| `title` | 标题，必填 |
| `description` | 说明 |
| `status` | `pending` 待处理、`in_progress` 进行中、`review` 待验收、`completed` 已完成 |
| `priority` | `urgent` 紧急、`high` 高、`medium` 中、`low` 低 |
| `assignee` | 负责人，空值会存成「未分配」 |
| `department` | 部门，空值会存成「综合部」 |
| `due_date` | 截止日期，格式 `YYYY-MM-DD` |
| `completed` | 是否完成。状态为 `completed` 时为 `true`；只把该字段设为 `true` 且状态仍是 `pending` 时，会自动改成已完成 |

不在上述范围内的状态会退回「待处理」或「已完成」，不在范围内的优先级会退回「中」。
