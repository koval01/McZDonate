from aiogram import executor
import asyncio

from handlers import *
from other.utils import scheduler
from dispatcher import dp

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
