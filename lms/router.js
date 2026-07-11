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
    const pages = ['dashboard','learn','assessments','mentor','practice','community','coach'];
    const ids = ['statsContent','learnContent','assessmentsContent','mentorMessages','practiceContent','communityContent','coachContent'];
    pages.forEach((p, i) => {
      const el = document.getElementById(ids[i]);
      if (!el) return;
      const isActive = p === page;
      el.classList.toggle('hidden', !isActive);
      if (isActive) {
        if (p === 'dashboard') this.renderDashboard(el);
        if (p === 'learn') this.renderLearn(el);
        if (p === 'assessments') this.renderAssessments(el);
        if (p === 'mentor') this.renderMentor(el);
        if (p === 'practice') this.renderPractice(el);
        if (p === 'community') this.renderCommunity(el);
        if (p === 'coach') this.renderCoach(el);
      }
    });
  },
  renderLearn(container) {
    const lessons = Store.lessons;
    const progress = Progress.load();
    container.innerHTML = lessons.map(l => {
      const state = progress[l.id];
      const locked = !Progress.canAccess(l.id);
      const displayTitle = l.displayTitle || l.title;
      const displayOutcome = l.displayOutcome || (l.outcomes && l.outcomes[0]) || 'Sing with intention.';
      const outcome = displayOutcome ? (' — ' + displayOutcome) : '';
      return '<div class="lesson-item ' + (locked ? 'locked' : '') + '" data-practice-title="' + displayTitle + '" data-practice-body="' + displayOutcome + '">' +
        '<div><div style="font-weight:700">' + displayTitle + outcome + '</div>' +
        '<div style="font-size:0.8rem;color:#6B7280">' + l.level + ' · ' + l.durationMin + ' min</div></div>' +
        '<div style="font-size:0.75rem">' + (locked ? 'Locked' : state?.status || 'Start') + '</div>' +
        '</div>';
    }).join('');
  },
  renderDashboard(container) {
    const progress = Progress.load();
    const xp = Progress.xpFor(progress);
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
    const currentLesson = document.querySelector('.lesson-item.active, .lesson-item[data-current="true"]');
    const title = currentLesson ? (currentLesson.querySelector('[data-practice-title]')?.textContent || 'Focused Practice') : 'Focused Practice';
    const body = currentLesson ? (currentLesson.querySelector('[data-practice-body]')?.textContent || 'Sing with intention. Focus on one action: breath, vowel, or transition.') : 'Sing with intention. Focus on one action: breath, vowel, or transition.';
    container.innerHTML = '<div style="padding:14px;border-radius:12px;background:#11141f;border:1px solid #252a3a"><div style="font-weight:800;font-size:1.05rem;margin-bottom:6px">' + title + '</div><div style="font-size:0.85rem;color:#9CA3AF;line-height:1.55">' + body + '</div><div style="margin-top:12px;font-size:0.75rem;color:#6B7280">Focus timer: 60s · Breathe first.</div></div>';
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
