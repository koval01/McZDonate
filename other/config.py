import os

# Значения подтягиваются из виртуального окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_OWNER = os.environ.get("BOT_OWNER")

SRV_HOST = os.environ.get("SRV_HOST")
SRV_SECRET = os.environ.get("SRV_SECRET")

QIWI_TOKEN = os.environ.get("QIWI_TOKEN")
QIWI_WALLET = os.environ.get("QIWI_WALLET")
QIWI_WALLET_NICKNAME = os.environ.get("QIWI_WALLET_NICKNAME")

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
