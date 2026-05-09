from datetime import datetime, timezone
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import User
from repositories.user_repository import UserRepository
from utils.exceptions import UserNotFoundException, TokenNotFound, NoJwtException, NoUserIdException, ForbiddenException, TokenExpiredException
from db.database_deps import get_session_without_commit
from config import settings

from fastapi import Request, Depends


def get_access_token(request: Request) -> str:
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenNotFound
    return token


def get_refresh_token(request: Request) -> str:
    token = request.cookies.get("user_refresh_token")
    if not token:
        raise TokenNotFound
    return token


async def check_refresh_token(token: str = Depends(get_refresh_token), session: AsyncSession = Depends(get_session_without_commit)) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise NoJwtException
        try:
            user_id = int(user_id_str)
        except (TypeError, ValueError):
            raise NoUserIdException

        repository = UserRepository()
        user = await repository.get_user_by_id(user_id, session=session)
        if not user:
            raise NoJwtException
        return user
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException


async def get_current_user(token: str = Depends(get_access_token), session: AsyncSession = Depends(get_session_without_commit)) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise NoJwtException
        try:
            user_id = int(user_id_str)
        except (TypeError, ValueError):
            raise NoUserIdException

        exp: int = payload.get("exp")
        if not exp or datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise TokenExpiredException

        repository = UserRepository()
        user = await repository.get_user_by_id(user_id, session)

        if not user:
            raise UserNotFoundException
        return user
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role.id in [3, 4]:
        return current_user
    raise ForbiddenException
