import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter, \
    IsPrivateFilter, IsGroupFilter, IsBanned
from other.load_params import *

logging.basicConfig(level=logging.INFO)

if not BOT_TOKEN:
    exit("Не указан токен бота")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)
dp.filters_factory.bind(IsPrivateFilter)
dp.filters_factory.bind(IsGroupFilter)
dp.filters_factory.bind(IsBanned)
