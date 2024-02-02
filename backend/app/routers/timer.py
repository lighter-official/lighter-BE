from fastapi import WebSocket,APIRouter
import asyncio
import datetime
from backend.core import utils
import json

router = APIRouter()

# remaining_time 이 1 days 를 넘으면 계산되지 않음
def remain_time_str(start: datetime, end: datetime) -> str:
    remaining_time = end - start
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"

@router.websocket('/main')
async def timer(websocket: WebSocket):
    await websocket.accept()

    # JSON 형식으로 데이터 수신
    data_received = await websocket.receive_text()

    # JSON 문자열을 파싱하여 Python 객체로 변환
    data_dict = json.loads(data_received)

    # 데이터 사용
    h = data_dict.get('h')
    m = data_dict.get('m')
    for_hours = data_dict.get('for_hours')

    cur = datetime.datetime.now()
    start = cur.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
    end = start + datetime.timedelta(hours=int(for_hours))

    while True:
        cur = datetime.datetime.now()
        write_button_activated = False
        text_red = False

        # 글쓰기 시간 전
        if cur < start:
            remaining_time_str = remain_time_str(cur,start)
            print('=============== 글쓰기 시간 전 ====================')

        else:
            # 글쓰기 시간 중
            if start <= cur <= end:
                remaining_time = end - cur
                remaining_time_str = remain_time_str(cur,end)
                write_button_activated = True
                print('=============== 글쓰기 시간 중 ====================')

                if remaining_time.total_seconds() <= 600: # 10분 밖에 안 남았을 때
                    text_red = True

            # 글쓰기 시간이 지나 다음날
            else:
                next_start = start + datetime.timedelta(days=1)
                remaining_time_str = remain_time_str(cur,next_start)
                print('=============== 글쓰기 시간이 지나 다음날을 기다림 ====================')

        data_to_send = {
            'remaining_time': remaining_time_str,
            'write_button_activated': write_button_activated,
            'text_red': text_red,
        }
        await websocket.send_text(json.dumps(data_to_send))
        await asyncio.sleep(1)

