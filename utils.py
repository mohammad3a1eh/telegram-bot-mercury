from telegram import (
    Update,
    ChatMemberAdministrator,
    ChatMemberOwner
)
from telegram.ext import ContextTypes
from typing import Tuple, List

async def get_moderators(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Tuple[List[ChatMemberOwner], List[ChatMemberAdministrator]]:
    chat_id = update.message.chat_id

    admins = await context.bot.get_chat_administrators(chat_id)
    just_admins = [admin for admin in admins if admin.status == "administrator"]
    just_owner = [admin for admin in admins if admin.status == "creator"]

    return just_owner, just_admins
