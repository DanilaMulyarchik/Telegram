from datetime import datetime, timedelta


def get_time_out(start, minutes):
    now = datetime.now()
    start_time = datetime.strptime(start, '%H:%M:%S').time()
    start = datetime.combine(now.date(), start_time)

    end_time = start + timedelta(minutes=minutes)

    time_difference = end_time - now

    total_minutes = int(time_difference.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)

    if minutes == 1:
        word_minutes = 'минута'
    elif 2 <= minutes <= 4:
        word_minutes = 'минуты'
    else:
        word_minutes = 'минут'

    return f"{minutes} {word_minutes}"


def get_time():
    return datetime.now().time().strftime('%H:%M:%S')


def get_time_difference(start, hour, minutes, seconds):
    now = datetime.now()
    start_time = datetime.strptime(start, '%H:%M:%S').time()
    start = datetime.combine(now.date(), start_time)
    difference = timedelta(hours=hour, minutes=minutes, seconds=seconds)
    if not (start - difference <= now <= start + difference):
        return True
    else:
        return False