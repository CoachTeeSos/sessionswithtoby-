/* bootstrap.js — replaces inline app.js with modular LMS */
window.app = {
  lmsNav(page) { LMS.nav(page); },
  lmsLogin() {
    const email = document.getElementById('lmsEmail')?.value?.trim();
    const user = email ? {email} : null;
    localStorage.setItem('swt_user', JSON.stringify(user));
    LMS.boot();
  },
  lmsLogout() {
    localStorage.removeItem('swt_user');
    localStorage.removeItem('swt_progress_v1');
    location.reload();
  },
  submitGateEmail() {
    const email = document.getElementById('gateEmail')?.value?.trim();
    if (!email) return;
    localStorage.setItem('swt_email_captured', JSON.stringify({email, ts: Date.now()}));
    document.getElementById('emailGate').style.display = 'none';
  }
};
document.addEventListener('DOMContentLoaded', () => {
  LMSPages.init();
  if (localStorage.getItem('swt_email_captured')) {
    const gate = document.getElementById('emailGate');
    if (gate) gate.style.display = 'none';
  }
});
