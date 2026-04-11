from db.database_deps import get_session_with_commit, get_session_without_commit
from repositories.user_repository import UserRepository
from schemas.schemas import SUserRegister, SUserInfo, SUserAddDb, SUserAuth
from sqlalchemy.ext.asyncio import AsyncSession
from utils.exceptions import UserAlreadyExistsException, InvalidCredentialsException, UserNotFoundException
from utils.utils import get_hashed_password, authenticate_user, set_tokens
from config import settings
from fastapi import Response


class UserService:
    def __init__(self):
        self.repository = UserRepository

    async def register_user(self, user_data: SUserRegister, session: AsyncSession) -> SUserInfo:
        existing_user = await self.repository.get_user_by_email(user_data.email, session)
        if existing_user:
            raise UserAlreadyExistsException

        hashed_password = get_hashed_password(user_data.password)
        user_to_save = SUserAddDb(email=user_data.email, first_name=user_data.first_name,
                                  last_name=user_data.last_name, password=hashed_password)
        new_user = await self.repository.add_user(user_to_save, session)
        return SUserInfo.model_validate(new_user)

    async def login_user(self, auth_data: SUserAuth, response: Response, session: AsyncSession) -> SUserInfo:
        user = await self.repository.get_user_by_email(auth_data.email, session)
        authenticated_user = await authenticate_user(user, auth_data.password)
        if not authenticated_user:
            raise InvalidCredentialsException
        set_tokens(response=response, user_id=authenticated_user.id)
        return SUserInfo.model_validate(authenticated_user)

    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> SUserInfo:
        user = await self.repository.get_user_by_id(user_id, session)
        if not user:
            raise UserNotFoundException
        return SUserInfo.model_validate(user)
