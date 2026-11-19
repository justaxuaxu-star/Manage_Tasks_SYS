from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.deps import get_current_user
from backend.database import get_db
from backend.modules.user import UserModel
from backend.schemas.auth import LoginRequest, LoginResponse, UserPublic
from backend.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    result = auth_service.login(db, payload.username, payload.password)
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return result


@router.get("/me", response_model=UserPublic)
def me(user: UserModel = Depends(get_current_user)):
    return auth_service.to_user_public(user)