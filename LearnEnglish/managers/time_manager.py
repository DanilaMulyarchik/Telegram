from datetime import datetime, timedelta


def get_time():
    return datetime.now().time().strftime('%H:%M:%S')


def get_tomorrow_date(days: int):
    return (datetime.now() + timedelta(days=days+1)).strftime('%Y-%m-%d')


def get_date():
    return datetime.now().strftime("%Y-%m-%d")


def get_time_out(start, minutes):
    now = datetime.now()
    start_time = datetime.strptime(start, '%H:%M:%S').time()
    start = datetime.combine(now.date(), start_time)

    end_time = start + timedelta(minutes=minutes)

    time_difference = end_time - now

    total_minutes = int(time_difference.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)

    return minutes


def get_time_difference(start, hour, minutes, seconds):
    now = datetime.now()
    start_time = datetime.strptime(start, '%H:%M:%S').time()
    start = datetime.combine(now.date(), start_time)
    difference = timedelta(hours=hour, minutes=minutes, seconds=seconds)
    if not (start - difference <= now <= start + difference):
        return True
    else:
        return False