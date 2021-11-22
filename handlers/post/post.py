import typing
from aiogram import types
from db.model import Post
from loader import dp, bot
from buttons.inlines import inline_kb

from aiogram.dispatcher import FSMContext
from crud.post import create_post, set_approval
from aiogram.utils.callback_data import CallbackData
from utils.bot_helpers import format_post, format_post_final
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_media_group import MediaGroupFilter, media_group_handler
from constants.inline_kbs import BRANDS, PROD_CATS, POST_MANAGE, POST_USER_MANAGE, CONTACT_OPTS

post_cb = CallbackData('post', 'action', 'sid')


def posted_markup(post):
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.add(*[
        types.InlineKeyboardButton(
            x["label"], callback_data=post_cb.new(action=x["id"], sid=post)) for x in [
            {"label": "🏹 Share", "id": "approve"},
            {"label": "🤙 Contact", "id": "decline"},
        ]
    ])
    return ikb


def post_inline_kb(cbk, post):
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.add(*[
        types.InlineKeyboardButton(
            x["label"], callback_data=cbk.new(action=x["id"], sid=post)) for x in [
            {"label": "✅ Approve", "id": "approve"},
            {"label": "❌ Decline", "id": "decline"},
            {"label": "🛑 Report", "id": "report"},
        ]
    ])
    return ikb


class PostForm(StatesGroup):
    item_name = State()
    price = State()
    detail_desc = State()
    item_type = State()
    brand = State()
    pictures = State()
    contact_method = State()
    contact = State()


@ dp.message_handler(state=PostForm.pictures, content_types=[types.ContentType.PHOTO])
# @dp.message_handler( content_types=[types.ContentType.PHOTO])
async def process_single_pic(message: types.Message,  state: FSMContext):
    async with state.proxy() as data:
        # await state.set_state(PostForm.item_type)
        # await state.finish()
        data["pic"] = message.photo[0].file_id
        await state.set_state(PostForm.contact_method)
        await bot.send_message(
            message.from_user.id,
            "Which way would you like to be contacted ?",
            reply_markup=inline_kb(CONTACT_OPTS, post_cb)
        )

        # await message.answer(formatted, reply_markup=inline_kb(POST_USER_MANAGE, post_cb))
    # await message.answer("Form complete")


@ dp.message_handler(state=PostForm.contact)
async def process_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.text
        await state.finish()
        await message.answer(format_post(data), reply_markup=inline_kb(POST_USER_MANAGE, post_cb))


@dp.message_handler(MediaGroupFilter(), state=PostForm.pictures, content_types=types.ContentType.PHOTO)
@media_group_handler
# @dp.message_handler( content_types=[types.ContentType.PHOTO])
async def process_pics(messages: [types.Message],  state: FSMContext):
    print("bpt 1")
    media = types.MediaGroup()
    for x in messages:
        # if ix == 0:
        #     media.attach_photo(x.photo[0].file_id, caption="He",)
        media.attach_photo(x.photo[0].file_id)
    # async with state.proxy() as data:
    #     # await state.set_state(PostForm.item_type)
    #     await state.finish()

    # # print(media, "whoa")
    # # await bot.send_photo(-1001702851184, mgs)
    # await bot.send_media_group(-1001702851184, media)
    # await bot.send_message(-1001702851184, "some message", reply_markup=inline_kb(POST_MANAGE, post_cb))
    # # await bot.send_message(-1001702851184, "Wazzaa")
    await messages[0].answer("Form complete")


@ dp.message_handler(state=PostForm.detail_desc)
async def process_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
        await state.set_state(PostForm.item_type)
        await message.reply("Select Category", reply_markup=inline_kb(PROD_CATS, post_cb))


@ dp.message_handler(state=PostForm.price)
async def process_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
        await state.set_state(PostForm.detail_desc)
        await message.reply("Add some information here: ")

# All message handlers go here now


