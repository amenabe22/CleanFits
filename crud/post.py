from db.model import Post, Store, BotUser


def create_post(post):
    try:
        store = Store.get_by_id(post["store"])
        post = Post(
            name=post["name"],
            desc=post["desc"],
            price=post["price"],
            brand=post["brand"],
            store=store
        )
        post.save()
    except Exception as e:
        raise Exception("Error saving post {}".format(e))

