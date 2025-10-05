from enum import Enum
import json
import os

if os.path.exists("tools/messages.json"):
    with open("tools/messages.json", "r") as f:
        messages = json.load(f)
else:
    messages = {}

class AccessPermission(Enum):
    """Enum for access permission."""
    ALLOW = 1
    """User has permission to perform the action."""
    DENY = 2
    """User does not have permission to perform the action."""
    NOT_ADMIN = 3
    """User is not an admin."""
    CHAT_NOT_FOUND = 4
    """Chat is not found."""
    NEED_UPDATE = 5
    """Chat needs update."""

chat_privileges_meaning = {
    "can_manage_chat": "ניהול צ'אט ✨",
    "can_delete_messages": "מחיקת הודעות 🗑️",
    "can_delete_stories": "מחיקת סטורי 📖",
    "can_manage_video_chats": "ניהול שיחות וידאו 🎥",
    "can_restrict_members": "הגבלת חברים 🚫",
    "can_promote_members": "קידום חברים ⬆️",
    "can_change_info": "שינוי מידע על הקבוצה ℹ️",
    "can_post_messages": "פרסום הודעות 📝",
    "can_post_stories": "פירסום סטורי 📚",
    "can_edit_messages": "עריכת הודעות 📝",
    "can_edit_stories": "עריכת סטורי 📚",
    "can_invite_users": "הזמנת משתמשים 💌",
    "can_pin_messages": "נעיצת הודעות 📌",
    "can_manage_topics": "ניהול נושאים 📋",
    "is_anonymous": "אנונימי 🕶️"
}

class Messages:
    def __init__(self, language: str="he"):
        self.language = language
        self.messages = dict(messages)

    def __getattr__(self, name):
        if self.language and name in self.messages.get(self.language, {}):
            return self.messages[self.language][name]
        else:
            # Fallback to English if the message doesn't exist in the current language
            if name in self.messages.get("en", {}):
                return self.messages["en"][name]
            else:
                return f"Message '{name}' not found"

    def __setattr__(self, name, value):
        if name == 'language' or name == 'messages':
            super().__setattr__(name, value)
        else:
            # Handle dynamic message setting
            if hasattr(self, 'language') and hasattr(self, 'messages') and self.language:
                if self.language in self.messages and name in self.messages[self.language]:
                    self.messages[self.language][name] = value
                elif self.language in self.messages:
                    self.messages[self.language][name] = value
                # Don't set as instance attribute for message keys

    def supported_languages(self):
        """Return a list of all available language codes."""
        return list(self.messages.keys())

language_display_names = {
        "he": "עברית 🇮🇱",
        "en": "English 🇺🇸",
        "fr": "Français 🇫🇷"
        # Add more languages here if needed
    }