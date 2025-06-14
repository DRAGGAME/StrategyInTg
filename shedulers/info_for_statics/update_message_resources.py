from aiogram.exceptions import TelegramBadRequest

from config import bot
from database.db import PostgresBase
from kb.static_kb import StaticKeyboard
from shedulers.info_for_statics.scheduler_object import update_scheduler


async def update_message(chat_id: int, message_id: int, sqlbase: PostgresBase, kb_static: StaticKeyboard) -> None:
    await sqlbase.connect()
    info_resources = await sqlbase.select_resource(chat_id)
    level_info = info_resources[0][0]
    gold_info = info_resources[0][1]
    stone_info = info_resources[0][2]
    food_info = info_resources[0][3]
    villagers_info = info_resources[0][4]
    villagers_busy_info = info_resources[0][5]

    all_villagers_info = villagers_info+villagers_busy_info
    await sqlbase.connect_close()
    kb = await kb_static.cancel_keyboard()

    try:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id,text=f'Ваш уровень: {level_info}\n'
                                                f'Золото: {gold_info}\n'
                                                f'Камень: {stone_info}\n'
                                                f'Еда: {food_info}\n'
                                                f'Свободные жители: {villagers_info}\n'
                                                f'Занятые жители: {villagers_busy_info}\n'
                                                f'Все жители: {all_villagers_info}\nВыберите, что вы хотите построить',
                               reply_markup=kb)
    except TelegramBadRequest:
        pass
