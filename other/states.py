from aiogram import types

from database import PostSQL
from other import buttons
from other.actions_outside import SellStates
from other.buttons import create_inline_buttons
from other.qiwi import QiwiApi
from other.services import get_list as get_list_services
from other.services import get_service_from_str, service_check_
from other.static_msg import *
from other.utils import nick_check


async def nick_state(message, state) -> None:
    if message.text == buttons.cancel_text:
        pass
    elif nick_check(message.text):
        list_services = PostSQL().get_all_services()  # получаем услуги
        buttons_donate = await create_inline_buttons(get_list_services(list_services))
        return await state.update_data(player_name=str(message.text)), await SellStates.next(), \
               await message.reply(
                   "Был получен никнейм - %s\n"
                   "Выберите что Вы хотите купить." % message.text,
                   reply_markup=buttons_donate
               )

    else:
        await message.reply(nick_error)
    return await state.finish(), await message.reply(
        canceled, reply_markup=types.ReplyKeyboardRemove()
    )


async def sell_donate(message, state) -> None:
    service_id = get_service_from_str(message.text)
    if message.text == buttons.cancel_text:
        pass
    elif service_check_(message.text):
        async with state.proxy() as data:
            list_services = PostSQL().get_all_services()  # обновляем список услуг
            service_ = [s for s in list_services if s["id"] == service_id][0]

            await message.reply(
                "Был получен выбор - \"%s\"\n"
                "Никнейм - %s\n"
                "Осталось оплатить. Цена - %d RUB" % (
                    message.text, data["player_name"], service_["price"]
                )
            )
            receipt = PostSQL().add_pay(
                data["player_name"], service_id, service_["price"], message.from_user.id
            )
            qiwi_link = QiwiApi(service_["price"], receipt).generate_link()
            return await message.reply(
                "Ссылка для оплаты: <a href=\"%s\">тык</a>\nПроверить чек - /receipt_%d\n\n%s" % (
                    qiwi_link, receipt, qiwi_disclaimer
                )
            ), await state.finish()

    else:
        await message.reply(service_error)
    return await state.finish(), await message.reply(
        canceled, reply_markup=types.ReplyKeyboardRemove()
    )
