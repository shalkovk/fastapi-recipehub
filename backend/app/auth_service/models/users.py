from datetime import datetime
from typing import Optional
from db.database import str_uniq

from sqlalchemy import String, DateTime, Boolean, func, text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str_uniq] = mapped_column(index=True)
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str_uniq] = mapped_column(index=True)
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey(
        "roles.id"), default=1, server_default=text("1"), index=True)
    role: Mapped["Role"] = relationship(
        "Role", back_populates="users", lazy="joined")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
