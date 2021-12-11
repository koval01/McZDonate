from database import PostSQL


def get_var(name_var: str, database_params: list) -> str:
    return [v["param"] for v in database_params if v["name"] == name_var][0]


# Значения из БД
dbparams = PostSQL().get_all_settings()

BOT_TOKEN = get_var("BOT_TOKEN", dbparams)
BOT_OWNER = get_var("BOT_OWNER", dbparams)

SRV_HOST = get_var("SRV_HOST", dbparams)
SRV_SECRET = get_var("SRV_SECRET", dbparams)

QIWI_TOKEN = get_var("QIWI_TOKEN", dbparams)
QIWI_WALLET = get_var("QIWI_WALLET", dbparams)
QIWI_WALLET_NICKNAME = get_var("QIWI_WALLET_NICKNAME", dbparams)
