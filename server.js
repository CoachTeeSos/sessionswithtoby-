/* ═══════════════════════════════════════════════════════════════
   server.js — Express Controller for Sessions with Toby
   Serves 20 flat HTML pages + Flutterwave webhook
   ═══════════════════════════════════════════════════════════════ */

const express = require('express');
const path = require('path');
const nodemailer = require('nodemailer');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;
const SITE_DIR = path.join(__dirname);

// ── Middleware ──
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ── Static Assets ──
app.use('/assets', express.static(path.join(SITE_DIR, 'assets')));

// ── Security: Verify Flutterwave webhook hash ──
function verifyFWWebhook(req, res, next) {
  const secretHash = process.env.FLW_WEBHOOK_HASH || '';
  const verify = req.query.verif_hash || req.headers['verif-hash'] || '';
  if (secretHash && verify !== secretHash) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
}

// ═══════════════════════════════════════════════════════════════
// FLUTTERWAVE WEBHOOK
// Receives async payment notifications
// ═══════════════════════════════════════════════════════════════
app.post('/webhook/flutterwave', verifyFWWebhook, async (req, res) => {
  const payload = req.body;

  // Only process successful charges
  if (payload.event === 'charge.completed' && payload.data && payload.data.status === 'successful') {
    const tx = payload.data;
    const customerEmail = tx.customer && tx.customer.email;
    const customerName = tx.customer && tx.customer.name || 'Student';
    const amount = tx.amount;
    const currency = tx.currency;
    const txRef = tx.tx_ref;

    console.log(`✅ Payment received: ${txRef} — ${currency} ${amount} from ${customerEmail}`);

    if (customerEmail) {
      try {
        await sendOnboardingEmail(customerEmail, customerName, amount, currency, txRef);
      } catch (err) {
        console.error('Email send failed:', err.message);
      }
    }
  }

  // Always return 200 so Flutterwave doesn't retry
  res.json({ status: 'ok' });
});

// ═══════════════════════════════════════════════════════════════
// ONBOARDING EMAIL (Nodemailer)
// ═══════════════════════════════════════════════════════════════
async function sendOnboardingEmail(email, name, amount, currency, txRef) {
  // Configure transporter from env vars
  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp-relay.brevo.com',
    port: parseInt(process.env.SMTP_PORT) || 587,
    secure: false,
    auth: {
      user: process.env.SMTP_USER || '',
      pass: process.env.SMTP_PASS || ''
    }
  });

  const telegramLink = 'https://t.me/Retpipebot';

  const htmlBody = `
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#FDFBF7;font-family:'Inter',system-ui,sans-serif;color:#004B49">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#FDFBF7;padding:2rem 1rem">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#fff;border:3px solid #004B49;border-radius:24px;overflow:hidden;box-shadow:6px 6px 0 #004B49">
        <!-- Header -->
        <tr><td style="background:#004B49;padding:2rem;text-align:center">
          <div style="font-size:2.5rem;margin-bottom:0.5rem">🎤</div>
          <h1 style="color:#D2E823;font-family:'Syne',sans-serif;font-weight:800;font-size:1.5rem;margin:0;letter-spacing:-0.02em">Sessions with Toby</h1>
          <p style="color:rgba(253,251,247,0.6);font-size:0.85rem;margin:0.5rem 0 0">Payment Confirmed ✓</p>
        </td></tr>

        <!-- Body -->
        <tr><td style="padding:2.5rem 2rem">
          <h2 style="font-family:'Syne',sans-serif;font-weight:800;font-size:1.3rem;margin:0 0 1rem;letter-spacing:-0.02em">Welcome, ${escapeHtml(name)}! 🎉</h2>

          <p style="color:#5A7D7C;font-size:1rem;line-height:1.7;margin:0 0 1.5rem">
            Your payment of <strong>${currency} ${parseFloat(amount).toLocaleString()}</strong> has been confirmed.
            Transaction reference: <code style="background:#F5F0E8;padding:2px 8px;border-radius:4px;font-size:0.85rem">${escapeHtml(txRef)}</code>
          </p>

          <p style="color:#5A7D7C;font-size:1rem;line-height:1.7;margin:0 0 2rem">
            You're one step closer to transforming your voice. Let's get you started.
          </p>

          <!-- Telegram CTA -->
          <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 2rem">
            <tr><td align="center" style="background:#F5F0E8;border:2px solid #004B49;border-radius:16px;padding:1.5rem;text-align:center">
              <p style="font-weight:700;font-size:1rem;margin:0 0 1rem">Your next step is simple:</p>
              <a href="${telegramLink}" style="display:inline-block;background:#58CC02;color:#004B49;font-weight:700;font-size:1rem;text-decoration:none;padding:1rem 2.5rem;border:3px solid #004B49;border-radius:16px;box-shadow:0 4px 0 #46A302">🎤 Open Telegram & Start →</a>
              <p style="color:#5A7D7C;font-size:0.8rem;margin:1rem 0 0">Click the button above to continue in Telegram</p>
            </td></tr>
          </table>

          <!-- Alternative -->
          <p style="color:#5A7D7C;font-size:0.9rem;line-height:1.6;text-align:center;margin:0 0 1rem">
            <strong>Don't have Telegram?</strong><br>
            No problem — simply reply to this email and we'll send you an alternative access link manually. We'll get you set up either way.
          </p>
        </td></tr>

        <!-- Footer -->
        <tr><td style="background:#004B49;padding:1.5rem 2rem;text-align:center">
          <p style="color:rgba(253,251,247,0.5);font-size:0.8rem;margin:0">© 2026 Sessions with Toby · All rights reserved</p>
          <p style="color:rgba(253,251,247,0.3);font-size:0.7rem;margin:0.5rem 0 0">You received this because a payment was made on coachtoby.com</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>`;

  const mailOptions = {
    from: process.env.SMTP_FROM || '"Sessions with Toby" <prosperolumotobi@gmail.com>',
    to: email,
    subject: '🎤 Welcome to Sessions with Toby — Your Payment is Confirmed',
    html: htmlBody,
    text: `Welcome, ${name}! Your payment of ${currency} ${amount} is confirmed.\n\nNext step: Open Telegram at ${telegramLink} to get started.\n\nDon't have Telegram? Reply to this email and we'll send you an alternative link.`
  };

  await transporter.sendMail(mailOptions);
  console.log(`📧 Onboarding email sent to ${email}`);
}

