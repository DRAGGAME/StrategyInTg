from typing import Union, Type

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from kb.fabirc_kb import KeyboardFactory, InlineChoiceBuild, InlineChoiceUpgrade


class KbMenu(KeyboardFactory):

    async def inline_regime_build(self, key_phrase: bool, class_n: Type[Union[InlineChoiceBuild, InlineChoiceUpgrade]],
                                  add_man: bool=False):
        await self.create_builder_inline()

        if key_phrase:
            phrase = 'Улучшить'
        else:
            phrase = 'Построить'

        create_gold_mine = InlineKeyboardButton(
            text=f'{phrase} золотую шахту💰',
            callback_data=class_n(
                construction='gold_mines',
            ).pack()
        )

        create_stone_mine = InlineKeyboardButton(
            text=f'{phrase} каменную шахту🗻',
            callback_data=class_n(
                construction='stone_mines',
#                 phrase='каменную шахту'
            ).pack()
        )

        create_ranch = InlineKeyboardButton(
            text=f'{phrase} ферму🌾',
            callback_data=class_n(
                construction='ranches',
#                 phrase='ферму'
            ).pack()
        )

        create_home = InlineKeyboardButton(
            text=f'{phrase} дом🏡',
            callback_data=class_n(
                construction='homes',
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

        if add_man:
            self.builder_inline.row(self.button_add_man)

        self.builder_inline.row(button_cancel)

        return self.builder_inline.as_markup()
