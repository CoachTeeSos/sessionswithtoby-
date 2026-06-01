"""
services/router.py — Message categorization engine.
Matches incoming text to menu categories. Zero AI. Pure keyword scoring.
"""
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

# ── Keyword Banks ──
MENU_KEYWORDS: dict[str, list[str]] = {
    "schedule": [
        "schedule", "class", "time", "when", "timetable", "calendar",
        "session", "booking", "book", "lesson", "timing", "hour",
        "what time", "next class", "my schedule", "class time",
        "📅", "sched",
    ],
    "assignment": [
        "assignment", "homework", "task", "exercise", "practice",
        "work", "lesson", "recording", "submit", "upload", "send",
        "my homework", "my assignment", "📝", "hw",
    ],
    "payment": [
        "payment", "pay", "status", "invoice", "receipt", "paid",
        "how much", "pricing", "cost", "fee", "renew", "subscription",
        "extend", "outstanding", "balance", "💳",
    ],
    "bottleneck": [
        "bottleneck", "stuck", "blocked", "struggling", "problem",
        "issue", "help", "cant", "can't", "cannot", "difficult",
        "hard", "confused", "don't understand", "frustrated",
        "not working", "failing", "worried", "stressed", "anxious",
        " advice", " guidance", "support",
        "❓", "😭", "😫", "🙏",
    ],
    "contact": [
        "contact", "admin", "human", "person", "talk", "call",
        "speak", "reach", "message", "chat", "voice call",
        "one on one", "1-on-1", "private", "direct",
        "whatsapp", "phone", "📞",
    ],
    "menu": [
        "menu", "options", "back", "main", "home", "start",
        "help", "/help", "/menu", "👋",
    ],
}


def categorize(text: str) -> Optional[str]:
    """
    Match message text to the best menu category.
    Returns category name or None if no match (off-topic → escalate).
    """
    if not text:
        return None

    normalized = text.lower().strip()
    # Remove common punctuation
    normalized = re.sub(r"[!?.,;:]+", " ", normalized)

    scores: dict[str, int] = {}

    for category, keywords in MENU_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in normalized:
                score += 1
                # Exact word match gets bonus points
                if re.search(rf"\b{re.escape(kw)}\b", normalized):
                    score += 1
        if score > 0:
            scores[category] = score

    if not scores:
        logger.debug(f"No keyword match for: '{text[:50]}...'")
        return None

    best = max(scores, key=scores.get)
    logger.debug(f"Categorized '{text[:50]}' → {best} (score: {scores[best]})")
    return best


def is_payment_slip(update_text: str) -> bool:
    """Check if a message might be a payment slip (has photo or document)."""
    return False  # Handled by Telegram file type, not text
