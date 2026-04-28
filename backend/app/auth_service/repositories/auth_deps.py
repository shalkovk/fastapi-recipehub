from utils.exceptions import UserNotFoundException, TokenNotFound, NoJwtException, NoUserIdException
from fastapi import Request
from models.models import User
from db.database_deps import get_session_with_commit


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


async def get_current_user() -> User:
    pass


async def get_current_admin_user() -> User:
    pass


async def check_refresh_token() -> str:
    pass
