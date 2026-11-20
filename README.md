# 齐天大圣科技数据中心后台

一个前后端分离的企业任务管理系统（齐天大圣科技 · 数据中心后台）。用来查看交付压力、分派工作项，并按阶段推进任务。

前端为科技风工作台（支持深色 / 浅色主题切换、侧边栏收起），后端提供鉴权与任务接口，数据保存在 PostgreSQL。适合作为可运行的全栈示例：有列表、看板、筛选、JWT 登录与 RBAC，也有清晰的接口分层。

## 它能做什么

打开前端后有三个页面：

| 页面 | 路径 | 作用 |
| --- | --- | --- |
| 工作台 | `/` | 查看未完成数量、完成率、逾期、三日内到期、优先级分布和部门在办量 |
| 任务中心 | `/tasks` | 搜索、筛选、排序，并直接修改状态、编辑或删除 |
| 进度看板 | `/board` | 按「待处理 / 进行中 / 待验收 / 已完成」分列，拖拽卡片改变阶段 |

新建和编辑使用右侧表单，字段包括标题、说明、状态、优先级、负责人、部门和截止日期。需要先登录；顶栏显示当前用户，并可按权限控制新建、编辑、删除等操作。具备 `user:write` / `role:write` 的管理员可进入用户与角色管理页。

## 技术组成

- 前端：Vue 3、Vue Router、Vite、Axios
- 后端：FastAPI、SQLAlchemy、Pydantic、JWT（`python-jose`）、密码哈希（`bcrypt`）
- 数据库：PostgreSQL（通过 `psycopg` 连接）
- 权限：数据库 RBAC（用户 ↔ 角色 ↔ 权限码），接口与前端按钮按权限码控制

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
├── frontend/                  Vue 3 数据中心后台（主题切换、侧边栏收起）
└── fastapi-vue3-demo/
    └── backend/
        ├── main.py            应用入口
        ├── api/               路由（auth、tasks、users、roles）
        ├── core/              JWT、权限依赖
        ├── schemas/           数据契约
        ├── modules/           表模型（任务、用户、RBAC）
        ├── services/          业务逻辑
        ├── data/tasks.json    示例任务
        ├── database.py
        ├── seed.py            示例任务
        └── seed_rbac.py       权限、角色与演示账号
```

## 本地运行

需要 Python 3.12、Node.js，以及本机可连接的 PostgreSQL。先建库 `taskdb`。

### 1. 后端

在 `fastapi-vue3-demo` 下创建虚拟环境并安装依赖：

```powershell
cd fastapi-vue3-demo
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv "psycopg[binary]" bcrypt "python-jose[cryptography]"
```

另在 **全局 Python**（不必激活 venv）执行一次，这样 PowerShell 里可直接敲 `uvicorn` 而不用先 `Activate.ps1`：

```powershell
python -m pip install -e .
```

安装后，全局 `uvicorn` 会自动转调本项目 `venv` 里的 Python，并默认使用 `.env` 中的 `API_PORT`（8001）。

同目录复制 `.env.example` 为 `.env` 并修改数据库密码（`.env` 已被 git 忽略）：

```text
DATABASE_URL=postgresql+psycopg://postgres:你的密码@localhost:5432/taskdb
API_PORT=8001
JWT_SECRET_KEY=请替换为随机长字符串
JWT_EXPIRE_MINUTES=480
```

生产环境务必修改 `JWT_SECRET_KEY`，且勿将 `.env` 提交到版本库。

未写 `--port` 时，会自动读取 `.env` 里的 `API_PORT`（默认 **8001**），避免与本机占用 8000 端口的其他服务冲突。

在 `fastapi-vue3-demo` 目录下启动（**无需**先 `Activate.ps1`）：

```powershell
uvicorn backend.main:app --reload
```

也可使用同目录脚本：`.\dev.ps1 backend.main:app --reload`，或在 CMD 中执行 `uvicorn.cmd backend.main:app --reload`。

- 接口：http://localhost:8001
- 交互文档：http://localhost:8001/docs

首次启动会建表并执行 RBAC 种子与任务表字段迁移。`tasks` 表为空时，会从 `backend/data/tasks.json` 写入示例任务；表里已有数据时不会覆盖。

**演示账号（仅开发环境，上线前请改密或禁用）：**

| 用户名 | 密码 | 角色 | 说明 |
| --- | --- | --- | --- |
| `admin` | `admin123` | 管理员 | 全部权限，含用户/角色管理 |
| `manager` | `demo123` | 经理 | 任务全操作 + 查看用户/角色 |
| `member` | `demo123` | 成员 | 仅可见范围内任务，可更新状态 |

### 2. 前端

另开一个终端：

```powershell
cd frontend
npm install
npm run dev
```

浏览器打开 http://localhost:5173 。未登录会跳转到 `/login`。登录后顶栏可切换 **深色 / 浅色** 主题（选择会保存在浏览器 `localStorage`）；侧栏底部 **收起 / 展开** 可腾出更多内容区宽度。前端通过 `frontend/.env.development` 中的 `VITE_API_BASE_URL` 连接 `http://localhost:8001`；请求头携带 `Authorization: Bearer <token>`，401 时会清除本地 Token 并回到登录页。后端 CORS 允许 `http://localhost:5173`，并支持携带凭证与 `Authorization` 头。

## 接口

除 `POST /auth/login` 外，任务与管理接口均需在请求头携带有效 JWT。

### 认证

| 方法 | 路径 | 作用 |
| --- | --- | --- |
| `POST` | `/auth/login` | 用户名密码登录，返回 `access_token` 与用户信息（含 `permissions` 数组） |
| `GET` | `/auth/me` | 当前用户与权限 |

### 任务

| 方法 | 路径 | 权限码（概要） |
| --- | --- | --- |
| `GET` | `/tasks` | `task:read`（成员仅能看本人相关或同部门；`task:read_all` 可看全部） |
| `GET` | `/tasks/{id}` | `task:read` + 数据范围 |
| `POST` | `/tasks` | `task:create` |
| `PUT` | `/tasks/{id}` | `task:update`（改负责人需 `task:assign`；改状态走状态机） |
| `DELETE` | `/tasks/{id}` | `task:delete` |
| `GET` | `/tasks/{id}/status-transitions` | `task:read`（返回当前可变更的目标状态） |
| `GET` | `/tasks/{id}/status-history` | `task:read`（状态流转审计记录） |

**任务状态机（成员默认）**：`待处理 → 进行中 → 待验收 → 已完成`，不可跳步。拥有 `task:read_all` 或管理员角色可驳回、重开（如从待验收退回进行中）。非法变更返回 HTTP `422`。

### 用户与角色（管理端）

| 方法 | 路径 | 权限码 |
| --- | --- | --- |
| `GET/POST/PUT` | `/users`… | `user:read` / `user:write` |
| `GET/POST/PUT` | `/roles`… | `role:read` / `role:write` |
| `GET` | `/roles/permissions` | `role:read` |

常用权限码：`task:read`、`task:read_all`、`task:create`、`task:update`、`task:delete`、`task:assign`、`task:change_status`、`user:read`、`user:write`、`role:read`、`role:write`。角色 `admin` 拥有上述全部权限。

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
