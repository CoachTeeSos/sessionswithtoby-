"""
Email nurture sequence for Coach Toby leads.
5-email follow-up series after welcome email.
Each template is personalized with lead's name, interest, and source.
"""
from datetime import datetime

SENDER_NAME = "Coach Toby"
SENDER_EMAIL = "prosperolumotobi@gmail.com"
WHATSAPP = "+234 916 010 6084"
WEBSITE = "https://coachteesos.github.io/coachtoby-site"

def _header(name):
    first = name.split()[0] if name else "there"
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;padding:24px;color:#1a1a1a;background:#f8f9fa;">
<div style="background:#fff;border-radius:16px;padding:32px;border:1px solid #e2e8f0;">
<h1 style="color:#004B49;margin-top:0;">Hey {first}! 🎤</h1>"""

def _footer():
    return f"""
<p>— Coach Toby<br><em>Sessions with Toby</em><br>
<a href="{WEBSITE}">{WEBSITE}</a><br>
WhatsApp: <strong>{WHATSAPP}</strong></p>
</div></body></html>"""

def email_2_biggest_mistake(name, interest="vocal coaching"):
    """Day 2: Value content - the #1 mistake singers make"""
    interest_label = "singing" if "vocal" in interest.lower() else "speaking" if "speak" in interest.lower() else "performing"
    return {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"name": name}],
        "subject": f"The #1 mistake {interest_label} students make (and how to fix it)",
        "htmlContent": _header(name) + f"""
<p>I've worked with 50+ students across 10+ countries, and there's <strong>one mistake</strong> I see over and over again:</p>

<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;padding:20px;margin:16px 0;">
<h3 style="margin-top:0;color:#92400E;">🚫 The Mistake</h3>
<p style="color:#92400E;">Trying to fix everything at once. Breath control, pitch, range, tone, confidence — all at the same time.</p>
</div>

<p>Here's what happens: you get overwhelmed, practice inconsistently, and after 3 months you feel like nothing changed.</p>

<p><strong>Here's the fix:</strong></p>

<ol>
<li><strong>Pick ONE thing.</strong> Just one. The thing that bothers you most.</li>
<li><strong>Work on it for 2 weeks.</strong> 10 minutes a day. Every day.</li>
<li><strong>Measure progress.</strong> Record yourself on day 1 and day 14. The difference will shock you.</li>
</ol>

<div style="background:#F0F9FF;border:2px solid #0EA5E9;border-radius:12px;padding:20px;margin:16px 0;">
<h3 style="margin-top:0;color:#0C4A6E;">🎯 This Week's Challenge</h3>
<p style="color:#0C4A6E;">Record yourself singing a simple song. Just 30 seconds. Don't judge it — just save it. That's your baseline. In 2 weeks, you'll thank yourself.</p>
</div>

<p>Want me to personally guide you through this? <a href="{WEBSITE}/book.html">Book a free 15-min demo</a> and I'll show you exactly where to start.</p>

<p>No pressure. Just one step at a time. 🎤</p>""" + _footer()
    }

def email_3_success_story(name, student_name="Sarah"):
    """Day 4: Social proof - student success story"""
    return {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"name": name}],
        "subject": f"How {student_name} went from 'I can't sing' to performing on stage",
        "htmlContent": _header(name) + f"""
<p>Let me tell you about {student_name}.</p>

<p>{student_name} came to me 6 months ago. She'd been singing in her church choir for 5 years but had <strong>never</strong> sung a solo. Every time she tried, her voice would crack on the high notes. Her throat would tighten. She'd feel the embarrassment wash over her.</p>

<p>She thought she just wasn't built for singing.</p>

<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:20px;margin:16px 0;">
<h3 style="margin-top:0;color:#166534;">✅ Where She Is Now</h3>
<p style="color:#166534;">Last month, {student_name} sang a solo in front of 200 people. No cracking. No tightening. Just her voice, clear and strong. She cried afterward — the good kind of crying.</p>
</div>

<p>What changed?</p>

<p>Not talent. Not luck. <strong>Technique + consistency.</strong></p>

<p>We worked on three things:</p>
<ol>
<li><strong>Breath support</strong> — Stopping the throat from doing all the work</li>
<li><strong>Placement</strong> — Getting the sound forward so it resonates, not strains</li>
<li><strong>Progressive range building</strong> — Expanding one half-step at a time, no forcing</li>
</ol>

<p>{student_name}'s exact words: <em>"I thought I wasn't built for singing. Turns out I just wasn't built to figure it out alone."</em></p>

<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;padding:20px;margin:16px 0;text-align:center;">
<h3 style="margin-top:0;color:#92400E;">🎤 Your Turn</h3>
<p style="color:#92400E;">The first session is free. No commitment. Just 15 minutes to see if we're a good fit.</p>
<a href="{WEBSITE}/book.html" style="display:inline-block;padding:16px 32px;background:#004B49;color:#fff;font-weight:700;text-decoration:none;border-radius:12px;margin-top:8px;">Book Your Free Demo →</a>
</div>

<p>Your voice has more in it than you think. Let's find out together. 🎤</p>""" + _footer()
    }

