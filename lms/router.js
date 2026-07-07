/* lms/router.js — page router with data-driven lesson/completion logic */
const LMS = {
  current: 'dashboard',
  boot() {
    setTimeout(async () => {
      await Store.init();
      this.show('dashboard');
    }, 0);
  },
  show(page) {
    this.current = page;
    document.querySelectorAll('[data-page]').forEach(el => el.classList.add('hidden'));
    const root = document.querySelector('[data-page="' + page + '"]');
    if (root) root.classList.remove('hidden');
    if (page === 'learn') this.renderLearn();
    if (page === 'dashboard') this.renderDashboard();
    if (page === 'mentor') this.renderMentor();
    if (page === 'practice') this.renderPractice();
    if (page === 'assessments') this.renderAssessments();
  },
  nav(page) { this.show(page); },
  renderLearn() {
    const container = document.getElementById('learnContent');
    if (!container) return;
    const lessons = Store.lessons;
    const progress = Progress.load();
    container.innerHTML = lessons.map(l => {
      const state = progress[l.id];
      const locked = !Progress.canAccess(l.id);
      return '<div class="lesson-item ' + (locked ? 'locked' : '') + '">' +
        '<div><div style="font-weight:700">' + l.title + '</div>' +
        '<div style="font-size:0.8rem;color:#6B7280">' + l.level + ' · ' + l.durationMin + ' min</div></div>' +
        '<div style="font-size:0.75rem">' + (locked ? 'Locked' : state?.status || 'Start') + '</div>' +
        '</div>';
    }).join('');
  },
  startLesson(id) {
    if (!Progress.canAccess(id)) return;
    Progress.mark(id, {status:'started'});
    this.show('learn');
  },
  renderDashboard() {
    const progress = Progress.load();
    const xp = Progress.xpFor(progress);
    const completed = Object.values(progress).filter(s => s.status === 'passed' || s.status === 'mastered').length;
    const el = document.getElementById('statsContent');
    if (!el) return;
    el.innerHTML = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">' +
      '<div><div style="font-size:1.5rem;font-weight:800">' + xp + '</div><div style="font-size:0.8rem;color:#6B7280">XP</div></div>' +
      '<div><div style="font-size:1.5rem;font-weight:800">' + completed + '</div><div style="font-size:0.8rem;color:#6B7280">Lessons done</div></div>' +
      '<div><div style="font-size:1.5rem;font-weight:800">' + Store.lessons.length + '</div><div style="font-size:0.8rem;color:#6B7280">Lessons total</div></div>' +
      '</div>';
  },
  renderMentor() {
    const wrap = document.getElementById('mentorMessages');
    if (!wrap) return;
    wrap.innerHTML = '<div class="mentor-msg mentor-msg-bot">What do you want to work on today?</div>';
    const input = document.getElementById('mentorInput');
    if (!input) return;
    input.focus();
    input.onkeydown = (e) => {
      if (e.key !== 'Enter') return;
      const text = input.value.trim(); if (!text) return;
      wrap.innerHTML += '<div class="mentor-msg mentor-msg-user">' + text + '</div>';
      input.value = '';
      setTimeout(() => {
        wrap.innerHTML += '<div class="mentor-msg mentor-msg-bot">' + Mentor.reply([], text) + '</div>';
        wrap.scrollTop = wrap.scrollHeight;
      }, 200);
    };
  },
  renderPractice() {
    const el = document.getElementById('practiceContent');
    if (!el) return;
    el.innerHTML = '<div style="padding:12px;border-radius:8px;background:#F3F4F6"><div style="font-weight:700">Sustained Note</div><div style="font-size:0.85rem">Sing a comfortable note for 20 seconds while keeping ribs expanded.</div></div>';
  },
  renderAssessments() {
    const el = document.getElementById('assessmentsContent');
    if (!el) return;
    el.innerHTML = '<div><div style="font-weight:700">Lesson Quiz</div><div style="font-size:0.85rem">Passing score: 80%. Retries: immediate.</div></div>';
  }
};
window.LMS = LMS;
