import copy
import datetime
import re
from dataclasses import asdict
from datetime import time,timedelta
import pytz
from backend.core.utils.date_time import datetime_to_str, check_time_range, ampm_to_str, str_to_12hours, str_to_24hours, \
    get_now, different_date, datetime_to_str_kr, datetime_to_list
from bson.objectid import ObjectId

from fastapi import APIRouter, Depends, HTTPException

from backend.app.models import writing_setting, writing
from backend.core.db.connect import writing_db, writing_setting_db, my_badge_db, finished_writing_setting_db, finished_writing_db, badges_db
from backend.core.security.dependency import has_access
from backend.core.config import const

router = APIRouter()

# @router.get("/set-up", response_model=writing_setting.Res, summary='글쓰기 설정 확인 테스트용')
# def writing_config(payload: dict = Depends(has_access)):
#     result = writing_setting_db.find_one({'user_id': payload['sub']})
#     if not result:
#         raise HTTPException(status_code=404, detail='데이터가 없습니다.')
#     result['start_time'] = str_to_24hours(result.get('start_time'))
#     if result:
#         return result
#     else:
#         raise HTTPException(status_code=404, detail='데이터가 없습니다.')

@router.post("/set-up", summary='글쓰기 설정')
def set_up_writing(item: writing_setting.Item, payload: dict = Depends(has_access)):
    if len(item.start_time) != 3:
        raise HTTPException(status_code=400, detail='start_time 이 ["AM",3,30] format 이 아닙니다.')

    item.subject = item.subject.strip()
    item.subject = re.sub('[ ]{2,}',' ',item.subject)
    user_id = payload['sub']
    data = asdict(item)

    data.setdefault('user_id', user_id)
    data.setdefault('change_num', 0)
    data.setdefault('created_at', get_now())
    data['start_time'] = ampm_to_str(item.start_time)

    exist = writing_setting_db.find_one({'user_id': user_id})
    if not exist:
        writing_setting_db.insert_one(data)
        return {'result': 'success'}
    else:
        raise HTTPException(status_code=409, detail='이미 글쓰기 설정이 있습니다.')

@router.delete("/set-up", summary='글쓰기 설정 삭제')
def delete_writing_setting(payload: dict = Depends(has_access)):
    user_id = payload['sub']
    writing_setting_db.delete_one({'user_id': user_id})
    writing_db.delete_many({'user_id': user_id})
    return {'result': 'success'}

@router.get("/writings", summary='메인', response_model=writing.MainRes)
def writings(payload: dict = Depends(has_access)):
    user_id = payload['sub']
    writing_setting = writing_setting_db.find_one({'user_id': user_id})
    if writing_setting:
        created_at = writing_setting.get('created_at')

        res = dict()
        res.setdefault('setting', copy.deepcopy(writing_setting))
        res.get('setting')['start_time'] = str_to_24hours(writing_setting.get('start_time'))

        writings = []
        for w in writing_db.find({'user_id': user_id}):
            d = dict(w)
            dt:datetime.datetime = d.get('created_at')

            d['created_at'] = datetime_to_list(dt) # UTC datetime 을 한국시간 yyyymmdd 로 변환
            d.setdefault('id', str(w.get('_id')))
            writings.append(d)
        writings.sort(key=lambda x:x['idx'], reverse=True) # 글 최신순 정렬
        res.setdefault('writings', writings)
        res.setdefault('can_write', check_time_range(writing_setting.get('start_time'), writing_setting.get('for_hours')))
        res.setdefault('total_writing', writing_db.count_documents({'user_id': user_id})) # 작성한 게시글 수
        res.setdefault('start_date',datetime_to_str_kr(created_at))
        res.setdefault('end_date',datetime_to_str_kr(created_at+timedelta(writing_setting.get('period'))))
        res.setdefault('d_day', different_date(get_now(), created_at + timedelta(writing_setting.get('period'))))

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

@router.post("/writings", summary='글쓰기', response_model=writing.WritingInsertRes)
def writings(req: writing.Writing, payload: dict = Depends(has_access)):
    user_id = payload['sub']
    setting = None
    try:
        setting = dict(writing_setting_db.find_one({'user_id': user_id}))
    except:
        pass
    if setting == None:
        raise HTTPException(status_code=404, detail='글쓰기 설정이 없습니다.')

    setting_id = setting['_id']
    target_writing = setting['page']

    total = writing_db.count_documents({'user_id': user_id})
    idx = total + 1

    issued_badge = None

    ## 1. 뱃지발급
    # 첫 업로드 뱃지 발급
    if idx == 1:
        badge_issued = issue_badge(user_id,'first-upload')
        if badge_issued:
            issued_badge = 'first-upload'
    
    if target_writing == 0:
        raise HTTPException(status_code=409, detail='목표 페이지 수가 0 입니다.')
    achieve_rate = round((idx/target_writing)*100) # 달성률

    # 달성률 체크 및 뱃지 발급
    for i in range(len(const.achieve_badges) - 1, -1, -1):
        target = const.achieve_badges[i]
        if achieve_rate >= target:
            badge_issued = issue_badge(user_id, 'achievement', target)
            if badge_issued:
                issued_badge = f'achievement-{str(target)}'

    ## 2. 글 저장
    data = req.dict(exclude_unset=True)
    data.setdefault('idx',idx)
    data.setdefault('created_at',datetime.datetime.now(tz=datetime.timezone.utc))
    data.setdefault('writing_setting_id',setting_id)
    data.setdefault('user_id',user_id)

    writing_db.insert_one(data)

    ## 3. 목표 달성 시 글 아카이브
    if idx == setting.get('page'):

        # 글 아카이브
        documents_to_move = writing_db.find({'writing_setting_id': setting_id})
        documents = []
        for doc in documents_to_move:
            setting = writing_setting_db.find_one({'_id': doc.get('writing_setting_id')})
            subject = setting.get('subject')
            result = dict(doc)
            result.setdefault('subject', subject)
            documents.append(result)
        finished_writing_db.insert_many(documents)
        writing_db.delete_many({'writing_setting_id': setting_id})

        # 글 설정 아카이브
        documents_to_move = writing_setting_db.find({'_id': setting_id})
        finished_writing_setting_db.insert_many(documents_to_move)
        writing_setting_db.delete_many({'_id': setting_id})

    res = writing.WritingInsertRes(
        idx=idx,
        issued_badge=issued_badge,
    )
    if achieve_rate >= 75: # 75% 이상 도달한 유저에게 노출
        res.achieve_rate = achieve_rate

    return res

@router.patch("/writings/{id}", summary='수정')
def writings(id:str, req: writing.Writing, payload: dict = Depends(has_access)):
    update_data = req.dict(exclude_unset=True)

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

def issue_badge(user_id: str,type: str, target: int|None=None) -> bool:
    if target:
        badge_type = f'{type}-{str(target)}'
    else:
        badge_type = type

    id = badges_db.find_one({'type': badge_type}).get('_id')
    exist = my_badge_db.find_one({'user_id': user_id, 'badge_id': id})
    if not exist:
        my_badge_db.insert_one({
            'user_id': user_id,
            'badge_id': id,
            'created_at': get_now()
        })
        return True
    return False
