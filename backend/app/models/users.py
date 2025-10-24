import uuid

from sqlalchemy import ForeignKey, null
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.database import Base

if TYPE_CHECKING:
  from app.models.rooms import Room
  from app.models.message import Message


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(default=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    room_id: Mapped[str] = mapped_column(ForeignKey("rooms.id"), nullable=True, unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False) 
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    room: Mapped["Room"] = relationship("Room", back_populates="user", uselist=False)
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")
