import uuid
import jwt
from app.models.rooms import Room as RoomModel
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.models.messages import Message as MessageModel
from app.models.users import User as UserModel
from app.schemas.user import UserRead, UserCreate
from app.db_depends import get_async_db
from app.auth import hash_password, create_access_token, create_refresh_token, verify_password, get_current_user
from app.config import SECRET_KEY, ALGORITHM


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserRead)
async def get_my_profile(current_user: UserModel = Depends(get_current_user)):
    """
    Возвращает профиль
    """
    return current_user

@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает юзера по айди
    """
    stmt_user = select(UserModel).where(UserModel.id == user_id, UserModel.is_active == True)
    result_user = await db.execute(stmt_user)
    db_user = result_user.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return db_user

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Регистрация нового пользователя
    """
    # проверка на уникальность
    stmt_email = select(UserModel).where(UserModel.email == user.email)
    result_email = await db.execute(stmt_email)
    email = result_email.scalar_one_or_none()
    if email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    db_user = UserModel(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Аутентифицирует пользователя и возращает токены
    """
    stmt_user = select(UserModel).where(UserModel.email == form_data.username)
    result_user = await db.execute(stmt_user)
    user = result_user.scalar_one_or_none()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.email, "id": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": user.email, "id": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh_token")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_async_db)):
    """
    Обновляет аксес токен с помощью рефреш токена
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    stmt_user = select(UserModel).where(UserModel.email == email, UserModel.is_active == True)
    result_user = await db.execute(stmt_user)
    user = result_user.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.email, "id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_async_db)):
    # Проверяем, есть ли у пользователя комнаты
    stmt_rooms = select(RoomModel).where(RoomModel.owner_id == user_id)
    result = await db.execute(stmt_rooms)
    owned_room = result.scalar_one_or_none()
    
    if owned_room:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить пользователя, который является владельцем комнаты"
        )
    
    # Удаляем все сообщения пользователя
    stmt_delete_messages = delete(MessageModel).where(MessageModel.user_id == user_id)
    await db.execute(stmt_delete_messages)
    
    # Удаляем пользователя
    stmt_delete_user = delete(UserModel).where(UserModel.id == user_id)
    await db.execute(stmt_delete_user)
    
    await db.commit()
    return {"detail": "Пользователь и его сообщения успешно удалены"}

