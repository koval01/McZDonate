import logging

from aiogram import types
from aiogram.types.message import Message
from aiogram.dispatcher.storage import FSMContext

from database import PostSQL
from other import buttons
from other.actions_outside import SellStates
from other.buttons import create_inline_buttons
from other.qiwi import QiwiApi
from other.services import get_list as get_list_services
from other.services import get_service_from_str, service_check_
from other.static_msg import *
from other.utils import nick_check, sell_donate_process


async def nick_state(message: Message, state: FSMContext) -> None:
    if message.text == buttons.cancel_text:
        pass
    elif nick_check(message.text):
        list_services = PostSQL().get_all_services()
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


async def sell_donate(message: Message, state: FSMContext) -> None:
    try:
        service_id = get_service_from_str(message.text)
        if message.text == buttons.cancel_text:
            pass
        elif service_check_(message.text):
            await sell_donate_process(message, state, service_id)
    except Exception as e:
        logging.error("Donate select error: %s" % e)
        await message.reply(service_error)
    return await state.finish(), await message.reply(
        canceled, reply_markup=types.ReplyKeyboardRemove()
    )

async def cancel_receipts(message: Message) -> None:
    u_id = message.from_user.id
    receipts = PostSQL().get_receipts(u_id)
    if receipts:
        logging.debug("Cancel receipts user - %d" % message.from_user.id)
        PostSQL().delete_user_not_paid_receipts(u_id)
        [QiwiApi().cancel_qiwi_receipt(r["bill_id_qiwi"]) for r in receipts]
        await message.reply(cancel_receipt)
    else:
        await message.reply(not_found_receipt)


async def init_new_receipt(message: Message) -> bool:
    if PostSQL().get_receipts(message.from_user.id):
        await message.reply(limit_receipts)
        return False
    return True


async def start_buy(message: Message) -> None:
    if await init_new_receipt(message):
        await message.reply(start_answer, reply_markup=buttons.cancel)
        await SellStates.sell_nick.set()
