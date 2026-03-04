import uuid
from typing import Annotated, AsyncGenerator
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from config import database_url

engine = create_async_engine(url=database_url)
async_sessionmaker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close
