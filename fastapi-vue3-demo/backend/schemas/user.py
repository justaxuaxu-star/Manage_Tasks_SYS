from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=6, max_length=64)
    display_name: str
    department: str = "综合部"
    role_ids: list[int] = []


class UserUpdate(BaseModel):
    display_name: str | None = None
    department: str | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=6, max_length=64)
    role_ids: list[int] | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    display_name: str
    department: str
    is_active: bool
    roles: list[str] = []