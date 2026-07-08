/* lms/pages.js — runtime app: auth, nav, submission */
const app = {
  init() {
    try {
      const cfg = JSON.parse(localStorage.getItem('swt_config')||'{}');
      if (cfg.formsubmitUrl) Store.formsubmitUrl = cfg.formsubmitUrl;
    } catch {}
  },
  setFormSubmit(url) {
    url = (url||'').trim();
    if (!url) return false;
    Store.formsubmitUrl = url;
    try { localStorage.setItem('swt_config', JSON.stringify({formsubmitUrl: url})); } catch {}
    return true;
  },
  lmsNav(page) {
    if (!LMS) return;
    LMS.show(page);
  },
  lmsLogout() {
    try { localStorage.removeItem('swt_user'); } catch {}
    const gate = document.getElementById('emailGate');
    const user = document.getElementById('lmsUser');
    if (gate) gate.style.display = 'block';
    if (user) user.textContent = '';
    const main = document.getElementById('lmsMain');
    if (main) main.style.display = 'none';
    if (LMS) LMS.current = 'dashboard';
  },
  submitGateEmail() {
    const input = document.getElementById('gateEmail');
    const email = (input && input.value || '').trim();
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      if (input) input.style.borderColor = '#EF4444';
      return;
    }
    const payload = {email, Plan: 'LMS Access', Source: 'entry_gate'};
    Promise.resolve(Store.submitEmail(payload)).catch(() => {});
    try {
      localStorage.setItem('swt_user', JSON.stringify({email, submittedAt: Date.now()}));
    } catch {}
    const gate = document.getElementById('emailGate');
    const user = document.getElementById('lmsUser');
    const main = document.getElementById('lmsMain');
    if (gate) gate.style.display = 'none';
    if (user) user.textContent = email;
    if (main) main.style.display = 'block';
    if (LMS) LMS.show('dashboard');
    try { Store.flushQueue(); } catch {}
  }
};
window.app = app;
