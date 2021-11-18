import logging
from crud.settings import BOT_TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Initialize logger and load bot
logging.basicConfig(level=logging.INFO)
logging.info("-------------")
logging.info("Bot Started")
logging.info("-------------")
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)