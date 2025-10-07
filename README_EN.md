# 🧹 Service Cleaner Bot

A Telegram bot designed to help manage and clean up services with admin controls and user management.

## ✨ Features

- **Service Management** - Add, remove, and list services
- **Admin Controls** - Manage users and permissions
- **Multi-language Support** - Built-in support for multiple languages
- **Database Integration** - SQLAlchemy ORM with SQLite
- **Logging** - Comprehensive logging system

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Telegram Bot Token from [@BotFather](https://t.me/botfather)
- API ID and API Hash from [Telegram](https://my.telegram.org/auth)
- Required Python packages (install via `pip install -r requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sudo-py-dev/clean-service-bot.git
   cd clean-service-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the bot:
   - Copy `.env.example` to `.env`
   - Update the environment variables in `.env`

5. Run the bot:
   ```bash
   python index.py
   ```

## 📂 Project Structure

```
.
├── bot_management/      # Bot management utilities (Bot manager)
├── handlers/           # Message and callback handlers
├── locales/            # Language files
├── tools/              # Utility functions and helpers
├── .env.example        # Example environment variables
├── index.py            # Main application entry point
└── requirements.txt    # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
