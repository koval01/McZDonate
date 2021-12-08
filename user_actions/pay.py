import logging
from aiogram.types.message import Message

import config
import database
from additional.utils import get_name_, notify_


async def init_pay(message: Message, sum_: int, user_: int) -> None:
    """
    Функция для передачи гривен
    :param message: Тело сообщения
    :param sum_: Сумма
    :param user_: Получатель
    :return:
    """
    name_ = await get_name_(message)

    try:
        if not database.PostSQL(message).check_user(custom_user=user_):
            await message.reply("Ошибка, не удалось найти получателя.")
            return

        if int(database.PostSQL(message).check_user()[2]) < sum_:
            await message.reply("Недостаточно гривен!")
            return

        if sum_ < 100:
            await message.reply("Минимум 100 гривен!")
            return

        # Сначала пробуем снять монеты со счёта отправителя
        try:
            database.PostSQL(message).modify_balance(
                sum_, take=True,
            )
        except Exception as e:
            logging.error(e)
            return

        # Посчитаем комиссию
        recount_ = (config.COM_TRANS / 100)
        coef_ = float(sum_) * float(recount_)
        com_result = round(float(sum_) - float(coef_))

        # Если получилось снять, то теперь пробуем зачислить
        try:
            database.PostSQL(message).modify_balance(
                com_result, custom_user=user_,
            )
        except Exception as e:
            logging.error(e)
            return

        # Уведомим получателя
        await notify_("На счёт было зачислено <b>%d</b> гривен от <b>%s</b>, комиссия <b>%d%%</b>" % (
            com_result, name_, config.COM_TRANS
        ), user_)

    except Exception as e:
        await message.reply("Что-то пошло не так, проверьте правильно лы всё ввели"
                            " и убедитесь - существует ли получатель.")
        logging.warning(e)
        return

    return True
