import jwt
from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from backend.core.security.dependency import has_access
from backend.examples.tutorial import get_authorization_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/my", tags=['로그인'], description='로그인 후 Gloo 에서 발행한 access token 을 헤더에 담아 정보를 반환')
def profile(payload: dict = Depends(has_access)):
    return {
        'nickname': payload['nickname'],
        'picture': payload['picture'],
    }
