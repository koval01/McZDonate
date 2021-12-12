import logging
import requests_cache

from urllib.parse import urlencode

from other.load_params import *


class QiwiApi:
    def __init__(self, sum_, receipt_id):
        self.qiwi_token = QIWI_TOKEN
        self.qiwi_nick = QIWI_WALLET_NICKNAME
        self.url = "https://edge.qiwi.com/payment-history" \
                   "/v2/persons/%s/payments" % QIWI_WALLET
        self.pay_link = "https://qiwi.com/payment/form/99999"
        self.sum_ = sum_
        self.receipt_id = receipt_id
        self.session_req = requests_cache.CachedSession(
            'qiwi_api', backend="memory")

    def request(self) -> (dict, dict) or None:
        resp = self.session_req.get(url=self.url, headers={
            "Authorization": "Bearer %s" % self.qiwi_token
        }, params={
            "rows": 50,
            "operation": "IN",
            "sources": "QW_RUB",
        })
        if resp.status_code >= 200 < 400:
            resp = resp.json()
            if len(resp): return resp["data"], resp

    def check_receipt(self) -> bool:
        data, orig_data = self.request()
        comment = "Оплата чека #%d" % self.receipt_id
        try:
            checked = [
                rc for rc in data
                if rc["type"] == "IN"
                   and rc["status"] == "SUCCESS"
                   and rc["sum"]["amount"] == self.sum_
                   and rc["comment"] == comment
            ]
            return len(checked) != 0
        except TypeError as e:
            logging.warning("Error check qiwi receipt: %s" % e)
            return False

    def generate_link(self) -> str:
        params = {
            "amountInteger": self.sum_,
            "amountFraction": 0,
            "currency": 643,
            "extra['comment']": "Оплата чека #%d" % self.receipt_id,
            "extra['account']": self.qiwi_nick
        }
        return "%s?%s" % (self.pay_link, urlencode(params))
