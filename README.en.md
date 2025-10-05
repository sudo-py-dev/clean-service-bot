# Clean Service Bot - Service Messages Cleaner

## What does this bot do?
This bot automatically cleans up service messages in Telegram groups. It deletes notifications like 'X joined the group', 'Y changed the group name', etc., to keep your chat clean and clear.

## How to install?
1. Add the bot to your Telegram group
2. Give it admin permissions
3. The bot will start automatically deleting service messages

## What kind of messages does the bot delete?
- User join/leave notifications
- Group setting changes
- Message edit notifications
- And other service messages

## Need help?
Found a bug? You can:
- Open an issue on GitHub

---

# Clean Service Bot - For Developers

## What do you need to run the bot?
- Python 3.8+
- pip
- API_HASH + API_ID from ([my.telegram.org](https://my.telegram.org/auth))
- BOT_TOKEN from @BotFather

## How to install?
1. Download the code:
   ```bash
   git clone https://github.com/sudo-py-dev/clean-service-bot.git
   cd clean-service-bot
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy .env.example to .env
   ```bash
   cp .env.example .env
   ```

4. Update the parameters in the .env file

5. Run the bot:
   ```bash
   python index.py
   ```

## How does the code work?
- The code is organized into directories by functionality
- Uses `tools/logger.py` for logging
- Important to write tests for each new feature

## License
Available under the MIT License - see the [LICENSE](LICENSE) file for details
