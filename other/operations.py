import logging
import re

from database import PostSQL
from other.giver import ServiceGiver
from other.qiwi import QiwiApi
from other.services import get_status_from_receipt
from other.static_msg import *


async def give_service_(receipt, receipt_id, message) -> None:
    try:
        logging.info("Give service init for receipt: %d" % receipt_id)
        ServiceGiver(receipt).execute()
        PostSQL().update_status(receipt_id, status="done")
        await message.reply(service_done)
    except Exception as e:
        logging.error("Error give service: %s" % e)


async def receipt_process(message) -> None:
    try:
        receipt_id = int(re.sub(
            r'/receipt_([0-9]*)?.*', r'\1', message.text
        ))
        receipt = PostSQL().get_status(receipt_id)
        if receipt["user_id_bot"] == message.from_user.id:
            if receipt["status_pay"] == 'wait':
                await message.reply(qiwi_check)
                check_result = QiwiApi().check_qiwi_receipt(receipt["bill_id_qiwi"])
                if check_result:
                    PostSQL().update_status(receipt_id, status="paid")
                    await message.reply(qiwi_ok)
                else:
                    await message.reply(qiwi_err)
            if receipt["status_pay"] == 'paid':
                await give_service_(receipt, receipt_id, message)
            await message.reply("%s\n\n%s" % (
                get_status_from_receipt(PostSQL().get_status(receipt_id)),
                thr_receipt
            ))
    except Exception as e:
        logging.error("Receipt get error: %s" % e)
        await message.reply(receipt_get_error)
