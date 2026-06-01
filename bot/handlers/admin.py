"""
handlers/admin.py — Admin-only commands: /reply, /broadcast, /stats, /escalations.
"""
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_IDS
from services.airtable import AirtableService
from templates.messages import (
    REPLY_SENT, REPLY_NOT_FOUND, BROADCAST_USAGE, BROADCAST_SENT,
    ADMIN_HELP, STATS_TEMPLATE,
    ESCALATIONS_HEADER, ESCALATION_ITEM, ESCALATIONS_EMPTY,
)

logger = logging.getLogger(__name__)


async def admin_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        return
    await update.message.reply_text(ADMIN_HELP, parse_mode="Markdown")


async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: /reply <esc_id> <message> — reply to escalated student message."""
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Usage: `/reply <message_id> <your message>`\n\n"
            "Example: `/reply 42 Thanks for reaching out! Let's schedule a call.`",
            parse_mode="Markdown",
        )
        return

    esc_id = context.args[0]
    reply_text = " ".join(context.args[1:])
    airtable: AirtableService = context.bot_data["airtable"]

    # Find the escalation
    esc = await airtable.get_escalation(int(esc_id))
    if not esc:
        await update.message.reply_text(
            REPLY_NOT_FOUND.format(esc_id=esc_id),
            parse_mode="Markdown",
        )
        return

    # Forward reply to student
    student_id = esc["telegram_id"]
    try:
        await context.bot.send_message(
            chat_id=student_id,
            text=f"**From your coach:**\n\n{reply_text}",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Failed to send reply to {student_id}: {e}")
        await update.message.reply_text(f"❌ Could not reach student {student_id}.")
        return

    # Mark escalation as replied
    await airtable.reply_escalation(int(esc_id), reply_text)

    await update.message.reply_text(
        REPLY_SENT.format(student_name=f"Student #{student_id}"),
    )


async def escalations_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: /escalations — list pending escalations."""
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        return

    airtable: AirtableService = context.bot_data["airtable"]
    pending = await airtable.get_pending_escalations()

    if not pending:
        await update.message.reply_text(ESCALATIONS_EMPTY)
        return

    lines = [ESCALATIONS_HEADER]
    for esc in pending:
        lines.append(ESCALATION_ITEM.format(
            esc_id=esc["id"],
            student_name=f"Student #{esc['telegram_id']}",
            message=(esc["message_text"] or "")[:100],
        ))

    await update.message.reply_text("".join(lines), parse_mode="Markdown")


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: /broadcast <message> — send to all active students."""
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        return

    if not context.args:
        await update.message.reply_text(BROADCAST_USAGE, parse_mode="Markdown")
        return

    broadcast_text = " ".join(context.args)
    airtable: AirtableService = context.bot_data["airtable"]

    # Get all active students
    active_students = await airtable.get_all_active_students()

    if not active_students:
        await update.message.reply_text("No active students to broadcast to.")
        return

    sent = 0
    failed = 0
    for student in active_students:
        sid = student.get("telegram_id", "")
        if not sid:
            continue
        try:
            await context.bot.send_message(
                chat_id=int(sid),
                text=f"📢 **Announcement**\n\n{broadcast_text}",
                parse_mode="Markdown",
            )
            sent += 1
        except Exception as e:
            logger.warning(f"Broadcast failed for {sid}: {e}")
            failed += 1

    await update.message.reply_text(
        BROADCAST_SENT.format(count=f"{sent} sent, {failed} failed"),
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin: /stats — student statistics."""
    user = update.effective_user
    if user.id not in ADMIN_IDS:
        return

    airtable: AirtableService = context.bot_data["airtable"]

    active = await airtable.get_all_active_students()
    pending = await airtable.get_pending_payments()

    total_sessions = sum(s.get("sessions_used", 0) for s in active)

    # Calculate revenue
    from config import SERVICES
    revenue = 0
    for s in active:
        svc = SERVICES.get(s.get("service_key", ""), {})
        revenue += svc.get("price", 0)

    await update.message.reply_text(
        STATS_TEMPLATE.format(
            active_count=len(active),
            pending_count=len(pending),
            total_sessions=total_sessions,
            revenue=f"${revenue:,}" if revenue < 10000 else f"₦{revenue:,}",
            timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        ),
        parse_mode="Markdown",
    )
