import re
from pyrogram import Client
from pyrogram.enums import ChatMembersFilter, ChatType
from pyrogram.types import CallbackQuery, Message
from pyrogram.errors import ChatIdInvalid, ChatAdminRequired, ChannelPrivate, PeerIdInvalid
from tools.inline_keyboards import select_language_buttons
from tools.database import Chats, Users, AdminsPermissions, BotSettings
from tools.enums import Messages, chat_privileges_meaning, AccessPermission
from functools import wraps
from tools.logger import logger
from typing import Union
import os


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


def is_admin_message(permission_require="can_restrict_members"):
    """
    Check if a message or callback query is from an admin of the chat and has the required permission.

    :param permission_require: Permission required (e.g., "can_restrict_members")
    :return: AccessPermission enum value
    """
    def function(func):
        @wraps(func)
        async def wrapper(client: Client, message: Message, *args, **kwargs):
            if not isinstance(message, Message):
                raise TypeError("Invalid Type, expected Message only")
            
            chat_type = message.chat.type

            if chat_type in [ChatType.PRIVATE, ChatType.CHANNEL]:
                return await func(client, message, *args, **kwargs)
            else:
                user_id = message.from_user.id
                chat_id = message.chat.id
                access = await is_admin(client, chat_id, user_id, permission_require)
                if access == AccessPermission.ALLOW:
                    return await func(client, message, *args, **kwargs)
                elif access == AccessPermission.DENY:
                    language = Chats.get(chat_id=chat_id).get("language") or os.getenv("DEFAULT_LANGUAGE") or "he"
                    miss_permission = chat_privileges_meaning.get(permission_require, permission_require.replace('_', ' '))
                    await message.reply(Messages(language=language).unauthorized_admin.format(miss_permission))
                    return
                return
        return wrapper
    return function


def with_language(func):
    @wraps(func)
    async def wrapper(client: Client, msg: [Message, CallbackQuery], *args, **kwargs):
        if isinstance(msg, CallbackQuery):
            chat_type = msg.message.chat.type
        elif isinstance(msg, Message):
            chat_type = msg.chat.type
        else:
            raise ValueError("Invalid Object, expected Message or CallbackQuery only")
        
        
        default_language = os.getenv("DEFAULT_LANGUAGE") or "he"

        if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            chat_id = msg.chat.id
            chat = Chats.get(chat_id=chat_id)
            if not chat:
                Chats.create(chat_id=chat_id,
                             chat_type=chat_type,
                             chat_title=msg.chat.title)
                chat = Chats.get(chat_id=chat_id)
            language = chat.get("language") or default_language

        elif chat_type == ChatType.PRIVATE:
            user_id = msg.from_user.id
            user = Users.get(user_id=user_id)
            if not user:
                Users.create(user_id=user_id,
                             username=msg.from_user.username,
                             full_name=msg.from_user.full_name,
                             is_active=True)
                user = Users.get(user_id=user_id)
                await msg.reply(Messages(language=default_language).select_language, reply_markup=select_language_buttons())
                return
            language = user.get("language") or default_language
        else:
            raise TypeError("Invalid chat type only groups, supergroups or private allowd")
        try:
            return await func(client, msg, language, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in function {func.__name__} for user {msg.from_user.id}: {e}")
            return
    return wrapper


def chat_settings():
    def function(func):
        @wraps(func)
        async def wrapper(client: Client, msg_or_cq: [Message, CallbackQuery]):
            if isinstance(msg_or_cq, CallbackQuery):
                message = msg_or_cq.message
            elif not isinstance(msg_or_cq, Message):
                raise ValueError("Invalid Object, expected Message or CallbackQuery only")
            message = msg_or_cq
            if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
                logger.warning(f"wrapper work only in groups")
                return
            chat = Chats.get(chat_id=message.chat.id)
            if not chat:
                chat = Chats.create(chat_id=message.chat.id,
                             chat_type=message.chat.type.value,
                             title=message.chat.title)
            try:
                return await func(client, msg_or_cq, chat)
            except Exception as e:
                logger.error(f"Error in function {func.__name__} for chat {message.chat.id}: {e}")
                return
        return wrapper
    return function


def owner_only(func):
    """Decorator to restrict access to the bot owner only"""
    @wraps(func)
    async def wrapper(client: Client, update: Union[Message, CallbackQuery], *args, **kwargs):
        try:
            user_id = update.from_user.id
            if user_id != BotSettings.get_settings().owner_id:
                if isinstance(update, CallbackQuery):
                    await update.answer("⛔️ You are not authorized to use this command.", show_alert=True)
                return
            # Call the original function
            return await func(client, update, *args, **kwargs)

        except Exception as e:
            logger.error(f"Error in owner_only decorator: {e}")
            if isinstance(update, CallbackQuery):
                await update.answer("❌ An error occurred. Please try again later.", show_alert=True)
            return

    return wrapper    