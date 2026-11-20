from backend.modules.user import UserModel
from backend.services import rbac_service

STATUSES = ("pending", "in_progress", "review", "completed")

STATUS_LABELS = {
    "pending": "待处理",
    "in_progress": "进行中",
    "review": "待验收",
    "completed": "已完成",
}

# 成员：顺序推进为主
MEMBER_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"in_progress"},
    "in_progress": {"review"},
    "review": {"completed"},
    "completed": set(),
}

# 经理 / 管理员：可驳回、重开
ELEVATED_TRANSITIONS: dict[str, set[str]] = {
    "pending": {"in_progress", "completed"},
    "in_progress": {"review", "pending"},
    "review": {"completed", "in_progress"},
    "completed": {"in_progress", "pending"},
}


def can_override_workflow(user: UserModel) -> bool:
    return rbac_service.is_admin(user) or rbac_service.has_permission(user, "task:read_all")


def allowed_targets(from_status: str, user: UserModel) -> list[str]:
    if from_status not in STATUSES:
        from_status = "pending"
    if can_override_workflow(user):
        targets = ELEVATED_TRANSITIONS.get(from_status, set())
    else:
        targets = MEMBER_TRANSITIONS.get(from_status, set())
    return [s for s in STATUSES if s in targets]


def can_transition(from_status: str, to_status: str, user: UserModel) -> bool:
    if from_status == to_status:
        return True
    if to_status not in STATUSES:
        return False
    if from_status not in STATUSES:
        from_status = "pending"
    if can_override_workflow(user):
        return to_status in ELEVATED_TRANSITIONS.get(from_status, set())
    return to_status in MEMBER_TRANSITIONS.get(from_status, set())


def transition_error_message(from_status: str, to_status: str) -> str:
    from_label = STATUS_LABELS.get(from_status, from_status)
    to_label = STATUS_LABELS.get(to_status, to_status)
    allowed = ", ".join(STATUS_LABELS.get(s, s) for s in MEMBER_TRANSITIONS.get(from_status, set())) or "无"
    return (
        f"不允许从「{from_label}」直接变更为「{to_label}」。"
        f"当前角色可变更至：{allowed}。"
    )