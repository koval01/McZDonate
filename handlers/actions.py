import logging

from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import PostSQL
from dispatcher import dp
from other import buttons
from other.buttons import create_inline_buttons
from other.services import get_list as get_list_services
from other.services import get_service_from_str, \
    service_check_, get_status_from_receipt
from other.static_msg import *
from other.utils import nick_check
from other.qiwi import QiwiApi
from other.giver import ServiceGiver

import re


class SellStates(StatesGroup):
    sell_nick = State()
    sell_service = State()


@dp.message_handler(commands=['start'], is_private=True)
@dp.throttled(rate=2)
async def start_message(message: types.Message):
    await message.reply(start_answer, reply_markup=buttons.cancel)
    await SellStates.sell_nick.set()


@dp.message_handler(state=SellStates.sell_nick)
async def sell_donate_state_nick(message: types.Message, state: FSMContext):
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


@dp.message_handler(state=SellStates.sell_service)
async def sell_donate_state_nick(message: types.Message, state: FSMContext):
    service_id = get_service_from_str(message.text)
    if message.text == buttons.cancel_text:
        pass
    elif service_check_(message.text):
        async with state.proxy() as data:
            list_services = PostSQL().get_all_services()  # обновляем список услуг
            service_ = list_services[service_id]
            await message.reply(
                "Был получен выбор - %s\n"
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
                "Ссылка для оплаты: <a href=\"%s\">тык</a>\nПроверить чек - /receipt_%d" % (
                    qiwi_link, receipt
                )
            ), await state.finish()

    else:
        await message.reply(service_error)
    return await state.finish(), await message.reply(
        canceled, reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['receipt_([0-9]*)']))
@dp.throttled(rate=15)
async def receipt_message(message: types.Message):
    try:
        receipt_id = int(re.sub(r'/receipt_([0-9]*)?.*', r'\1', message.text))
        receipt = PostSQL().get_status(receipt_id)
        if receipt["user_id_bot"] == message.from_user.id:
            if receipt["status_pay"] == 'wait':
                await message.reply(qiwi_check)
                check_result = QiwiApi(receipt["price"], receipt_id).check_receipt()
                if check_result:
                    PostSQL().update_status(receipt_id, "paid")
                    await message.reply(qiwi_ok)

                    ServiceGiver(receipt).execute()
                    await message.reply(service_done)
                else: await message.reply(qiwi_err)
                # return

            await message.reply("%s\n\n%s" % (
                get_status_from_receipt(receipt),
                thr_receipt
            )); return
    except Exception as e:
        logging.error("Receipt get: %s" % e)
        await message.reply(receipt_get_error)

