from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.deps import require_permissions
from backend.database import get_db
from backend.modules.user import UserModel
from backend.schemas.user import UserCreate, UserOut, UserUpdate
from backend.services import rbac_service, user_service

router = APIRouter(prefix="/users", tags=["users"])


def to_user_out(user: UserModel) -> UserOut:
    return UserOut(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        department=user.department,
        is_active=user.is_active,
        roles=rbac_service.user_role_codes(user),
    )


@router.get("", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_permissions("user:read")),
):
    return [to_user_out(user) for user in rbac_service.list_users(db)]


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_permissions("user:write")),
):
    try:
        user = user_service.create_user(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    user = rbac_service.get_user_with_roles(db, user.id)
    return to_user_out(user)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_permissions("user:write")),
):
    user = user_service.update_user(db, user_id, payload)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = rbac_service.get_user_with_roles(db, user.id)
    return to_user_out(user)