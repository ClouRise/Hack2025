import uuid

from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime, null
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from app.database import Base

if TYPE_CHECKING:
  from app.models.users import User
  from app.models.message import Message

class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(default=lambda: str(uuid.uuid4()), primary_key=True, index=True) 
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user: Mapped["User"] = relationship("User", back_populates="room", uselist=False)
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="room")
