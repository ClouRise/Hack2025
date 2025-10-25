import uuid
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.database import Base

if TYPE_CHECKING:
    from app.models.rooms import Room
    from app.models.messages import Message


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4, primary_key=True, index=True)
    room_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rooms.id"), nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False) 
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Комната, в которой находится пользователь
    room: Mapped["Room"] = relationship("Room", back_populates="users", foreign_keys=[room_id])
    
    # Комнаты, созданные пользователем
    owned_rooms: Mapped[list["Room"]] = relationship("Room", back_populates="owner", foreign_keys="Room.owner_id")
    
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")