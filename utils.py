from telegram import Update
from telegram.ext import ContextTypes

async def is_owner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Check if the user who sent the message is the owner (creator) of the chat.

    Args:
        update (Update): The incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): The context for the callback.

    Returns:
        bool: True if the user is the owner, False otherwise.
    """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    admins = await context.bot.get_chat_administrators(chat_id)
    for admin in admins:
        if admin.status == "creator" and admin.user.id == user_id:
            return True
    return False

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Check if the user who sent the message is an administrator of the chat.

    Args:
        update (Update): The incoming update from Telegram.
        context (ContextTypes.DEFAULT_TYPE): The context for the callback.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    admins = await context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]

    return user_id in admin_ids
