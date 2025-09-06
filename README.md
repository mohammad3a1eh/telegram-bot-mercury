# Mercury – Telegram Group Management Bot

![Mercury NASA](https://science.nasa.gov/wp-content/uploads/2023/05/mercury-from-messenger-pia15160-1920x640-1.jpg)

This project is a Telegram group management bot built with [python-telegram-bot](https://docs.python-telegram-bot.org/).  
The purpose of Mercury is to provide efficient tools for managing Telegram groups.

## Features

### For Administrators (replay)
- Remove a user by replying to their message with `حذف کاربر`
- Mute a user for 10 minutes by replying with `بی صدا`
- Unmute a user by replying with `حذف بی صدا`
- Pin a message by replying with `پین`
- Pin a message silently (without notification) by replying with `پین بی صدا`
- Unpin a message by replying with `حذف پین`
- Warn users with `اخطار`

### For Administrators (non replay)
- Enable text-only mode with `قفل رسانه`
- Enable full lock mode with `قفل کامل`
- Disable lock with `حذف قفل`

### For the Group Owner (replay)
- Promote a user to admin by replying with `ارتقا به ادمین`
- Demote an admin by replying with `حذف از ادمین`
- Remove the bot from the group by sending `حذف ربات از گروه`

### For all users
- Get a random meme with `میم`

All administrator commands are also available to the group owner

## Installation and Setup

### 1. Clone the repository
```bash
git clone https://github.com/mohammad3a1eh/telegram-bot-mercury.git
cd telegram-bot-mercury
```

Before running the bot with Docker, make sure to create and properly configure the .env file with your bot token and any other required environment variables.

### 2. Run with Docker
```bash
docker-compose up -d
```

## Dependencies
- python-telegram-bot
- python-dotenv
- mysql-connector-python
- python-dotenv

To check all project dependencies, you can open the [requirements.txt](requirements.txt) file.
