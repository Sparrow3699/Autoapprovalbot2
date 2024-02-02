from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from bot import bot, CMD_LOG
from bot.helpers.filters import CustomFilters
from bot.helpers.message_utils import sendFile


async def get_log(_, message: Message):
    await sendFile(message, 'log.txt', '<code>log.txt</code>')


bot.add_handler(MessageHandler(get_log, command(CMD_LOG) & CustomFilters.owner))
