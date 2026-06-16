#!/usr/bin/env python3
"""
Fulfillment Engine — Automated client journey management.
Handles: onboarding → nurturing → retention → graduation.
Runs as a cron job. No human intervention needed.
"""

import json
import os
import sys
import requests
from datetime import datetime, timedelta
from pathlib import Path

# ── Paths ──
BASE = Path.home() / ".hermes" / "coachtoby-site" / "bot"
DB_FILE = BASE / "fulfillment_db.json"
SEND_SCRIPT = Path.home() / ".hermes" / "coaching" / "send_telegram.py"

# ── Load DB ──
def load_db():
    if DB_FILE.exists():
        return json.loads(DB_FILE.read_text())
    return {"clients": {}, "automations": [], "metrics": {"total_clients": 0, "active": 0, "graduated": 0, "revenue_usd": 0}}

def save_db(db):
    DB_FILE.write_text(json.dumps(db, indent=2))

# ── Send Telegram ──
def send_tg(chat_id, text):
    try:
        token = None
        env_file = BASE / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("BOT_TOKEN="):
                    token = line.split("=", 1)[1].strip()
        if not token:
            return False
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        r = requests.post(url, json=data, timeout=10)
        return r.json().get("ok", False)
    except Exception as e:
        print(f"TG send error: {e}")
        return False

# ── Phase Detection ──
def get_phase(client):
    """Determine client phase based on journey progress."""
    joined = datetime.fromisoformat(client.get("joined", datetime.now().isoformat()))
    days_since = (datetime.now() - joined).days
    sessions = client.get("sessions_completed", 0)
    compliance = client.get("compliance_rate", 0)
    milestone = client.get("current_milestone", 0)

    if days_since <= 1:
        return "scouting"
    elif days_since <= 14:
        return "nurturing"
    elif sessions < 4:
        return "onboarding"
    elif milestone < 3:
        return "retaining"
    else:
        return "fulfillment"

# ── Automation Actions ──
def run_scouting(client_id, client):
    """Post-demo automation."""
    actions = []
    last_action = client.get("last_automation", "")
    tg_id = client.get("telegram_id")

    if last_action != "scout_welcome":
        send_tg(tg_id,
            "Welcome to Sessions with Toby! 🎤\n\n"
            "I'm your vocal coach assistant. Here's what happens next:\n\n"
            "1. I'll send you a quick vocal warmup every morning\n"
            "2. Track your progress as you practice\n"
            "3. Your coach will check in after your first session\n\n"
            "Reply with your full name to get started!"
        )
        actions.append("scout_welcome")

    return actions

def run_nurturing(client_id, client):
    """Week 1-2 daily engagement."""
    actions = []
    tg_id = client.get("telegram_id")
    day = client.get("nurture_day", 1)

    daily_messages = {
        1: "Day 1 🎤 Your first exercise:\n\n"
           "Lie on your back, put a book on your belly.\n"
           "Breathe in for 4 counts (book rises).\n"
           "Breathe out for 8 counts (book lowers).\n"
           "Do this for 3 minutes.\n\n"
           "Reply DONE when finished!",
        2: "Day 2 🎤 Lip trills!\n\n"
           "Relax your lips, blow air to make a buzz sound.\n"
           "Slide up and down your range like a siren.\n"
           "3 minutes. No forcing!\n\n"
           "Reply DONE when finished!",
        3: "Day 3 🎤 Sirens!\n\n"
           "Say 'WEE' sliding from your lowest to highest note.\n"
           "Then 'WOO' sliding back down.\n"
           "Keep it smooth — no gaps!\n\n"
           "How did it feel? Reply 1-5.",
        4: "Day 4 🎤 5-tone scale!\n\n"
           "Sing: Mum-mum-mum-mum-mum\n"
           "Go up a note. Back down.\n"
           "Keep the tone consistent.\n"
           "5 minutes today.\n\n"
           "Reply DONE!",
        5: "Day 5 🎤 Song day!\n\n"
           "Pick a song you love.\n"
           "Sing it using your new breath support.\n"
           "Record yourself — even just 30 seconds.\n\n"
           "What song did you pick?",
        6: "Day 6 🎤 Staccato breathing!\n\n"
           "Say 'HA-HA-HA-HA' — short bursts.\n"
           "Feel your abs engage each time.\n"
           "Do 20 bursts without breathing.\n\n"
           "How many could you do?",
        7: "Day 7 🎤 Week 1 check-in!\n\n"
           "You've completed your first week! 🎉\n\n"
           "Rate yourself 1-5:\n"
           "Breath control: ?\n"
           "Vocal comfort: ?\n"
           "Confidence: ?\n\n"
           "Reply with your 3 numbers!",
    }

    if day <= 7:
        msg = daily_messages.get(day, daily_messages[7])
        send_tg(tg_id, msg)
        client["nurture_day"] = day + 1
        actions.append(f"nurture_day_{day}")

    return actions

