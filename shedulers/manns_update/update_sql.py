from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from database.db import PostgresBase
from kb.kb_menu import KbMenu
from shedulers.manns_update.scheduler_object import man_scheduler


async def quantity_update(user_id: int, bot: Bot):
    count = 0
    sqlbase_for_quantity = PostgresBase()
    kb_man_update = KbMenu()
    kb = await kb_man_update.builder_inline_choice_menu(True)
    user_id = str(user_id)
    await sqlbase_for_quantity.connect()


    user_data = await sqlbase_for_quantity.execute_query("""SELECT message_id, count_new_villagers FROM user_and_villagers_data WHERE user_id = $1""",
                                    (user_id, ))

    msg_id = user_data[0][0]
    count_new_villagers = user_data[0][1]
    first_count_new_villagers = count_new_villagers + 1


    await sqlbase_for_quantity.execute_query("""UPDATE user_and_villagers_data SET count_new_villagers = $1 WHERE user_id = $2""",
                                             (first_count_new_villagers, user_id))
    for number_scheduler in range(6):
        truth_check = man_scheduler.get_job(job_id=f'{user_id}_{number_scheduler+1}')
        if truth_check:
            count += 1
    if count > 1:
        await bot.edit_message_text(chat_id=user_id, text=f'В ваше поселение пришли люди({count}). Вы можете их принять или выгнать',
                                    message_id=msg_id,
                                    reply_markup=kb)
    else:
        await bot.edit_message_text(chat_id=user_id, text='В ваше поселение пришёл человек. Вы можете его принять или выгнать',
                                    message_id=msg_id,
                                    reply_markup=kb)

    await sqlbase_for_quantity.connect_close()
