from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import settings
from fastapi.responses import Response


def create_tokens(data: dict) -> dict:
    pass


def set_tokens(response: Response, user_id: int):
    new_tokens = create_tokens(data={"sub": str(user_id)})
    access_token = new_tokens.get("access_token")
    refresh_token = new_tokens.get("refresh_token")

    response.set_cookie(key="user_access_token", value=access_token,
                        httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="user_refresh_token", value=refresh_token,
                        httponly=True, secure=True, samesite="lax")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(user, password) -> bool:
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
