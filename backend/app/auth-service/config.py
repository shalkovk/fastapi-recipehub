from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "RecipeHub Auth service"
    debug: bool = True
    database_url: str
    cors_origins: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
