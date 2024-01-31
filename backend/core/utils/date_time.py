import datetime
import pytz
from datetime import datetime, timedelta
from datetime import datetime, timedelta, time
import datetime

korea_timezone = pytz.timezone('Asia/Seoul')

def datetime_to_str(dt: datetime) -> str:
    korea_now = dt.replace(tzinfo=pytz.utc).astimezone(korea_timezone) # UTC 시간을 한국 시간으로 변환
    formatted_date = korea_now.strftime('%Y.%m.%d') # yyyymmdd 형식의 문자열로 변환

    return formatted_date

def check_time_range(start_time_str, duration_hours):
    current_datetime = datetime.now()
    current_time = current_datetime.time()
    # 입력된 문자열 형태의 시간을 datetime 객체로 변환
    start_time = datetime.strptime(start_time_str, "%H%M").time()

    # 종료 시간 계산
    end_time = (datetime.combine(datetime.today(), start_time) +
                timedelta(hours=duration_hours)).time()

    # 현재 시간이 범위 내에 있는지 확인
    return start_time <= current_time <= end_time

def ampm_to_str(time: list) -> str:
    ampm,hour,minute = time

    try:
        if ampm == 'PM':
            hour += 12
        h = str(hour).rjust(2,'0')
        m = str(minute).rjust(2,'0')
        return f'{h}{m}'
    except:
        raise HTTPException(status_code=400, detail='["AM",3,30] format 이 아닙니다.')

def str_to_12hours(time: str) -> list:
    hour,minute = int(time[:2]),int(time[2:])
    ampm = 'AM'

    if hour >= 12:
        ampm = 'PM'
        hour -= 12

    return [ampm,hour,minute]
def str_to_24hours(time: str) -> list:
    hour,minute = int(time[:2]),int(time[2:])
    return [hour,minute]

def now():
    return datetime.datetime.now(tz=datetime.timezone.utc)

if __name__ == '__main__':
    print(str_to_12hours('1730'))
    # print(ampm_to_str(['PM',11,5]))