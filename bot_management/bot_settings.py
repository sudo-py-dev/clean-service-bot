from pyrogram import filters
from pyrogram.types import Message
from tools.tools import with_language
from tools.inline_keyboards import bot_settings_buttons
from tools.enums import Messages
from pyrogram.handlers import MessageHandler
from tools.database import BotSettings


@with_language
async def bot_settings(_, message: Message, language: str):
    messages = Messages(language=language)
    bot_settings = BotSettings.get_settings()
    buttons = bot_settings_buttons(bot_settings, language)
    await message.reply(messages.bot_settings, reply_markup=buttons)


bot_handlers = [MessageHandler(bot_settings, filters.command("settings") & filters.chat(BotSettings.get_settings().owner_id))]