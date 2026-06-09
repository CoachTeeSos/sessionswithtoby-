/* ═══════════════════════════════════════════════════════════════
   GEO-IP CURRENCY ENGINE — ipapi.co
   Detects visitor country, swaps pricing NGN ↔ USD
   ═══════════════════════════════════════════════════════════════ */
(function() {
  'use strict';

  window.USER_CURRENCY = 'USD';
  window.USER_SYMBOL = '$';
  window.USER_IS_NG = false;

  function applyCurrency(isNG, currency, symbol) {
    window.USER_IS_NG = isNG;
    window.USER_CURRENCY = currency;
    window.USER_SYMBOL = symbol;

    // Swap all price elements
    document.querySelectorAll('[data-price-usd]').forEach(function(el) {
      var usd = el.getAttribute('data-price-usd');
      var ngn = el.getAttribute('data-price-ngn');
      if (isNG && ngn) {
        el.textContent = symbol + parseInt(ngn).toLocaleString();
      } else {
        el.textContent = symbol + parseInt(usd).toLocaleString();
      }
    });

    // Update currency labels
    document.querySelectorAll('[data-currency-label]').forEach(function(el) {
      el.textContent = currency;
    });

    // Show/hide region-specific elements
    document.querySelectorAll('[data-ng-only]').forEach(function(el) {
      el.style.display = isNG ? '' : 'none';
    });
    document.querySelectorAll('[data-intl-only]').forEach(function(el) {
      el.style.display = isNG ? 'none' : '';
    });

    // Update Flutterwave data-currency on pay buttons
    document.querySelectorAll('[data-fw-btn]').forEach(function(el) {
      el.setAttribute('data-currency', currency);
    });

    document.dispatchEvent(new CustomEvent('currencyDetected', {
      detail: { currency: currency, symbol: symbol, isNG: isNG }
    }));
  }

  function detect() {
    // Check localStorage cache (24h)
    try {
      var cached = localStorage.getItem('ct_geo');
      if (cached) {
        var d = JSON.parse(cached);
        if (d.ts && (Date.now() - d.ts) < 86400000) {
          applyCurrency(d.isNG, d.currency, d.symbol);
          return;
        }
      }
    } catch (e) {}

    // Primary: ipapi.co
    fetch('https://ipapi.co/json/')
      .then(function(r) { return r.json(); })
      .then(function(d) {
        var isNG = d.country_code === 'NG';
        var cur = isNG ? 'NGN' : 'USD';
        var sym = isNG ? '₦' : '$';
        localStorage.setItem('ct_geo', JSON.stringify({ isNG: isNG, currency: cur, symbol: sym, ts: Date.now() }));
        applyCurrency(isNG, cur, sym);
      })
      .catch(function() {
        // Fallback: ip-api.com
        fetch('https://ip-api.com/json/')
          .then(function(r) { return r.json(); })
          .then(function(d) {
            var isNG = d.countryCode === 'NG';
            var cur = isNG ? 'NGN' : 'USD';
            var sym = isNG ? '₦' : '$';
            applyCurrency(isNG, cur, sym);
          })
          .catch(function() {
            applyCurrency(false, 'USD', '$');
          });
      });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', detect);
  } else {
    detect();
  }
})();
