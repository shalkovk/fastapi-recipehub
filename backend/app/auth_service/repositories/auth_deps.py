from utils.exceptions import UserNotFoundException, TokenNotFound, NoJwtException, NoUserIdException
from fastapi import Request


async def get_current_user():
    pass


async def get_current_admin_user():
    pass


def get_access_token():
    pass


def get_refresh_token():
    pass


async def check_refresh_token():
    pass
