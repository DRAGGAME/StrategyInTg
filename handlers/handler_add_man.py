from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db import PostgresBase
from kb.fabirc_kb import InlineChoiceMenu

from kb.kb_for_add_man import InlineAddMan, KbFactoryAddMan

router_add_man = Router()
sqlbase_add_man = PostgresBase()
kb_add_man = KbFactoryAddMan()


@router_add_man.callback_query(InlineAddMan.filter(F.confirm.regexp(r".\d")))
async def man_for_minus_two(callback: CallbackQuery, callback_data: InlineAddMan, state: FSMContext):
    kb = await kb_add_man.add_man_inline_kb()

    await sqlbase_add_man.connect()
    user_id = callback.message.chat.id
    user_data = await sqlbase_add_man.execute_query("""SELECT villagers, villagers_busy, count_new_villagers FROM user_and_villagers_data WHERE user_id = $1""",
                                    (str(user_id), ))
    count = await state.get_value('count')

    slices_count = callback_data.confirm
    if count is None:
        count = 0
        await state.update_data(count=0)

    if int(slices_count) < 0:
        if count + int(slices_count) < 0: # Число отрицательное, поэтому +
            await callback.answer('Количество людей будет отрицательное количество')

        else:
            count += int(slices_count)
            await state.update_data(count=count)
            # await sqlbase_add_man.execute_query(""""UPDATE user_and_villagers_data SET villagers = $1 WHERE user_id = $2""", ())
    elif int(slices_count) > 0:
        if count+1 > user_data[0][-1]:
            await callback.answer('Вы не можете добавить больше, чем к вам хотят присоединиться')
        else:
            count += int(slices_count)
            await state.update_data(count=count)
    try:
        await callback.message.edit_text(f'К вам в поселение хотят присоединится\n'
                                         f'Количество ваших людей: {user_data[0][0]+user_data[0][1]}\n'
                                         f'Количество людей в очереди: {user_data[0][-1]}\n'
                                         f'Количество, которое вы хотите принять: {count}\n'
                                         f'Вы можете выбрать количество человек, после подтверждаете, если вам больше людей не надо, нажмите "Отклонить"'
                                         , reply_markup=kb
                                         )
    except TelegramBadRequest:
        pass
    await callback.answer()
    await sqlbase_add_man.connect_close()

@router_add_man.callback_query(InlineAddMan.filter(F.confirm == 'no'))
async def man_confirm(callback: CallbackQuery, state: FSMContext):
    await sqlbase_add_man.connect()

    user_id = callback.message.chat.id
    count_new_villagers = 0

    await sqlbase_add_man.execute_query("""UPDATE user_and_villagers_data SET count_new_villagers = $1
     WHERE user_id = $2 ;""", (count_new_villagers, str(user_id)))

    await state.clear()
    await callback.answer('Вы отказали остальным людям')

@router_add_man.callback_query(InlineAddMan.filter(F.confirm == 'yes'))
async def man_confirm(callback: CallbackQuery, state: FSMContext):
    await sqlbase_add_man.connect()
    kb = await kb_add_man.add_man_inline_kb()

    count = await state.get_value('count')
    if count is False:
        await callback.answer('Вы не выбрали количество людей')
        return
    user_id = callback.message.chat.id
    user_data = await sqlbase_add_man.execute_query("""SELECT villagers, villagers_busy, count_new_villagers FROM user_and_villagers_data WHERE user_id = $1""",
                                    (str(user_id), ))
    villagers = user_data[0][0] + user_data[0][1]
    count_new_villagers = user_data[0][-1]
    count_new_villagers -= count
    villagers += count
    count = 0
    await state.update_data(count=count)
    await sqlbase_add_man.execute_query("""UPDATE user_and_villagers_data SET (villagers, count_new_villagers) = ($1, $2)
     WHERE user_id = $3;""", (villagers, count_new_villagers, str(user_id)))
    await callback.message.edit_text(f'К вам в поселение хотят присоединится\n'
                                     f'Количество ваших людей: {villagers}\n'
                                     f'Количество людей в очереди: {count_new_villagers}\n'
                                     f'Вы можете выбрать количество человек, после подтверждаете, если вам больше людей не надо, нажмите "Отклонить"',
                                     reply_markup=kb)

    await callback.answer('Подтверждено')

@router_add_man.callback_query(InlineChoiceMenu.filter(F.regime=='add_man'))
async def regime_add_man(callback: CallbackQuery, state: FSMContext):
    kb = await kb_add_man.add_man_inline_kb()
    user_id = callback.message.chat.id
    await sqlbase_add_man.connect()
    await state.update_data(count=0)
    user_data = await sqlbase_add_man.execute_query("""SELECT villagers, villagers_busy, count_new_villagers FROM user_and_villagers_data WHERE user_id = $1""",
                                    (str(user_id), ))


    await callback.message.edit_text(f'К вам в поселение хотят присоединится\n'
                                     f'Количество ваших людей: {user_data[0][0]+user_data[0][1]}\n'
                                     f'Количество людей в очереди: {user_data[0][-1]}\n'
                                     f'Вы можете выбрать количество человек, после подтверждаете, если вам больше людей не надо, нажмите "Отклонить"', reply_markup=kb)

    await callback.answer('Выберите, что вы хотите сделать с этими людьми')
