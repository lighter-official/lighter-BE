from fastapi import WebSocket
from fastapi import APIRouter
import asyncio
import datetime
from backend.core.utils import date_time

router = APIRouter()

@router.websocket('/timer')
async def timer(websocket: WebSocket):
    await websocket.accept()
    start_time = await websocket.receive_text() # start_time 을 20:00 -> "2000" 으로 입력받는다.

    target_hour = int(start_time[:2])
    target_minute = int(start_time[2:])
    current_time = date_time.kr_now()
    target_time = current_time.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    while True:
        current_time = date_time.kr_now()

        if current_time > target_time:  # 시간이 지났을 때
            target_time += datetime.timedelta(days=1) # Target time has already passed, calculate for the next day

        remaining_time = target_time - current_time
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}" # Format remaining time as hh:mm:ss
        print(remaining_time_str)

        await websocket.send_text(remaining_time_str) # Send formatted remaining time to the frontend
        await asyncio.sleep(1)
