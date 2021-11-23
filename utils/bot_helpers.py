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


def format_from_post(post):
    formatted = """Item Name: {}\n\nPrice: {}\n\nDetail: {}\n\nBrand: {}\n\n#{}\n""".format(
        post.name, post.price, post.desc, post.brand, post.brand, post.category
    )
    return formatted


def format_from_post_final(post, store=None):
    contact_message = "@" + post.username
    if post.contact_method == "phone":
        contact_message = post.phone
    if store:
        formatted = """Store: {}\n\nItem Name: {}\n\nPrice: {}\n\nDetail: {}\n\nBrand: {}\n\nContact: {}\n\n#{} #{}\n""".format(
            store.store_name, post.name, post.price, post.desc, post.brand,
            contact_message, post.category, store.store_name
        )
    else:
        formatted = """\nItem Name: {}\n\nPrice: {}\n\nDetail: {}\n\nBrand: {}\n\nContact: {}\n\n#{}\n""".format(
            post.name, post.price, post.desc, post.brand,
            contact_message, post.category
        )   

    return formatted


def format_post_final(data, store=None):
    contact_message = "@" + data["contact"]
    if data["c_method"] == "phone":
        contact_message = data["contact"]
    if store:
        formatted = """Store: {}\n\nItem Name: {}\n\nPrice: {}\n\nDetail: {}\n\nBrand: {}\n\nContact: {}\n\n#{}#{}\n""".format(
            store.name, data["item_name"], data["price"], data["desc"], data["brand"], contact_message, data["item_type"], store.name
        )
    else:
        formatted = """\nItem Name: {}\n\nPrice: {}\n\nDetail: {}\n\nBrand: {}\n\nContact: {}\n\n#{}\n""".format(
            data["item_name"], data["price"], data["desc"], data["brand"], contact_message, data["item_type"]
        )

    return formatted
