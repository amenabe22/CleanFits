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
    formatted = """<b>Item Name:</b> {}\n\n<b>Price:</b> {}\n\n<b>Detail:</b> {}\n\n<b>Brand:</b> {}\n\n#{}\n""".format(
        data["item_name"], data["price"], data["desc"], data["brand"], data["item_type"]
    )
    return formatted


def format_from_post(post):
    formatted = """<b>Item Name:</b> {}\n\n<b>Price:</b> {}\n\n<b>Detail:</b> {}\n\n<b>Brand:</b> {}\n\n#{}\n""".format(
        post.name, post.price, post.desc, post.brand, post.brand, post.category
    )
    return formatted


def format_from_post_final(post, store=None):
    contact_message = "@"
    if post.contact_method == "phone":
        contact_message = post.phone
    else:
        contact_message += post.username
    if store:
        formatted = """<b>Store:</b> {}\n\n<b>Item Name:</b> {}\n\n<b>Price:</b> {}\n\n<b>Detail:</b> {}\n\nBrand: {}\n\n<b>Contact:</b> {}\n\n#{} #{}\n""".format(
            store.store_name, post.name, post.price, post.desc, post.brand,
            contact_message, post.category, store.store_name
        )
    else:
        formatted = """\n<b>Item Name:</b> {}\n\n<b>Price:</b> {}\n\n<b>Detail:</b> {}\n\n<b>Brand:</b> {}\n\n<b>Contact:</b> {}\n\n#{}\n""".format(
            post.name, post.price, post.desc, post.brand,
            contact_message, post.category
        )

    return formatted


def format_post_final(data, store=None):
    contact_message = "@" + data["contact"]
    if data["c_method"] == "phone":
        contact_message = data["contact"]
    if store:
        formatted = """<b>Store:</b> {}\n\n<b><b>Item Name:</b> {}\n\n<b>Price:</b> {}\n\n<b>Detail:</b> {}\n\n<b>Brand:</b> {}\n\n<b>Contact:</b> {}\n\n#{}#{}\n""".format(
            store.name, data["item_name"], data["price"], data["desc"], data["brand"], contact_message, data["item_type"], store.name
        )
    else:
        formatted = """\n<b>Item Name:</b> {}\n\n<b>Price:</b> {}\n\n<b>Detail:</b> {}\n\n<b>Brand:</b> {}\n\n<b>Contact:</b> {}\n\n#{}\n""".format(
            data["item_name"], data["price"], data["desc"], data["brand"], contact_message, data["item_type"]
        )

    return formatted
