from loader import dp
from aiogram.dispatcher.filters.builtin import Message, Filter
from filters.core import AccountMenuMessage
from crud.core import user_data_with_bid
from utils.bot_formats import format_account

@dp.message_handler(AccountMenuMessage())
async def store_message(message: Message):
    if message.text == '🔓 Account':
        user = user_data_with_bid(message.chat.id)        
        acc_format = format_account(user)
        await message.answer(acc_format)

    if message.text == '⚙️ Settings':
        # TODO: show account information
        await message.answer("Basic settings handler")
