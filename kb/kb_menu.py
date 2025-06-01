from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from kb.fabirc_kb import KeyboardFactory, InlineChoiceBuild


class KbMenu(KeyboardFactory):

    async def inline_regime_build(self, add_man=False):
        await self.create_builder_inline()
        create_gold_mine = InlineKeyboardButton(
            text='Построить золотую шахту💰',
            callback_data=InlineChoiceBuild(
                construction='gold_mine',
#                 phrase='золотую шахту'
            ).pack()
        )

        create_stone_mine = InlineKeyboardButton(
            text='Построить каменную шахту🗻',
            callback_data=InlineChoiceBuild(
                construction='stone_mine',
#                 phrase='каменную шахту'
            ).pack()
        )

        create_ranch = InlineKeyboardButton(
            text='Построить ферму🌾',
            callback_data=InlineChoiceBuild(
                construction='ranch',
#                 phrase='ферму'
            ).pack()
        )

        create_home = InlineKeyboardButton(
            text='Построить дом🏡',
            callback_data=InlineChoiceBuild(
                construction='home',
#                 phrase='дом'
            ).pack()
        )

        button_cancel = InlineKeyboardButton(
            text='Выйти в меню❌',
            callback_data=InlineChoiceBuild(
                construction='cancel',
#                 phrase='0'
            ).pack()
        )

        self.builder_inline.add(create_ranch, create_home)
        self.builder_inline.row(create_gold_mine)
        self.builder_inline.row(create_stone_mine)
        self.builder_inline.row(button_cancel)

        if add_man:
            self.builder_inline.add(self.button_add_man)

        return self.builder_inline.as_markup()
