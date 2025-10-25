import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.messages import Message as MessageModel
from app.models.rooms import Room as RoomModel
from app.models.users import User as UserModel
from app.schemas.message import MessageCreate, MessageRead
from app.db_depends import get_async_db


#Создаём маршрутизатор для сообщений
router = APIRouter(
    prefix="/messages",
    tags=["messages"],
)


@router.get("/", response_model=list[MessageRead], status_code=status.HTTP_200_OK)
async def get_all_messages(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех сообщений
    """
    stmt_messages = select(MessageModel)
    result_messages = await db.execute(stmt_messages)
    return result_messages.scalars().all()

@router.get("/room/{room_id}", response_model=list[MessageRead], status_code=status.HTTP_200_OK)
async def get_room_messages(room_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список сообщений определенной комнаты по ее UUID
    """
    stmt_room = select(RoomModel).where(RoomModel.id == room_id, RoomModel.is_active == True)
    result_room = await db.execute(stmt_room)
    db_room = result_room.scalar_one_or_none()
    if db_room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    stmt_messages = select(MessageModel).where(MessageModel.room_id == db_room.id)
    result_messages = await db.execute(stmt_messages)
    messages = result_messages.scalars().all()
    return messages

@router.post("/message", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(message: MessageCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Создает новое СМС ХААХАХАХАХХААХАХ
    """
    stmt_user = select(UserModel).where(UserModel.id == message.user_id, UserModel.is_active == True)
    result_user = await db.execute(stmt_user)
    db_user = result_user.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    stmt_room = select(RoomModel).where(RoomModel.id == message.room_id, RoomModel.is_active == True)
    result_room = await db.execute(stmt_room)
    db_room = result_room.scalar_one_or_none()
    if db_room is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong room"
        )
    
    db_message = MessageModel(**message.model_dump())
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message