from email.utils import unquote

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.schedulers import SchedulerAlreadyRunningError

from database.db import PostgresBase
from handlers.handler_choice import kb_static
from kb.static_kb import InlineStaticKeyboard, StaticKeyboard, InlineRegimeInfo
from shedulers.info_for_statics.scheduler_object import update_scheduler
from shedulers.info_for_statics.update_message_resources import update_message
from apscheduler.triggers.interval import IntervalTrigger

router_of_static = Router()
static_pg = PostgresBase()
place_for_number = {

    0: ("gold_mines", "золотым шахтам", ),

    1: ("stone_mines", "каменным шахтам", ),

    2: ("ranches", "фермам", ),

    3: ("homes", "домам", )
}

@router_of_static.callback_query(InlineStaticKeyboard.filter(F.static_info=='resource_info'))
async def resource_info(callback: CallbackQuery):
    await static_pg.connect()
    kb_static = StaticKeyboard()

    info_resources = await static_pg.select_resource(callback.message.chat.id)
    level_info = info_resources[0][0]
    stone_info = info_resources[0][1]
    gold_info = info_resources[0][2]
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

@router_of_static.callback_query(InlineStaticKeyboard.filter(F.static_info=='buildings_info'))
async def buildings_info(callback: CallbackQuery, state: FSMContext):
    kb_static = StaticKeyboard()
    await static_pg.connect()
    count = 0
    await state.update_data(count=count)
    dict_data = place_for_number.get(count)
    builders = await static_pg.select_builders(callback.message.chat.id, dict_data[0])
    kb = await kb_static.static_keyboard_two()
    await static_pg.connect_close()
    await callback.message.edit_text(f'<b>Вся информация по {dict_data[1]}:</b>\n\nЗданий первого уровня: {builders[0]}\n'
                                     f'Зданий второго уровня: {builders[1]}\n'
                                     f'Зданий третьего уровня: {builders[2]}\n'
                                     f'Зданий четвёртого уровня: {builders[3]}\n'
                                     f'Зданий пятого уровня: {builders[4]}\n'
                                     f'Всего зданий данного типа: {builders[5]}'
                                     , reply_markup=kb, parse_mode=ParseMode.HTML)

@router_of_static.callback_query(InlineRegimeInfo.filter(F.regime_state=="back"))
@router_of_static.callback_query(InlineRegimeInfo.filter(F.regime_state=="next"))
async def buildings_update(callback: CallbackQuery, state: FSMContext, callback_data: InlineRegimeInfo):
    dict_data = None
    await static_pg.connect()
    count = await state.get_value('count')

    if count is None:
        count = 0
        dict_data = place_for_number.get(count)

        await state.update_data(count=count)

    elif callback_data.regime_state=="back":
        if count-1 < 0:
            await callback.answer('Это начало...')
            return

        count -= 1
        dict_data = place_for_number.get(count)
        await state.update_data(count=count)

    elif callback_data.regime_state=="next":
        if count+1 > 3:
            await callback.answer("Это конец...")
            return

        count += 1
        dict_data = place_for_number.get(count)
        await state.update_data(count=count)

    builders = await static_pg.select_builders(callback.message.chat.id, dict_data[0])
    kb = await kb_static.static_keyboard_two()
    try:
        dict_data = place_for_number.get(count)
        await callback.message.edit_text(f'<b>Вся информация по {dict_data[1]}:</b>\n\nЗданий первого уровня: {builders[0]}\n'
                                         f'Зданий второго уровня: {builders[1]}\n'
                                         f'Зданий третьего уровня: {builders[2]}\n'
                                         f'Зданий четвёртого уровня: {builders[3]}\n'
                                         f'Зданий пятого уровня: {builders[4]}\n'
                                         f'Всего зданий данного типа: {builders[5]}'
                                         , reply_markup=kb, parse_mode=ParseMode.HTML)
    except TelegramBadRequest:
        pass
    await callback.answer()

