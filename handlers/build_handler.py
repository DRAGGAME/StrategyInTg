from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery
from pyexpat.errors import messages

from database.db import PostgresBase
from function.update_resources import update_res
from kb.kb_menu import KbMenu, InlineChoiceBuild

build_router = Router()
build_kb_menu = KbMenu()
sqlbase_build = PostgresBase()

@build_router.callback_query(InlineChoiceBuild.filter(F.construction=='gold_mine'))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    await sqlbase_build.connect()
    user_id = callback.message.chat.id
    decision, first_count_gold_mines = await update_res(sqlbase_build, 'gold_mines', user_id)
    try:
        kb = await build_kb_menu.inline_regime_build()

        if decision == 'village_error':
            await callback.message.edit_text(f'Не хватает жителей для обеспечения работы здания. \nОбщее количество: {first_count_gold_mines}'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(f'Не хватает камня для строительства здания. \nОбщее количество: {first_count_gold_mines}'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            await callback.message.edit_text(f'Не хватает золота для строительства здания. \nОбщее количество: {first_count_gold_mines}'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        else:
            await callback.message.edit_text(f'Вы построили золотую шахту. \nОбщее количество: {first_count_gold_mines}'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
    except TelegramBadRequest:
        pass

    await sqlbase_build.connect_close()

    await callback.answer()

@build_router.callback_query(InlineChoiceBuild.filter(F.construction=='stone_mine'))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    await sqlbase_build.connect()
    user_id = callback.message.chat.id
    decision, first_count_stone_mines = await update_res(sqlbase_build, "stone_mines", user_id)
    try:
        kb = await build_kb_menu.inline_regime_build()

        if decision == 'village_error':
            await callback.message.edit_text(
                f'Не хватает жителей для обеспечения работы здания. \nОбщее количество: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(
                f'Не хватает камня для строительства здания. \nОбщее количество: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            await callback.message.edit_text(
                f'Не хватает золота для строительства здания. \nОбщее количество: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        else:
            await callback.message.edit_text(
                f'Вы построили каменную шахту. \nОбщее количество: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
    except TelegramBadRequest:
        pass

    await sqlbase_build.connect_close()

    await callback.answer()

@build_router.callback_query(InlineChoiceBuild.filter(F.construction=='ranch'))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    await sqlbase_build.connect()
    user_id = callback.message.chat.id
    decision, first_count_stone_mines = await update_res(sqlbase_build, 'stone_mines', user_id)
    try:
        kb = await build_kb_menu.inline_regime_build()

        if decision == 'village_error':
            await callback.message.edit_text(
                f'Не хватает жителей для обеспечения работы здания. \nОбщее количество: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(
                f'Не хватает камня для строительства здания. \nОбщее количество: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            await callback.message.edit_text(
                f'Не хватает золота для строительства здания. \nОбщее количество: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        else:
            await callback.message.edit_text(
                f'Вы построили каменную шахту. \nОбщее количество: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
    except TelegramBadRequest:
        pass

    await sqlbase_build.connect_close()

    await callback.answer()


@build_router.callback_query(InlineChoiceBuild.filter(F.construction=='home'))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    kb = await build_kb_menu.inline_regime_build()

    await callback.message.edit_text(f'Вы построили дом.\n\nВыберите, что вы хотите построить', reply_markup=kb)
    await callback.answer()