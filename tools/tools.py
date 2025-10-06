import re
from pyrogram import Client
from pyrogram.enums import ChatMembersFilter, ChatType
from pyrogram.types import CallbackQuery, Message
from pyrogram.errors import ChatIdInvalid, ChatAdminRequired, ChannelPrivate, PeerIdInvalid
from handlers.callback_buttons import select_language_buttons
from .database import Users, AdminsPermissions, Chats
from .enums import Messages, chat_privileges_meaning, AccessPermission
from functools import wraps
from .logger import logger


def is_valid_chat_id(chat_id) -> bool:
    return bool(re.match(r"^-?\d{5,32}$", str(chat_id)))


def is_valid_user_id(user_id) -> bool:
    return bool(re.match(r"^\d{1,32}$", str(user_id)))


def is_valid_username(username) -> bool:
    return bool(re.match(r"^@[a-zA-Z][a-zA-Z0-9_]{3,30}[a-zA-Z0-9]$", str(username)))


async def is_admin(
    client: Client,
    chat_id: int,
    user_id: int,
    permission_require: str = "can_restrict_members"
) -> AccessPermission:
    """
    Check if a user is an admin of the group and has the required permission.

    Args:
        client: Pyrogram Client instance
        chat_id: ID of the chat to check
        user_id: ID of the user to check
        permission_require: Name of the permission to check

    Returns:
        AccessPermission: The result of the permission check
    """
    # Chat is always admin of itself also anonymous admin
    if user_id == chat_id:
        return AccessPermission.ALLOW
    
    try:
        # First check the database
        admin_status = AdminsPermissions.is_admin(chat_id, user_id, permission_require)
        
        # If we need to refresh the admin list
        if admin_status == AccessPermission.NEED_UPDATE:
            try:
                # Get fresh admin list from Telegram
                admin_list = [(member.user.id, member.privileges) 
                                async for member in client.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)
                             ]
        
                
                # Update database
                AdminsPermissions.create(chat_id, admin_list)
                # Check again after update
                admin_status = AdminsPermissions.is_admin(chat_id, user_id, permission_require)
                if admin_status in [AccessPermission.ALLOW, AccessPermission.DENY, AccessPermission.NOT_ADMIN]:
                    return admin_status
                
            except (ChatIdInvalid, ChatAdminRequired, ChannelPrivate, PeerIdInvalid) as e:
                logger.warning(f"Failed to fetch admin list for chat {chat_id}: {e}")
                return AccessPermission.CHAT_NOT_FOUND
            except Exception as e:
                logger.error(f"Unexpected error updating admin list for chat {chat_id}: {e}")
                return AccessPermission.CHAT_NOT_FOUND
        elif admin_status in [AccessPermission.ALLOW, AccessPermission.DENY, AccessPermission.NOT_ADMIN]:
            return admin_status
        else:
            return AccessPermission.CHAT_NOT_FOUND
    except Exception as e:
        logger.error(f"Error in is_admin for chat {chat_id}, user {user_id}: {e}")
        return AccessPermission.CHAT_NOT_FOUND


def is_admin_message_or_callback(permission_require="can_restrict_members"):
    """
    Check if a message or callback query is from an admin of the chat and has the required permission.

    :param permission_require: Permission required (e.g., "can_restrict_members")
    :return: AccessPermission enum value
    """
    def function(func):
        @wraps(func)
        async def wrapper(client: Client, msg_or_cq: [Message, CallbackQuery]):
            if isinstance(msg_or_cq, CallbackQuery):
                message = msg_or_cq.message
            elif not isinstance(msg_or_cq, Message):
                raise ValueError("Invalid Object, expected Message or CallbackQuery only")
            message = msg_or_cq
            chat_id = message.chat.id
            user_id = message.from_user.id if message.from_user else message.sender_chat.id
            if message.chat.type in [ChatType.PRIVATE, ChatType.CHANNEL]:
                logger.warning(f"Use this wrapper only in groups")
                return await func(client, msg_or_cq)
            else:
                access = await is_admin(client, chat_id, user_id, permission_require)
                if access == AccessPermission.ALLOW:
                    return await func(client, msg_or_cq)
                elif access == AccessPermission.DENY:
                    miss_permission = chat_privileges_meaning.get(permission_require, permission_require.replace('_', ' '))
                    await message.reply(Messages(language="he").unauthorized_admin.format(miss_permission))
                    return
        return wrapper
    return function


def get_user_preferred_language():
    def function(func):
        @wraps(func)
        async def wrapper(client: Client, msg_or_cq: [Message, CallbackQuery]):
            if isinstance(msg_or_cq, CallbackQuery):
                message = msg_or_cq.message
            elif not isinstance(msg_or_cq, Message):
                raise ValueError("Invalid Object, expected Message or CallbackQuery only")
            
            message = msg_or_cq
            if message.chat.type != ChatType.PRIVATE:
                logger.warning("Use this wrapper only in private chat")
                return
            user = Users.get(user_id=message.from_user.id)
            if not user:
                Users.create(user_id=message.from_user.id,
                             username=message.from_user.username,
                             full_name=message.from_user.full_name,
                             is_contact=True)
                await message.reply(Messages(language="he").select_language, reply_markup=select_language_buttons())
                return
            language = user.language or "he"
            return await func(client, msg_or_cq, language)
        return wrapper
    return function


def group_settings(is_bot_admin: bool = True):
    def function(func):
        @wraps(func)
        async def wrapper(client: Client, msg_or_cq: [Message, CallbackQuery]):
            if isinstance(msg_or_cq, CallbackQuery):
                message = msg_or_cq.message
            elif not isinstance(msg_or_cq, Message):
                raise ValueError("Invalid Object, expected Message or CallbackQuery only")
            message = msg_or_cq
            if message.chat.type not in [ChatType.SUPERGROUP, ChatType.GROUP]:
                logger.warning("Use this wrapper only in groups")
                return
            settings = Chats.get(chat_id=message.chat.id)
            if not settings:
                Chats.create(chat_id=message.chat.id, chat_type=message.chat.type.value, chat_title=message.chat.title, bot_is_admin=True)
                settings = Chats.get(chat_id=message.chat.id)
            elif not settings.get("chat_type") or not settings.get("chat_title"):
                Chats.update(chat_id=message.chat.id, chat_type=message.chat.type.value, chat_title=message.chat.title)
                settings = Chats.get(chat_id=message.chat.id)
            if not is_bot_admin:
                    return await func(client, msg_or_cq, settings)
            if is_bot_admin and settings.get("bot_is_admin"):
                return await func(client, msg_or_cq, settings)
            return
        return wrapper
    return function


