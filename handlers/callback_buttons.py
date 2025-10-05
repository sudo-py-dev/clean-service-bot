from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tools.enums import Messages, language_display_names


def select_language_buttons():
    languages = Messages().supported_languages()
    buttons = []

    row = []
    for i, lang in enumerate(languages, start=1):
        row.append(InlineKeyboardButton(language_display_names.get(lang, lang), callback_data=f"lang:{lang}"))
        if i % 2 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(buttons)


def buttons_builder(name, data):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(name, callback_data=data)
            ]
        ]
    )


def button_url_builder(name, url):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(name, url=url)
            ]
        ]
    )

# Add more callback buttons here