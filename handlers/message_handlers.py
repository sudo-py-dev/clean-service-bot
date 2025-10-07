from pyrogram import Client, filters
from pyrogram.errors import MessageDeleteForbidden, MessageIdInvalid
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram.enums import MessageServiceType
from tools.database import Chats
from tools.enums import Messages
from tools.tools import with_language

@with_language
async def service_message_handler(client: Client, message: Message, language: str):
    chat_id = message.chat.id
    if message.service and message.service == MessageServiceType.NEW_CHAT_TITLE:
       new_title = message.new_chat_title
       chat_type = message.chat.type.value
       Chats.update(chat_id=chat_id, chat_type=chat_type, chat_title=new_title)
    
    if Chats.get(chat_id=chat_id).get("is_active"):
        try:
            await message.delete()
        except (MessageIdInvalid, MessageDeleteForbidden):
            messages = Messages(language)
            await message.reply(messages.missing_permission)
            Chats.update(chat_id=chat_id, is_active=False)



message_handlers = [MessageHandler(service_message_handler, filters.service)]
