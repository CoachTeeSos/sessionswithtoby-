/**
 * Security Module — Sessions with Toby
 * Include on every page with forms.
 * Handles: CSRF tokens, input sanitization, honeypot, rate limiting, referrer checks
 */
(function() {
  'use strict';

  // ── CSRF Token Generation ──
  function generateToken() {
    var array = new Uint8Array(32);
    if (window.crypto && window.crypto.getRandomValues) {
      window.crypto.getRandomValues(array);
    } else {
      for (var i = 0; i < 32; i++) {
        array[i] = Math.floor(Math.random() * 256);
      }
    }
    return Array.from(array, function(b) { return b.toString(16).padStart(2, '0'); }).join('');
  }

  // Get or create CSRF token
  function getCSRFToken() {
    var token = sessionStorage.getItem('ct_csrf');
    if (!token) {
      token = generateToken();
      sessionStorage.setItem('ct_csrf', token);
    }
    return token;
  }

  // ── Input Sanitization ──
  function sanitizeInput(value) {
    if (typeof value !== 'string') return '';
    return value
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;')
      .replace(/javascript:/gi, '')
      .replace(/on\w+=/gi, '')
      .trim();
  }

  function sanitizeEmail(value) {
    var sanitized = sanitizeInput(value);
    // Basic email validation
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(sanitized) ? sanitized : '';
  }

  function sanitizeName(value) {
    var sanitized = sanitizeInput(value);
    // Allow letters, spaces, hyphens, apostrophes only
    return sanitized.replace(/[^a-zA-ZÀ-ÿ\s\-']/g, '').substring(0, 100);
  }

  function sanitizePhone(value) {
    var sanitized = sanitizeInput(value);
    // Allow +, digits, spaces, hyphens only
    return sanitized.replace(/[^\d+\s\-()]/g, '').substring(0, 20);
  }

  // ── Rate Limiting ──
  function checkRateLimit(action, maxAttempts, windowMs) {
    var key = 'ct_ratelimit_' + action;
    var now = Date.now();
    var attempts = JSON.parse(localStorage.getItem(key) || '[]');

    // Remove old attempts outside the window
    attempts = attempts.filter(function(ts) { return now - ts < windowMs; });

    if (attempts.length >= maxAttempts) {
      return false; // Rate limited
    }

    attempts.push(now);
    localStorage.setItem(key, JSON.stringify(attempts));
    return true;
  }

  // ── Honeypot Check ──
  function isHoneypotFilled(form) {
    var honeypot = form.querySelector('[data-honeypot]');
    return honeypot && honeypot.value !== '';
  }

  // ── Referrer Validation ──
  function isValidReferrer() {
    var referrer = document.referrer;
    var currentHost = window.location.hostname;
    // Allow empty referrer (direct access) or same origin
    if (!referrer) return true;
    try {
      var refUrl = new URL(referrer);
      return refUrl.hostname === currentHost ||
             refUrl.hostname === 'coachteesos.github.io' ||
             refUrl.hostname === '';
    } catch(e) {
      return false;
    }
  }

  // ── Secure Form Submission Wrapper ──
  function secureSubmit(form, options) {
    options = options || {};

    // Check honeypot
    if (isHoneypotFilled(form)) {
      console.warn('Honeypot triggered — possible bot');
      // Fake success to confuse bots
      if (options.onSuccess) options.onSuccess({success: true});
      return false;
    }

    // Rate limit
    var action = options.action || 'form_submit';
    if (!checkRateLimit(action, options.maxAttempts || 5, options.windowMs || 60000)) {
      if (options.onRateLimited) {
        options.onRateLimited();
      } else {
        alert('Too many attempts. Please wait a moment and try again.');
      }
      return false;
    }

    // Sanitize all inputs
    var sanitizedData = {};
    var inputs = form.querySelectorAll('input[name], textarea[name], select[name]');
    inputs.forEach(function(input) {
      var name = input.name;
      var value = input.value;

      if (name === 'email') {
        sanitizedData[name] = sanitizeEmail(value);
      } else if (name === 'name' || Name || 'Name') {
        sanitizedData[name] = sanitizeName(value);
      } else if (name === 'phone' || name === 'whatsapp' || name === 'WhatsApp') {
        sanitizedData[name] = sanitizePhone(value);
      } else {
        sanitizedData[name] = sanitizeInput(value);
      }
    });

    // Add CSRF token
    sanitizedData._csrf = getCSRFToken();
    sanitizedData._timestamp = Date.now();

    // Add sanitized data to form as hidden fields
    Object.keys(sanitizedData).forEach(function(key) {
      var existing = form.querySelector('input[name="' + key + '"]');
      if (existing) {
        existing.value = sanitizedData[key];
      } else {
        var hidden = document.createElement('input');
        hidden.type = 'hidden';
        hidden.name = key;
        hidden.value = sanitizedData[key];
        form.appendChild(hidden);
      }
    });

    return true; // Allow submission to proceed
  }

  // ── Secure Storage ──
  // Don't store sensitive data in localStorage. Use sessionStorage instead.
  function secureSet(key, value) {
    try {
      sessionStorage.setItem(key, JSON.stringify(value));
    } catch(e) {
      // Storage full or disabled — fail silently
    }
  }

  function secureGet(key) {
    try {
      var value = sessionStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch(e) {
      return null;
    }
  }

  function secureRemove(key) {
    try {
      sessionStorage.removeItem(key);
    } catch(e) {}
  }

  // ── Expose Public API ──
  window.CoachTobySecurity = {
    csrfToken: getCSRFToken,
    sanitize: {
      input: sanitizeInput,
      email: sanitizeEmail,
      name: sanitizeName,
      phone: sanitizePhone
    },
    rateLimit: checkRateLimit,
    honeypot: isHoneypotFilled,
    referrer: isValidReferrer,
    submit: secureSubmit,
    storage: {
      set: secureSet,
      get: secureGet,
      remove: secureRemove
    }
  };
})();
