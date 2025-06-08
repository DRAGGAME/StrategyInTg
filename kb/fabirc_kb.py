from sys import prefix
from typing import Union

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


class InlineChoiceGame(CallbackData, prefix='game_change'):
    category_id: str


class InlineChoiceMenu(CallbackData, prefix='regime_change'):
    regime: str


class InlineChoiceBuild(CallbackData, prefix='build_change'):
    construction: str
    # phrase: str


class InlineChoiceUpgrade(InlineChoiceBuild, prefix='upgrade_change'):
    construction: str


class KeyboardFactory:

    def __init__(self):
        self.builder_reply = None

        self.builder_inline = None

        self.button_add_man = InlineKeyboardButton(
            text='Добавить человека',
            callback_data=InlineChoiceMenu(
                regime='add_man',
                #                 phrase='0'
            ).pack()
        )

    async def create_builder_reply(self) -> None:
        self.builder_reply = ReplyKeyboardBuilder()

    async def create_builder_inline(self) -> None:
        self.builder_inline = InlineKeyboardBuilder()

    async def builder_reply_choice(self, text_input: str) -> ReplyKeyboardMarkup:
        await self.create_builder_reply()
        self.builder_reply.add(KeyboardButton(text="Да✅"))
        self.builder_reply.add(KeyboardButton(text="Нет❌"))

        keyboard = self.builder_reply.as_markup(
                                       resize_keyboard=True,
                                         input_field_placeholder=text_input, one_time_keyboard=True)
        return keyboard

    async def builder_text(self, texts: Union[tuple, list, set], input_field: str) -> ReplyKeyboardMarkup:
        await self.create_builder_reply()
        for text in texts:
            self.builder_reply.add(KeyboardButton(text=text))
        first_keyboard = self.builder_reply.as_markup(resize_keyboard=True,
                                                      input_field_placeholder=input_field)
        return first_keyboard

    async def builder_reply_cancel(self) -> ReplyKeyboardMarkup:
        await self.create_builder_reply()
        self.builder_reply.add(KeyboardButton(text='Отмена'))
        keyboard_cancel = self.builder_reply.as_markup(resize_keyboard=True,
                                                input_field_placeholder='Нажмите кнопку в случае необходимости')
        return keyboard_cancel

    async def builder_inline_choice_category(self):

        button_game = InlineKeyboardButton(
            text='Зайти в игру',
            callback_data=InlineChoiceGame(
                category_id='run_in_game',
            ).pack()
        )

        button_settings = InlineKeyboardButton(
            text='Настройки',
            callback_data=InlineChoiceGame(
                category_id='settings',
            ).pack()
        )

        button_del = InlineKeyboardButton(
            text='Удалить',
            callback_data=InlineChoiceGame(
                category_id='del',
            ).pack()
        )

        await self.create_builder_inline()

        self.builder_inline.add(button_game)
        self.builder_inline.add(button_settings)
        self.builder_inline.add(button_del)

        return self.builder_inline.as_markup()

    async def builder_inline_choice_menu(self, add_man=False):

        button_upgrade = InlineKeyboardButton(
            text='Улучшения',
            callback_data=InlineChoiceMenu(
                regime='upgrade',
            ).pack()
        )

        button_plan = InlineKeyboardButton(
            text='Статистика деревни',
            callback_data=InlineChoiceMenu(
                regime='stats',
            ).pack()
        )

        button_building = InlineKeyboardButton(
            text='Строительство',
            callback_data=InlineChoiceMenu(
                regime='build',
            ).pack()
        )

        button_cancel = InlineKeyboardButton(
            text='Назад',
            callback_data=InlineChoiceMenu(
                regime='cancel',
            ).pack()
        )

        await self.create_builder_inline()

        self.builder_inline.add(button_building, button_upgrade)
        self.builder_inline.row(button_plan)

        if add_man:
            self.builder_inline.row(self.button_add_man)

        self.builder_inline.row(button_cancel)


        return self.builder_inline.as_markup()
