from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db.database_deps import get_session_with_commit, get_session_with_commit
from services.user_service import UserService
from schemas.schemas import SUserInfo, SUserRegister, SUserAuth
from utils.exceptions import UserAlreadyExistsException, InvalidCredentialsException

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
