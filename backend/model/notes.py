from sqlalchemy.orm import  mapped_column, Mapped, relationship
from uuid import UUID, uuid4
from backend.model.user import User
from sqlalchemy import String, ForeignKey
from backend.model.base import Base


class Notes(Base):
    __tablename__ = "notes"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    content: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="notes")
