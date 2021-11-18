from peewee import *
from loader import dp
from aiogram import executor
from db import create_tables
from utils import set_default_commands
import handlers

async def init_bot(dispatcher):
    await set_default_commands(dispatcher)


def main():
    # create tables
    create_tables()
    executor.start_polling(dp, on_startup=init_bot, skip_updates=True)


if __name__ == '__main__':
    main()
