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
    const container = document.getElementById('lmsMain');
    if (!container) return;
    if (page === 'learn') this.renderLearn(container);
    if (page === 'dashboard') this.renderDashboard(container);
    if (page === 'mentor') this.renderMentor(container);
    if (page === 'practice') this.renderPractice(container);
    if (page === 'assessments') this.renderAssessments(container);
    if (page === 'community') this.renderCommunity(container);
    if (page === 'coach') this.renderCoach(container);
  },
  renderLearn(container) {
    const lessons = Store.lessons;
    const progress = Progress.load();
    container.innerHTML = lessons.map(l => {
      const state = progress[l.id];
      var locked = false; try { locked = !(Progress.meetsPrereqs ? Progress.meetsPrereqs([]) : true); } catch(e) { locked = false; }
      return '<div class="lesson-item ' + (locked ? 'locked' : '') + '">' +
        '<div><div style="font-weight:700">' + l.title + '</div>' +
        '<div style="font-size:0.8rem;color:#6B7280">' + l.level + ' · ' + l.durationMin + ' min</div></div>' +
        '<div style="font-size:0.75rem">' + (locked ? 'Locked' : state?.status || 'Start') + '</div>' +
        '</div>';
    }).join('');
  },
  renderDashboard(container) {
    const progress = Progress.load();
    var xp = (typeof Progress.xp === "function" ? Progress.xp() : 0);
    const completed = Object.values(progress).filter(s => s.status === 'passed' || s.status === 'mastered').length;
    container.innerHTML = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">' +
      '<div><div style="font-size:1.5rem;font-weight:800">' + xp + '</div><div style="font-size:0.8rem;color:#6B7280">XP</div></div>' +
      '<div><div style="font-size:1.5rem;font-weight:800">' + completed + '</div><div style="font-size:0.8rem;color:#6B7280">Lessons done</div></div>' +
      '<div><div style="font-size:1.5rem;font-weight:800">' + Store.lessons.length + '</div><div style="font-size:0.8rem;color:#6B7280">Lessons total</div></div>' +
      '</div>';
  },
  renderMentor(container) {
    container.innerHTML = '<div data-mentor id="mentorMessages" style="min-height:140px"><div class="mentor-msg mentor-msg-bot">What do you want to work on today?</div></div>' +
      '<input data-mentor-input id="mentorInput" placeholder="Ask Mentor..." style="width:100%;margin-top:10px;padding:10px;background:#161820;color:#F4F5F7;border:1px solid #242838;border-radius:10px">';
    this.wireMentor(container);
  },
  renderPractice(container) {
    container.innerHTML = '<div style="padding:12px;border-radius:8px;background:#F3F4F6"><div style="font-weight:700">Sustained Note</div><div style="font-size:0.85rem">Sing a comfortable note for 20 seconds while keeping ribs expanded.</div></div>';
  },
  renderAssessments(container) {
    container.innerHTML = '<div><div style="font-weight:700">Lesson Quiz</div><div style="font-size:0.85rem">Passing score: 80%. Retries: immediate.</div></div>';
  },
  renderCommunity(container) {
    container.innerHTML = '<div><div style="font-weight:700">Community</div><div style="font-size:0.85rem">Forum and peer feedback coming next.</div></div>';
  },
  renderCoach(container) {
    container.innerHTML = '<div><div style="font-weight:700">Coach</div><div style="font-size:0.85rem">Scheduling and notes coming next.</div></div>';
  },
  wireMentor(root) {
    const wrap = root.querySelector('[data-mentor]');
    const input = root.querySelector('[data-mentor-input]');
    if (!wrap || !input) return;
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
  }
};
window.LMS = LMS;
