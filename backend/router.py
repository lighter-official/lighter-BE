from fastapi.routing import APIRouter
from fastapi import Depends
from app.routers import root
from backend.app.routers import user
from examples import tutorial
from backend.core.security.dependency import has_access
from backend.app.routers import sample

PROTECTED = [Depends(has_access)]
api_router = APIRouter()

# 비 로그인 api
api_router.include_router(root.router)
api_router.include_router(main.router)
api_router.include_router(sample.router, prefix='/data')
api_router.include_router(tutorial.router, prefix='/login', tags=['로그인'])

# 로그인 api
api_router.include_router(user.router, dependencies=PROTECTED)
