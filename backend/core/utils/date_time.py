import datetime
import pytz
from fastapi import HTTPException
from backend.core import utils

korea_timezone = pytz.timezone('Asia/Seoul')
days_en = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
days_kr = ['월','화','수','목','금','토','일']

def datetime_to_str(dt: datetime) -> str:
    korea_now = dt.replace(tzinfo=pytz.utc).astimezone(korea_timezone) # UTC 시간을 한국 시간으로 변환
    formatted_date = korea_now.strftime('%Y.%m.%d') # yyyymmdd 형식의 문자열로 변환
    return formatted_date

def datetime_to_list(dt: datetime) -> list:
    dt_kr = dt.replace(tzinfo=pytz.utc).astimezone(korea_timezone) # UTC 시간을 한국 시간으로 변환
    idx = days_en.index(dt_kr.strftime('%a'))
    return [dt_kr.year, dt_kr.month, dt_kr.day, days_kr[idx]]

def datetime_to_str_split(dt: datetime, split: str|None=None) -> str:
    if not split:
        split = '.'
    korea_now = dt.replace(tzinfo=pytz.utc).astimezone(korea_timezone) # UTC 시간을 한국 시간으로 변환
    formatted_date = korea_now.strftime(f'%Y{split}%m{split}%d') # yyyymmdd 형식의 문자열로 변환
    return formatted_date

def datetime_to_str_kr(dt: datetime) -> str:
    korea_now = dt.replace(tzinfo=pytz.utc).astimezone(korea_timezone) # UTC 시간을 한국 시간으로 변환
    formatted_date = korea_now.strftime(f'%Y년 %m월 %d일') # yyyymmdd 형식의 문자열로 변환
    return formatted_date

def check_time_range(start_time_str: str, duration_hours: int) -> bool:
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time()
    # 입력된 문자열 형태의 시간을 datetime 객체로 변환
    start_time = datetime.datetime.strptime(start_time_str, "%H%M").time()

    # 종료 시간 계산
    end_time = (datetime.datetime.combine(datetime.datetime.today(), start_time) +
                datetime.timedelta(hours=duration_hours)).time()

    # 현재 시간이 범위 내에 있는지 확인
    return start_time <= current_time <= end_time

def check_time_range_kr(start_time_str: str, duration_hours: int) -> bool:
    current_datetime = utils.date_time.kr_now()
    print(current_datetime)
    current_time = current_datetime.time()
    # 입력된 문자열 형태의 시간을 datetime 객체로 변환
    start_time = datetime.datetime.strptime(start_time_str, "%H%M").time()
    print(datetime.datetime.today())
    print(utils.date_time.kr_now().date())
    print(datetime.datetime.combine(datetime.datetime.today(), start_time))
    # 종료 시간 계산
    end_time = (datetime.datetime.combine(datetime.datetime.today(), start_time) +
                datetime.timedelta(hours=duration_hours)).time()
    print(f'end_time={end_time}')

    # 현재 시간이 범위 내에 있는지 확인
    return start_time <= current_time <= end_time

def ampm_to_str(time: list) -> str:
    ampm,hour,minute = str(time[0]),int(time[1]),int(time[2])

    if hour == 12: # 오후 12시를 낮 12시로
        if ampm == 'AM':
            ampm = 'PM'
        else:
            ampm = 'AM'

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
    hour,minute = time[:2],time[2:]
    return [hour,minute]

def get_now():
    return datetime.datetime.now(tz=datetime.timezone.utc)

def kr_now():
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=pytz.utc).astimezone(korea_timezone)

def different_date(dt1: datetime, dt2: datetime) -> str:
    a = dt1.date()
    b = dt2.date()
    days_remaining = (b - a).days
    if days_remaining == 0:
        return f'D-DAY'
    else:
        return f'D-{days_remaining}'

if __name__ == '__main__':
    different_date(datetime(2024, 2, 5))
    # print(str_to_12hours('1730'))
    # print(ampm_to_str(['PM',11,5]))