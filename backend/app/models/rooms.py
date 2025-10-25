import uuid
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.database import Base

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.messages import Message


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4, primary_key=True, index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False) 
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    # Создатель комнаты
    owner: Mapped["User"] = relationship("User", back_populates="owned_rooms", foreign_keys=[owner_id])
    
    # Участники комнаты
    users: Mapped[list["User"]] = relationship("User", back_populates="room", foreign_keys="User.room_id")
    
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="room",
        cascade="all, delete-orphan",
        passive_deletes=True
        )