from utils.exceptions import UserNotFoundException, TokenNotFound, NoJwtException, NoUserIdException, ForbiddenException
from models.models import User
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


async def get_current_user():
    pass


async def check_refresh_token():
    pass


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role.id in [3, 4]:
        return current_user
    raise ForbiddenException
