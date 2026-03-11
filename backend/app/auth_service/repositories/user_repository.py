from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from sqlalchemy.ext. asyncio import AsyncSession
from db.database_deps import get_session_with_commit, get_session_without_commit
from models.models import User
from db.database import Base


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_users(self) -> List[User]:
        query = select(User)
        result = await self._session.execute(query)
        records = result.scalars().all()
        return records

    async def get_user_by_id(self, id: int) -> Optional[User]:
        query = select(User).filter_by(id)
        result = await self._session.execute(query)
        record = result.scalar_one_or_none()
        return record

    async def get_users_by_role(self, role_id: int) -> List[User]:
        query = select(User).filter_by(role_id)
        result = await self._session.execute(query)
        records = result.scalars().all()
        return records
