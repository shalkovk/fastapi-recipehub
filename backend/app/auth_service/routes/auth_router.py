from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.auth_deps import get_current_user
from models.models import User
from db.database_deps import get_session_with_commit, get_session_without_commit
from services.user_service import UserService
from schemas.schemas import SUserInfo, SUserRegister, SUserAuth
from utils.utils import set_tokens

router = APIRouter(
    prefix="/api/auth",
    tags=["authorization"]
)


@router.post("/register", response_model=SUserInfo, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserRegister, session: AsyncSession = Depends(get_session_with_commit)):
    service = UserService()
    user_info = await service.register_user(user_data, session)
    return user_info


@router.post("/login", response_model=SUserInfo, status_code=status.HTTP_200_OK)
async def login_user(auth_data: SUserAuth, response: Response, session: AsyncSession = Depends(get_session_with_commit)):
    service = UserService()
    user_info = await service.login_user(auth_data, response, session)
    return user_info


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key="user_access_token")
    response.delete_cookie(key="user_refresh_token")
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=SUserInfo, status_code=status.HTTP_200_OK)
async def get_me(user_data: User = Depends(get_current_user)) -> SUserInfo:
    return SUserInfo.model_validate(user_data)


@router.post("/refresh")
async def refresh_token(response: Response, user: User = Depends(get_current_user)):
    set_tokens(response, user.id)
    return {"message": "Tokens are now up-to-date"}
