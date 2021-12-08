import asyncio
from aiogram import executor

from dispatcher import dp

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=True)
    # Запускаем лонгполлинг, если бот запущен от bot.py
