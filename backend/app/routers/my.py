import jwt
from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from backend.core.security.dependency import has_access
from backend.examples.tutorial import get_authorization_token
from backend.core.db import connect
from backend.core.utils import date_time
from backend.app.models import badge
from dataclasses import asdict

router = APIRouter()

@router.get("/badge", summary='나의 뱃지', response_model=badge.BadgeRes)
def badges(payload: dict = Depends(has_access)):
    user_id = payload['sub']
    res = []
    for b in connect.my_badge_db.find({'user_id': user_id}):
        id = b.get('badge_id')
        badge = connect.badges_db.find_one({'_id':id})

        res.append({
            'category': badge.get('category'),
            'name': badge.get('name'),
            'type': badge.get('type'),
            'created_at': date_time.datetime_to_str(b.get('created_at')),
        })
    # res.sort(key=lambda x:(x['type'])) # 달성도 순 정렬
    return {'badges': res}
