/* bootstrap.js — replaces inline app.js with modular LMS */
// Google Analytics — matches prior property for SEO continuity
(function(){var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-J9V395RPDH';document.head.appendChild(s);window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-J9V395RPDH');})();
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
    if (window.Store && window.Store.submitEmail) {
      window.Store.submitEmail({
        Name: email.split('@')[0] || email,
        Email: email,
        Plan: 'LMS Entry',
        Status: 'Active',
        Source: 'LMS Entry'
      }).catch(()=>{});
    }
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
