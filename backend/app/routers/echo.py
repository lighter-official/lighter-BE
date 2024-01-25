from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def send_echo_message():
    return {'msg': 'hello'}