def email_4_urgency(name):
    """Day 7: Urgency - limited spots, your voice won't wait"""
    return {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"name": name}],
        "subject": "Your voice won't wait (and neither should you)",
        "htmlContent": _header(name) + f"""
<p>Hey {name.split()[0] if name else "there"},</p>

<p>I want to be real with you for a second.</p>

<p>Every week, I get messages from people saying the same thing: <em>"I've been thinking about getting a vocal coach for months..."</em></p>

<p>Months.</p>

<p>Here's what I've learned after coaching 50+ students: <strong>The ones who start now are the ones who see results.</strong> The ones who wait for the "perfect time" are still waiting a year later.</p>

<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;padding:20px;margin:16px 0;">
<h3 style="margin-top:0;color:#92400E;">⏰ Why Now?</h3>
<ul style="color:#92400E;padding-left:20px;">
<li>Your voice is aging — the sooner you train it, the better the results</li>
<li>Bad habits get harder to fix the longer you wait</li>
<li>I only take <strong>5 new students per month</strong> — this month has 2 spots left</li>
</ul>
</div>

<p>I'm not saying this to pressure you. I'm saying it because I've seen too many talented people wait too long.</p>

<p><strong>The free demo is exactly that — free.</strong> No commitment. No credit card. Just 15 minutes to see what's possible.</p>

<div style="text-align:center;margin:24px 0;">
<a href="{WEBSITE}/book.html" style="display:inline-block;padding:16px 32px;background:#004B49;color:#fff;font-weight:700;text-decoration:none;border-radius:12px;font-size:1.1rem;">Claim Your Free Demo →</a>
</div>

<p>If it's not the right time, no hard feelings. But if you've been thinking about it... <strong>now is the time.</strong></p>

<p>Let's do this. 🎤</p>""" + _footer()
    }

def email_5_final(name):
    """Day 14: Final follow-up - last chance or still interested"""
    return {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"name": name}],
        "subject": "Should I close your file?",
        "htmlContent": _header(name) + f"""
<p>Hey {name.split()[0] if name else "there"},</p>

<p>I've sent you a few emails over the past couple weeks, and I haven't heard back.</p>

<p>That's totally fine — life gets busy, and maybe the timing isn't right.</p>

<p>But I want to make sure I'm not clogging up your inbox, so here's what I'm going to do:</p>

<p><strong>If you're still interested in vocal coaching,</strong> just reply to this email or send me a WhatsApp message at <strong>{WHATSAPP}</strong> and I'll get back to you within 24 hours.</p>

<p><strong>If now's not the right time,</strong> no worries at all. I'll remove you from this sequence and you won't hear from me again (unless you reach out).</p>

<p>Either way, I wish you the best with your voice. 🎤</p>

<p>— Coach Toby</p>

<p><small>P.S. — If you want to stay connected without the emails, you can always find me on WhatsApp: <strong>{WHATSAPP}</strong></small></p>""" + _footer()
    }

def build_nurture_email(name, email, sequence_day, interest="Vocal Coaching", source="Quiz"):
    """Build the right email based on sequence day."""
    templates = {
        2: email_2_biggest_mistake,
        3: email_3_success_story,
        4: email_4_urgency,
        5: email_5_final,
    }
    builder = templates.get(sequence_day)
    if not builder:
        return None
    payload = builder(name)
    payload["to"] = [{"email": email, "name": name}]
    return payload

if __name__ == "__main__":
    # Test: print email 2 for a sample lead
    test = email_2_biggest_mistake("David")
    print(f"Subject: {test['subject']}")
    print(f"To: {test['to']}")
    print(f"HTML length: {len(test['htmlContent'])} chars")
    print("Templates OK")
