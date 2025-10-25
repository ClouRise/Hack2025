from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import messages, rooms, users
from app import liveKit



app = FastAPI(
    title="FastAPI конфа",
    version="0.1.1"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       #Разрешить все домены   
    allow_credentials=True,    # Разрешить куки и авторизацию
    allow_methods=["*"],       # Разрешить все HTTP методы
    allow_headers=["*"],       # Разрешить все заголовки
    expose_headers=["*"],
)

#ПРИЛОЖЕНИЕ FASTAPI
app.include_router(messages.router)
app.include_router(rooms.router)
app.include_router(liveKit.router)
app.include_router(users.router)

#КОРНЕВОЙ ЭНДПОИНТ 
@app.get("/")
async def root():
    """
    КОРНЕВОЙ МАРШРУТ, ДЛЯ ПРОВЕРКИ API
    """
    return {"message": "ДОБРО ПОЖАЛОВАТЬ"}