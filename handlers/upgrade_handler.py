from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db import PostgresBase
from function.update_resources import update_res
from kb.fabirc_kb import InlineChoiceUpgrade
from kb.kb_menu import KbMenu, InlineChoiceBuild
from kb.upgrade_kb import UpgradeKb, InlineUpgradeKb

upgrade_router = Router()
keyboards = UpgradeKb()
build_kb_menu = KbMenu()
sqlbase_upgrade = PostgresBase()

@upgrade_router.callback_query(InlineChoiceUpgrade.filter(F.construction))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild, state: FSMContext):
    await state.update_data(construction=callback_data.construction)
    kb = await keyboards.upgrade_keyboard()
    await callback.message.edit_text('Какого левела вы хотите улучшить здание?', reply_markup=kb)
    await callback.answer()

@upgrade_router.callback_query(InlineUpgradeKb.filter(F.level.in_([1, 2, 3, 4])))
async def upgrade_builder(callback: CallbackQuery, callback_data: InlineChoiceUpgrade, state: FSMContext):
    await sqlbase_upgrade.connect()
    phrase = ''
    type_build = await state.get_value('construction')

    tier = callback_data.level
    decision, first_count, item_info = await update_res(sqlbase_upgrade, type_build, tier+1, callback.message.chat.id)
    await sqlbase_upgrade.connect_close()
    try:
        kb = await build_kb_menu.inline_regime_build(True, InlineChoiceUpgrade)

        if decision == 'about_count_error':
            await callback.message.edit_text(
                f'Зданий этого <b>уровня</b> слишком много! Повысьте уровень для возможности увелечения их количества.\nОбщее количество построек: {first_count}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb, parse_mode=ParseMode.HTML)
            return

        elif decision == 'about_last_count_error':
            await callback.message.edit_text(
                f'Нечего улучшать! Постройте или улучшите здание, чтобы улучшить до этого уровня\nОбщее количество построек: {first_count}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'count_error':
            await callback.message.edit_text(
                f'Зданий этого <b>типа</b> слишком много! Повысьте уровень для возможности увелечения их количества.\nОбщее количество построек: {first_count}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb, parse_mode=ParseMode.HTML)
            return

        elif decision == 'village_error':
            await callback.message.edit_text(
                f'Не хватает жителей для обеспечения работы здания. \nОбщее количество построек: {first_count}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(
                f'Не хватает камня для строительства здания. \nОбщее количество построек: {first_count}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            await callback.message.edit_text(
                f'Не хватает золота для строительства здания. \nОбщее количество построек: {first_count}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'food_error':

            await callback.message.edit_text(
                f'Не хватает еды для строительства здания. \nОбщее количество построек : {first_count}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        else:
            if type_build=='gold_mines':
                phrase = 'золотую шахту'
            elif type_build=='stone_mines':
                phrase = 'каменную шахту'
            elif type_build=='ranches':
                phrase = 'ферму'
            elif type_build=='homes':
                phrase = 'дом'

            await callback.message.edit_text(
                f'Вы построили улучшенную {phrase}. \nОбщее количество построек: {first_count}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)

    except TelegramBadRequest:
        pass

    await callback.answer()
