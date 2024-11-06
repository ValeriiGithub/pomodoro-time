from fastapi import APIRouter

from settings import settings

router = APIRouter(prefix="/ping",
                   tags=["ping"])


@router.get("/ping")
async def ping():
    return {"message": settings}

@router.get("/db")
async def ping_db():
    return {"db": "pomodoro"}

@router.get("/app")
async def ping_app():
    return {"text": "app is working"}