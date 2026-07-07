/* lms/pages.js — page render shells for current SPA data-page nodes */
const LMSPages = {
  init() {
    ['dashboard','learn','practice','assessments','mentor','coach','feedback','insights','community','funnel','analytics','email'].forEach(page => {
      const existing = document.querySelector('[data-page="' + page + '"]');
      if (existing && !existing.id) existing.id = page + 'Root';
    });
    const learnRoot = document.getElementById('learnRoot');
    if (learnRoot) { const d = document.createElement('div'); d.id='learnContent'; learnRoot.appendChild(d); }
    const dashboardRoot = document.getElementById('dashboardRoot');
    if (dashboardRoot) { const d = document.createElement('div'); d.id='statsContent'; dashboardRoot.appendChild(d); }
    const mentorRoot = document.getElementById('mentorRoot');
    if (mentorRoot) {
      const w = document.createElement('div'); w.id='mentorMessages'; w.className='mentor-messages'; mentorRoot.appendChild(w);
      const input = document.createElement('div'); input.className='mentor-input';
      input.innerHTML = '<input id="mentorInput" placeholder="Ask your vocal mentor...">';
      mentorRoot.appendChild(input);
    }
    const practiceRoot = document.getElementById('practiceRoot');
    if (practiceRoot) { const d = document.createElement('div'); d.id='practiceContent'; practiceRoot.appendChild(d); }
    const assessmentsRoot = document.getElementById('assessmentsRoot');
    if (assessmentsRoot) { const d = document.createElement('div'); d.id='assessmentsContent'; assessmentsRoot.appendChild(d); }
  }
};
window.LMSPages = LMSPages;
