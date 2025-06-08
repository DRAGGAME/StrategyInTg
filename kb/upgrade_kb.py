from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from kb.fabirc_kb import KeyboardFactory, InlineChoiceBuild


class InlineUpgradeKb(CallbackData, prefix='upgrade_kb'):
    level: int
    confirm: str

class UpgradeKb(KeyboardFactory):

    async def upgrade_keyboard(self):
        await self.create_builder_inline()

        one_button = InlineKeyboardButton(
            text='1',
            callback_data=InlineUpgradeKb(
                level=1,
                confirm='None'
            ).pack()
        )

        two_button = InlineKeyboardButton(
            text='2',
            callback_data=InlineUpgradeKb(
                level=2,
                confirm='None'
            ).pack()
        )

        three_button = InlineKeyboardButton(
            text='3',
            callback_data=InlineUpgradeKb(
                level=3,
                confirm='None'
            ).pack()
        )

        four_button = InlineKeyboardButton(
            text='4',
            callback_data=InlineUpgradeKb(
                level=4,
                confirm='None'
            ).pack()
        )

        button_cancel = InlineKeyboardButton(
            text='Выбрать другую постройку',
            callback_data=InlineUpgradeKb(
                level=0,
                confirm='cancel'
                #                 phrase='0'
            ).pack()
        )

        self.builder_inline.add(one_button)
        self.builder_inline.add(two_button)
        self.builder_inline.add(three_button)
        self.builder_inline.add(four_button)
        self.builder_inline.row(button_cancel)
        return self.builder_inline.as_markup()
