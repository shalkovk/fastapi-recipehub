from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import async_session_maker

# Dependency session with commit


async def get_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Dependency session without commit


async def get_session_without_commit() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
