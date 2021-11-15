from db.model import BotUser


def user_data_with_bid(bid):
    user = BotUser.get(BotUser.bot_id == bid)
    print(type(user))
    # user = BotUser.select().where(BotUser.bot_id==bid)
    return user


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
