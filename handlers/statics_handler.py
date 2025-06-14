from email.utils import unquote

from aiogram import Router, F
from aiogram.types import CallbackQuery
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.schedulers import SchedulerAlreadyRunningError

from database.db import PostgresBase
from kb.static_kb import InlineStaticKeyboard, StaticKeyboard
from shedulers.info_for_statics.scheduler_object import update_scheduler
from shedulers.info_for_statics.update_message_resources import update_message
from apscheduler.triggers.interval import IntervalTrigger

router_of_static = Router()
static_pg = PostgresBase()

@router_of_static.callback_query(InlineStaticKeyboard.filter(F.static_info=='resource_info'))
async def resource_info(callback: CallbackQuery):
    await static_pg.connect()
    kb_static = StaticKeyboard()

    info_resources = await static_pg.select_resource(callback.message.chat.id)
    level_info = info_resources[0][0]
    gold_info = info_resources[0][1]
    stone_info = info_resources[0][2]
    food_info = info_resources[0][3]
    villagers_info = info_resources[0][4]
    villagers_busy_info = info_resources[0][5]

    all_villagers_info = villagers_info+villagers_busy_info
    kb = await kb_static.cancel_keyboard()
    try:
        update_scheduler.add_job(func=update_message, trigger=IntervalTrigger(seconds=20), args=[callback.message.chat.id,
                                                                                                 info_resources[0][-1],
                                                                                                 static_pg, kb_static],
                                                                                                id=f"upd_msg{callback.message.chat.id}")
    except ConflictingIdError:
        update_scheduler.remove_job(id=f"upd_msg{callback.message.chat.id}")
    try:
        update_scheduler.start()

    except SchedulerAlreadyRunningError:
        pass

    await callback.message.edit_text(f'Ваш уровень: {level_info}\n'
                                            f'Золото: {gold_info}\n'
                                            f'Камень: {stone_info}\n'
                                            f'Еда: {food_info}\n'
                                            f'Свободные жители: {villagers_info}\n'
                                            f'Занятые жители: {villagers_busy_info}\n'
                                            f'Все жители: {all_villagers_info}\nВыберите, что вы хотите построить', reply_markup=kb)
    await static_pg.connect_close()

    await callback.answer()