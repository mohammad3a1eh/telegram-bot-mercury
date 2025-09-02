from dotenv import load_dotenv
from os import getenv
from asyncio import sleep
from datetime import datetime, timedelta, timezone
from logging import (
    debug,
    info,
    basicConfig,
    INFO,
    DEBUG as DEBUGG,
)
from telegram import (
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from messages import *
from utils import (
    is_admin,
    is_owner
)

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
DEBUG = getenv("DEBUG")

if DEBUG == "true":
    basicConfig(level=DEBUGG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')

info("Bot started")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    debug("bot start in PV")
    await update.message.reply_text(MSG_START)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_admin(update, context):
        text = update.message.text.strip()
        if update.message.reply_to_message:
            debug("admin replay message")
            target_user = update.message.reply_to_message.from_user
            target_message = update.message.reply_to_message


            if text == "حذف کاربر":
                # This command deletes the user.
                debug("remove user called")
                await context.bot.ban_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=target_user.id
                )

                await update.message.delete()

            elif text == "بی صدا" or text == "بیصدا":
                # This command mutes the user for 10 minutes.
                debug("mute user called")
                until_time = datetime.now(timezone.utc) + timedelta(minutes=10)

                await context.bot.restrict_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=target_user.id,
                    permissions={
                        "can_send_messages": False,
                        "can_send_media_messages": False,
                        "can_send_polls": False,
                        "can_send_other_messages": False,
                        "can_add_web_page_previews": False,
                        "can_change_info": False,
                        "can_invite_users": False,
                        "can_pin_messages": False
                    },
                    until_date=until_time
                )

                msg = await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=MSG_YOU_SILENT_10_MINUTES,
                    reply_to_message_id=target_message.message_id
                )
                await sleep(10)
                await msg.delete()

                await update.message.delete()

            elif text == "حذف بی صدا" or text == "حذف بیصدا":
                # This command silently deletes the user.
                debug("unmute user called")
                await context.bot.restrict_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=target_user.id,
                    permissions={
                        "can_send_messages": True,
                        "can_send_media_messages": True,
                        "can_send_polls": True,
                        "can_send_other_messages": True,
                        "can_add_web_page_previews": True,
                        "can_change_info": False,
                        "can_invite_users": True,
                        "can_pin_messages": False
                    }
                )

                await update.message.delete()

            elif text == "پین":
                # This command pins the message.
                debug("pin called")
                await context.bot.pin_chat_message(
                    chat_id=update.effective_chat.id,
                    message_id=target_message.message_id,
                    disable_notification=False
                )

                await update.message.delete()

            elif text == "پین بی صدا" or text == "پین بیصدا":
                # This command pins the message but does not send a notification.
                debug("mute pin called")
                await context.bot.pin_chat_message(
                    chat_id=update.effective_chat.id,
                    message_id=target_message.message_id,
                    disable_notification=True
                )

                await update.message.delete()

            elif text == "حذف پین":
                # This command deletes the PIN message.
                debug("remove pin called")
                await context.bot.unpin_chat_message(
                    chat_id=update.effective_chat.id,
                    message_id=target_message.message_id
                )

                await update.message.delete()

        else:
            pass

    if await is_owner(update, context):
        debug("owner replay message")
        text = update.message.text.strip()
        if update.message.reply_to_message:
            target_user = update.message.reply_to_message.from_user
            admins = await context.bot.get_chat_administrators(update.effective_chat.id)
            admin_ids = [admin.user.id for admin in admins]

            if text == "ارتقا به ادمین":
                # This command will promote the user to admin if they are not already an admin.
                debug("promote user to admin called")
                if target_user.id in admin_ids:
                    await context.bot.send_message(
                        chat_id=update.message.from_user.id,
                        text=MSG_USER_ALREADY_ADMIN
                    )
                    return

                await context.bot.promote_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=target_user.id,
                    can_change_info=True,
                    can_delete_messages=True,
                    can_invite_users=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=False
                )

                await update.message.delete()

            elif text == "حذف از ادمین":
                # This command removes the specified user from the admin role if they are an admin.
                debug("remove admin from admins called")
                if target_user.id not in admin_ids:
                    await context.bot.send_message(
                        chat_id=update.message.from_user.id,
                        text=MSG_USER_ALREADY_NOT_ADMIN
                    )
                    return

                await context.bot.promote_chat_member(
                    chat_id=update.effective_chat.id,
                    user_id=target_user.id,
                    can_change_info=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_promote_members=False
                )

                await update.message.delete()

        else:
            if text == "حذف ربات از گروه":
                # This command removes the bot from the group.
                debug("remove bot called")
                await update.message.reply_text(MSG_DELETE_FROM_GROUP)

                await update.message.delete()

                await context.bot.leave_chat(update.effective_chat.id)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