def run_onboarding(client_id, client):
    """Week 3-4 curriculum setup."""
    actions = []
    tg_id = client.get("telegram_id")
    last = client.get("last_automation", "")

    if last != "onboard_curriculum":
        path = client.get("curriculum_path", "Vocal Foundations")
        send_tg(tg_id,
            f"Your curriculum is ready! 📋\n\n"
            f"Path: {path}\n"
            f"Duration: 8-12 weeks\n\n"
            f"Here's your Week 3 plan:\n"
            f"1. Register blending exercises (10 min/day)\n"
            f"2. Vowel shaping drills (5 min/day)\n"
            f"3. Song application (10 min/day)\n\n"
            f"I'll check in daily. Let's build on your foundation!"
        )
        actions.append("onboard_curriculum")

    return actions

def run_retaining(client_id, client):
    """Ongoing engagement + upsell triggers."""
    actions = []
    tg_id = client.get("telegram_id")
    sessions = client.get("sessions_completed", 0)
    last = client.get("last_automation", "")

    # Upsell trigger at session 4
    if sessions == 4 and last != "retain_upsell":
        send_tg(tg_id,
            "You've completed 4 sessions! 🎉\n\n"
            "You've built a strong foundation. Ready to go deeper?\n\n"
            "The Monthly Package gives you:\n"
            "- 4 sessions/month (priority booking)\n"
            "- Daily check-ins with me\n"
            "- Personalized practice plans\n"
            "- Between-session support\n\n"
            "Reply UPGRADE to learn more!"
        )
        actions.append("retain_upsell")

    # Monthly progress report
    if sessions > 0 and sessions % 4 == 0:
        send_tg(tg_id,
            f"Monthly Progress Report 📊\n\n"
            f"Sessions completed: {sessions}\n"
            f"Practice compliance: {client.get('compliance_rate', 0)}%\n"
            f"Current milestone: {client.get('current_milestone', 0)}/5\n\n"
            f"Keep going! Your voice is transforming. 🎤"
        )
        actions.append(f"progress_report_{sessions}")

    return actions

def run_fulfillment(client_id, client):
    """Graduation + advocacy."""
    actions = []
    tg_id = client.get("telegram_id")
    milestone = client.get("current_milestone", 0)

    if milestone >= 5 and client.get("last_automation") != "graduated":
        send_tg(tg_id,
            "🎓 GRADUATION TIME! 🎓\n\n"
            "You've completed the Sessions with Toby program!\n\n"
            "Here's what you've achieved:\n"
            "✅ Strong breath support\n"
            "✅ Expanded vocal range\n"
            "✅ Confident performance skills\n"
            "✅ A voice you're proud of\n\n"
            "We'd love a short testimonial from you.\n"
            "Reply with your experience!\n\n"
            "P.S. Ask about our Alumni Maintenance Plan!"
        )
        actions.append("graduated")

    return actions

# ── Main Runner ──
def run_all():
    db = load_db()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[{now}] Fulfillment engine running...")

    for client_id, client in db["clients"].items():
        if client.get("status") != "active":
            continue

        phase = get_phase(client)
        actions = []

        if phase == "scouting":
            actions = run_scouting(client_id, client)
        elif phase == "nurturing":
            actions = run_nurturing(client_id, client)
        elif phase == "onboarding":
            actions = run_onboarding(client_id, client)
        elif phase == "retaining":
            actions = run_retaining(client_id, client)
        elif phase == "fulfillment":
            actions = run_fulfillment(client_id, client)

        if actions:
            client["last_automation"] = actions[-1]
            client["last_automation_time"] = now
            print(f"  {client_id}: {phase} → {actions}")

    save_db(db)
    print(f"[{now}] Done. {len(db['clients'])} clients processed.")

if __name__ == "__main__":
    run_all()
