import asyncio
import logging

from database.db import PostgresBase
from shedulers.item_update import item_update

from shedulers.scheduler_object import item_schedulers
from aiogram import Dispatcher
from apscheduler.triggers.interval import IntervalTrigger

from config import bot
from handlers import create_village

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] #%(levelname)-4s %(filename)s:'
                    '%(lineno)d - %(name)s - %(message)s'
                    )

dp = Dispatcher()
dp.include_router(create_village.router_create)

async def main():
    try:
        sqlbase_run = PostgresBase()
        await sqlbase_run.connect()
        user_ids = await sqlbase_run.execute_query('''SELECT user_id FROM user_and_villagers_data''')
        if user_ids:
            for user_id in user_ids:
                item_schedulers.add_job(func=item_update,
                                        trigger=IntervalTrigger(seconds=20),
                                        args=(int(user_id[0]), ),
                                        id=f'farm{user_id[0]}')
            item_schedulers.start()
        await sqlbase_run.connect_close()

        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Бот не запустился\nОшибка: {e}")

    finally:
        item_schedulers.shutdown(wait=False)

if __name__ == '__main__':
    asyncio.run(main())