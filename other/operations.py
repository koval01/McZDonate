import logging
import re

from database import PostSQL
from other.giver import ServiceGiver
from other.qiwi import QiwiApi
from other.services import get_status_from_receipt
from other.static_msg import *


async def receipt_process(message) -> None:
    try:
        receipt_id = int(re.sub(
            r'/receipt_([0-9]*)?.*', r'\1', message.text
        ))
        receipt = PostSQL().get_status(receipt_id)
        if receipt["user_id_bot"] == message.from_user.id:
            if receipt["status_pay"] == 'wait':
                await message.reply(qiwi_check)
                check_result = QiwiApi(receipt["price"], receipt_id).check_receipt()
                if check_result:
                    PostSQL().update_status(receipt_id, "paid")
                    await message.reply(qiwi_ok)

                    ServiceGiver(receipt).execute()
                    PostSQL().update_status(receipt_id, "done")
                    await message.reply(service_done)
                else:
                    await message.reply(qiwi_err)
            await message.reply("%s\n\n%s" % (
                get_status_from_receipt(receipt),
                thr_receipt
            ))
    except Exception as e:
        logging.error("Receipt get error: %s" % e)
        await message.reply(receipt_get_error)
