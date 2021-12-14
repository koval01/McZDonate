from time import time
from random import randrange


def generate_bill_id() -> str:
    return hex(int(str("%.5f%d" % (
        time(), randrange(9999*101, 99999*100))
    ).replace(".", "")))[2:]
