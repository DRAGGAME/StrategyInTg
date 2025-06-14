from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from kb.fabirc_kb import KeyboardFactory


class InlineStaticKeyboard(CallbackData, prefix='static_kb'):
    static_info: str


class StaticKeyboard(KeyboardFactory):

    cancel_button = InlineKeyboardButton(
        text='Назад',
        callback_data=InlineStaticKeyboard(
            static_info='cancel',
        ).pack()
    )

    async def static_keyboard(self):
        await self.create_builder_inline()

        about_resources = InlineKeyboardButton(
            text='О ресурсах',
            callback_data=InlineStaticKeyboard(
                static_info='resource_info',
            ).pack()
        )

        about_buildings = InlineKeyboardButton(
            text='О постройках',
            callback_data=InlineStaticKeyboard(
                static_info='buildings_info',
            ).pack()
        )

        self.builder_inline.add(about_resources, about_buildings)
        self.builder_inline.row(self.cancel_button)

        return self.builder_inline.as_markup()

    async def cancel_keyboard(self):
        await self.create_builder_inline()

        self.builder_inline.row(self.cancel_button)

        return self.builder_inline.as_markup()

