import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.schedulers import SchedulerAlreadyRunningError
from apscheduler.triggers.interval import IntervalTrigger

from database.db import PostgresBase
from kb.fabirc_kb import KeyboardFactory
from shedulers.manns_update.scheduler_object import man_scheduler
from shedulers.manns_update.update_mans import update_man
from shedulers.update_resources.item_update import item_update

from shedulers.update_resources.scheduler_object import item_schedulers


router_create = Router()
kb_create_village = KeyboardFactory()
sql_for_create_village = PostgresBase()


class CreateAccount(StatesGroup):
    """Класс для создания аккаунта"""
    account_name = State()
    name_villages = State()


@router_create.message(Command(commands=['start', 'Start']))
async def create_account(message: Message, state: FSMContext):
    """Начало создания аккаунта"""

    await sql_for_create_village.connect() # Проверка на существования аккаунта
    user_id: int = message.from_user.id
    check = await sql_for_create_village.execute_query('''SELECT id FROM user_and_villagers_data WHERE user_id = $1''',
                                               (str(user_id), ))
    if check:
        await sql_for_create_village.connect_close()
        await message.reply('У вас уже имеется учётная запись')
        return

    user_name: str = message.from_user.username

    account_kb = await kb_create_village.builder_text((user_name, ), # Кнопка с именем пользователя
                                                      input_field='Введите название аккаунта')

    await state.set_state(CreateAccount.account_name)

    await message.answer('Давайте создадим игровой аккаунт!\n' 
                         'Введите имя аккаунта или выберите готовое: ',
                         reply_markup=account_kb) # Предлагаем пользователю использовать для названия аккаунта, своё имя

@router_create.message(CreateAccount.account_name, F.text.lower().contains('да'))
async def confirmation_account_name(message: Message, state: FSMContext):
    """При подтверждении имени аккаунта"""
    data_account_name = await state.get_value('account_name')

    await state.set_state(CreateAccount.name_villages)

    await message.answer(f'Выбор подтверждён, имя аккаунта: {data_account_name}\nВведите имя деревни',
                         reply_markup=ReplyKeyboardRemove())

@router_create.message(CreateAccount.account_name, F.text.lower().contains('нет'))
async def confirmation_account_name(message: Message, state: FSMContext):
    """Если имя аккаунта не подтвердили"""
    user_name: str = message.from_user.username

    account_kb = await kb_create_village.builder_text((user_name, ),
                                                input_field='Введите название аккаунта') # Кнопка с именем пользователя

    await message.answer(f'Вас не устроило имя вашего аккаунта?\n'
                         f'Введите имя нового вашего аккаунта:', reply_markup=account_kb)

@router_create.message(CreateAccount.account_name)
async def add_account_name(message: Message, state: FSMContext):
    """Сообщение о том, что надо подтвердить имя аккаунта"""
    choice_name = await kb_create_village.builder_reply_choice('Подтвердите имя аккаунта')
    await state.update_data(account_name=message.text)
    await message.answer(f'Подтвердите имя вашего аккаунта\nТекущее имя: {message.text}', reply_markup=choice_name)

@router_create.message(CreateAccount.name_villages, F.text.lower().contains('да'))
async def confirmation_account_name(message: Message, state: FSMContext):
    """Окончательное подтверждение данных о вводе имени деревни и вставка данных в БД"""
    data_account_name = await state.get_value('account_name')
    data_village_name = await state.get_value('village_name')

    user_id = message.chat.id

    await sql_for_create_village.insert_default(user_id, data_account_name, data_village_name)

    try:
        item_schedulers.add_job(func=item_update,
                                       trigger=IntervalTrigger(seconds=20),
                                       args=(int(user_id), ),
                                       id=f'farm{user_id}')
        man_scheduler.add_job(func=update_man, trigger=IntervalTrigger(seconds=20),
                              args=(int(user_id)), id=f'farm_man{user_id}')

    except ConflictingIdError:
        item_schedulers.remove_job(job_id=f'farm{user_id}')
        item_schedulers.add_job(func=item_update,
                                       trigger=IntervalTrigger(seconds=20),
                                       args=(int(user_id), ),
                                       id=f'farm{user_id}')
        man_scheduler.add_job(func=update_man, trigger=IntervalTrigger(seconds=20),
                              args=(int(user_id)), id=f'farm_man{user_id}')
    try:
        item_schedulers.start()

    except SchedulerAlreadyRunningError:
        logging.warn(f'Уже всё запущено')

    inli = await kb_create_village.builder_inline_choice_category()
    await state.clear()
    await sql_for_create_village.connect_close()
    await message.answer(f'Выбор подтверждён, аккаунт создан\n'
                         f'Имя аккаунта: {data_account_name}\n'
                         f'Имя деревни: {data_village_name}\n\n'
                         f'Выберите, куда вы хотите зайти:',
                         reply_markup=inli)

@router_create.message(CreateAccount.name_villages, F.text.lower().contains('нет'))
async def confirmation_account_name(message: Message):
    """Если имя деревни не подтвердилось"""

    await message.answer(f'Вас не устроило имя вашей деревни?\n'
                         f'Введите новое имя вашей деревни:')

@router_create.message(CreateAccount.name_villages)
async def add_village_name(message: Message, state: FSMContext):
    """Сообщение о том, что надо подтвердить имя деревни"""
    choice_name = await kb_create_village.builder_reply_choice('Подтвердите имя деревни')

    await state.update_data(village_name=message.text)

    await message.answer(f'Подтвердите имя вашей деревни\nТекущее имя: {message.text}', reply_markup=choice_name)



