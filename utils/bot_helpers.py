from aiogram.types import ReplyKeyboardMarkup

# TODO: split to separate module


def make_markup(button_rows: list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_row in button_rows:
        kb.row(*button_row)
    return kb
