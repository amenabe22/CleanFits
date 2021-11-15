from loader import dp
from filters.core import StoreMenuMessage
from utils.bot_helpers import make_markup
from constants import STORE_DETAIL_BUTTONS
from forms.account import NewStoreForm
from aiogram.dispatcher.filters.builtin import Message, Filter

async def save_store():
    data = await NewStoreForm.get_data()
    print(data, "store info saved")

@dp.message_handler(StoreMenuMessage())
async def store_message(message: Message):
    if message.text == '🛍 My Store':
        # markup = make_markup(STORE_DETAIL_BUTTONS)
        # Check if user has a store and show store welcome
        # await message.answer("Welcome to your store", reply_markup=markup)
        await NewStoreForm.start(callback=save_store)