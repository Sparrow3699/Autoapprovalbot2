from asyncio import gather
from pyrogram import Client
from pyrogram.filters import group, channel, chat
from pyrogram.handlers import ChatJoinRequestHandler
from pyrogram.types import Message

from bot import bot, CHAT_IDS, APPROVE_MESSAGE_TEXT
from bot.helpers.message_utils import sendCustom
from bot.helpers.utils import update_users


async def on_join_request(client: Client, message: Message):
    user_id = message.from_user.id
    await gather(update_users(user_id, 'tag', message.from_user.mention),
                 client.approve_chat_join_request(message.chat.id, user_id),
                 sendCustom(APPROVE_MESSAGE_TEXT, user_id))


bot.add_handler(ChatJoinRequestHandler(on_join_request, (group | channel) & chat(list(CHAT_IDS)) if CHAT_IDS else (group | channel)))
