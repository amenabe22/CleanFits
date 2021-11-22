from db.model import Post, Store, BotUser


def create_post(post):
    try:
        p = None
        username = None
        if post["c_method"] == "phone":
            p = post["contact"]
        else:
            username = post["contact"]
        store = Store.get_by_id(post["store"])
        post = Post(
            name=post["item_name"],
            desc=post["desc"],
            price=post["price"],
            brand=post["brand"],
            contact_method=post["c_method"],
            phone=p,
            username=username,
            store=store
        )
        post.save()
        return post
    except Exception as e:
        raise Exception("Error saving post {}".format(e))


def set_approval(post, status):
    x = Post.update(approved=status).where(Post.id == post)
    x.execute()
    print(x, "dawg")
