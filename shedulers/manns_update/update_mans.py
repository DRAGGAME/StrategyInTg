from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.schedulers import SchedulerAlreadyRunningError

from config import bot
from database.db import PostgresBase
from function.random_time import random_time
from shedulers.manns_update.scheduler_object import man_scheduler
from shedulers.manns_update.update_sql import quantity_update


async def update_man(user_id: int):

    sqlbase_man = PostgresBase()

    await sqlbase_man.connect()
    count = 0
    user_data = await sqlbase_man.execute_query("""SELECT villagers, villagers_busy, count_new_villagers, level FROM user_and_villagers_data WHERE user_id = $1""",
                                    (str(user_id), ))
    print(user_data)
    try:
        all_villagers = user_data[0][0] + user_data[0][1] + user_data[0][2]
    except IndexError:
        man_scheduler.remove_job(job_id=f'farm_man{user_id}')
        return
    level = int(user_data[0][-1])

    count_for_level = await sqlbase_man.execute_query("""SELECT count(*) FROM table_limits;""")

    if level < 10:
        level = 1
    else:
        level = min((level // 10) * 10, count_for_level[0][0] * 10)

    limit_villages = await sqlbase_man.execute_query("""SELECT villagers FROM table_limits WHERE level = $1""",
                                    (level, ))

    if limit_villages:
        pass
    else:
        return

    first_no_villagers = limit_villages[0][0] - all_villagers
    for number_scheduler in range(6):
        truth_check = man_scheduler.get_job(job_id=f'{user_id}_{number_scheduler+1}')
        if truth_check:
            count += 1

    if count >= 6:
        pass

    if first_no_villagers == 0:
        pass

    elif first_no_villagers <= 6 and count == 0:
        for number_scheduler in range(first_no_villagers):
            time_start = await random_time()
            try:
                print(f'Запуск по дате {time_start}')
                man_scheduler.add_job(quantity_update, 'date', run_date=time_start, args=[user_id, bot], id=f'{user_id}_{number_scheduler+1}')

            except ConflictingIdError:
                pass

            try:
                man_scheduler.start()

            except SchedulerAlreadyRunningError:
                pass

    elif first_no_villagers > 6 and count == 0:

        delta_villagers = first_no_villagers - 6
        first_no_villagers -= delta_villagers

        for number_scheduler in range(first_no_villagers):
            time_start = await random_time()
            try:
                man_scheduler.add_job(quantity_update, 'date', run_date=time_start, args=[user_id, bot], id=f'{user_id}_{number_scheduler+1}')
                print('запуск')
            except ConflictingIdError:
                pass

            try:
                man_scheduler.start()

            except SchedulerAlreadyRunningError:
                pass
    await sqlbase_man.connect_close()