from fastapi.routing import APIRouter
from app.routers import echo
from examples import tutorial

api_router = APIRouter()

api_router.include_router(echo.router)
api_router.include_router(tutorial.router)