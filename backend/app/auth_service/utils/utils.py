from fastapi.responses import Response


def create_tokens(data: dict):
    pass


def set_tokens(response: Response, user_id: int):
    pass


async def authenticate_user(user, password):
    pass


def get_hashed_password(password: str) -> str:
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pass
