from fastapi.routing import APIRouter
from app.routers import echo

api_router = APIRouter()

api_router.include_router(echo.router)