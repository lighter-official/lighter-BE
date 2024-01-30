import datetime
import pytz
from datetime import datetime, timedelta
from datetime import datetime, timedelta, time

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

