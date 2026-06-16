/* ═══════════════════════════════════════════════════════════════
   FLUTTERWAVE PAYMENT ENGINE
   Security: validates amounts against allowed values
   ═══════════════════════════════════════════════════════════════ */
(function() {
  'use strict';

  // Flutterwave public key (safe to expose — required by FW SDK)
  window.FLUTTERWAVE_PUBLIC_KEY = 'FLWPUBK-78adfe8e1b994186bb4af437f33105cc-X';

  // Allowed payment amounts — prevents tampering
  var ALLOWED_AMOUNTS = {
    'single': {usd: 50, ngn: 70000},
    'monthly': {usd: 200, ngn: 300000},
    'ngn-single': {ngn: 70000},
    'ngn-monthly': {ngn: 300000}
  };

  // Telegram bot deep link (from data-telegram attribute on page)
  var TELEGRAM_BOT_HANDLE = '';
  var TELEGRAM_BOT_ID = '';

  /** Validate payment amount against allowed values **/
  function validateAmount(plan, amount, currency) {
    var allowed = ALLOWED_AMOUNTS[plan];
    if (!allowed) return false;
    var cur = currency.toLowerCase();
    if (allowed[cur] && allowed[cur] === parseFloat(amount)) return true;
    return false;
  }

  /**
   * Initialize a Flutterwave checkout from a button click.
   * Reads: data-amount, data-currency, data-email, data-name, data-telegram
   */
  function initFWCheckout(btn) {
    var amount = btn.getAttribute('data-amount') || '0';
    var currency = btn.getAttribute('data-currency') || window.USER_CURRENCY || 'USD';
    var email = btn.getAttribute('data-email') || '';
    var name = btn.getAttribute('data-name') || '';
    var telegram = btn.getAttribute('data-telegram') || '';
    var plan = btn.getAttribute('data-plan') || '';
    var ref = 'CT-' + Date.now() + '-' + Math.random().toString(36).substr(2, 6).toUpperCase();

    // Validate amount hasn't been tampered with
    if (plan && !validateAmount(plan, amount, currency)) {
      console.warn('Payment amount validation failed — possible tampering');
      alert('Invalid payment amount. Please refresh the page and try again.');
      return;
    }

    if (telegram) {
      TELEGRAM_BOT_HANDLE = telegram;
    }

    if (typeof FlutterwaveCheckout !== 'function') {
      alert('Payment system loading... Please try again in a few seconds.');
      return;
    }

    FlutterwaveCheckout({
      public_key: window.FLUTTERWAVE_PUBLIC_KEY,
      tx_ref: ref,
      amount: parseFloat(amount),
      currency: currency,
      payment_options: 'card,banktransfer,ussd',
      customer: {
        email: email,
        name: name
      },
      callback: function(data) {
        if (data.status === 'successful' || data.status === 'completed') {
          var botUrl = TELEGRAM_BOT_ID
            ? 'https://t.me/' + TELEGRAM_BOT_ID
            : 'https://t.me/Retpipebot';

          // Show brief confirmation then redirect
          document.body.innerHTML =
            '<div style="display:flex;align-items:center;justify-content:center;min-height:100vh;background:#FDFBF7;text-align:center;padding:2rem">' +
              '<div>' +
                '<div style="font-size:4rem;margin-bottom:1rem">✅</div>' +
                '<h2 style="font-family:Syne,sans-serif;font-weight:800;color:#004B49;font-size:1.8rem;margin-bottom:0.5rem">Payment Confirmed!</h2>' +
                '<p style="color:#5A7D7C;margin-bottom:1.5rem">Redirecting you to Telegram...</p>' +
                '<a href="' + botUrl + '" class="btn-primary" id="tg-redirect">Go to Bot Now →</a>' +
              '</div>' +
            '</div>';

          setTimeout(function() {
            window.location.href = botUrl;
          }, 2000);
        }
      },
      onclose: function() {},
      customizations: {
        title: 'Sessions with Toby',
        description: 'Vocal coaching payment',
        logo: ''
      }
    });
  }

  // Auto-wire all buttons with data-fw-btn attribute
  function wireFWButtons() {
    document.querySelectorAll('[data-fw-btn]').forEach(function(btn) {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        initFWCheckout(btn);
      });
    });
  }

  // Wire on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wireFWButtons);
  } else {
    wireFWButtons();
  }

  // Expose globally
  window.initFWCheckout = initFWCheckout;
  window.validateFWAmount = validateAmount;
})();
