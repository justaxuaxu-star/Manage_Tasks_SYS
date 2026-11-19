from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.core.perms import ADMIN_ROLE, ALL_PERMISSIONS
from backend.modules.rbac import PermissionModel, RoleModel
from backend.modules.user import UserModel


def user_role_codes(user: UserModel) -> list[str]:
    return [role.code for role in user.roles]


def is_admin(user: UserModel) -> bool:
    return ADMIN_ROLE in user_role_codes(user)


def user_permission_codes(user: UserModel) -> set[str]:
    if is_admin(user):
        return {code for code, _ in ALL_PERMISSIONS}
    codes: set[str] = set()
    for role in user.roles:
        for perm in role.permissions:
            codes.add(perm.code)
    return codes


def has_permission(user: UserModel, code: str) -> bool:
    if is_admin(user):
        return True
    return code in user_permission_codes(user)


def get_user_with_roles(db: Session, user_id: int) -> UserModel | None:
    stmt = (
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.roles).selectinload(RoleModel.permissions))
    )
    return db.scalar(stmt)


def get_user_by_username(db: Session, username: str) -> UserModel | None:
    stmt = (
        select(UserModel)
        .where(UserModel.username == username)
        .options(selectinload(UserModel.roles).selectinload(RoleModel.permissions))
    )
    return db.scalar(stmt)


def list_permissions(db: Session) -> list[PermissionModel]:
    return list(db.scalars(select(PermissionModel).order_by(PermissionModel.code)).all())


def list_roles(db: Session) -> list[RoleModel]:
    stmt = select(RoleModel).options(selectinload(RoleModel.permissions)).order_by(RoleModel.code)
    return list(db.scalars(stmt).all())


def get_role(db: Session, role_id: int) -> RoleModel | None:
    stmt = (
        select(RoleModel)
        .where(RoleModel.id == role_id)
        .options(selectinload(RoleModel.permissions))
    )
    return db.scalar(stmt)


def list_users(db: Session) -> list[UserModel]:
    stmt = select(UserModel).options(selectinload(UserModel.roles)).order_by(UserModel.id)
    return list(db.scalars(stmt).all())