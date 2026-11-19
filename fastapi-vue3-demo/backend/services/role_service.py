from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.modules.rbac import PermissionModel, RoleModel
from backend.schemas.role import RoleCreate, RoleUpdate


def _load_permissions(db: Session, permission_ids: list[int]) -> list[PermissionModel]:
    if not permission_ids:
        return []
    return list(db.scalars(select(PermissionModel).where(PermissionModel.id.in_(permission_ids))).all())


def create_role(db: Session, payload: RoleCreate) -> RoleModel:
    exists = db.scalar(select(RoleModel).where(RoleModel.code == payload.code))
    if exists:
        raise ValueError("role code exists")
    role = RoleModel(code=payload.code, name=payload.name)
    role.permissions = _load_permissions(db, payload.permission_ids)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role_id: int, payload: RoleUpdate) -> RoleModel | None:
    role = db.scalar(
        select(RoleModel).where(RoleModel.id == role_id).options(selectinload(RoleModel.permissions))
    )
    if role is None:
        return None
    if payload.name is not None:
        role.name = payload.name
    if payload.permission_ids is not None:
        role.permissions = _load_permissions(db, payload.permission_ids)
    db.commit()
    db.refresh(role)
    return role