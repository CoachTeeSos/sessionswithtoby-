/* services/progress-engine.js — competency state + prerequisites */
const Progress = {
  load() {
    try { return JSON.parse(localStorage.getItem('swt_progress_v1') || '{}'); }
    catch { return {}; }
  },
  save(state) { localStorage.setItem('swt_progress_v1', JSON.stringify(state)); },
  canAccess(lessonId) {
    const state = this.load();
    const meta = window.Store.lessons.find(l => l.id === lessonId);
    if (!meta) return false;
    if (!meta.prereqIds.length) return true;
    return meta.prereqIds.every(pid => state[pid]?.status === 'passed' || state[pid]?.status === 'mastered');
  },
  mark(lessonId, patch) {
    const state = this.load();
    state[lessonId] = Object.assign(state[lessonId] || {}, patch);
    this.save(state);
    return state[lessonId];
  },
  xpFor(state) {
    let xp = 0;
    for (const id in state) {
      if (state[id].status === 'passed') xp += 10;
      if (state[id].status === 'mastered') xp += 20;
    }
    return xp;
  }
};
window.Progress = Progress;
