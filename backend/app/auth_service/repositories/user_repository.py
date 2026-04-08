from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext. asyncio import AsyncSession
from models.models import User
from schemas.schemas import SUserAddDb


class UserRepository:
    async def get_all_users(self, session: AsyncSession) -> List[User]:
        query = select(User).limit(100)
        result = await session.execute(query)
        records = result.scalars().all()
        return records

    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

    async def get_users_by_role(self, role_id: int, session: AsyncSession) -> List[User]:
        query = select(User).where(User.role_id == role_id)
        result = await session.execute(query)
        records = result.scalars().all()
        return records

    async def get_user_by_email(self, user_email: str, session: AsyncSession) -> Optional[User]:
        query = select(User).where(User.email == user_email)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

    async def get_users_by_role(self, role_id: int, session: AsyncSession) -> Optional[User]:
        query = select(User).where(User.role_id == role_id)
        result = await session.execute(query)
        records = result.scalars().all()
        return records

    async def add_user(self, user_data: SUserAddDb, session: AsyncSession) -> User:
        new_user = User(**user_data.model_dump())
        session.add(new_user)
        await session.flush()
        return new_user
