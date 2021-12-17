import typing
from ..post import post
from aiogram import types
from loader import dp, bot
from constants import BASIC_ACCOUNT
from buttons.inlines import inline_kb
from crud.core import create_bot_user
from forms.account import NewStoreForm
from aiogram.dispatcher import FSMContext
from utils.bot_helpers import make_markup
from filters.core import StoreMenuMessage
from constants import STORE_DETAIL_BUTTONS
from constants.inline_kbs import STORE_OPTS
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters.builtin import Message, Filter
from aiogram.dispatcher.filters.state import State, StatesGroup
from crud.core import create_store, check_store_stat, get_store, delete_store

vote_cb = CallbackData('cat', 'action')  # vote:<action>
loc_cb = CallbackData('loc', 'action')  # vote:<action>
st_cb = CallbackData('store', 'action', 'stid')
likes = {}


class StForm(StatesGroup):
    name = State()
    category = State()
    location = State()


def get_store_manager_opts(sid):
    sman = [
        {"label": "📌 Add Post", "id": "addpost"},
        {"label": "📣 Promote", "id": "promote"},
        {"label": "❌ Close Store", "id": "close"}
    ]
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.add(*[
        types.InlineKeyboardButton(
            x["label"], callback_data=post.post_cb.new(action=x["id"], sid=sid)) for x in sman
    ])
    return ikb


def get_keyboard():
    xTypes = [
        {"label": "Female Dresses", "id": "dress"},
        {"label": "Socks and Panties", "id": "sock"},
        {"label": "Shoes & Slippers", "id": "shoes"}
    ]
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.add(*[
        types.InlineKeyboardButton(
            x["label"], callback_data=vote_cb.new(action=x["id"], )) for x in xTypes
    ])
    return ikb


def store_list_kb(stores):
    store_btns = types.InlineKeyboardMarkup()
    store_btns.add(*[
        types.InlineKeyboardButton(
            x.store_name, callback_data=st_cb.new(action="storec", stid=x.id))
        for x in stores
    ])
    return store_btns


def store_remove_btns():
    loc_opts = types.InlineKeyboardMarkup()
    loc_opts.add(*[
        types.InlineKeyboardButton(
            x["label"], callback_data=post.post_cb.new(action=x["id"], sid=x["id"]))
        for x in [
            {"label": "Yes !", "id": "syes"},
            {"label": "Not Yet", "id": "sno"}
        ]
    ])
    return loc_opts


def get_loc_opts():
    loc_opts = types.InlineKeyboardMarkup()
    loc_opts.add(*[
        types.InlineKeyboardButton(
            x["label"], callback_data=loc_cb.new(action=x["id"]))
        for x in [
            {"label": "Yes !", "id": "lyes"},
            {"label": "Not Yet", "id": "lno"}
        ]
    ])
    return loc_opts


@ dp.message_handler(commands='add')
async def store_message_cmd(message: Message, state: FSMContext):
    stat, stores = check_store_stat(message.chat.id)
    if len(stores) == 0:
        await state.set_state(StForm.name)
        await message.reply("What's the name of your store ?", reply_markup=types.ReplyKeyboardRemove())
    else:
        print(stores[0].store_name, "jacked up")
        await message.reply("Welcome back which store would you like to manage ?",
                            reply_markup=store_list_kb(stores))


@ dp.message_handler(StoreMenuMessage())
async def store_message(message: Message, state: FSMContext):
    if message.text == '🛍 My Stores':
        stat, stores = check_store_stat(message.chat.id)
        if len(stores) == 0:
            await state.set_state(StForm.name)
            await message.reply("What's the name of your store ?", reply_markup=types.ReplyKeyboardRemove())
        else:
            print(stores[0].store_name, "jacked up")
            await message.reply("Welcome back which store would you like to manage ?",
                                reply_markup=store_list_kb(stores))


@ dp.message_handler(state=StForm.name)
async def process_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await StForm.next()
        await message.reply("What category of clothing you got ?", reply_markup=get_keyboard())


@ dp.callback_query_handler(post.post_cb.filter(action=['syes', 'sno']))
async def callback_store_pop_final(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await query.answer()
    final_message = "Store successfull removed"

    callback_data_action = callback_data['action']

    async with state.proxy() as data:
        if callback_data_action == "sno":
            final_message = "Okay"
        else:
            store = data["cbk"]["sid"]
            delete_store(store)

    await bot.edit_message_text(
        final_message,
        query.from_user.id,
        query.message.message_id,
        # reply_markup=get_loc_opts()
        # reply_markup=types.ReplyKeyboardRemove()
    )


@ dp.callback_query_handler(loc_cb.filter(action=['lyes', 'lno']), state=StForm.category)
async def callback_loc_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await query.answer()
    callback_data_action = callback_data['action']
    # update loc
    async with state.proxy() as data:
        data["location"] = callback_data_action
        create_store(
            data,
            types.Chat.get_current().id
        )
        await state.finish()
    await bot.edit_message_text(
        "Form completed",
        query.from_user.id,
        query.message.message_id
    )


@ dp.callback_query_handler(st_cb.filter(action="storec"))
async def callback_store_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await query.answer()
    callback_data_action = callback_data['action']
    # Select store and prompt user to manage products
    print("check", callback_data)
    store = get_store(callback_data["stid"])
    await bot.edit_message_text(
        "You have selected {}".format(store.store_name),
        query.from_user.id,
        query.message.message_id,
        reply_markup=get_store_manager_opts(store.id)
    )


@ dp.callback_query_handler(vote_cb.filter(action=['dress', 'sock', 'shoes']), state=StForm.category)
async def callback_vote_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    # logging.info('Got this callback data: %r', callback_data)  # callback_data contains all info from callback data
    await query.answer()
    callback_data_action = callback_data['action']

    # update category state
    async with state.proxy() as data:
        data["cat"] = callback_data_action

    # update amount of likes in storage
    # likes[query.from_user.id] = likes_count
    # await bot.edit_message_text("asdf")
    await bot.edit_message_text(
        "Do you have a physical location ?",
        # f'You voted {callback_data_action}! Now you have {12} vote[s].',
        query.from_user.id,
        query.message.message_id,
        reply_markup=get_loc_opts()
        # reply_markup=types.ReplyKeyboardRemove()
    )


@ dp.callback_query_handler(post.post_cb.filter(action=['close']))
async def callback_close_store(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await query.answer()
    async with state.proxy() as data:
        data["cbk"] = callback_data
        await bot.edit_message_text(
            "Are you sure you want to remove this store ?",
            query.from_user.id,
            query.message.message_id,
            reply_markup=store_remove_btns()
            # reply_markup=types.ReplyKeyboardRemove()
        )

# handle the cases when this exception raises


@ dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    print("Got some Error")
    return True  # errors_handler must return True if error was handled correctly
