from aiogram import types
from aiogram.dispatcher.filters.builtin import Filter

class HomeNavigationFilter(Filter):
    async def check(self, message :types.Message):
        nav_str = "👈 Take me home"
        return message.text == nav_str

class StoreMenuMessage(Filter):
    
    async def check(self, message: types.Message):
        store_opts = ["🛍 My Stores", "Create Store"]
        return message.text in store_opts

class AccountMenuMessage(Filter):
    
    async def check(self, message: types.Message):
        store_opts = ["🔓 Account","⚙️ Settings"]
        return message.text in store_opts
