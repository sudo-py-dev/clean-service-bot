"""
Bot setup and initialization utilities.

This module contains functions for setting up and configuring the bot,
including owner configuration and other initialization tasks.
"""

from tools.logger import logger
from tools.database import BotSettings
from tools.tools import is_valid_user_id


def setup_bot_owner():
    """
    Configure the bot owner if not already set.
    
    This function guides the user through the process of setting up
    the bot owner ID if it hasn't been configured yet.
    """
    bot_settings = BotSettings().get_settings()
    
    if bot_settings.owner_id:
        logger.info(f"Bot owner already configured with ID: {bot_settings.owner_id}")
        return True

    print("\n" + "="*60)
    print("BOT OWNER SETUP".center(60))
    print("="*60)
    print("\nNo owner ID is currently configured for the bot.")
    print("The owner will have full control over the bot's administrative functions.\n")
    
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            user_input = input(
                f"\nPlease enter the owner's Telegram user ID (or press Enter to skip, attempt {attempt}/{max_attempts}): "
            )
            
            if not user_input.strip():
                logger.warning("Owner ID setup was skipped")
                print("\n⚠️  Warning: Running bot without owner ID. Some features will be disabled.")
                return False
                
            if not user_input.isdigit() or not is_valid_user_id(user_input):
                print("❌ Invalid user ID. Please enter a valid numeric Telegram user ID.")
                continue
                
            owner_id = int(user_input)
            BotSettings().update_settings(owner_id=owner_id)
            logger.info(f"Successfully set owner ID to: {owner_id}")
            print(f"\n✅ Success! Owner ID set to: {owner_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting owner ID: {e}")
            print(f"❌ An error occurred: {e}")
            
    print("\n⚠️  Failed to set owner ID after multiple attempts. Some features will be disabled.")
    logger.warning("Failed to set owner ID after maximum retries")
    return False
