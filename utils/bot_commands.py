from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start CleanFit"),
            types.BotCommand("quick", "Quick Item Post"),
            types.BotCommand("add", "Post From Store"),
            types.BotCommand("cancel", "Cancel Form"),
            types.BotCommand("help", "Help Section")
        ]
    )