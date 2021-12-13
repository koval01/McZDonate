from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from dispatcher import dp
from other.actions_outside import *
from other.operations import *
from other.states import *
from other.filters_common import banned_user


@dp.message_handler(commands=['start'], is_private=True, is_banned=False)
@dp.throttled(rate=2)
async def start_message(message: types.Message):
    await start_buy(message)


@dp.message_handler(commands=['cancel'], is_private=True, is_banned=False)
@dp.throttled(rate=2)
async def start_message(message: types.Message):
    await cancel_receipts(message)


@dp.message_handler(state=SellStates.sell_nick, is_private=True, is_banned=False)
async def sell_donate_state_nick(message: types.Message, state: FSMContext):
    await nick_state(message, state)


@dp.message_handler(state=SellStates.sell_service, is_private=True, is_banned=False)
async def sell_donate_state_nick(message: types.Message, state: FSMContext):
    await sell_donate(message, state)


@dp.message_handler(filters.RegexpCommandsFilter(
    regexp_commands=['receipt_([0-9]*)']), is_private=True, is_banned=False)
@dp.throttled(throttled_qiwi, rate=5)
async def receipt_message(message: types.Message):
    await receipt_process(message)


@dp.message_handler(is_private=True)
@dp.throttled(rate=5)
async def start_message(message: types.Message):
    await banned_user(message)
