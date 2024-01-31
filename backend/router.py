from fastapi.routing import APIRouter
from fastapi import Depends
from app.routers import root
from backend.app.routers import user, glooing, my,ws_glooing
from examples import tutorial
from backend.core.security.dependency import has_access
from backend.app.routers import sample

PROTECTED = [Depends(has_access)]
api_router = APIRouter()
ws_router = APIRouter()

## 비 로그인 라우터

# api
api_router.include_router(root.router)
api_router.include_router(sample.router, prefix='/data')
api_router.include_router(tutorial.router, prefix='/login', tags=['로그인'])

# 웹 소켓
ws_router.include_router(ws_glooing.router, prefix='/glooing', tags=['글루ING'])

## 로그인 라우터
api_router.include_router(user.router, dependencies=PROTECTED)
api_router.include_router(glooing.router, prefix='/glooing', tags=['글루ING'], dependencies=PROTECTED)
api_router.include_router(my.router, prefix='/my', tags=['나의 보관함'], dependencies=PROTECTED)
