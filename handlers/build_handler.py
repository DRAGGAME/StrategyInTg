from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from database.db import PostgresBase
from function.update_resources import update_res
from kb.kb_menu import KbMenu, InlineChoiceBuild

build_router = Router()
build_kb_menu = KbMenu()
sqlbase_build = PostgresBase()

@build_router.callback_query(InlineChoiceBuild.filter(F.construction.in_(['gold_mines', 'stone_mines', 'ranches', 'homes'])))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    await sqlbase_build.connect()
    phrase = ''
    type_build = callback_data.construction
    user_id = callback.message.chat.id
    decision, first_count_gold_mines, item_info = await update_res(sqlbase_build, type_build, 1, user_id)
    await sqlbase_build.connect_close()

    try:
        kb = await build_kb_menu.inline_regime_build(False, InlineChoiceBuild)
        level_info = item_info[0]
        gold_info = item_info[1]
        stone_info = item_info[2]
        food_info = item_info[3]
        villagers_info = item_info[4]
        villagers_busy_info = item_info[5]

        all_villagers_info = item_info[6]

        if decision == 'about_count_error':
            await callback.message.edit_text(
                f'Зданий этого <b>уровня</b> слишком много! Повысьте уровень для возможности увелечения их количества.\nПовысьте уровень для возможности увелечения их количества.\n'
                                            f'Ваш уровень: {level_info}\n'                           
                                             f'Золото: {gold_info}\n'
                                             f'Камень: {stone_info}\n'
                                             f'Еда: {food_info}\n'
                                             f'Свободные жители: {villagers_info}\n'
                                             f'Занятые жители: {villagers_busy_info}\n'
                                             f'Все жители: {all_villagers_info}\n'
                                             f'Количество построек этого типа и уровня: {first_count_gold_mines}\n', reply_markup=kb, parse_mode=ParseMode.HTML)
            return

        elif decision == 'about_last_count_error':
            await callback.message.edit_text(
                f'Нечего улучшать! Постройте или улучшите здание, чтобы улучшить до этого уровня\nПовысьте уровень для возможности увелечения их количества.\n'
                                            f'Ваш уровень: {level_info}\n'                           
                                             f'Золото: {gold_info}\n'
                                             f'Камень: {stone_info}\n'
                                             f'Еда: {food_info}\n'
                                             f'Свободные жители: {villagers_info}\n'
                                             f'Занятые жители: {villagers_busy_info}\n'
                                             f'Все жители: {all_villagers_info}\n'
                                             f'Количество построек этого типа и уровня: {first_count_gold_mines}\n'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'count_error':
            await callback.message.edit_text(
                f'Зданий слишком много! Повысьте уровень для возможности увелечения их количества.\n'
                                            f'Ваш уровень: {level_info}\n'                           
                                             f'Золото: {gold_info}\n'
                                             f'Камень: {stone_info}\n'
                                             f'Еда: {food_info}\n'
                                             f'Свободные жители: {villagers_info}\n'
                                             f'Занятые жители: {villagers_busy_info}\n'
                                             f'Все жители: {all_villagers_info}\n'
                                             f'Количество построек этого типа и уровня: {first_count_gold_mines}\n'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'village_error':
            await callback.message.edit_text(f'Не хватает жителей для обеспечения работы здания.                                             '
                                             f'Ваш уровень: {level_info}\n'
                                             f'Золото: {gold_info}\n'
                                             f'Камень: {stone_info}\n'
                                             f'Еда: {food_info}\n'
                                             f'Свободные жители: {villagers_info}\n'
                                             f'Занятые жители: {villagers_busy_info}\n'
                                             f'Все жители: {all_villagers_info}\n'
                                             f'Количество построек этого типа и уровня: {first_count_gold_mines}\n'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(f'Не хватает камня для строительства здания.\n'
                                             f'Ваш уровень: {level_info}\n'
                                             f'Золото: {gold_info}\n'
                                             f'Камень: {stone_info}\n'
                                             f'Еда: {food_info}\n'
                                             f'Свободные жители: {villagers_info}\n'
                                             f'Занятые жители: {villagers_busy_info}\n'
                                             f'Все жители: {all_villagers_info}\n'
                                             f'Количество построек этого типа и уровня: {first_count_gold_mines}\n'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            level_info = item_info[0]
            gold_info = item_info[1]
            stone_info = item_info[2]
            food_info = item_info[3]
            villagers_info = item_info[4]
            villagers_busy_info = item_info[5]

            all_villagers_info = item_info[6]
            await callback.message.edit_text(f'Не хватает золота для строительства здания.\n                                             '
                                             f'Ваш уровень: {level_info}\n'
                                             f'Золото: {gold_info}\n'
                                             f'Камень: {stone_info}\n'
                                             f'Еда: {food_info}\n'
                                             f'Свободные жители: {villagers_info}\n'
                                             f'Занятые жители: {villagers_busy_info}\n'
                                             f'Все жители: {all_villagers_info}\n'
                                             f'Количество построек этого типа и уровня: {first_count_gold_mines}\n'
                                             f'Выберите, что вы хотите построить', reply_markup=kb)
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

            await callback.message.edit_text(f'Вы построили {phrase}\n'
                                             f'Ваш уровень: {level_info}\n'
                                             f'Золото: {gold_info}\n'
                                             f'Камень: {stone_info}\n'
                                             f'Еда: {food_info}\n'
                                             f'Свободные жители: {villagers_info}\n'
                                             f'Занятые жители: {villagers_busy_info}\n'
                                             f'Все жители: {all_villagers_info}\n'
                                             f'Количество построек этого типа и уровня: {first_count_gold_mines}\n'
                                             f'Выберите, что вы хотите построить',
                                             reply_markup=kb)
    except TelegramBadRequest:
        pass

    await sqlbase_build.connect_close()

    await callback.answer()

