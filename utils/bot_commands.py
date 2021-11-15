from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start CleanFit"),
            types.BotCommand("help", "Help section")
        ]
    )