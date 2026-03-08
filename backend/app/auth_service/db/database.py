import uuid
from typing import Annotated
from sqlalchemy.orm import mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from config import database_url

engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(DeclarativeBase):
    pass
