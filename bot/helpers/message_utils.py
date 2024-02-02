from asyncio import sleep, gather
from functools import wraps
from pyrogram.errors import FloodWait, UserBlocked, UserDeactivatedBan, UserDeactivated, UserIsBlocked, InputUserDeactivated
from pyrogram.types import Message, InlineKeyboardMarkup
from re import findall as re_findall

from bot import bot, DATABASE_URL, LOGGER
from bot.helpers.db_manager import DbManager


class Limits:
    def __init__(self):
        self.total = 0

    def _extracted_text(self, msg: str, lmax: int):
        if match := re_findall(r'(</?\S{,4}>|<a\s?href=[\'"]\S+[\'"]|>)', msg):
            self.total = len(''.join(match))
        limit = self.total + lmax
        space = msg[:limit].count(' ')
        return msg.strip()[:limit - space]

    def caption(self, caption: str):
        return self._extracted_text(caption, 1024)

    def text(self, text: str):
        return self._extracted_text(text, 4096)


limit = Limits()


def handle_message(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = func.__name__
        try:
            return await func(*args, **kwargs)
        except FloodWait as f:
            LOGGER.error('%s(): %s', func_name, f)
            await sleep(f.value * 1.2)
            return await wrapper(*args, **kwargs)
        except (UserBlocked, UserDeactivatedBan, UserDeactivated, UserIsBlocked, InputUserDeactivated):
            if DATABASE_URL:
                await DbManager().delete_user(args[1])
        except Exception as e:
            LOGGER.error('%s(): %s', func_name, e)
    return wrapper


@handle_message
async def sendMessage(text: str, message: Message, reply_markup: InlineKeyboardMarkup=None):
    return await message.reply_text(limit.text(text), True, reply_markup=reply_markup, disable_notification=True,
                                    disable_web_page_preview=True)


@handle_message
async def sendPhoto(caption: str, message: Message, photo, reply_markup: InlineKeyboardMarkup=None):
    return await message.reply_photo(photo, True, limit.caption(caption), reply_markup=reply_markup, disable_notification=True)


@handle_message
async def sendFile(message: Message, doc: str, caption: str=''):
    await message.reply_document(doc, caption=limit.caption(caption), quote=True)


@handle_message
async def sendCustom(text: str, chat_id: str | int, reply_markup: InlineKeyboardMarkup=None):
    return await bot.send_message(chat_id, limit.text(text), reply_markup=reply_markup, disable_notification=True)


@handle_message
async def editMessage(text: str, message: Message, reply_markup: InlineKeyboardMarkup=None):
    return await message.edit_text(limit.text(text), reply_markup=reply_markup, disable_web_page_preview=True)


@handle_message
async def editCustom(text: str, chat_id: int, message_id: int, reply_markup=None):
    return await bot.edit_message_text(chat_id, message_id, limit.text(text), reply_markup=reply_markup, disable_web_page_preview=True)


@handle_message
async def copyMessage(message: Message, chat_id: int, caption: str=None, reply_markup: InlineKeyboardMarkup=None):
    if not reply_markup:
        if (markup := message.reply_markup) and markup.inline_keyboard:
            reply_markup = markup
    return await message.copy(chat_id, caption, disable_notification=True, reply_markup=reply_markup)


@handle_message
async def deleteMessage(*args: Message):
    await gather(*[msg.delete() for msg in args if isinstance(msg, Message)])