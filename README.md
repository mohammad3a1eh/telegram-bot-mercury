# Mercury – Telegram Group Management Bot

![Mercury NASA](https://science.nasa.gov/wp-content/uploads/2023/05/mercury-from-messenger-pia15160-1920x640-1.jpg)

This project is a Telegram group management bot built with [python-telegram-bot](https://docs.python-telegram-bot.org/).  
The purpose of Mercury is to provide efficient tools for managing Telegram groups.

## Features

### For Administrators
- Remove a user by replying to their message with `حذف کاربر`
- Mute a user for 10 minutes by replying with `بی صدا`
- Unmute a user by replying with `حذف بی صدا`
- Pin a message by replying with `پین`
- Pin a message silently (without notification) by replying with `پین بی صدا`
- Unpin a message by replying with `حذف پین`

### For the Group Owner
- Promote a user to admin by replying with `ارتقا به ادمین`
- Demote an admin by replying with `حذف از ادمین`
- Remove the bot from the group by sending `حذف ربات از گروه`

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/username/atarod-bot.git
cd atarod-bot
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
BOT_TOKEN=your_bot_token_here
DEBUG=true
```

### 5. Run the bot
```bash
python mercury.py
```

## Dependencies
- python-telegram-bot
- python-dotenv
