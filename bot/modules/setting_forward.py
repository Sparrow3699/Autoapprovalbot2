from ast import literal_eval
from asyncio import sleep, gather
from functools import partial
from pyrogram import Client
from pyrogram.filters import command, regex, create
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import Message, CallbackQuery
from re import findall as re_findall
from time import time

from bot import bot, chats_ids, LOGGER
from bot.helpers.button_build import ButtonMaker
from bot.helpers.db_manager import DbManager
from bot.helpers.filters import CustomFilters
from bot.helpers.message_utils import deleteMessage, sendMessage, editMessage, auto_delete_message
from bot.helpers.utils import update_chat, update_destination, new_thread


chats_info = {}
handler_dict = {}


async def get_info_chat(chat_id: int):
    try:
        return chats_info.setdefault(chat_id, await bot.get_chat(chat_id))
    except Exception as e:
        LOGGER.error('CHAT_ID: %s, %s', chat_id, e)
        update_destination(chat_id)
        await DbManager().delete_chats(chat_id)


async def get_buttons(data='', pre=''):
    buttons = ButtonMaker()
    index = 1
    if pre:
        text = ''
        cid = data if pre == 'source' else pre
        if info := await get_info_chat(int(cid)):
            text += '<b>CHAT INFO</b>\n'
            text += f'<b>Title:</b> {info.title}\n'
            text += f'<b>ID:</b> <code>{cid}</code>\n'
            text += f'<b>Type:</b> {info.type.name.title()}\n'
            text += f'<b>Member:</b> {info.members_count}\n'
            text += f'<b>Data Center:</b> {info.dc_id or "Unknown"}\n'
            text += f'<b>Protect Content:</b> {info.has_protected_content}\n'
        if pre == 'source':
            buttons.button_data('Delete Source', f'ids del {data}')
            buttons.button_data('Add Destination', f'ids {data}')
            text += '\n<i>Choose operation.</i>'
        else:
            rm_link = chats_ids.get(int(data)).get(pre)
            text += f'<b>Remove Link:</b> {"Yes ✅" if rm_link else "No"}\n'
            buttons.button_data(f'Remove Link {" ✅" if rm_link else ""}', f'ids rml {data} {pre} {bool(rm_link)}', 'header')
            buttons.button_data('<<', f'ids {data}')
            buttons.button_data('Delete', f'ids rmd {data} {pre}')
            text += '\nDo you wanna delete this destination?'
    elif not data:
        text = 'Available Source Chat:\n'
        for chat, value in chats_ids.items():
            if info := await get_info_chat(chat):
                text += f'{index}. <b>{info.title}</b> (<code>{chat}</code>): {len(value.get("ids", ""))} Destination\n'
                buttons.button_data(info.title, f'ids pre {chat}')
        buttons.button_data('Add Chat', 'ids add', 'header')
    elif data == 'add':
        text = 'Send valid source chat id.\nExample -100XXXXXXXX'
    else:
        text = ''
        for id_ in list(chats_ids.get(int(data), {}).get('ids', set())):
            if info := await get_info_chat(id_):
                buttons.button_data(str(index), f'ids des {data} {id_}')
                text += f'{index}. <b>{info.title}</b>\n'
                index += 1
        text += '\nSend one or some valid destionation chat id.\nExample -100123XXXXX -100456XXXX -100789XXXX'
    if data:
        buttons.button_data('Home', 'ids home', 'footer')
    buttons.button_data('Close', 'ids close', 'footer')

    return text, buttons.build_menu(3, f_cols=3)


async def update_buttons(message: Message, data='', pre=''):
    text, buttons = await get_buttons(data, pre)
    await editMessage(text, message, buttons)


@new_thread
async def event_handler(client: Client, query: CallbackQuery, pfunc: partial, rfunc: partial):
    chat_id = query.message.chat.id
    handler_dict[chat_id] = True
    start_time = time()

    async def event_filter(_, __, event):
        user = event.from_user or event.sender_chat
        return user.id == query.from_user.id and event.chat.id == chat_id

    handler = client.add_handler(MessageHandler(pfunc, filters=create(event_filter)), group=-1)
    while handler_dict[chat_id]:
        await sleep(0.5)
        if time() - start_time > 60:
            handler_dict[chat_id] = False
            await rfunc()
    client.remove_handler(*handler)


async def setting_chats(_, message: Message, omsg: Message, key: str):
    ids = re_findall(r'-100\d{10}', message.text)
    if not ids:
        msg = await sendMessage('Invalid chat id, try again...!', message)
        auto_delete_message(msg)
        return

    if key == 'add':
        data = ''
        chat_id = int(ids[0])
        if not await get_info_chat(chat_id):
            msg = await sendMessage(f'This is a valid chat? Make sure bot have been added to the this chat: {chat_id}.', message)
            auto_delete_message(msg)
            return
        value = ''
    else:
        chat_id = int(key)
        des_ids = {int(id_) for id_ in ids if int(id_) not in chats_ids and await get_info_chat(int(id_))}
        if not des_ids:
            msg = await sendMessage('This is a valid chat? Make sure bot have been added to the chat this is not a source chat.', message)
            auto_delete_message(msg)
            return
        value = chats_ids[chat_id].get('ids') or set()
        value.update(des_ids)
        data = key
    await update_chat(chat_id, 'ids', value)
    handler_dict[omsg.chat.id] = False
    await gather(deleteMessage(message), update_buttons(omsg, data))


async def get_chats(_, message: Message):
    text, buttons = await get_buttons()
    await sendMessage(text, message, buttons)


async def cb_chats(client: Client, query: CallbackQuery):
    message = query.message
    handler_dict[message.chat.id] = False
    data = query.data.split()
    await query.answer()
    match data[1]:
        case 'home':
            await update_buttons(message)
        case 'close':
            await deleteMessage(message, message.reply_to_message)
        case 'pre':
            await update_buttons(message, data[2], 'source')
        case 'rml':
            chats_ids[int(data[2])].pop(int(data[3]), None)
            await update_chat(int(data[2]), data[3], not literal_eval(data[4]))
            await update_buttons(message, data[2], data[3])
        case 'del':
            await DbManager().delete_chats(int(data[2]))
            await update_buttons(message)
        case 'rmd':
            ids = chats_ids[int(data[2])]['ids']
            if int(data[3]) in ids:
                ids.remove(int(data[3]))
            await update_chat(int(data[2]), 'ids', ids or '')
            await update_buttons(message)
        case 'des':
            await update_buttons(message, data[2], data[3])
        case _:
            await update_buttons(message, data[1])
            pfunc = partial(setting_chats, omsg=message, key=data[1])
            rfunc = partial(update_buttons, message)
            event_handler(client, query, pfunc, rfunc)


bot.add_handler(MessageHandler(get_chats, command('chats') & CustomFilters.forward_mode))
bot.add_handler(CallbackQueryHandler(cb_chats, regex('^ids')))
