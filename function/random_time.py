import datetime
import pytz
import random

async def random_time(min_increment=30, max_range_hours=15):
    moscow_timezone = pytz.timezone('Europe/Moscow')
    now = datetime.datetime.now(moscow_timezone)

    lower_bound = max(now, now + datetime.timedelta(minutes=min_increment))

    upper_bound = lower_bound + datetime.timedelta(hours=max_range_hours)

    available_minutes = int((upper_bound - lower_bound).total_seconds() / 60)
    random_minute = random.randint(0, available_minutes)

    target_time = lower_bound + datetime.timedelta(minutes=random_minute)

    return target_time.strftime('%Y-%m-%d %H:%M:%S')

