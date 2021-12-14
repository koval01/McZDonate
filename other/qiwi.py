import logging
from pyqiwip2p import QiwiP2P

from other.load_params import *


class QiwiApi:
    def __init__(self, sum_=None, receipt_id=None):
        self.qiwi_token = QIWI_PRIVATE_KEY
        self.p2p_qiwi = QiwiP2P(auth_key=self.qiwi_token)
        self.sum_ = sum_
        self.receipt_id = receipt_id

    def create_qiwi_receipt(self, bill_id, service) -> object:
        try:
            return self.p2p_qiwi.bill(
                bill_id=bill_id, amount=self.sum_, lifetime=30,
                comment="Оплата чека на Zalupa.online; Чек: %d; Услуга: %s" % (self.receipt_id, service)
            )
        except Exception as e:
            logging.error("QIWI create receipt error: %s" % e)

    def cancel_qiwi_receipt(self, bill_id) -> None:
        try:
            self.p2p_qiwi.reject(bill_id=bill_id)
        except Exception as e:
            logging.error(e)

    def check_qiwi_receipt(self, bill_id) -> bool:
        if self.p2p_qiwi.check(bill_id=bill_id).status == "PAID":
            return True
        return False
