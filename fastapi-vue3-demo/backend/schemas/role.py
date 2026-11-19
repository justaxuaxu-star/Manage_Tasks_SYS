from pydantic import BaseModel, ConfigDict


class PermissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str


class RoleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    permissions: list[str] = []


class RoleCreate(BaseModel):
    code: str
    name: str
    permission_ids: list[int] = []


class RoleUpdate(BaseModel):
    name: str | None = None
    permission_ids: list[int] | None = None