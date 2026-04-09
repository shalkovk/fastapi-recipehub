from db.database_deps import get_session_with_commit, get_session_without_commit
from repositories.user_repository import UserRepository
from schemas.schemas import SUserRegister, SUserInfo, SUserAddDb
from sqlalchemy.ext.asyncio import AsyncSession
from utils.exceptions import UserAlreadyExistsException
from utils.utils import get_hashed_password
from config import settings
from fastapi.requests import Request


class UserService:
    def __init__(self):
        self.repository = UserRepository

    async def register_user(self, user_data: SUserRegister, session: AsyncSession) -> SUserInfo:
        existing_user = await self.repository.get_user_by_email(user_data.email, session)
        if existing_user:
            raise UserAlreadyExistsException(
                f"Username with email {user_data.email} already exists")

        hashed_password = get_hashed_password(user_data.password)
        user_to_save = SUserAddDb(email=user_data.email, first_name=user_data.first_name,
                                  last_name=user_data.last_name, password=hashed_password)
        new_user = await self.repository.add_user(user_to_save, session)
        return SUserInfo.model_validate(new_user)
