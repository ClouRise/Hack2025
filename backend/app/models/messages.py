from ast import For
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from app.database import Base


if TYPE_CHECKING:
    from app.models.users import User
    from app.models.rooms import Room


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_id: Mapped[str] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    room: Mapped["Room"] = relationship("Room", back_populates="messages")
    user: Mapped["User"] = relationship("User", back_populates="messages")
    

