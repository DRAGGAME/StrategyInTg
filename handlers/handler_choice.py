from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.db import PostgresBase
from kb.fabirc_kb import InlineChoiceGame, InlineChoiceMenu
from kb.kb_for_add_man import KbFactoryAddMan
from kb.kb_menu import KbMenu, InlineChoiceBuild
from shedulers.update_resources.scheduler_object import item_schedulers

sqlbase_choice = PostgresBase()
router_choice = Router()
kb_menus = KbMenu()
kb_add = KbFactoryAddMan()

@router_choice.callback_query(InlineChoiceGame.filter(F.category_id=='del'))
async def delete_for_acc(callback: CallbackQuery):
    user_id = callback.message.chat.id
    await sqlbase_choice.connect()
    await sqlbase_choice.execute_query("""DELETE FROM user_and_villagers_data WHERE user_id = $1""", (str(user_id), ))
    item_schedulers.remove_job(job_id=f'farm{user_id}')
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

@router_choice.callback_query(InlineChoiceBuild.filter(F.construction=='cancel'))
@router_choice.callback_query(InlineChoiceGame.filter(F.category_id=='run_in_game'))
async def press_run_in_game(callback: CallbackQuery):
    kb = await kb_menus.builder_inline_choice_menu(True)
    await callback.message.edit_text('Выберите, что вы хотите сделать', reply_markup=kb)
    await callback.answer()

@router_choice.callback_query(InlineChoiceMenu.filter(F.regime=='build'))
async def regime_build(callback: CallbackQuery):
    kb = await kb_menus.inline_regime_build()
    await callback.message.edit_text('Выберите, что вы хотите построить', reply_markup=kb)
    await callback.answer()

@router_choice.callback_query(InlineChoiceMenu.filter(F.regime=='add_man'))
async def regime_add_man(callback: CallbackQuery):
    kb = await kb_add.add_man_inline_kb()
    user_id = callback.message.chat.id
    await sqlbase_choice.connect()

    user_data = await sqlbase_choice.execute_query("""SELECT villagers, count_new_villagers FROM user_and_villagers_data WHERE user_id = $1""",
                                    (str(user_id), ))



    await callback.message.edit_text(f'К вам в поселение хотят присоединится\n'
                                     f'Количество ваших людей: {user_data[0][0]}\n'
                                     f'Количество людей в очереди: {user_data[0][1]}\n'
                                     f'Вы можете выбрать человека ', reply_markup=kb)

    await callback.answer('Выберите, что вы хотите сделать с этими людьми')