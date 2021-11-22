from aiogram.types import ReplyKeyboardMarkup

# TODO: split to separate module


def make_markup(button_rows: list):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for button_row in button_rows:
        kb.row(*button_row)
    return kb


def format_post(data):
    # store = get
    print(data)
    formatted = """Item Name: {}\n\nPrice: {}\n\nDetail: {}\n\nBrand: {}\n\n#{}\n""".format(
        data["item_name"], data["price"], data["desc"], data["brand"], data["item_type"]
    )
    return formatted


def format_post_final(data):
    contact_message = "@" + data["contact"]
    if data["c_method"] == "phone":
        contact_message = data["contact"]
    formatted = """Item Name: {}\n\nPrice: {}\n\nDetail: {}\n\nBrand: {}\n\nContact: {}\n\n#{}\n""".format(
        data["item_name"], data["price"], data["desc"], data["brand"], contact_message, data["item_type"]
    )
    return formatted
