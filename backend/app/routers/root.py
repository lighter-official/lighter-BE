from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
def say_hello():
    return {'msg': 'hello'}

@router.post("/")
def say_post_hello():
    return {'msg': 'post hello'}
