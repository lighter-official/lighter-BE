from fastapi.routing import APIRouter
from app.routers import main
from backend.app.routers import sample

api_router = APIRouter()

api_router.include_router(main.router)
api_router.include_router(sample.router, prefix='/data')