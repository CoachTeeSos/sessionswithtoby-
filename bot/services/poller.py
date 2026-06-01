"""
services/poller.py — Polls Airtable for payment status changes.
When a student's status flips from pending_payment → active,
Bot 2 auto-sends them the welcome message + menu.
"""
import asyncio
import logging
from datetime import datetime, timedelta

from services.airtable import AirtableService

logger = logging.getLogger(__name__)


class PaymentPoller:
    """Polls Airtable every 60s for students who became active."""

    def __init__(self, bot, airtable: AirtableService, interval: int = 60):
        self.bot = bot
        self.airtable = airtable
        self.interval = interval
        self._task = None
        self._seen_active: set[str] = set()  # telegram_ids we already welcomed

    async def start(self):
        self._task = asyncio.create_task(self._poll_loop())
        logger.info(f"Payment poller started (interval={self.interval}s)")

    async def stop(self):
        if self._task:
            self._task.cancel()
            logger.info("Payment poller stopped")

    async def _poll_loop(self):
        while True:
            try:
                await self._check_pending()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Poller error: {e}")
            await asyncio.sleep(self.interval)

    async def _check_pending(self):
        """Check all pending_payment records. If any changed to active, notify student."""
        # Only poll — don't require interaction
        try:
            students = await self.airtable.get_all_active_students()
            for student in students:
                tid = str(student.get("telegram_id", "")).strip()
                if not tid or tid in self._seen_active:
                    continue

                # Verify this student is now active and hasn't been welcomed
                record = await self.airtable.find_student(int(tid))
                if record and record.get("status") == "active":
                    # Check cache — did we already welcome them?
                    cache = await self.airtable._cache_get(tid)
                    if cache and cache.get("welcomed"):
                        self._seen_active.add(tid)
                        continue

                    # Send welcome + menu
                    from handlers.start import get_main_menu_keyboard
                    name = record.get("name", "there")
                    plan = record.get("plan", "")
                    sessions_used = record.get("sessions_used", 0)
                    total = record.get("total_sessions", 0)
                    sessions_left = max(0, total - sessions_used)

                    try:
                        await self.bot.send_message(
                            chat_id=int(tid),
                            text=(
                                f"✅ **Payment Confirmed!**\n\n"
                                f"Welcome aboard, **{name}**!\n"
                                f"📋 Plan: {plan}\n"
                                f"🎯 Sessions left: {sessions_left}\n\n"
                                f"Here's what I can help you with:"
                            ),
                            parse_mode="Markdown",
                            reply_markup=get_main_menu_keyboard(),
                        )
                        self._seen_active.add(tid)
                        # Mark as welcomed in cache
                        if cache:
                            cache["welcomed"] = True
                            await self.airtable._cache_set(cache)
                        logger.info(f"Auto-welcomed student {tid} ({name})")
                    except Exception as e:
                        logger.warning(f"Failed to welcome {tid}: {e}")
        except Exception as e:
            logger.error(f"Pending check failed: {e}")
