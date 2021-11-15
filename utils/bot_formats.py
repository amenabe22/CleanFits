def format_account(user):
    ver = "❌"
    if user.verified:
        ver = "✅"
    account_format = """Full Name: {}\nEmail: {}\nVerified: {}""".format(
        user.first_name,
        user.email,
        ver
    )
    return account_format
