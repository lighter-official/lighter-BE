import secrets
from typing import Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Depends, FastAPI, Header, Query, Request, HTTPException, status, APIRouter

from backend.fastapi_oauth_client import OAuthClient, oauth_client
from backend.core.utils.jwt_token import generate_access_token

router = APIRouter()

naver_client = OAuthClient(
    client_id="your_client_id",
    client_secret_id="your_client_secret_id",
    redirect_uri="your_callback_uri",
    authentication_uri="https://nid.naver.com/oauth2.0",
    resource_uri="https://openapi.naver.com/v1/nid/me",
    verify_uri="https://openapi.naver.com/v1/nid/verify",
)

kakao_client = OAuthClient(
    client_id="your_client_id",
    client_secret_id="your_client_secret_id",
    redirect_uri="your_callback_uri",
    authentication_uri="https://kauth.kakao.com/oauth",
    resource_uri="https://kapi.kakao.com/v2/user/me",
    verify_uri="https://kapi.kakao.com/v1/user/access_token_info",
)

def get_oauth_client(provider: str = Query(..., pattern="naver|kakao")):
    if provider == "naver":
        return naver_client
    elif provider == "kakao":
        return kakao_client

def get_authorization_token(authorization: str = Header(...)) -> str:
    scheme, _, param = authorization.partition(" ")
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return param

async def login_required(
    oauth_client: OAuthClient = Depends(get_oauth_client),
    access_token: str = Depends(get_authorization_token),
):
    if not await oauth_client.is_authenticated(access_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.get("/kakao", description='카카오 소셜로그인 후 받은 code 로 유저정보와 Gloo 토큰 반환.  \n code 는 1회용인 것 같아요.  \n state 없어도 되네요.')
async def kakao_login(code: str, state: Optional[str] = None):
    token_response = await kakao_client.get_tokens(code, state)
    user_info = await kakao_client.get_user_info(access_token=token_response['access_token'])
    profile = user_info['properties']
    access_token = generate_access_token(profile['nickname'],profile['thumbnail_image'])

    return {
        'profile': profile,
        'access_token': access_token
    }