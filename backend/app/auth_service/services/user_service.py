from db.database_deps import get_session_with_commit, get_session_without_commit
from repositories.user_repository import UserRepository
from config import settings
from fastapi.requests import Request


class UserService:
    def __init__(self, session):
        self.repository = UserRepository(session)
