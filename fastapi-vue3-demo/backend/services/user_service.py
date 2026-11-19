from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.core.security import hash_password
from backend.modules.rbac import RoleModel
from backend.modules.user import UserModel
from backend.schemas.user import UserCreate, UserUpdate


def _load_roles(db: Session, role_ids: list[int]) -> list[RoleModel]:
    if not role_ids:
        return []
    return list(db.scalars(select(RoleModel).where(RoleModel.id.in_(role_ids))).all())


def create_user(db: Session, payload: UserCreate) -> UserModel:
    exists = db.scalar(select(UserModel).where(UserModel.username == payload.username))
    if exists:
        raise ValueError("username exists")
    user = UserModel(
        username=payload.username,
        password_hash=hash_password(payload.password),
        display_name=payload.display_name,
        department=payload.department,
        is_active=True,
    )
    user.roles = _load_roles(db, payload.role_ids)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, payload: UserUpdate) -> UserModel | None:
    user = db.scalar(
        select(UserModel).where(UserModel.id == user_id).options(selectinload(UserModel.roles))
    )
    if user is None:
        return None
    if payload.display_name is not None:
        user.display_name = payload.display_name
    if payload.department is not None:
        user.department = payload.department
    if payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.password:
        user.password_hash = hash_password(payload.password)
    if payload.role_ids is not None:
        user.roles = _load_roles(db, payload.role_ids)
    db.commit()
    db.refresh(user)
    return user