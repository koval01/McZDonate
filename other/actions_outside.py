from aiogram.dispatcher.filters.state import State, StatesGroup

from other.static_msg import *


async def throttled_qiwi(*args, **kwargs):
    message = args[0]
    await message.answer(throttled_check_pay)


class SellStates(StatesGroup):
    sell_nick = State()
    sell_service = State()
