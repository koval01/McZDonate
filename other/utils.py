import logging
import re
import asyncio

from database import PostSQL
import aioschedule as schedule

from random import choice
from string import ascii_letters, digits

from aiogram.types.message import Message

from dispatcher import bot


def get_random_string(length=32) -> str:
    return "".join([choice(ascii_letters + digits) for _ in range(length)])


async def get_name_(message: Message) -> str:
    """
    Получаем имя пользователя
    :param message: Тело сообщения
    :return: Строка с именем пользователя
    """
    name_ = "Неизвестный"
    try:
        try:
            name_ = message.chat.title
        except Exception as e:
            logging.debug(e)

        if not name_:
            try:
                name_ = message.from_user.full_name
            except Exception as e:
                logging.debug(e)
    except Exception as e:
        logging.warning(e)

    return name_


async def notify_(text_: str, user_: int) -> bool:
    """
    Отправка уведомления
    :param text_: Текст
    :param user_: ID юзера
    :return: Результат отправки, успешно или нет
    """
    try:
        await bot.send_message(
            user_, text_,
        )
        return True
    except Exception as e:
        logging.warning(e)
        return False


def number_to_words(number: int) -> str:
    """
    Переводим число в пропись
    :param number: Число
    :return: Пропись
    """
    x = {1: 'одна', 2: 'две', 3: 'три', 4: 'четыре', 5: 'пять',
         6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'}
    y = {10: 'десять', 20: 'двадцать', 30: 'тридцать', 40: 'сорок',
         50: 'пятьдесят', 60: 'шестьдесят', 70: 'семьдесят',
         80: 'восемьдесят', 90: 'девяносто'}
    b = {11: 'одиннадцать', 12: 'двенадцать', 13: 'тринадцать',
         14: 'четырнадцать', 15: 'пятнадцать', 16: 'шестнадцать',
         17: 'семнадцать', 18: 'восемнадцать', 19: 'девятнадцать'}

    number_1 = number % 10
    number_2 = number - number_1

    if number < 10:
        return x.get(number)
    elif number >= 10 and number_2 == 0:
        return y.get(number)
    elif number > 20:
        return y.get(number_2) + ' ' + x.get(number_1)
    elif 10 < number < 20:
        return b.get(number)
    else:
        return 'Число вне диапазона среза!'


def nick_check(nick: str) -> bool:
    """
    Проверка ника на валидность
    :param nick: Строка с ником
    :return: Результат проверки
    """
    if re.sub(r"[^A-Za-z0-9_]*", "", nick) == nick \
            and 2 < len(nick) <= 40:
        return True


async def flush_old_receipt() -> None:
    try:
        PostSQL().delete_old_receipts()
        logging.debug("delete old receipts: loop")
    except Exception as e:
        logging.error(e)


async def scheduler():
    schedule.every().minute.do(flush_old_receipt)

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
