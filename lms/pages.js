/* lms/pages.js — runtime app: auth, nav, logging */
const app = {
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
    if (!email) return;
    const payload = {email, Plan: 'LMS Access'};
    Promise.resolve(Store.submitEmail(payload)).catch(() => {});
    try {
      localStorage.setItem('swt_user', JSON.stringify({email}));
    } catch {}
    const gate = document.getElementById('emailGate');
    const user = document.getElementById('lmsUser');
    const main = document.getElementById('lmsMain');
    if (gate) gate.style.display = 'none';
    if (user) user.textContent = email;
    if (main) main.style.display = 'block';
    if (LMS) LMS.show('dashboard');
  }
};
window.app = app;
