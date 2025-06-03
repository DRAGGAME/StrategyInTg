
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from kb.fabirc_kb import KeyboardFactory


class InlineAddMan(CallbackData, prefix='add_man'):
    confirm: str


class KbFactoryAddMan(KeyboardFactory):

    async def add_man_inline_kb(self):
        await self.create_builder_inline()

        yes_button = InlineKeyboardButton(
            text='Подтвердить',
            callback_data=InlineAddMan(
                confirm='yes',
            ).pack()
        )

        no_button = InlineKeyboardButton(
            text='Отклонить остальных',
            callback_data=InlineAddMan(
                confirm='no',
            ).pack()
        )

        plus_two_button = InlineKeyboardButton(
            text='+2',
            callback_data=InlineAddMan(
                confirm='+2',
            ).pack()
        )

        plus_one_button = InlineKeyboardButton(
            text='+1',
            callback_data=InlineAddMan(
                confirm='+1',
            ).pack()
        )
        minus_one_button = InlineKeyboardButton(
            text='-1',
            callback_data=InlineAddMan(
                confirm='-1',
            ).pack()
        )
        minus_two_button = InlineKeyboardButton(
            text='-2',
            callback_data=InlineAddMan(
                confirm='-2',
            ).pack()
        )

        cancel_button = InlineKeyboardButton(
            text='Назад',
            callback_data=InlineAddMan(
                confirm='cancel',
            ).pack()
        )

        self.builder_inline.add(minus_two_button, minus_one_button, plus_one_button, plus_two_button)
        self.builder_inline.row(yes_button)
        self.builder_inline.row(no_button)
        self.builder_inline.row(cancel_button)

        return self.builder_inline.as_markup()

