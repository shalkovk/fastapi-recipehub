from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import settings
from fastapi.responses import Response


def create_tokens(data: dict) -> dict:
    now = datetime.now(timezone.utc)

    access_expire = now + timedelta(minutes=2)
    access_payload = data.copy()
    access_payload.update(
        {"exp": int(access_expire.timestamp()), "type": "access"})
    access_token = jwt.encode(
        access_payload, settings.secret_key, algorithm=settings.algorithm)

    refresh_expire = now + timedelta(days=7)
    refresh_payload = data.copy()
    refresh_payload.update(
        {"exp": int(refresh_expire.timestamp()), "type": "refresh"})
    refresh_token = jwt.encode(
        refresh_payload, settings.secret_key, algorithm=settings.algorithm)

    return {"access_token": access_token, "refresh_token": refresh_token}


def set_tokens(response: Response, user_id: int):
    new_tokens = create_tokens(data={"sub": str(user_id)})
    access_token = new_tokens.get("access_token")
    refresh_token = new_tokens.get("refresh_token")

    response.set_cookie(key="user_access_token", value=access_token,
                        httponly=True, secure=True, samesite="lax")
    response.set_cookie(key="user_refresh_token", value=refresh_token,
                        httponly=True, secure=True, samesite="lax")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(user, password):
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
