import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter, \
    IsPrivateFilter, IsGroupFilter
from other.load_params import *

# Конфигурация логинга
logging.basicConfig(level=logging.INFO)

# Условие запуска
if not BOT_TOKEN:
    exit("Не указан токен бота")

# Инициализируем хранилище и диспетчер бота
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

# Инициализируем фильтры
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)
dp.filters_factory.bind(IsPrivateFilter)
dp.filters_factory.bind(IsGroupFilter)
