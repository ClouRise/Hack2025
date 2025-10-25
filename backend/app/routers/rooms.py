import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rooms import Room as RoomModel

from app.schemas.room import RoomRead, RoomCreate, RoomAddParticipant
from app.db_depends import get_async_db


#Создаём маршрутизатор для комнат
router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)


@router.get("/", response_model=list[RoomRead], status_code=status.HTTP_200_OK)
async def get_all_rooms(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех комнат
    """
    stmt_rooms = select(RoomModel).where(RoomModel.is_active == True)
    result_rooms = await db.execute(stmt_rooms)
    return result_rooms.scalars().all()


@router.post("/", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
async def create_room(room: RoomCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Создание новой комнаты
    """
    db_room = RoomModel(**room.model_dump())
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room
