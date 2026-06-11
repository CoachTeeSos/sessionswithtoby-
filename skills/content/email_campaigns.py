#!/usr/bin/env python3
"""
Email Campaign Generator - Vocal Coaching
Generates targeted email sequences based on pain points + location data.
"""
import json, os
from datetime import datetime
from pathlib import Path

VAULT_DIR = Path('/home/user/workspace/vault')

# ── EMAIL TEMPLATES ─────────────────────────────────────────────────────────

COLD_OUTREACH = {
    'subject_lines': [
        "{name}, your voice is holding you back",
        "The real reason you can't hit those notes",
        "Why 90% of singers plateau (and how to break through)",
        "{name}, what if your voice could do more?",
        "The singing secret nobody teaches",
    ],
    'hooks': [
        "Most singers spend years practicing the wrong things.",
        "Your voice isn't broken — your coordination is.",
        "The difference between amateurs and professionals isn't talent.",
        "You've probably been told you 'can't sing.' That's a lie.",
        "What if the problem was never your voice?",
    ],
    'pain_points': [
        "Straining for high notes",
        "Voice cracks and breaks",
        "Running out of breath",
        "Can't find your mix voice",
        "Vocal fatigue",
        "Inconsistent tone",
        "Fear of judgment",
        "No progress despite practice",
    ],
    'solutions': [
        "NYVC-based vocal coordination training",
        "Private 1-on-1 coaching with instant feedback",
        "Customized exercise programs for your voice type",
        "Performance coaching for stage confidence",
        "Vocal health and longevity protocols",
    ],
    'ctas': [
        "Book a free vocal assessment → [link]",
        "Watch a free training → [link]",
        "Reply 'VOICE' for a personalized plan",
        "Join the free community → [link]",
        "Schedule a call → [link]",
    ],
}

WELCOME_SEQUENCE = {
    'day_0': {
        'subject': "Welcome — your voice journey starts here",
        'content': """Hey {name},

Welcome to Sessions with Toby.

You're here because you know your voice can do more. Maybe you've been told you "can't sing." Maybe you've tried YouTube tutorials with no progress. Maybe you just want to sing with confidence.

Here's what I know: Your voice isn't broken. It's a coordination issue — and coordination can be trained.

Over the next few days, I'm going to share:
- The #1 mistake most singers make
- A simple exercise that changes everything
- How to practice without wasting time

Talk soon,
Coach Toby""",
    },
    'day_1': {
        'subject': "The #1 mistake singers make",
        'content': """Hey {name},

Quick question: Do you push harder for high notes?

If so, you're not alone. It's the most common mistake I see.

Here's the truth: High notes don't require more force. They require different coordination.

Think of it like shifting gears in a car. You don't press the gas harder — you shift.

Your voice has "gears" too (chest, mix, head). The problem isn't power — it's coordination.

Tomorrow, I'll show you a simple exercise that helps you find your "gears."

Talk soon,
Coach Toby""",
    },
    'day_3': {
        'subject': "The exercise that changes everything",
        'content': """Hey {name},

Here's an exercise that takes 2 minutes and can change how you think about your voice.

It's called the "Cry" exercise:

1. Think of a sad movie moment
2. Say "Wah" (like a baby crying) on a comfortable pitch
3. Feel the "sob" in your voice
4. Now sing "Wah" on a 5-tone scale: 1-2-3-4-5-4-3-2-1

What you're feeling is your mix voice — the coordination that lets you sing high notes without straining.

Try it now. It should feel easy, not forced.

If this clicks for you, I have a free training that goes deeper: [link]

Talk soon,
Coach Toby""",
    },
    'day_7': {
        'subject': "Ready to go deeper?",
        'content': """Hey {name},

It's been a week since you joined. I hope the exercises have been helpful.

Here's the thing: Free content can only take you so far. At some point, you need personalized feedback.

That's what I do. I work with singers 1-on-1 to:
- Identify your specific coordination issues
- Build a customized training plan
- Get you results in weeks, not months

If you're serious about your voice, I have a few spots open this month.

Book a free vocal assessment: [link]

No pressure. Just a conversation about your voice and where you want to go.

Talk soon,
Coach Toby""",
    },
}

def generate_cold_email(name, location, pain_point, solution):
    """Generate a personalized cold email."""
    import random
    subject = random.choice(COLD_OUTREACH['subject_lines']).format(name=name)
    hook = random.choice(COLD_OUTREACH['hooks'])
    cta = random.choice(COLD_OUTREACH['ctas'])
    
    email = f"""Subject: {subject}

Hey {name},

{hook}

If you're in {location}, you know the music scene is competitive. The singers who stand out aren't always the most talented — they're the ones with the best coordination.

Here's what I've found working with singers:
- {pain_point} is the #1 issue I see
- It's not a talent problem — it's a training problem
- The right exercises can change everything in weeks

I help singers like you solve this through {solution}.

{cta}

Talk soon,
Coach Toby
Sessions with Toby
https://coachteesos.github.io/coachtoby-site/"""
    
    return email

def generate_welcome_email(name, day):
    """Generate welcome sequence email."""
    seq = WELCOME_SEQUENCE.get(day)
    if not seq:
        return None
    return f"Subject: {seq['subject']}\n\n{seq['content'].format(name=name)}"

def generate_campaign(target_location, target_audience='singers'):
    """Generate a full campaign for a target location."""
    targets = {
        'pain_points': COLD_OUTREACH['pain_points'][:3],
        'solutions': COLD_OUTREACH['solutions'][:2],
        'emails': [],
    }
    
    # Generate 3 emails for the campaign
    for i in range(3):
        email = generate_cold_email(
            name='{name}',
            location=target_location,
            pain_point=targets['pain_points'][i % len(targets['pain_points'])],
            solution=targets['solutions'][i % len(targets['solutions'])],
        )
        targets['emails'].append(email)
    
    return targets

if __name__ == '__main__':
    # Test
    print("=== CAMPAIGN TEST ===")
    campaign = generate_campaign('Lagos, Nigeria')
    for i, email in enumerate(campaign['emails'], 1):
        print(f"\n--- Email {i} ---")
        print(email[:300])
