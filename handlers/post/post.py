import typing
from aiogram import types
from db.model import Post
from loader import dp, bot
from crud.core import get_store
from buttons.inlines import inline_kb
from filters.core import QuickPostFilter
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from crud.post import create_post, set_approval, get_post
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_media_group import MediaGroupFilter, media_group_handler
from constants.inline_kbs import BRANDS, PROD_CATS, POST_MANAGE, POST_USER_MANAGE, CONTACT_OPTS
from utils.bot_helpers import format_post, format_post_final, format_from_post, format_from_post_final

post_cb = CallbackData('post', 'action', 'sid')


def message_link_btn(message_id):
    ikb = types.InlineKeyboardMarkup(row_width=1)
    link = "https://t.me/cleanfits/"+message_id
    ikb.add(*[types.InlineKeyboardButton(
        "See Post", url=link
    )])
    return ikb


def inline_post_kb(items, cbk, pst):
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.add(*[
        types.InlineKeyboardButton(
            x["label"], callback_data=cbk.new(
                action=x["id"], sid=pst)) for x in items
    ])
    return ikb


def posted_markup(message, post):
    ikb = types.InlineKeyboardMarkup(row_width=2)
    ikb.add(*[
        types.InlineKeyboardButton(
            x["label"], url='https://t.me/share/url?url='+message) for x in [
            {"label": "🏹 Share", "id": "share"},
        ]
    ])
    print(post.username, "bitch")
    if post.contact_method == "telegram":
        ikb.add(
            types.InlineKeyboardButton(
                text='🤙 Contact', url='https://t.me/'+post.username,
            )
        )

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

@dp.message_handler(commands='quick')
async def quick_post_cmd(message: types.Message, state: FSMContext):
    await state.set_state(PostForm.item_name)
    async with state.proxy() as data:
        data["quick"] = True
        await message.answer(
            "Enter Item Name",
        )

@dp.message_handler(QuickPostFilter())
async def quick_post(message: types.Message, state: FSMContext):
    await state.set_state(PostForm.item_name)
    async with state.proxy() as data:
        data["quick"] = True
        await message.answer(
            "Enter Item Name",
        )


@ dp.message_handler(state=PostForm.pictures, content_types=[types.ContentType.PHOTO])
# @dp.message_handler( content_types=[types.ContentType.PHOTO])
async def process_single_pic(message: types.Message,  state: FSMContext):
    async with state.proxy() as data:
        # await state.set_state(PostForm.item_type)
        await state.finish()
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
        pst = create_post(data, message.chat.id)
        # await state.finish()
        await message.answer(text=format_post(data), parse_mode='HTML', reply_markup=inline_post_kb(POST_USER_MANAGE, post_cb, pst))

        await state.finish()


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

        data["quick"] = False
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
    print(callback_data, "bitch stfu")
    print(callback_data_action)
    pst = get_post(callback_data['sid'])
    if callback_data_action == "publish":
        # callback_data_action = callback_data['action']
        async with state.proxy() as data:
            if not pst.quick_post:
                # store = get_store(data["store"])
                await bot.send_photo(
                    -1001702851184, pst.pic,
                    reply_markup=post_inline_kb(
                        post_cb, pst),
                    caption=format_from_post_final(pst, pst.store))
            else:
                await bot.send_photo(
                    -1001702851184, pst.pic,
                    reply_markup=post_inline_kb(
                        post_cb, pst),
                    caption=format_from_post_final(pst))

            await bot.edit_message_text(
                format_from_post(pst),
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

        if(callback_data_action == "telegram"):
            data["c_method"] = "telegram"
            data["contact"] = query.message.chat.username
            print(query.message.from_user.id, "whoa man")
            # await bot.edit_message_text(
            #     "Contact method saved",
            #     query.from_user.id,
            #     query.message.message_id,
            # )
            # await state.set_state(PostForm.contact)
            # await state.finish()
            print("assssssssss")
            print(query.message.chat)
            print("assssssssss")
            pst = create_post(data, query.message.chat)
            formatted = format_post(data)
            await bot.edit_message_text(formatted,
                                        query.from_user.id,
                                        query.message.message_id,
                                        reply_markup=inline_post_kb(
                                            POST_USER_MANAGE, post_cb, pst.id),
                                        )
            await state.finish()

        else:
            data["c_method"] = "phone"
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
    post = set_approval(callback_data["sid"], True)

    txt = "Approved by @{}\n\n{}".format(
        query.from_user.username, query.message.caption)

    p_txt = "\n{}".format(query.message.caption)

    await bot.edit_message_caption(
        caption=txt,
        chat_id=-1001702851184,
        message_id=query.message.message_id
    )
    print("^"*30)
    print(p_txt)
    print("^"*30)
    print(query.message.caption_entities)
    print("^"*30)
    try:
        response = await bot.send_photo(
            caption_entities=query.message.caption_entities,
            chat_id="@cleanfits",
            photo=query.message.photo[0].file_id,
            caption=p_txt,
            reply_markup=posted_markup(
                p_txt, post))
    except Exception as e:
        raise Exception(e)
    message = "Congrats your post has been approved."
    await bot.send_message(post.user.bot_id, message, reply_markup=message_link_btn(str(response.message_id)))


@ dp.callback_query_handler(post_cb.filter(action=['decline', 'report']))
async def callback_post_decline(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
    pass


# @ dp.callback_query_handler(post_cb.filter(action=['share']))
# async def callback_post_share(query: types.CallbackQuery, callback_data: typing.Dict[str, str], state: FSMContext):
#     pass
