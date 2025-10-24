from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


#Асинхронное подключение к PostgreSQL

DATABASE_URL = "postgresql+asyncpg://admin_user:123@localhost:5432/backend_db"
async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass