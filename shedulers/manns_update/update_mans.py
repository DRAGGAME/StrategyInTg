from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.schedulers import SchedulerAlreadyRunningError

from config import bot
from database.db import PostgresBase
from function.random_time import random_time
from shedulers.manns_update.scheduler_object import man_scheduler
from shedulers.manns_update.update_sql import quantity_update

sqlbase_man = PostgresBase()

async def update_man(user_id: int):

    await sqlbase_man.connect()

    user_data = await sqlbase_man.execute_query("""SELECT villagers, villagers_busy, level FROM user_and_villagers_data WHERE user_id = $1""",
                                    (str(user_id), ))

    all_villagers = user_data[0][0] + user_data[0][1]
    level = user_data[0][-1]

    limit_villages = await sqlbase_man.execute_query("""SELECT villages FROM table_limits WHERE level = $1""",
                                    (level, ))

    first_no_villagers = limit_villages[0][0] - all_villagers

    if first_no_villagers == 0:
        pass

    elif first_no_villagers > 6:

        delta_villagers = first_no_villagers - 6
        first_no_villagers -= delta_villagers

        for number_scheduler in range(6):
            time_start = await random_time()
            try:
                man_scheduler.add_job(quantity_update, 'date', run_date=time_start, args=[user_id, bot], id=f'{user_id}_{number_scheduler+1}')
            except ConflictingIdError:
                pass

            try:

                man_scheduler.start()

            except SchedulerAlreadyRunningError:
                pass

    await sqlbase_man.connect_close()