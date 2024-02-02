from fastapi import WebSocket,APIRouter
import asyncio
import datetime
from backend.core import utils
import json
import websockets

router = APIRouter()
websocket_connections = []

@router.websocket('/main')
async def timer(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    print('1------------------------')
    # ampm = await websocket.receive_text()
    print('2------------------------')
    h = await websocket.receive_text()
    print('3------------------------')
    m = await websocket.receive_text()
    print('4------------------------')
    for_hours = await websocket.receive_text()
    ampm = 'AM'
    if int(h) >= 12:
        h = str(int(h) - 12)
        ampm = 'PM'
    print(ampm,h,m,for_hours)
    time_str = utils.date_time.ampm_to_str([ampm,h,m])

    target_hour = int(time_str[:2])
    target_minute = int(time_str[2:])
    current_time = utils.date_time.kr_now()
    target_time = current_time.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    text_red = False

    try:
        while True:

            # 글쓰기 시간이 아닐 때
            while not utils.date_time.check_time_range(time_str,int(for_hours)):
                current_time = utils.date_time.kr_now()

                if current_time > target_time:  # 시간이 지났을 때
                    target_time += datetime.timedelta(days=1) # Target time has already passed, calculate for the next day

                remaining_time = target_time - current_time
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}" # Format remaining time as hh:mm:ss

                data_to_send = {
                    'remaining_time': remaining_time_str,
                    'write_button_activated': False,
                    'text_red': False,
                }

                json_data = json.dumps(data_to_send) # Convert the dictionary to a JSON string
                print(json_data)

                await websocket.send_text(json_data) # Send formatted remaining time to the frontend
                await asyncio.sleep(1)

            # 글쓰기 시간일 때
            current_time = utils.date_time.kr_now()

            end_time = target_time + datetime.timedelta(hours=int(for_hours))

            remaining_time = end_time - current_time
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}" # Format remaining time as hh:mm:ss
            if remaining_time.total_seconds() <= 600:  # 10 minutes = 600 seconds
                text_red = True

            data_to_send = {
                'remaining_time': remaining_time_str,
                'write_button_activated': True,
                'text_red': text_red,
            }

            json_data = json.dumps(data_to_send) # Convert the dictionary to a JSON string
            print(json_data)

            await websocket.send_text(json_data) # Send formatted remaining time to the frontend
            await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosed:
        # WebSocket 연결이 닫힌 경우
        websocket_connections.remove(websocket)

@router.websocket('/writing')
async def timer(websocket: WebSocket):
    await websocket.accept()
    ampm = await websocket.receive_text()
    h = await websocket.receive_text()
    m = await websocket.receive_text()
    for_hours = await websocket.receive_text()
    time_str = utils.date_time.ampm_to_str([ampm,h,m])
    print(time_str)

    target_hour = int(time_str[:2])
    target_minute = int(time_str[2:])
    current_time = utils.date_time.kr_now()
    target_time = current_time.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    text_red = False

    # 글쓰기 시간일 때
    while utils.date_time.check_time_range_kr(time_str,int(for_hours)):
        current_time = utils.date_time.kr_now()

        end_time = target_time + datetime.timedelta(hours=int(for_hours))

        remaining_time = end_time - current_time
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}" # Format remaining time as hh:mm:ss

        if remaining_time.total_seconds() <= 600:  # 10 minutes = 600 seconds
            text_red = True

        data_to_send = {
            'remaining_time': remaining_time_str,
            'text_red': text_red
        }

        json_data = json.dumps(data_to_send) # Convert the dictionary to a JSON string
        print(json_data)

        await websocket.send_text(json_data) # Send formatted remaining time to the frontend
        await asyncio.sleep(1)
