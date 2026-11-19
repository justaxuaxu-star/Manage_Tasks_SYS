from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.deps import require_permissions
from backend.database import get_db
from backend.modules.user import UserModel
from backend.schemas.role import PermissionOut, RoleCreate, RoleOut, RoleUpdate
from backend.services import rbac_service, role_service

router = APIRouter(prefix="/roles", tags=["roles"])


def to_role_out(role) -> RoleOut:
    return RoleOut(
        id=role.id,
        code=role.code,
        name=role.name,
        permissions=[perm.code for perm in role.permissions],
    )


@router.get("/permissions", response_model=list[PermissionOut])
def list_permissions(
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_permissions("role:read")),
):
    return rbac_service.list_permissions(db)


@router.get("", response_model=list[RoleOut])
def list_roles(
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_permissions("role:read")),
):
    return [to_role_out(role) for role in rbac_service.list_roles(db)]


@router.post("", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreate,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_permissions("role:write")),
):
    try:
        role = role_service.create_role(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    role = rbac_service.get_role(db, role.id)
    return to_role_out(role)


@router.put("/{role_id}", response_model=RoleOut)
def update_role(
    role_id: int,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    _: UserModel = Depends(require_permissions("role:write")),
):
    role = role_service.update_role(db, role_id, payload)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    role = rbac_service.get_role(db, role.id)
    return to_role_out(role)