from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime


class RoomCreate(BaseModel):
    name: str = Field(min_length=2)
    owner_id: UUID


class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    is_active: bool
    created_at: datetime

class RoomAddParticipant(BaseModel):
    user_id: UUID
