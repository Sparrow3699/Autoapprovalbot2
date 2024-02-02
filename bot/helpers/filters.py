from pyrogram.filters import create
from pyrogram.types import Message

from bot import SUDO, OWNER_ID


class CustomFilters:
    @staticmethod
    async def owner_filter(_, message: Message):
        user = message.from_user or message.sender_chat
        return user.id == OWNER_ID

    owner = create(owner_filter)

    @staticmethod
    async def sudo_user(_, message: Message):
        user = message.from_user or message.sender_chat
        return user.id == OWNER_ID or user.id in SUDO

    sudo = create(sudo_user)
