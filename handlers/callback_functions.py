from pyrogram.types import CallbackQuery
from tools.database import Users
from tools.enums import Messages
from pyrogram.handlers import CallbackQueryHandler
from pyrogram import filters
from tools.enums import language_display_names


async def select_language_handler(_, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    language = callback_query.data.split(":")[1]
    language_name = language_display_names.get(language)
    if language not in Messages().supported_languages():
        await callback_query.answer(Messages(language="en").language_not_supported.format(language_name))
        return
    
    if not Users.get(user_id=user_id):
        full_name = callback_query.from_user.full_name
        username = callback_query.from_user.username
        Users.create(user_id=user_id, full_name=full_name, username=username, language=language)
    else:
        Users.update(user_id=user_id, language=language)
    await callback_query.edit_message_text(Messages(language=language).language_selected.format(language_display_names.get(language)))


# Add more callback query handlers here


callback_query_handlers = [
    CallbackQueryHandler(select_language_handler, filters.regex(r"lang:(\w{2})"))
]
    