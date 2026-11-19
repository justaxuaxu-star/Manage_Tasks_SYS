from sqlalchemy import func, select

from backend.core.perms import ADMIN_ROLE, ALL_PERMISSIONS, MANAGER_ROLE, MEMBER_ROLE, ROLE_PERMISSIONS
from backend.core.security import hash_password
from backend.database import SessionLocal
from backend.modules.rbac import PermissionModel, RoleModel
from backend.modules.user import UserModel

DEMO_USERS = [
    ("admin", "管理员", "综合部", ADMIN_ROLE, "admin123"),
    ("manager", "林晓晨", "运营部", MANAGER_ROLE, "demo123"),
    ("member", "陈可", "研发部", MEMBER_ROLE, "demo123"),
]


def seed_rbac() -> None:
    with SessionLocal() as db:
        perm_count = db.scalar(select(func.count()).select_from(PermissionModel))
        if not perm_count:
            perms = [PermissionModel(code=code, name=name) for code, name in ALL_PERMISSIONS]
            db.add_all(perms)
            db.commit()

        db.expire_all()
        perms_by_code = {p.code: p for p in db.scalars(select(PermissionModel)).all()}

        role_count = db.scalar(select(func.count()).select_from(RoleModel))
        if not role_count:
            for code, name in [
                (ADMIN_ROLE, "系统管理员"),
                (MANAGER_ROLE, "部门经理"),
                (MEMBER_ROLE, "普通成员"),
            ]:
                role = RoleModel(code=code, name=name)
                role.permissions = [perms_by_code[c] for c in ROLE_PERMISSIONS[code] if c in perms_by_code]
                db.add(role)
            db.commit()

        user_count = db.scalar(select(func.count()).select_from(UserModel))
        if not user_count:
            roles = {r.code: r for r in db.scalars(select(RoleModel)).all()}
            for username, display_name, department, role_code, password in DEMO_USERS:
                user = UserModel(
                    username=username,
                    password_hash=hash_password(password),
                    display_name=display_name,
                    department=department,
                    is_active=True,
                )
                user.roles = [roles[role_code]]
                db.add(user)
            db.commit()