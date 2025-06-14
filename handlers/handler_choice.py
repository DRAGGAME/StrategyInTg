from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import PostgresBase
from handlers.handler_add_man import router_add_man
from kb.fabirc_kb import InlineChoiceGame, InlineChoiceMenu, InlineChoiceUpgrade
from kb.kb_for_add_man import KbFactoryAddMan, InlineAddMan
from kb.kb_menu import KbMenu, InlineChoiceBuild
from kb.static_kb import InlineStaticKeyboard, StaticKeyboard
from kb.upgrade_kb import InlineUpgradeKb
from shedulers.info_for_statics.scheduler_object import update_scheduler
from shedulers.update_resources.scheduler_object import item_schedulers

sqlbase_choice = PostgresBase()
router_choice = Router()
kb_menus = KbMenu()
kb_add = KbFactoryAddMan()
kb_static = StaticKeyboard()

@router_choice.callback_query(InlineChoiceGame.filter(F.category_id=='del'))
async def delete_for_acc(callback: CallbackQuery):
    user_id = callback.message.chat.id
    await sqlbase_choice.connect()
    await sqlbase_choice.execute_query("""DELETE FROM user_and_villagers_data WHERE user_id = $1""", (str(user_id), ))
    item_schedulers.remove_job(job_id=f'farm{user_id}')
    await sqlbase_choice.connect_close()
    await callback.message.edit_text('Учётная запись успешно удалена! Введите /start')

@router_choice.callback_query(InlineChoiceMenu.filter(F.regime=='cancel'))
async def change_regime(callback: CallbackQuery):
    await sqlbase_choice.connect()
    inli = await kb_menus.builder_inline_choice_category()
    user_id = callback.message.chat.id

    data_all = await sqlbase_choice.execute_query('''SELECT first_name, village_name FROM user_and_villagers_data WHERE user_id = $1''',
                                            (str(user_id), ))
    data_account_name = data_all[0][0]
    data_village_name = data_all[0][1]

    await sqlbase_choice.connect_close()
    await callback.message.edit_text(f'Выбор подтверждён, аккаунт создан\n'
                         f'Имя аккаунта: {data_account_name}\n'
                         f'Имя деревни: {data_village_name}\n\n'
                         f'Выберите, куда вы хотите зайти:',
                         reply_markup=inli)

@router_add_man.callback_query(InlineAddMan.filter(F.confirm=='cancel'))
@router_choice.callback_query(InlineChoiceBuild.filter(F.construction=='cancel'))
@router_choice.callback_query(InlineStaticKeyboard.filter(F.static_info=='cancel'))
@router_choice.callback_query(InlineChoiceGame.filter(F.category_id=='run_in_game'))
async def press_run_in_game(callback: CallbackQuery):
    kb = await kb_menus.builder_inline_choice_menu(True)
    job_true = update_scheduler.get_job(job_id=f'upd_msg{callback.message.chat.id}')
    if job_true:
        update_scheduler.remove_job(job_id=f"upd_msg{callback.message.chat.id}")

    await callback.message.edit_text('Выберите, что вы хотите сделать', reply_markup=kb)
    await callback.answer()

@router_choice.callback_query(InlineChoiceMenu.filter(F.regime=='build'))
async def regime_build(callback: CallbackQuery):
    await sqlbase_choice.connect()
    user_id = callback.message.chat.id
    item_info = await sqlbase_choice.select_resource(user_id)

    level_info = item_info[0][0]
    gold_info = item_info[0][1]
    stone_info = item_info[0][2]
    food_info = item_info[0][3]
    villagers_info = item_info[0][4]
    villagers_busy_info = item_info[0][5]

    all_villagers_info = villagers_info+villagers_busy_info

    await sqlbase_choice.connect_close()
    kb = await kb_menus.inline_regime_build(False, InlineChoiceBuild)
    await callback.message.edit_text(f'Ваш уровень: {level_info}\n'
                                            f'Золото: {gold_info}\n'
                                            f'Камень: {stone_info}\n'
                                            f'Еда: {food_info}\n'
                                            f'Свободные жители: {villagers_info}\n'
                                            f'Занятые жители: {villagers_busy_info}\n'
                                            f'Все жители: {all_villagers_info}\nВыберите, что вы хотите построить', reply_markup=kb)
    await callback.answer()

@router_choice.callback_query(InlineUpgradeKb.filter(F.confirm=='cancel' and F.level==0))
@router_choice.callback_query(InlineChoiceMenu.filter(F.regime=='upgrade'))
async def regime_build(callback: CallbackQuery, state: FSMContext):
    kb = await kb_menus.inline_regime_build(True, InlineChoiceUpgrade)
    await state.clear()
    await callback.message.edit_text('Выберите, что вы хотите улучшить', reply_markup=kb)
    await callback.answer()

@router_choice.callback_query(InlineChoiceMenu.filter(F.regime=='stats'))
async def regime_stats(callback: CallbackQuery):
    kb = await kb_static.static_keyboard()
    await callback.message.edit_text('Выберите, какую информацию вы хотите посмотреть', reply_markup=kb)


