from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import String
from bcrypt import gensalt, hashpw, checkpw
from uuid import uuid4, UUID
from typing import List, TYPE_CHECKING
from backend.model.base import Base

if TYPE_CHECKING:
    from backend.model.notes import Notes


class User(Base):
    __tablename__ = "user"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    admin:Mapped[bool]=mapped_column(default=False)
    notes :Mapped[List["Notes"]] = relationship(back_populates="user")


    def set_password(self, password: str):
        passoword_in_bytes = password.encode("utf-8")
        print("password in bytes", passoword_in_bytes)
        self.password = hashpw(passoword_in_bytes, gensalt()).decode()
        print("password decoding", self.password)

    def check_password(self, password: str) -> bool:
        return checkpw(password.encode(), self.password.encode("utf-8"))
