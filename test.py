import datetime
from backend.core.utils import date_time

if __name__ == '__main__':
    current_time = date_time.kr_now()
    target_time = current_time.replace(hour=5, minute=30, second=0, microsecond=0)

    if current_time > target_time: # 시간이 지났을 때
        # Target time has already passed, calculate for the next day
        target_time += datetime.timedelta(days=1)

    remaining_time = target_time - current_time
    # remaining_time_str = remaining_time.strftime("%H:%M:%S")

    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)


    # Format remaining time as hh:mm:ss
    # remaining_time_str = str(remaining_time).split(":")
    remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    print(remaining_time_str)