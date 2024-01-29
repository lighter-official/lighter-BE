from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
def send_echo_message():
    return {'msg': 'hello'}

@router.post("/")
def send_echo_message():
    return {'msg': 'post hello'}

