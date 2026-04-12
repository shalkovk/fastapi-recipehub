from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response

from repositories.user_repository import UserRepository
from schemas.schemas import SUserRegister, SUserInfo, SUserAddDb, SUserAuth
from utils.exceptions import UserAlreadyExistsException, InvalidCredentialsException, UserNotFoundException
from utils.utils import get_hashed_password, authenticate_user, set_tokens


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
        await self.update_last_login(authenticated_user.id, session)
        set_tokens(response=response, user_id=authenticated_user.id)
        return SUserInfo.model_validate(authenticated_user)

    async def get_user_by_id(self, user_id: int, session: AsyncSession) -> SUserInfo:
        user = await self.repository.get_user_by_id(user_id, session)
        if not user:
            raise UserNotFoundException
        return SUserInfo.model_validate(user)

    async def update_last_login(self, user_id: int, session: AsyncSession) -> None:
        user = await self.repository.get_user_by_id(user_id, session)
        if user:
            user.last_login_at = datetime.utcnow()
