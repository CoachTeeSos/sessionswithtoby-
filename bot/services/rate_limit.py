"""
services/rate_limit.py — Per-user rate limiter with in-memory cooldowns.
"""
import time
import logging
from collections import defaultdict
from telegram import Update

from config import RATE_LIMIT_DM, RATE_LIMIT_MENU, RATE_LIMIT_ESCALATION, RATE_LIMIT_START

logger = logging.getLogger(__name__)


class RateLimiter:
    """Sliding window rate limiter per user per action type."""

    def __init__(self):
        # action_type → { user_id: [timestamps] }
        self._windows: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
        self._limits: dict[str, tuple[int, int]] = {
            # action: (max_calls, window_seconds)
            "dm_message":   (RATE_LIMIT_DM, 60),
            "menu_button":  (RATE_LIMIT_MENU, 5),
            "escalation":   (RATE_LIMIT_ESCALATION, 300),
            "start":        (RATE_LIMIT_START, 10),
        }

    def check(self, user_id: int, action: str) -> bool:
        """Return True if the action is allowed, False if rate-limited."""
        limit, window = self._limits.get(action, (10, 60))
        now = time.time()
        timestamps = self._windows[action][user_id]

        # Prune old entries
        self._windows[action][user_id] = [t for t in timestamps if now - t < window]

        if len(self._windows[action][user_id]) >= limit:
            logger.warning(f"Rate limited user {user_id} on action '{action}'")
            return False

        self._windows[action][user_id].append(now)
        return True

    def get_retry_after(self, user_id: int, action: str) -> int:
        """Seconds until the next allowed action."""
        limit, window = self._limits.get(action, (10, 60))
        timestamps = self._windows[action].get(user_id, [])
        if len(timestamps) < limit:
            return 0
        oldest = min(timestamps)
        return max(0, int(window - (time.time() - oldest)))
