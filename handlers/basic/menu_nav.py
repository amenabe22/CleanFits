from loader import dp
from aiogram.types import Message
from utils.bot_helpers import make_markup
from filters.core import HomeNavigationFilter
from constants.menu_keyboards import BASIC_ACCOUNT


@dp.message_handler(HomeNavigationFilter())
async def home_nav(message: Message):
    await message.reply("Home", reply_markup=make_markup(BASIC_ACCOUNT))
