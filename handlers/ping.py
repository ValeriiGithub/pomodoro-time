from fastapi import APIRouter

from settings import Settings

router = APIRouter(prefix="/ping",
                   tags=["ping"])


@router.get("/ping")
async def ping():
    settings = Settings()
    return {"message": settings}

@router.get("/db")
async def ping_db():
    return {"db": "pomodoro"}

@router.get("/app")
async def ping_app():
    return {"text": "app is working"}