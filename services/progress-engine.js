/* services/progress-engine.js — competency state + prerequisites */
const Progress = {
  data: {},
  load() {
    try { this.data = JSON.parse(localStorage.getItem('swt_progress_v1') || '{}'); }
    catch { this.data = {}; }
    return this.data
  },
  isComplete(lessonId) {
    return !!(this.data.completed || []).includes(lessonId)
  },
  meetsPrereqs(prereqIds) {
    if (!Array.isArray(prereqIds) || !prereqIds.length) return true
    return prereqIds.every(id => this.isComplete(id))
  },
  xp() { return this.data.xp || 0 },
  streak() { return this.data.streak || 0 },
  reset() { this.data = {}; localStorage.removeItem('swt_progress_v1'); }
}
if (typeof module !== 'undefined') module.exports = Progress
