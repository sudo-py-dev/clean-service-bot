from tools.enums import Messages, language_display_names
from tools.inline_keyboards import select_language_buttons
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram import filters
from tools.tools import with_language, is_admin_message
from tools.database import Chats


@with_language
async def start_handler(client: Client, message: Message, language: str):
    await message.reply(Messages(language=language).start.format(message.from_user.mention, client.me.full_name))


@with_language
async def help_handler(_, message: Message, language: str):
    commands = Messages(language=language).commands
    commands_str = "\n".join([f"/{command} - {description}" for command, description in commands.items()])
    await message.reply(Messages(language=language).help.format(commands_str))


@is_admin_message()
@with_language
async def change_language_handler(_, message: Message, language: str):
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        parts = message.text.split(" ")
        supported_languages = Messages().supported_languages()
        if len(parts) != 2:
            await message.reply(Messages(language=language).select_language_groups.format("/".join(supported_languages)))
            return
        new_lang = parts[1].strip()
        if new_lang not in supported_languages:
            await message.reply(Messages(language=language).language_not_supported.format(new_lang, "/".join(supported_languages)))
            return
        
        Chats.update(chat_id=message.chat.id, language=new_lang)
        await message.reply(Messages(language=new_lang).language_set_groups.format(language_display_names[new_lang]))
    else:
        await message.reply(Messages(language=language).select_language, reply_markup=select_language_buttons())


# Add more commands handlers here


commands_handlers = [
    MessageHandler(start_handler, filters.command("start") & filters.private),
    MessageHandler(help_handler, filters.command("help") & filters.private),
    MessageHandler(change_language_handler, filters.command("lang") & (filters.private | filters.group))
    # Add the commands functions with the filters here
]
