from time import time
from random import randrange


def generate_bill_id() -> str:
    """
    Генератор Bill ID`s
    :return: example - 58e43ed61451dd9b20
    """
    return hex(int(str("%.5f%d" % (
        time(), randrange(9999*101, 99999*100))
    ).replace(".", "")))[2:]
