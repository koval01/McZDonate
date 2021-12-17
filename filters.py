from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from other import load_params
from other.filters_common import user_in_banlist


class IsOwnerFilter(BoundFilter):
    """
    Проверяем является ли пользователь владельцем бота
    """
    key = "is_owner"

    def __init__(self, is_owner):
        self.is_owner = is_owner

    async def check(self, message: types.Message):
        return int(message.from_user.id) == int(load_params.BOT_OWNER)


class IsBanned(BoundFilter):
    """
    Проверяем забанен ли юзер
    """
    key = "is_banned"

    def __init__(self, is_banned):
        self.is_banned = is_banned

    async def check(self, message: types.Message):
        return len(await user_in_banlist(message)) == 0


class IsAdminFilter(BoundFilter):
    """
    Проверяем ялвяется ли пользователь администратором
    """
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.is_chat_admin() == self.is_admin


class IsPrivateFilter(BoundFilter):
    """
    Проверяем является ли чат с ботом приватным
    """
    key = "is_private"

    def __init__(self, is_private: bool):
        self.is_private = is_private

    async def check(self, message: types.Message):
        return message.chat.type == "private"


class IsGroupFilter(BoundFilter):
    """
    Проверяем является ли чат с ботом групповым
    """
    key = "is_group"

    def __init__(self, is_group: bool):
        self.is_group = is_group

    async def check(self, message: types.Message):
        return message.chat.type in ["group", "supergroup"]


class MemberCanRestrictFilter(BoundFilter):
    """
    Filter that checks member ability for restricting
    aiogram code
    """
    key = 'member_can_restrict'

    def __init__(self, member_can_restrict: bool):
        self.member_can_restrict = member_can_restrict

    async def check(self, message: types.Message):
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

        return (member.is_chat_creator() or member.can_restrict_members) == self.member_can_restrict
