from db.model import BotUser, Store


def user_data_with_bid(bid):
    user = BotUser.get(BotUser.bot_id == bid)
    print(type(user))
    # user = BotUser.select().where(BotUser.bot_id==bid)
    return user


def store_exists(user):
    query = Store.select().where(Store.user == user)
    return query.exists()


def user_exists(bot_id):
    query = BotUser.select().where(BotUser.bot_id == bot_id)
    return query.exists()


def create_bot_user(payload):
    exists = user_exists(payload["bot_id"])
    if not exists:
        try:
            bot_user = BotUser(
                username=payload["username"],
                first_name=payload["name"],
                bot_id=payload["bot_id"])
            bot_user.save()
        except Exception as e:
            raise Exception("Error saving user {}".format(e))
        return exists

    return exists


def update_basic(payload):
    try:
        query = BotUser.update(email=payload["email"]).where(
            BotUser.bot_id == payload["bot_id"])
        query.execute()
    except Exception as e:
        raise Exception("Error updating user data, %s", e)


def check_store_stat(bid):
    stat = True
    all_stores = []
    # user = BotUser.get(BotUser.bot_id == bid)
    try:
        stores = Store.select().join(BotUser).where(Store.user.bot_id == bid)
        [all_stores.append(x) for x in stores]
    except Exception as e:
        stat = False
        print(e, " some error")
    return (stat, all_stores)
    # print(s)


def create_store(payload, bid):
    stat, loc = False, False
    # loc = False
    user = BotUser.get(BotUser.bot_id == bid)
    if payload['location'] == "lyes":
        loc = True
    if not store_exists(user):
        st = Store(
            user=user,
            category=payload['cat'],
            has_location=loc,
            store_name=payload["name"]
        )
        st.save()
        stat = True
    return stat


def get_store(store_id):
    store = Store.get_by_id(store_id)
    return store


def check_store_status(bid):
    pass
