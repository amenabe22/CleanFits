import typing
from os import name
from loader import dp
from aiogram import types
from buttons.inlines import inline_kb
from aiogram.dispatcher.filters.builtin import Message, Filter
from filters.core import AccountMenuMessage
from crud.core import user_data_with_bid
from utils.bot_formats import format_account
from constants.inline_kbs import ACCOUNT_USER_MANAGE
from aiogram.utils.callback_data import CallbackData
from forms.account import UserForm

acc_cb = CallbackData('post','action', 'sid')

@dp.message_handler(AccountMenuMessage())
async def store_message(message: Message):
    if message.text == '🔓 Account':
        user = user_data_with_bid(message.chat.id)        
        acc_format = format_account(user)
        await message.answer(acc_format,parse_mode='HTML')

    if message.text == '⚙️ Settings':
        # TODO: show account information
        await message.answer("Basic settings handler")

# @ dp.callback_query_handler(post_cb.filter(action=["addpost"]))
@ dp.callback_query_handler(acc_cb.filter(sid=['edit']))
async def callback_user_name_type(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: name):
    # logging.info('Got this callback data: %r', callback_data)  # callback_data contains all info from callback data
    print("."*20)
    await query.answer()
    callback_data_action = callback_data['action']

    # update category state
    async with state.proxy() as data:
        data["edit_name"] = callback_data_action
        # await state.set_state(PostForm.brand)
    await UserForm.next()
