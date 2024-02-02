from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from time import time

from bot import bot, users, CMD_BROADCAST
from bot.helpers.filters import CustomFilters
from bot.helpers.message_utils import sendMessage, copyMessage, sendCustom, editMessage
from bot.helpers.utils import get_readable_time


async def reset_user(_, message: Message):
    reply_to = message.reply_to_message
    total = len(users)
    if not reply_to and len(message.command) == 1 or not total:
        await sendMessage('Send command along with message or reply to a message!', message)
        return
    msg = await sendMessage(f'<i>Found {total} user. Sending broadcast message, please wait...</i>', message)
    sucess = 0
    for user in users:
        if reply_to:
            res = await copyMessage(reply_to, user)
        else:
            res = await sendCustom(message.text.split(maxsplit=1)[-1], user)
        if res:
            sucess += 1

    text = 'Message has been sended to users\n'
    text += f'<b>Total:</b> {total}\n'
    text += f'<b>Sucess:</b> {sucess}\n'
    text += f'<b>Failed:</b> {total - sucess}\n'
    text += f'<b>Time Taken:</b> {get_readable_time(time() - message.date.timestamp())}'
    await editMessage(text, msg)


bot.add_handler(MessageHandler(reset_user, command(CMD_BROADCAST) & CustomFilters.sudo))
