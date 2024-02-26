from time import time

from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

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
    success = 0
    for user in list(users):
        if reply_to:
            res = await copyMessage(reply_to, user)
        else:
            res = await sendCustom(message.text.split(maxsplit=1)[-1], user)
        if res:
            success += 1

    text = 'Broadcast message has been sent to users\n'
    text += f'<b>Total:</b> {total}\n'
    text += f'<b>Success:</b> {success}\n'
    text += f'<b>Failed:</b> {total - success}\n'
    text += f'<b>Time Taken:</b> {get_readable_time(time() - message.date.timestamp())}'
    await editMessage(text, msg)


bot.add_handler(MessageHandler(reset_user, command(CMD_BROADCAST) & CustomFilters.sudo))
