from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from pyrogram.errors import MessageDeleteForbidden
from tools.database import Chats
from tools.tools import group_settings


@group_settings(is_bot_admin=True)
async def clean_service_messages(_, message: Message, __: Chats):
    try:
        if message.service:
            await message.delete()
    except MessageDeleteForbidden:
        Chats.update(message.chat.id, bot_is_admin=False)


message_handlers = [
    MessageHandler(clean_service_messages, filters.service)
]

    