@ dp.message_handler(state=PostForm.item_name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['item_name'] = message.text
        await state.set_state(PostForm.price)
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


@ dp.callback_query_handler(post_cb.filter(action=['shoes', 'dress', 'shirts']), state=PostForm.item_type)
async def callback_post_type(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    # logging.info('Got this callback data: %r', callback_data)  # callback_data contains all info from callback data
    await query.answer()
    callback_data_action = callback_data['action']

    # update category state
    async with state.proxy() as data:
        data["item_type"] = callback_data_action
        # await state.set_state(PostForm.brand)
    await PostForm.next()
    # update amount of likes in storage
    # likes[query.from_user.id] = likes_count
    # await bot.edit_message_text("asdf")
    await bot.edit_message_text(
        "What is the brand of the item ?",
        # f'You voted {callback_data_action}! Now you have {12} vote[s].',
        query.from_user.id,
        query.message.message_id,
        reply_markup=inline_kb(BRANDS, post_cb)
        # reply_markup=types.ReplyKeyboardRemove()
    )


@ dp.callback_query_handler(post_cb.filter(action=['publish', 'wait', 'nah']))
async def callback_post_approve(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await query.answer()
    callback_data_action = callback_data['action']
    if callback_data_action == "publish":
        # callback_data_action = callback_data['action']
        async with state.proxy() as data:
            print("---------------")
            print(data, "whoa")
            print("---------------")
            pst = create_post(data)
            await bot.send_photo(
                -1001702851184, data["pic"],
                reply_markup=post_inline_kb(post_cb, pst),
                caption=format_post_final(data))
            await bot.edit_message_text(
                format_post(data),
                # f'You voted {callback_data_action}! Now you have {12} vote[s].',
                query.from_user.id,
                query.message.message_id,
                # reply_markup=brands_kb()
                # reply_markup=types.ReplyKeyboardRemove()
            )
            # print("+++", pst, "+++")
            # await bot.answer_callback_query(query.id, "THIS IS AN ALERT", show_alert=True)
            # await bot.answer_callback_query
            await bot.send_message(
                query.from_user.id,
                "Thanks your post is sent for moderation we will let you know once it's approved !!!",
            )


@ dp.callback_query_handler(post_cb.filter(action=['telegram', 'phone']), state=PostForm.contact_method)
async def callback_contact_method(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await query.answer()
    callback_data_action = callback_data['action']
    async with state.proxy() as data:
        data["c_method"] = callback_data_action

        if(callback_data_action == "telegram"):
            data["contact"] = query.message.chat.username
            await state.finish()
            print(query.message.from_user.id, "whoa man")
            await bot.edit_message_text(
                "Contact method saved",
                query.from_user.id,
                query.message.message_id,
            )
            formatted = format_post(data)
            await bot.edit_message_text(formatted,
                                        query.from_user.id,
                                        query.message.message_id,
                                        reply_markup=inline_kb(
                                            POST_USER_MANAGE, post_cb)
                                        )

        else:
            await state.set_state(PostForm.contact)
            await bot.edit_message_text(
                "Please Enter Your prefered phone number.",
                query.from_user.id,
                query.message.message_id,
            )


@ dp.callback_query_handler(post_cb.filter(action=['nikee', 'lv', 'bal', 'add']), state=PostForm.brand)
async def callback_post_brand(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    # logging.info('Got this callback data: %r', callback_data)  # callback_data contains all info from callback data
    await query.answer()
    callback_data_action = callback_data['action']
    # update category state
    async with state.proxy() as data:
        data["brand"] = callback_data_action
        await state.set_state(PostForm.pictures)
    await bot.edit_message_text(
        "Send pictures of the item.",
        # f'You voted {callback_data_action}! Now you have {12} vote[s].',
        query.from_user.id,
        query.message.message_id,
        # reply_markup=brands_kb()
        # reply_markup=types.ReplyKeyboardRemove()
    )


@ dp.callback_query_handler(post_cb.filter(action=['approve']))
async def callback_post_publish(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    await query.answer()
    # callback_data_action = callback_data['action']
    set_approval(callback_data["sid"], True)
    txt = "Approved by @{}\n\n{}".format(
        query.from_user.username, query.message.caption)

    p_txt = "\n{}".format(query.message.caption)

    await bot.edit_message_caption(
        caption=txt,
        chat_id=-1001702851184,
        message_id=query.message.message_id
    )
    await bot.send_photo(
        chat_id="@cleanfits",
        photo=query.message.photo[0].file_id,
        caption=p_txt,
        reply_markup=posted_markup(callback_data["sid"])
    )

@ dp.callback_query_handler(post_cb.filter(action=['decline', 'report']))
async def callback_post_decline(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    pass
