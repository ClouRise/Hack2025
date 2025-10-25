from fastapi import APIRouter, Depends, HTTPException, status
from livekit.api import AccessToken, VideoGrants
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, validator, Field, field_validator
import uuid

from typing import Optional
from app.db_depends import get_async_db
import os

from app.models.users import User
from app.models.rooms import Room

router = APIRouter(
    prefix="/liveKit",
    tags=["liveKit"]
)

# LIVEKIT_KONFIG = {
#     "host": "185.31.164.246",
#     "port": 7880,
#     "api_key": "hack2025",
#     "secret_key": "secret_hack2025"
# }

class TokenRequest(BaseModel):
    room_name: str
    user_id: int
    user_name: str

    # @field_validator('room_name') #только после основной валидации
    # @classmethod
    # def validate_uuid(cls, value_room):
    #     try:
    #         return uuid.UUID(value_room)
    #     except ValueError:
    #         raise ValueError("This value dont validate")
        
    # @field_validator('user_id')
    # @classmethod
    # def validate_user(cls, value_user):
    #     try:
    #         return uuid.UUID(value_user)
    #     except ValueError:
    #         raise ValueError("This value dont validate")
        
class GuestToken(BaseModel):
    room_name: str
    user_id: int
    user_name: Optional[str] = Field(default='guest')

    # @field_validator('room_name') #только после основной валидации
    # @classmethod
    # def validate_uuid(cls, value_room):
    #     try:
    #         return uuid.UUID(value_room)
    #     except ValueError:
    #         raise ValueError("This value dont validate")
        
    # @field_validator("user_id")
    # @classmethod
    # def validate_user(cls, value_user):
    #     try:
    #         return uuid.UUID(value_user)
    #     except ValueError:
    #         raise ValueError("This value dont validate")


@router.post('/api/get-token')
async def create_token(request: TokenRequest, db: AsyncSession = Depends(get_async_db)):
    # api_key = LIVEKIT_KONFIG["api_key"]
    # secret_key = LIVEKIT_KONFIG["secret_key"]
    # db_url = f"{LIVEKIT_KONFIG['host']}:{LIVEKIT_KONFIG['port']}"
    api_key = os.getenv("LIVEKIT_KONFIG_API_KEY")
    secret_key = os.getenv("LIVEKIT_KONFIG_SECRET_API_KEY")
    db_host = os.getenv("LIVEKIT_KONFIG_HOST")
    db_port = os.getenv("LIVEKIT_KONFIG_PORT")
    db_url = f"{db_host}:{db_port}"

    token = AccessToken(
        api_key=api_key,
        api_secret=secret_key
    )

    try:
        value_room_name = uuid.UUID(request.room_name)
    except ValueError:
        ValueError("This value not valid")

    nice_uuid_room = select(Room).where(Room.id == value_room_name , Room.is_active == True)
    if nice_uuid_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room by {request.uuid_room} not found"
        )
    
    stmt_room = select(Room).where(Room.id == value_room_name , Room.is_active == True)
    result_room = await db.execute(stmt_room)
    room = result_room.scalar_one_or_none()

    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found in system"
        )

    grant = VideoGrants(room=str(request.room_name), room_join=True, can_publish=True, can_subscribe=True)

    token.with_grants(grant)

    token.with_name(str(request.user_name))
    token.with_identity(str(request.user_id))

    # token.identity = json.dumps(request.user_id)
    # token.name = json.dumps(request.user_name)
    jwt = token.to_jwt()

    return {
        "token": jwt,
        "db_url": db_url,
        "room_id": str(room.id)
    }

@router.post('/api/get-token-for-guest')
async def create_token_for_guest(request: GuestToken):
    api_key = os.getenv("LIVEKIT_KONFIG_API_KEY")
    secret_key = os.getenv("LIVEKIT_KONFIG_SECRET_API_KEY")
    db_host = os.getenv("LIVEKIT_KONFIG_HOST")
    db_port = os.getenv("LIVEKIT_KONFIG_PORT")
    db_url = f"{db_host}:{db_port}"

    token = AccessToken(
        api_key=api_key,
        api_secret=secret_key
    )

    grant = VideoGrants(room=str(request.room_id), room_join=True, can_subscribe=True)

    token.with_grants(grant)

    token.with_name(str(request.user_name))
    token.with_identity(str(request.user_id))

    jwt = token.to_jwt()

    return {
        "token": jwt,
        "db_url": db_url
    }