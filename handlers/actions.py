import logging
from aiogram import types

import config
from dispatcher import dp


@dp.message_handler(commands=['start'], is_private=True)
@dp.throttled(rate=3)
async def start_for_private(message: types.Message):
    pass
