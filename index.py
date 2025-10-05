from tools.logger import logger
from pyrogram import Client
from dotenv import load_dotenv
import os
from handlers.commands import commands_handlers
from handlers.callback_functions import callback_query_handlers
from handlers.message_handler import message_handlers
from handlers.join_handler import join_handlers
load_dotenv()


api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
token = os.getenv("BOT_TOKEN")
bot_client_name = os.getenv("BOT_CLIENT_NAME")

if not api_id or not api_hash or not token or not bot_client_name:
    raise ValueError("API_ID, API_HASH, BOT_TOKEN, and BOT_CLIENT_NAME must be set in the environment variables")

app = Client(bot_client_name, api_id=api_id, api_hash=api_hash, bot_token=token, skip_updates=False)


# Commands handler
for handler in commands_handlers:
    app.add_handler(handler)

# Callback query handler
for handler in callback_query_handlers:
    app.add_handler(handler)

# Message handler
for handler in message_handlers:
    app.add_handler(handler)

# Join handler
for handler in join_handlers:
    app.add_handler(handler)


# Run the bot
logger.info("Bot started successfully")
app.run()
logger.info("Bot stopped")
