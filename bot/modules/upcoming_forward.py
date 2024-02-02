from asyncio import Lock, gather
from pyrogram import Client
from pyrogram.types import Message

from bot import chats_ids
from bot.helpers.message_utils import get_message, copyMessage
from bot.helpers.utils import filter_text


forward_lock = Lock()


async def send_it(client: Client, message: Message, value: dict, id_: int):
    caption = message.text or message.caption
    caption = filter_text(caption.html) if value.get(str(id_)) else None
    msg = await get_message(client, message)
    await copyMessage(id_, msg, caption)


async def upcoming_forward(client: Client, message: Message):
    for chats, value in chats_ids.items():
        chat_id = message.chat.id
        if chat_id == chats:
            async with forward_lock:
                await gather(*[send_it(client, message, value, id_) for id_ in value['ids']])
