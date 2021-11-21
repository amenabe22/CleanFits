from aiogram import types


def inline_kb(items, cbk):
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.add(*[
        types.InlineKeyboardButton(
            x["label"], callback_data=cbk.new(action=x["id"], sid=x["id"])) for x in items
    ])
    return ikb
