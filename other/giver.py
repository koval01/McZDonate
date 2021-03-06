import logging

from mcrcon import MCRcon
from database import PostSQL
from other.load_params import *


class ServiceGiver:
    def __init__(self, receipt: dict):
        self.host = SRV_HOST
        self.secret = SRV_SECRET
        self.receipt = receipt
        self.port = RCON_PORT

    def get_service(self) -> dict:
        return PostSQL().get_service(self.receipt["service_id"])

    def commands(self) -> list:
        service = self.get_service()
        return str(service["command"]).replace(
            "%_player%_", self.receipt["name_player"]).split("\n")

    def execute(self) -> bool:
        commands = self.commands()
        try:
            with MCRcon(self.host, self.secret, port=int(self.port)) as rcon:
                for cmd in commands:
                    rcon.command(cmd)
            return True
        except Exception as e:
            logging.error("Giver execute error: %s" % e)
        return False
