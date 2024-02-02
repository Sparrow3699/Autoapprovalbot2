from aiofiles import open as aiopen
from asyncio import create_subprocess_exec
from os import execl as osexecl
from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from sys import executable

from bot import bot, CMD_RESTART
from bot.helpers.filters import CustomFilters
from bot.helpers.message_utils import sendMessage


async def restart(_, message: Message):
    msg = await sendMessage('<i>Restarting, please wait...</i>', message)
    await (await create_subprocess_exec('python3', 'update.py')).wait()
    async with aiopen('.restartmsg', 'w') as f:
        await f.write(f'{msg.chat.id}\n{msg.id}\n')
    osexecl(executable, executable, '-m', 'bot')


bot.add_handler(MessageHandler(restart, command(CMD_RESTART) & CustomFilters.sudo))
