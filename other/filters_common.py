import logging

from database import PostSQL
from other.static_msg import banlist_msg

from aiogram.types.message import Message


async def user_in_banlist(message: Message) -> list:
    return PostSQL().get_banlist(message.from_user.id)


async def banned_user(message: Message) -> None:
    try:
        data = PostSQL().get_banlist(message.from_user.id)
        if data:
            comment = data[0]["comment"]
            await message.answer(banlist_msg % comment)
    except Exception as e:
        logging.error("Error function banned_user: %s" % e)
