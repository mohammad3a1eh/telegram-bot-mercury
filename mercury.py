from dotenv import load_dotenv
from os import getenv
from asyncio import sleep
from datetime import datetime, timedelta, timezone
from database import Database
from requests import get, exceptions
from random import choice
from logging import (
    debug,
    info,
    basicConfig,
    INFO,
    DEBUG as DEBUGG,
)
from telegram import (
    Update,
    ChatPermissions
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
    get_moderators
)

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
DEBUG = getenv("DEBUG")
MAX_WARNING = int(getenv("MAX_WARNING"))

if MAX_WARNING > 5:
    MAX_WARNING = 5

if DEBUG == "true":
    basicConfig(level=DEBUGG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')

info("Bot started")

db = Database()

info("Database initialized")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    debug("bot start in PV")
    await update.message.reply_text(MSG_START)

async def lock_text_only(update, context):
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_audios=False,
        can_send_documents=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
    )
    chat_id = update.effective_chat.id
    await context.bot.set_chat_permissions(chat_id, permissions=permissions)
    msg = await update.message.reply_text("قفل رسانه گروه فعال شد.")

    await sleep(10)
    await msg.delete()

async def lock_full(update, context):
    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_audios=False,
        can_send_documents=False,
        can_send_photos=False,
        can_send_videos=False,
        can_send_video_notes=False,
        can_send_voice_notes=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
    )

    chat_id = update.effective_chat.id
    await context.bot.set_chat_permissions(chat_id, permissions=permissions)
    msg = await update.message.reply_text("قفل کامل گروه فعال شد.")

    await sleep(10)
    await msg.delete()

async def lock_end(update, context):
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_audios=True,
        can_send_documents=True,
        can_send_photos=True,
        can_send_videos=True,
        can_send_video_notes=True,
        can_send_voice_notes=True,
        can_send_polls=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )

    chat_id = update.effective_chat.id

    await context.bot.set_chat_permissions(chat_id, permissions=permissions)
    msg = await update.message.reply_text("قفل گروه برداشته شد.")

    await sleep(10)
    await msg.delete()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    owner , admins = await get_moderators(update, context)
    admin_ids = [admin.user.id for admin in admins]
    owner_id = owner[0].user.id if owner else None

    text = update.message.text.strip()
    user_id = update.effective_user.id

    if user_id in [admin.user.id for admin in admins] or user_id == owner_id:
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

                await update.message.delete()

                msg = await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="شما برای 10 دقیقه بیصدا شدید.",
                    reply_to_message_id=target_message.message_id
                )
                await sleep(10)
                await msg.delete()

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

                msg = await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="ادمین شما را از بیصدا خارج کرد.",
                    reply_to_message_id=target_message.message_id
                )
                await sleep(10)
                await msg.delete()

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

            elif text == "اخطار":
                debug("warning user called")
                # check who sent the command
                sender_id = update.message.from_user.id

                if sender_id in admin_ids and sender_id != owner_id:
                    if target_user.id == owner_id:
                        msg = await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="شما نمیتوانید به سازنده اخطار بدهید.",
                            reply_to_message_id=update.message.message_id
                        )
                        await update.message.delete()
                        await sleep(10)
                        await msg.delete()
                        return
                    elif target_user.id in admin_ids:
                        msg = await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="شما نمیتوانید به ادمین اخطار بدهید.",
                            reply_to_message_id=update.message.message_id
                        )
                        await update.message.delete()
                        await sleep(10)
                        await msg.delete()
                        return
                    else:
                        db.add_warning(target_user.id)

                elif sender_id == owner_id:
                    db.add_warning(target_user.id)

                warnings = db.get_warning(target_user.id)
                if warnings >= MAX_WARNING:
                    msg = await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="کاربر به علت پر شدن ظرفیت اخطارها حذف خواهد شد.",
                        reply_to_message_id=update.message.message_id
                    )
                    await context.bot.ban_chat_member(
                        chat_id=update.effective_chat.id,
                        user_id=target_user.id
                    )

                    db.del_member(target_user.id)

                    await update.message.delete()
                else:
                    circles = " ".join(["🔴" if i < warnings else "⚪" for i in range(MAX_WARNING)])

                    msg = await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=(
                            f" کاربر {target_user.first_name} یک اخطار دریافت کرد.\n"
                            f"تعداد اخطارها: {circles}"
                        ),
                        reply_to_message_id=target_message.message_id
                    )
                    await update.message.delete()

                await sleep(10)
                await msg.delete()

        else:
            if text == "قفل رسانه":
                # This command allows users to only send text data.
                await lock_text_only(update=update, context=context)
                await update.message.delete()

            elif text == "قفل کامل":
                # This command completely restricts users from sending messages.
                await lock_full(update=update, context=context)
                await update.message.delete()

            elif text == "حذف قفل":
                # This command will reopen the sending of messages and media.
                await lock_end(update=update, context=context)
                await update.message.delete()

        if user_id == owner_id:
            debug("owner replay message")
            if update.message.reply_to_message:
                target_user = update.message.reply_to_message.from_user
                target_message = update.message.reply_to_message

                if text == "ارتقا به ادمین":
                    # This command will promote the user to admin if they are not already an admin.
                    debug("promote user to admin called")
                    if target_user.id in admin_ids:
                        await update.message.delete()

                        msg = await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="کاربر از قبل ادمین است.",
                            reply_to_message_id=target_message.message_id
                        )
                        await sleep(10)
                        await msg.delete()
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
                        await update.message.delete()

                        msg = await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="کاربر از قبل نیست.",
                            reply_to_message_id=target_message.message_id
                        )
                        await sleep(10)
                        await msg.delete()

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
                    await update.message.reply_text("ربات توسط سازنده از گروه حذف خواهد شد.")

                    await update.message.delete()

                    await context.bot.leave_chat(update.effective_chat.id)

    if text == "میم":
        # This command sends a random meme
        subreddits = ["memes", "funny", "dankmemes", "MinecraftMemes"]
        subreddit = choice(subreddits)

        try:
            url = f"https://meme-api.com/gimme/{subreddit}"
            res = get(url, timeout=5)
            res.raise_for_status()

            if "application/json" in res.headers.get("Content-Type", ""):
                data = res.json()
                meme_url = data.get("url")
                title = data.get("title", "")

                if meme_url:
                    await update.message.reply_photo(
                        photo=meme_url,
                        caption=title,
                        reply_to_message_id=update.message.message_id
                    )
                else:

                    error_msg = await update.message.reply_text("😅 میم پیدا نشد، دوباره امتحان کن!")
                    await update.message.delete()
                    await sleep(10)
                    await error_msg.delete()

            else:
                error_msg = await update.message.reply_text("📛 مشکل در دریافت میم (خروجی معتبر نبود).")
                await update.message.delete()
                await sleep(10)
                await error_msg.delete()

        except exceptions.RequestException as e:
            error_msg = await update.message.reply_text("🚧 فعلاً به میم‌ها دسترسی ندارم، یه کم بعد دوباره امتحان کن.")
            await update.message.delete()
            await sleep(10)
            await error_msg.delete()
            print("Error fetching meme:", e)

    # Add a user to the database if it does not already exist.
    db.check_or_add_member(
        user_id=user_id,
        username=update.message.from_user.username,
        first_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name,
    )

    # Add to sent message count
    db.increment_messages(user_id=user_id)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
