from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from backend.app.models.wrting_set_up import Item, Res
from backend.core.db.connect import writing_db
from backend.core.security.dependency import has_access

router = APIRouter()

@router.get("/set-up", response_model=Res)
def set_up_writing(payload: dict = Depends(has_access)):
    result = writing_db.find_one({'user_id': payload['sub']})
    return result

@router.post("/set-up")
def set_up_writing(item: Item, payload: dict = Depends(has_access)):
    item.subject = item.subject.strip()
    item.subject = item.subject.replace('  ', ' ')
    user_id = payload['sub']
    data = asdict(item)
    data.setdefault('user_id', user_id)
    exist = writing_db.find_one({'user_id': user_id})
    if not exist:
        writing_db.insert_one(data)
        return {'result': 'success'}
    else:
        raise HTTPException(status_code=409, detail='이미 글쓰기 설정이 있습니다.')
