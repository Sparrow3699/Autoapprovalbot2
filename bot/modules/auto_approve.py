from asyncio import sleep
from os import path as ospath

from aiofiles.os import makedirs, remove, path as aiopath
from pyrogram import Client
from pyrogram.filters import group, channel, chat
from pyrogram.handlers import ChatJoinRequestHandler
from pyrogram.types import Message

from bot import bot, CHAT_IDS, LOG_CHANNEL
from bot.helpers.message_utils import sendCustom, sendPhotoTo
from bot.helpers.utils import update_users


async def on_join_request(client: Client, message: Message):
    user_id = message.from_user.id
    chat = await client.get_chat(message.chat.id)
    text = '<b>CHAT INFO</b>\n'
    text += f'<b>Title:</b> {chat.title}\n'
    text += f'<b>ID:</b> <code>{chat.id}</code>\n'
    text += f'<b>Type:</b> {chat.type.name.title()}\n'
    text += f'<b>Member:</b> {chat.members_count}\n'
    text += f'<b>Data Center:</b> {chat.dc_id or "Unknown"}\n'
    text += f'<b>Protect Content:</b> {chat.has_protected_content}\n\n'
    text += f'Hey there {message.from_user.mention}, congratulation, your request was approved✅ Shop now! 95% off – unbeatable deals, limited time only! Visit @SmartSavingsClub'

    image = ''
    if chat.photo:
        await makedirs('images', exist_ok=True)
        try:
            image = await client.download_media(chat.photo.big_file_id, ospath.join('images', f'{chat.id}.jpg'))
        except:
            pass

    await sendPhotoTo(text, user_id, image) if image else await sendCustom(text, user_id)
    await sleep(1)
    await update_users(user_id, 'tag', message.from_user.mention)

    try:
        await client.approve_chat_join_request(message.chat.id, user_id)
    except:
        pass

    if LOG_CHANNEL:
        user = await client.get_users(user_id)
        image = ''
        if user.photo:
            try:
                image = await client.download_media(user.photo.big_file_id, ospath.join('images', f'{user.id}.jpg'))
            except:
                pass
        text = f'{message.from_user.mention} <code>({user_id})</code>, approved to join <b>{chat.title}</b> ({chat.type.name.title()})'
        if await aiopath.isfile(image):
            await sendPhotoTo(text, LOG_CHANNEL, image)
            await remove(image)
        else:
            await sendCustom(text, LOG_CHANNEL)


bot.add_handler(ChatJoinRequestHandler(on_join_request, (group | channel) & chat(list(CHAT_IDS)) if CHAT_IDS else (group | channel)))
