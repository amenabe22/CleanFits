def format_account(user):
    ver = "❌"
    if user.verified:
        ver = "✅"
    account_format = """<b>Full Name:</b> {}\n\n<b>Email:</b> {}\n\n<b>Verified:</b> {}""".format(
        user.first_name,
        user.email,
        ver
    )
    return account_format
