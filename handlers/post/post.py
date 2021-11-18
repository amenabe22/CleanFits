import typing
from aiogram import types
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import State, StatesGroup

post_cb = CallbackData('post', 'action', 'sid')


class PostForm(StatesGroup):
    item_name = State()
    price = State()
    detail_desc = State()
    item_type = State()
    brand = State()
    pictures = State()


# All message handlers go here now
@ dp.message_handler(state=PostForm.item_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item_name'] = message.text
        print("..................")
        print(data)
        print("..................")
        await PostForm.next()
        await message.reply("What is the price ?")


# All callback handelers go under here
@ dp.callback_query_handler(post_cb.filter(action=["addpost"]))
async def callback_post_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await query.answer()
    # callback_data_action = callback_data['action']
    print(callback_data, "cal DATA")
    async with state.proxy() as data:
        data['store'] = callback_data["sid"]

    await state.set_state(PostForm.item_name)
    await bot.edit_message_text(
        "Enter Item Name",
        query.from_user.id,
        query.message.message_id
    )