function escapeHtml(str) {
  return (str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ═══════════════════════════════════════════════════════════════
// PAGE ROUTES — Serve all 20 HTML pages
// ═══════════════════════════════════════════════════════════════

// Root
app.get('/', (req, res) => res.sendFile(path.join(SITE_DIR, 'index.html')));

// Main pages
app.get('/index.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'index.html')));
app.get('/home.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'home.html')));
app.get('/about.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'about.html')));
app.get('/book.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'book.html')));
app.get('/pricing.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'pricing.html')));
app.get('/blog.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'blog.html')));
app.get('/community.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'community.html')));
app.get('/abuja-community.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'abuja-community.html')));
app.get('/content.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'content.html')));
app.get('/lead-magnet.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'lead-magnet.html')));
app.get('/quiz.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'quiz.html')));
app.get('/links.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'links.html')));
app.get('/carousel-30days.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'carousel-30days.html')));
app.get('/carousel-generator.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'carousel-generator.html')));

// GEO pages
app.get('/geo/', (req, res) => res.sendFile(path.join(SITE_DIR, 'geo', 'index.html')));
app.get('/geo/index.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'geo', 'index.html')));
app.get('/geo/how-to-improve-singing-voice.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'geo', 'how-to-improve-singing-voice.html')));
app.get('/geo/how-to-overcome-stage-fright.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'geo', 'how-to-overcome-stage-fright.html')));
app.get('/geo/life-coaching-vs-therapy.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'geo', 'life-coaching-vs-therapy.html')));
app.get('/geo/online-vocal-coaching-nigeria.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'geo', 'online-vocal-coaching-nigeria.html')));
app.get('/geo/voice-coach-vs-singing-teacher.html', (req, res) => res.sendFile(path.join(SITE_DIR, 'geo', 'voice-coach-vs-singing-teacher.html')));

// 404 fallback
app.use((req, res) => {
  res.status(404).sendFile(path.join(SITE_DIR, 'home.html'));
});

// ═══════════════════════════════════════════════════════════════
// START
// ═══════════════════════════════════════════════════════════════
app.listen(PORT, () => {
  console.log(`🎤 Sessions with Toby — running on port ${PORT}`);
  console.log(`📂 Serving from: ${SITE_DIR}`);
});
