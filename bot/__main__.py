from aiofiles.os import path as aiopath, remove
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from time import time
from asyncio import gather

from bot import bot, bot_loop, config_dict, start_time, LOGGER, OWNER_ID, CMD_START
from bot.helpers.message_utils import sendMessage, sendCustom, editCustom
from bot.helpers.utils import get_readable_time
from bot.modules import auto_approve, broadcast, get_log, get_users, restart


async def start(_, message: Message):
    await sendMessage(f'Bot started since {get_readable_time(time() - start_time)}.', message)


async def main():
    if await aiopath.isfile('.restartmsg'):
        with open('.restartmsg') as f:
            chat_id, message_id  = map(int, f)
        await gather(editCustom('Restarted Successfully!', chat_id, message_id), remove('.restartmsg'))
    else:
        await sendCustom('Bot Restarted!', OWNER_ID)
    bot.add_handler(MessageHandler(start, command(CMD_START)))
    LOGGER.info('Bot started @%s', bot.me.username)


bot_loop.run_until_complete(main())
bot_loop.run_forever()
