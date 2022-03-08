from typing import AsyncGenerator
from click import echo

from fastapi import Depends
from sqlalchemy import true
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models.models import UserTable
from schemas.user_schemas import UserDB
import os
from .base import Base

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]




engine = create_async_engine(DATABASE_URL,echo = True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(UserDB, session, UserTable)
