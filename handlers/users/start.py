from loader import dp
from loader import bot
from aiogram import types
from forms.account import UserForm
from utils.bot_helpers import make_markup
from constants.menu_keyboards import BASIC_ACCOUNT
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from crud.core import create_bot_user, user_exists, update_basic


async def _show_info():
    data = await UserForm.get_data()
    # update basic details once form is complete
    update_basic({
        "bot_id": types.Chat.get_current().id,
        "name": data["UserForm:name"],
        "email": data["UserForm:email"],
    })
    await bot.send_message(
        chat_id=types.Chat.get_current().id,
        text='\n'.join([
            f'{field.label}: {data[field.data_key]}'
            for field in UserForm._fields
        ]),
        reply_markup=make_markup(BASIC_ACCOUNT)
    )


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    stat = create_bot_user({
        "username": message.chat.username,
        "name": message.from_user.full_name,
        "bot_id": message.chat.id
    })
    #  start some form here
    if not stat:
        await UserForm.start(callback=_show_info)
    else:
        await message.answer(
            f"Welcome to Clean Fits, {message.from_user.full_name}",
            reply_markup=make_markup(BASIC_ACCOUNT))
