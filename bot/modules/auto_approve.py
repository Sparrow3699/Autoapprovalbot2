from asyncio import gather
from pyrogram import Client
from pyrogram.filters import group, channel, chat
from pyrogram.handlers import ChatJoinRequestHandler
from pyrogram.types import Message

from bot import bot, CHAT_IDS, APPROVE_MESSAGE_TEXT, LOG_CHANNEL
from bot.helpers.message_utils import sendCustom
from bot.helpers.utils import update_users


async def on_join_request(client: Client, message: Message):
    user_id = message.from_user.id
    chat = await client.get_chat(message.chat.id)
    text = 'Congratulation, your request was approved!\n\n'
    text += '<b>CHAT INFO</b>\n'
    text += f'<b>Title:</b> {chat.title}\n'
    text += f'<b>ID:</b> <code>{chat.id}</code>\n'
    text += f'<b>Type:</b> {chat.type.name.title()}\n'
    text += f'<b>Member:</b> {chat.members_count}\n'
    text += f'<b>Data Center:</b> {chat.dc_id or "Unknown"}\n'
    text += f'<b>Protect Content:</b> {chat.has_protected_content}'
    await gather(update_users(user_id, 'tag', message.from_user.mention),
                 client.approve_chat_join_request(message.chat.id, user_id),
                 sendCustom(text, user_id))
    if LOG_CHANNEL:
        text = f'{message.from_user.mention} <code>({user_id})</code>, approved by tp join <b>{chat.title}</b> ({chat.type.name.title()})'
        await sendCustom(text, LOG_CHANNEL)


bot.add_handler(ChatJoinRequestHandler(on_join_request, (group | channel) & chat(list(CHAT_IDS)) if CHAT_IDS else (group | channel)))
