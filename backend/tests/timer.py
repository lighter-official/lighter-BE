import datetime

if __name__ == '__main__':
    h = '1'
    m = '0'
    for_hours = 1

    cur = datetime.datetime.now()
    start = cur.replace(hour=int(h), minute=int(m), second=0, microsecond=0)
    end = start + datetime.timedelta(hours=int(for_hours))

    # 1.
    # remaining_time = start - cur
    # remaining_time += datetime.timedelta(days=3)
    # hours, remainder = divmod(remaining_time.seconds, 3600)
    # minutes, seconds = divmod(remainder, 60)
    #
    # remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    # print(remaining_time_str)

    # 2.
    remaining_time = end - cur
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    print(remaining_time_str)

    # 3.
    next_start = start + datetime.timedelta(days=1)
    remaining_time = next_start - cur
    hours, remainder = divmod(remaining_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    remaining_time_str = f"{hours:02}:{minutes:02}:{seconds:02}"