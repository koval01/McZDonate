import logging
import re

from database import PostSQL

list_services = [
    {"id": 0, "name": "Гоша", "type": "prefix", "price": 50},
    {"id": 1, "name": "ЖоРРик", "type": "prefix", "price": 50},
    {"id": 2, "name": "ВалерчиК", "type": "prefix", "price": 50},
    {"id": 3, "name": "Большой БРАТ", "type": "prefix", "price": 50},
    {"id": 4, "name": "VIP", "type": "rank", "price": 200},
]  # статический список услуг для теста


def get_list(services) -> list:
    return [
        "#%d-%s %s (%d RUB)" % (s["id"], s["type"], s["name"], s["price"])
        for s in services
    ]


def get_service_from_str(msg_text: str) -> int:
    try:
        value = int(re.findall(r"#\d*", msg_text)[0][1:])
        logging.debug("%s: %s" % (get_service_from_str.__name__, value))
        return value
    except Exception as e:
        logging.error("%s: %s" % (get_service_from_str.__name__, e))
        return 0


def service_check_(msg_text: str) -> str:
    return re.findall(r"#\d*-\w", msg_text)[0]


def get_status_from_receipt(receipt: dict) -> str:
    services = PostSQL().get_service(receipt["service_id"])
    return f'Игрок: {receipt["name_player"]}\n' \
           f'Номер чека: {receipt["id"]}\n' \
           f'Услуга: {services["name"]}\n' \
           f'Цена: {receipt["price"]:.2f} RUB\n' \
           f'Статус: {receipt["status_pay"]}'
