// =============================================
// VOCAL MASTERY ACADEMY — Shared Engine v2
// A-Player quality. No compromises.
// =============================================

(function() {
  'use strict';
  
  var STORAGE_KEY = 'vma_student';
  var TERMS_KEY = 'vma_terms_agreed';

  // --- Student State ---
  function getStudent() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch(e) { return null; }
  }

  function setStudent(data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  }

  function initStudent(name) {
    var s = {
      name: name || 'Student',
      xp: 5,
      level: 1,
      modules: [0,0,0,0,0,0,0],
      lessons: {},
      quizzes: {},
      badges: [],
      streak: 0,
      lastPractice: null,
      termsAgreed: true,
      termsAgreedDate: new Date().toISOString(),
      startDate: new Date().toISOString()
    };
    localStorage.setItem(TERMS_KEY, 'true');
    setStudent(s);
    return s;
  }

  // --- Levels ---
  var LEVELS = [
    {xp:0, name:'Beginner', emoji:'🌱'},
    {xp:100, name:'Explorer', emoji:'🔍'},
    {xp:250, name:'Apprentice', emoji:'📖'},
    {xp:500, name:'Practitioner', emoji:'🎯'},
    {xp:800, name:'Performer', emoji:'🎤'},
    {xp:1200, name:'Artist', emoji:'🎨'},
    {xp:1800, name:'Virtuoso', emoji:'🏆'}
  ];

  function getLevel(xp) {
    var lvl = 1;
    for (var i = LEVELS.length - 1; i >= 0; i--) {
      if (xp >= LEVELS[i].xp) { lvl = i + 1; break; }
    }
    return lvl;
  }

  // --- Streak ---
  function updateStreak() {
    var s = getStudent();
    if (!s) return;
    var today = new Date().toDateString();
    var last = s.lastPractice ? new Date(s.lastPractice).toDateString() : null;
    var yesterday = new Date(Date.now() - 86400000).toDateString();

    if (last === today) return;

    if (last === yesterday || last === null) {
      s.streak = (s.streak || 0) + 1;
    } else {
      s.streak = 1;
    }

    s.lastPractice = new Date().toISOString();

    if (s.streak === 3) awardXP(10, '3-day streak! 🔥');
    if (s.streak === 7) { awardXP(25, '7-day streak! 🔥🔥'); awardBadge('streak'); }
    if (s.streak === 14) awardXP(50, '14-day streak!');
    if (s.streak === 30) awardXP(100, '30-day streak! Legend!');

    setStudent(s);
  }

  // --- XP & Badges ---
  function awardXP(amount, reason) {
    var s = getStudent();
    if (!s) return;
    var oldXP = s.xp;
    s.xp += amount;
    var oldLvl = getLevel(oldXP);
    var newLvl = getLevel(s.xp);
    if (newLvl > oldLvl) {
      s.level = newLvl;
      (function() {
        var msg = '🎉 Level Up! You\'re now ' + LEVELS[newLvl-1].emoji + ' ' + LEVELS[newLvl-1].name + '!';
        setTimeout(function() { showNotification(msg); }, 300);
      })();
    }
    setStudent(s);
  }

  function awardBadge(id) {
    var s = getStudent();
    if (!s) return;
    if (s.badges && s.badges.includes(id)) return;
    s.badges = s.badges || [];
    s.badges.push(id);
    setStudent(s);
  }

  // --- Notifications ---
  function showNotification(msg) {
    var el = document.createElement('div');
    el.style.cssText = 'position:fixed;top:60px;left:50%;transform:translateX(-50%);background:#111118;border:1px solid #d4a843;border-radius:14px;padding:14px 24px;font-size:.85rem;font-weight:600;color:#d4a843;z-index:9999;box-shadow:0 8px 32px rgba(0,0,0,.5);animation:VMAfadeIn .3s ease;max-width:90%;text-align:center';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(function() {
      el.style.transition = 'opacity .3s';
      el.style.opacity = '0';
      setTimeout(function() { 
        if (el.parentNode) el.parentNode.removeChild(el); 
      }, 300);
    }, 3000);
  }

  // --- Terms Check ---
  if (localStorage.getItem(TERMS_KEY) !== 'true') {
    window.location.href = 'terms.html';
    return;
  }

  // --- Expose globally ---
  window.VMA = {
    getStudent: getStudent,
    setStudent: setStudent,
    initStudent: initStudent,
    getLevel: getLevel,
    LEVELS: LEVELS,
    awardXP: awardXP,
    awardBadge: awardBadge,
    updateStreak: updateStreak,
    showNotification: showNotification,
    STORAGE_KEY: STORAGE_KEY,
    TERMS_KEY: TERMS_KEY
  };
})();
