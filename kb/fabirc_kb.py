from typing import Union

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


class KeyboardFactory:
    def __init__(self):
        self.builder_reply = None

        self.builder_inline = None
        self.back_from_butt = InlineKeyboardButton(
            text='Назад',
            callback_data='back_from_butt'
        )

        self.delete_from_butt = InlineKeyboardButton(
            text='УДАЛИТЬ ФАЙЛ',
            callback_data='delete_file'
        )

        self.another_action_butt = InlineKeyboardButton(
            text='Выбрать другое действие',
            callback_data='action'
        )

        self.cancel_from_butt = InlineKeyboardButton(
            text='Выбрать другой предмет',
            callback_data='cancel'
        )

        self.next_from_butt = InlineKeyboardButton(
            text='Вперёд',
            callback_data='next_from_butt'
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

    async def builder_inline_montage(self,
                                     next_boot: bool = False,
                                     back_boot: bool = False,
                                     cancel_bott: bool = False,
                                     action_boot: bool = False,
                                     delete_boot: bool = False
                                     ) -> None:

        await self.create_builder_inline()

        if back_boot is True:
            self.builder_inline.add(self.back_from_butt)

        if next_boot is True:
            self.builder_inline.add(self.next_from_butt)

        if cancel_bott is True:
            self.builder_inline.add(self.cancel_from_butt)

        if action_boot is True:
            self.builder_inline.add(self.another_action_butt)

        if delete_boot is True:
            self.builder_inline.add(self.delete_from_butt)

        self.builder_inline.adjust(2, 1)

        return self.builder_inline.as_markup()








