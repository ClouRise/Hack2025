from pydantic import BaseModel
from typing import List, Optional
from app.schemas.user import UserRead
from uuid import UUID
from datetime import datetime
class RoomCreate(BaseModel):
    name: str

class RoomRead(BaseModel):
    id: UUID
    name: str
    is_active: bool
    owner_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class RoomAddParticipant(BaseModel):
    user_id: UUID
