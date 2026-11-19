from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    display_name: str
    department: str
    roles: list[str]
    permissions: list[str]


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic