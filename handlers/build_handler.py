from xmlrpc.client import FastParser

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from database.db import PostgresBase
from function.update_resources import update_res
from kb.kb_menu import KbMenu, InlineChoiceBuild

build_router = Router()
build_kb_menu = KbMenu()
sqlbase_build = PostgresBase()

@build_router.callback_query(InlineChoiceBuild.filter(F.construction=='gold_mines'))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    await sqlbase_build.connect()
    user_id = callback.message.chat.id
    decision, first_count_gold_mines = await update_res(sqlbase_build, 'gold_mines', 1, user_id)
    await sqlbase_build.connect_close()

    try:
        kb = await build_kb_menu.inline_regime_build(False, InlineChoiceBuild)
        if decision == 'count_error':
            await callback.message.edit_text(
                f'Зданий слишком много! Повысьте уровень для возможности увелечения их количества.\nОбщее количество построек: {first_count_gold_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'village_error':
            await callback.message.edit_text(f'Не хватает жителей для обеспечения работы здания. \nОбщее количество построек: {first_count_gold_mines}'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(f'Не хватает камня для строительства здания. \nОбщее количество построек: {first_count_gold_mines}'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            await callback.message.edit_text(f'Не хватает золота для строительства здания. \nОбщее количество построек: {first_count_gold_mines}'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        else:
            await callback.message.edit_text(f'Вы построили золотую шахту. \nОбщее количество построек: {first_count_gold_mines}'
                                             f'\nВыберите, что вы хотите построить', reply_markup=kb)
    except TelegramBadRequest:
        pass

    await sqlbase_build.connect_close()

    await callback.answer()

@build_router.callback_query(InlineChoiceBuild.filter(F.construction=='stone_mines'))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    await sqlbase_build.connect()
    user_id = callback.message.chat.id
    decision, first_count_stone_mines = await update_res(sqlbase_build, "stone_mines", 1, user_id)
    await sqlbase_build.connect_close()

    try:
        kb = await build_kb_menu.inline_regime_build(False, InlineChoiceBuild)

        if decision == 'count_error':
            await callback.message.edit_text(
                f'Зданий слишком много! Повысьте уровень для возможности увелечения их количества.\nОбщее количество построек: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'village_error':
            await callback.message.edit_text(
                f'Не хватает жителей для обеспечения работы здания. \nОбщее количество построек: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(
                f'Не хватает камня для строительства здания. \nОбщее количество построек: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            await callback.message.edit_text(
                f'Не хватает золота для строительства здания. \nОбщее количество построек: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        else:
            await callback.message.edit_text(
                f'Вы построили каменную шахту. \nОбщее количество построек: {first_count_stone_mines}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
    except TelegramBadRequest:
        pass

    await callback.answer()

@build_router.callback_query(InlineChoiceBuild.filter(F.construction=='ranches'))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    await sqlbase_build.connect()
    user_id = callback.message.chat.id
    decision, first_count_ranch = await update_res(sqlbase_build, 'ranches', 1, user_id)

    await sqlbase_build.connect_close()
    try:
        kb = await build_kb_menu.inline_regime_build(False, InlineChoiceBuild)
        if decision == 'count_error':
            await callback.message.edit_text(
                f'Зданий слишком много! Повысьте уровень для возможности увелечения их количества.\nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'village_error':
            await callback.message.edit_text(
                f'Не хватает жителей для обеспечения работы здания. \nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(
                f'Не хватает камня для строительства здания. \nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            await callback.message.edit_text(
                f'Не хватает золота для строительства здания. \nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'food_error':

            await callback.message.edit_text(
                f'Не хватает еды для строительства здания. \nОбщее количество построек : {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        else:
            await callback.message.edit_text(
                f'Вы построили ферму. \nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)

    except TelegramBadRequest:
        pass

    await callback.answer()

@build_router.callback_query(InlineChoiceBuild.filter(F.construction=='homes'))
async def build_gold_mine(callback: CallbackQuery, callback_data: InlineChoiceBuild):
    await sqlbase_build.connect()
    user_id = callback.message.chat.id
    decision, first_count_ranch = await update_res(sqlbase_build, 'homes', 1, user_id)
    await sqlbase_build.connect_close()

    try:
        kb = await build_kb_menu.inline_regime_build(False, InlineChoiceBuild)
        if decision == 'count_error':
            await callback.message.edit_text(
                f'Зданий слишком много! Повысьте уровень для возможности увелечения их количества.\nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'village_error':
            await callback.message.edit_text(
                f'Не хватает жителей для обеспечения работы здания. \nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'stone_error':
            await callback.message.edit_text(
                f'Не хватает камня для строительства здания. \nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'gold_error':
            await callback.message.edit_text(
                f'Не хватает золота для строительства здания. \nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        elif decision == 'food_error':

            await callback.message.edit_text(
                f'Не хватает еды для строительства здания. \nОбщее количество построек : {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
            return

        else:
            await callback.message.edit_text(
                f'Вы построили дом. \nОбщее количество построек: {first_count_ranch}'
                f'\nВыберите, что вы хотите построить', reply_markup=kb)
    except TelegramBadRequest:
        pass

    await callback.answer()