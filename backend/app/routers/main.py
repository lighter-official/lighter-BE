from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def say_hello():
    return {'msg': 'hello'}

@router.post("/")
def say_post_hello():
    return {'msg': 'post hello'}
