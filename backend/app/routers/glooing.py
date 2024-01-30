import datetime
from dataclasses import asdict
from datetime import time
import pytz
from backend.core.utils.date_time import datetime_to_str, check_time_range
from bson.objectid import ObjectId

from fastapi import APIRouter, Depends, HTTPException

from backend.app.models import writing_setting, writing
from backend.core.db.connect import writing_db, writing_setting_db
from backend.core.security.dependency import has_access
from backend.core.config.const import max_change_num

router = APIRouter()

@router.get("/set-up", response_model=writing_setting.Res)
def writing_config(payload: dict = Depends(has_access)):
    result = writing_setting_db.find_one({'user_id': payload['sub']})
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail='데이터가 없습니다.')

@router.post("/set-up", summary='글쓰기 설정')
def set_up_writing(item: writing_setting.Item, payload: dict = Depends(has_access)):
    if len(item.start_time) != 4 or not item.start_time.isdigit():
        raise HTTPException(status_code=400, detail='start_time 이 네자리가 아니거나, 숫자가 아닙니다.')

    item.subject = item.subject.strip()
    item.subject = item.subject.replace('  ', ' ')
    user_id = payload['sub']
    data = asdict(item)

    data.setdefault('user_id', user_id)
    data.setdefault('change_num', 0)

    exist = writing_setting_db.find_one({'user_id': user_id})
    if not exist:
        writing_setting_db.insert_one(data)
        return {'result': 'success'}
    else:
        raise HTTPException(status_code=409, detail='이미 글쓰기 설정이 있습니다.')

@router.get("/writings", summary='메인', response_model=writing.MainRes)
def writings(payload: dict = Depends(has_access)):
    user_id = payload['sub']
    writing_setting = writing_setting_db.find_one({'user_id': user_id})
    if writing_setting:
        res = dict()
        res.setdefault('setting', writing_setting)

        writings = []
        for w in writing_db.find({'user_id': user_id}):
            d = dict(w)
            dt:datetime.datetime = d.get('created_at')

            f = datetime_to_str(dt) # UTC datetime 을 한국시간 yyyymmdd 로 변환
            d['created_at'] = f
            d.setdefault('id', str(w.get('_id')))
            writings.append(d)
        writings.sort(key=lambda x:x['idx'], reverse=True) # 글 최신순 정렬
        res.setdefault('writings', writings)
        res.setdefault('can_write', check_time_range(writing_setting.get('start_time'), writing_setting.get('for_hours')))
        res.setdefault('total_writing', writing_db.count_documents({'user_id': user_id})) # 작성한 게시글 수

        return res

    else:
        raise HTTPException(status_code=404, detail='글쓰기 설정이 없습니다.')

@router.get("/writings/{id}", summary='상세', response_model=writing.WritingRes)
def writings(id:str, payload: dict = Depends(has_access)):
    user_id = payload['sub']
    w = None
    try:
        w = writing_db.find_one({'_id': ObjectId(id)})
    except:
        pass
    if w:
        res = writing.WritingRes(w.get('idx'),w.get('title'),w.get('desc'),datetime_to_str(w.get('created_at')))
        return res
    else:
        raise HTTPException(status_code=404, detail='데이터가 없습니다.')

@router.post("/writings", summary='글쓰기')
def writings(req: writing.Writing, payload: dict = Depends(has_access)):
    user_id = payload['sub']
    setting_id = dict(writing_setting_db.find_one({'user_id': user_id}))['_id']

    total = writing_db.count_documents({'user_id': user_id})
    idx = total + 1

    data = asdict(req)
    data.setdefault('idx',idx)
    data.setdefault('created_at',datetime.datetime.now(tz=datetime.timezone.utc))
    data.setdefault('writing_setting_id',setting_id)
    data.setdefault('user_id',user_id)

    writing_db.insert_one(data)
    return {
        'idx': idx,
        'result': 'success',
    }

@router.put("/writings/{id}", summary='수정')
def writings(id:str, req: writing.Writing, payload: dict = Depends(has_access)):
    update_data = asdict(req)
    user_id = payload['sub']
    update ={'$set': update_data}

    result = None
    try:
        result = writing_db.find_one_and_update({'_id': ObjectId(id), 'user_id': user_id},update)
    except:
        pass
    if result:
        return {'result': 'success'}
    else:
        raise HTTPException(status_code=404, detail='데이터가 없습니다.')
