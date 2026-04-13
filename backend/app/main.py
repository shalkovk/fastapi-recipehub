from auth_service.routes.auth_router import APIRouter as auth_router
from auth_service.config import settings

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter

app = FastAPI(
    title=settings.app_name,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
