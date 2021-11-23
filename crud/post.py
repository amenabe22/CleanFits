from db.model import Post, Store, BotUser


def create_post(post, chat_id):
    bot_user = BotUser.get(BotUser.bot_id == chat_id)
    print(bot_user, "The user")
    try:
        print("---------------")
        print(post)
        print("---------------")
        p = None
        store = None
        username = None
        if post["c_method"] == "phone":
            p = post["contact"]
        else:
            username = post["contact"]
        if post['quick']:
            store = None
        else:
            store = Store.get_by_id(post["store"])

        post = Post(
            name=post["item_name"],
            desc=post["desc"],
            price=post["price"],
            brand=post["brand"],
            contact_method=post["c_method"],
            phone=p,
            pic=post["pic"],
            category=post["item_type"],
            username=username,
            store=store,
            user=bot_user
        )
        post.save()
        return post
    except Exception as e:
        raise Exception("Error saving post {}".format(e))


def set_approval(post, status):
    post = Post.get_by_id(post)
    x = Post.update(approved=status).where(Post.id == post)
    x.execute()
    return post 


def get_post(post):
    return Post.get_by_id(post)
