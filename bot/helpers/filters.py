from pyrogram.filters import create

from bot import SUDO, OWNER_ID, LOGGER


class CustomFilters:
    @staticmethod
    async def owner_filter(_, message):
        user = message.from_user or message.sender_chat
        return user.id == OWNER_ID

    owner = create(owner_filter)

    @staticmethod
    async def sudo_user(_, message):
        user = message.from_user or message.sender_chat
        # return user.id == OWNER_ID or user.id in SUDO
        is_sudo = user.id == OWNER_ID or user.id in SUDO
        LOGGER.info(is_sudo)
        LOGGER.info(user.id)
        LOGGER.info(OWNER_ID)
        LOGGER.info(SUDO)
        return is_sudo

    sudo = create(sudo_user)
