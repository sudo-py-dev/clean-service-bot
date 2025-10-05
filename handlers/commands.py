from handlers.callback_buttons import select_language_buttons, button_url_builder
from tools.enums import Messages
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from tools.tools import get_user_preferred_language, is_admin_message_or_callback
from tools.database import Chats, AdminsPermissions

@get_user_preferred_language()
async def start_handler(client: Client, message: Message, language: str):
    join_button = button_url_builder(Messages(language=language).join_button, f"https://t.me/{client.me.username}?startchannel=true&startgroup=true")
    await message.reply(Messages(language=language).start.format(client.me.full_name), reply_markup=join_button)


@get_user_preferred_language()
async def help_handler(_, message: Message, language: str):
    commands = Messages(language=language).commands
    commands_str = "\n".join([f"/{command} - {description}" for command, description in commands.items()])
    await message.reply(Messages(language=language).help.format(commands_str))


@get_user_preferred_language()
async def change_language_handler(_, message: Message, language: str):
    await message.reply(Messages(language=language).select_language, reply_markup=select_language_buttons())


@is_admin_message_or_callback()
async def register_handler(_, message: Message):
    Chats.register(message.chat.id, message.chat.type, message.chat.title, True)
    await message.reply(Messages(language="he").register)


@is_admin_message_or_callback()
async def reload_admins_handler(_, message: Message):
    if AdminsPermissions.reload(message.chat.id):
        await message.reply(Messages(language="he").reload_admins)
    else:
        await message.reply(Messages(language="he").reload_admins_failed)

# Add more commands handlers here


commands_handlers = [
    MessageHandler(start_handler, filters.command("start") & filters.private),
    MessageHandler(help_handler, filters.command("help") & filters.private),
    MessageHandler(change_language_handler, filters.command("lang") & filters.private),
    MessageHandler(register_handler, filters.command("register") & filters.group),
    MessageHandler(reload_admins_handler, filters.command("reload") & filters.group),
    # Add the commands functions with the filters here
]
