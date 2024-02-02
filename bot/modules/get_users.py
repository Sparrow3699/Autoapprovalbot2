from pyrogram.filters import command
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from bot import bot, users, CMD_USERS
from bot.helpers.filters import CustomFilters
from bot.helpers.message_utils import sendMessage


async def get_users(_, message: Message):
    usr = [value.get('tag') for value in users.values()]
    text = f'<b>Total {len(usr)} Users Connected</b>\n\n'
    text += '<b> | </b>'.join(x or 'Unknown' for x in usr) if usr else 'No users!'
    await sendMessage(text, message)


bot.add_handler(MessageHandler(get_users, command(CMD_USERS) & CustomFilters.sudo))
