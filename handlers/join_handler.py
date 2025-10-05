from pyrogram import Client
from pyrogram.types import ChatMemberUpdated
from pyrogram.enums import ChatMemberStatus
from tools.database import Chats
from pyrogram.handlers import ChatMemberUpdatedHandler



async def join_handler_chats(_, member: ChatMemberUpdated):
    if member.new_chat_member and member.new_chat_member.user.is_self:
        chat_id = member.chat.id
        chat_name = member.chat.title
        chat_type = member.chat.type
        if member.new_chat_member.status == ChatMemberStatus.ADMINISTRATOR:
            if not Chats.create(chat_id, chat_name, chat_type.value, True):
                Chats.update(chat_id, bot_is_admin=True)
        else:
            if not Chats.create(chat_id, chat_name, chat_type.value, False):
                Chats.update(chat_id, bot_is_admin=False)


join_handlers = [
    ChatMemberUpdatedHandler(join_handler_chats)
    ]