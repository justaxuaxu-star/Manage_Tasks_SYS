from sqlalchemy.orm import Session

from backend.core.security import create_access_token, verify_password
from backend.modules.user import UserModel
from backend.schemas.auth import LoginResponse, UserPublic
from backend.services import rbac_service


def authenticate(db: Session, username: str, password: str) -> UserModel | None:
    user = rbac_service.get_user_by_username(db, username)
    if user is None or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def to_user_public(user: UserModel) -> UserPublic:
    return UserPublic(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        department=user.department,
        roles=rbac_service.user_role_codes(user),
        permissions=sorted(rbac_service.user_permission_codes(user)),
    )


def login(db: Session, username: str, password: str) -> LoginResponse | None:
    user = authenticate(db, username, password)
    if user is None:
        return None
    token = create_access_token(user.id, user.username)
    return LoginResponse(access_token=token, user=to_user_public(user))