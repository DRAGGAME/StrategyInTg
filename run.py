import asyncio
import logging

from database.create_table_for_user_data import TableForVillage
from database.db import PostgresBase
from database.insert_limit import BuildLimit
from database.limit_on_resources_for_construction import ResourcesForConstruct
from handlers.handler_add_man import router_add_man
from shedulers.manns_update.scheduler_object import man_scheduler
from shedulers.manns_update.update_mans import update_man
from shedulers.update_resources.item_update import item_update

from shedulers.update_resources.scheduler_object import item_schedulers
from aiogram import Dispatcher
from apscheduler.triggers.interval import IntervalTrigger

from config import bot
from handlers import create_village, handler_choice, build_handler

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
                    '%(lineno)d - %(name)s - %(message)s'
                    )

dp = Dispatcher()
dp.include_routers(create_village.router_create, handler_choice.router_choice, build_handler.build_router, router_add_man)

async def main():
    """
    1) Creating tables in the DB
    2) Launching schedulers
    3) Start bot
    :return:
    """
    try:
        db_village = TableForVillage()
        await db_village.connect()

        await db_village.crate_group_table_data()
        await db_village.create_table_limits()
        await db_village.create_table_limit_const()

        await db_village.connect_close()

        db_limits = BuildLimit()

        await db_limits.connect()
        count = await db_limits.execute_query('''SELECT id FROM table_limits''')

        len_count = len(count)

        if len_count == 1:
            await db_limits.insert_limit_level_ten()
            await db_limits.insert_limit_level_twenty()
            await db_limits.insert_limit_level_thirty()
        elif len_count == 2:
            await db_limits.insert_limit_level_twenty()
            await db_limits.insert_limit_level_thirty()

        elif count == 3:
            await db_limits.insert_limit_level_thirty()
        else:
            await db_limits.insert_limit_level_one()
            await db_limits.insert_limit_level_ten()
            await db_limits.insert_limit_level_twenty()
            await db_limits.insert_limit_level_thirty()

        await db_limits.connect_close()


        res_db = ResourcesForConstruct()

        await res_db.connect()
        await res_db.limit_resources_for_construct()

        user_ids = await res_db.execute_query('''SELECT user_id FROM user_and_villagers_data''')

        if user_ids:
            for user_id in user_ids:
                item_schedulers.add_job(func=item_update,
                                        trigger=IntervalTrigger(seconds=20),
                                        args=(int(user_id[0]), ),
                                        id=f'farm{user_id[0]}')
                man_scheduler.add_job(func=update_man, trigger=IntervalTrigger(seconds=20),
                                      args=(int(user_id[0]), ), id=f'farm_man{user_id[0]}')

            man_scheduler.start()
            item_schedulers.start()

        await res_db.connect_close()

        await dp.start_polling(bot)

    finally:
        item_schedulers.shutdown(wait=False)
        man_scheduler.shutdown(wait=False)

if __name__ == '__main__':
    asyncio.run(main())