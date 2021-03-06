from database import PostSQL
from other.config import DEBUG


def get_var(name_var: str, database_params: list) -> str:
    """
    Загрузчик значений из БД
    :param name_var: Имя параметра
    :param database_params: Массив со всеми параметрами из БД
    :return: Полученое значение параметра
    """
    return [v["param"] for v in database_params if v["name"] == name_var][0]


# Значения из БД
dbparams = PostSQL().get_all_settings()

if DEBUG:
    BOT_TOKEN = "5041807584:AAEA3umuc_QAkhLIAwHHfKI6u6mdtX9FI88"  # test token
else:
    BOT_TOKEN = get_var("BOT_TOKEN", dbparams)

BOT_OWNER = get_var("BOT_OWNER", dbparams)

SRV_HOST = get_var("SRV_HOST", dbparams)
SRV_SECRET = get_var("SRV_SECRET", dbparams)
RCON_PORT = get_var("RCON_PORT", dbparams)

QIWI_PRIVATE_KEY = get_var("QIWI_PRIVATE_KEY", dbparams)
