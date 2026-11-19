from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base
from backend.modules.rbac import user_roles


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(50), default="综合部")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    roles = relationship("RoleModel", secondary=user_roles, back_populates="users", lazy="selectin")