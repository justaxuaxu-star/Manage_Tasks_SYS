ALL_PERMISSIONS: list[tuple[str, str]] = [
    ("task:read", "查看任务"),
    ("task:read_all", "查看全部任务"),
    ("task:create", "创建任务"),
    ("task:update", "编辑任务"),
    ("task:delete", "删除任务"),
    ("task:assign", "分派负责人"),
    ("task:change_status", "变更任务状态"),
    ("user:read", "查看用户"),
    ("user:write", "管理用户"),
    ("role:read", "查看角色"),
    ("role:write", "管理角色与权限"),
]

ADMIN_ROLE = "admin"
MANAGER_ROLE = "manager"
MEMBER_ROLE = "member"

ROLE_PERMISSIONS = {
    ADMIN_ROLE: [code for code, _ in ALL_PERMISSIONS],
    MANAGER_ROLE: [
        "task:read",
        "task:read_all",
        "task:create",
        "task:update",
        "task:delete",
        "task:assign",
        "task:change_status",
        "user:read",
        "role:read",
    ],
    MEMBER_ROLE: [
        "task:read",
        "task:update",
        "task:change_status",
    ],
}