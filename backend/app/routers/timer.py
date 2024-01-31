from fastapi import WebSocket,APIRouter
import asyncio
import datetime
from backend.core import utils
import json

router = APIRouter()

@router.websocket('/main')
async def timer(websocket: WebSocket):
    await websocket.accept()
    ampm = await websocket.receive_text() # start_time 을 20:00 -> "2000" 으로 입력받는다.
    h = await websocket.receive_text() # start_time 을 20:00 -> "2000" 으로 입력받는다.
    m = await websocket.receive_text() # start_time 을 20:00 -> "2000" 으로 입력받는다.
    for_hours = await websocket.receive_text() # start_time 을 20:00 -> "2000" 으로 입력받는다.
    time_str = utils.date_time.ampm_to_str([ampm,h,m])

    target_hour = int(time_str[:2])
    target_minute = int(time_str[2:])
    current_time = utils.date_time.kr_now()
    target_time = current_time.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    while True:
        current_time = utils.date_time.kr_now()

        if current_time > target_time:  # 시간이 지났을 때
            target_time += datetime.timedelta(days=1) # Target time has already passed, calculate for the next day

        remaining_time = target_time - current_time
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}" # Format remaining time as hh:mm:ss

        data_to_send = {
            'remaining_time': remaining_time_str,
            'write_button_activated': True
        }

        # Convert the dictionary to a JSON string
        json_data = json.dumps(data_to_send)
        print(json_data)

        await websocket.send_text(json_data) # Send formatted remaining time to the frontend
        await asyncio.sleep(1)
