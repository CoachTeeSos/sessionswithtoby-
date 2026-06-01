"""
handlers/group.py — Group message handler.
Bot 2 auto-leaves groups. Not designed for group use.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def group_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """If bot is added to a group, leave immediately."""
    chat = update.effective_chat
    if chat.type in ("group", "supergroup"):
        logger.info(f"Bot added to group {chat.id} — leaving")
        try:
            await context.bot.send_message(
                chat_id=chat.id,
                text="I only work in private DMs. Bye! 👋",
            )
            await context.bot.leave_chat(chat.id)
        except Exception as e:
            logger.error(f"Failed to leave group {chat.id}: {e}")
