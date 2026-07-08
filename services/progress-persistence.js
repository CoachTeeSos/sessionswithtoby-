/* services/progress-persistence.js — localStorage-backed progress store */
const Store = require('./store')
const Progress = require('./progress-engine')

const ProgressPersistence = {
  key: 'swt_progress_v1',
  save() {
    try { localStorage.setItem(this.key, JSON.stringify(Progress.data)); } catch {}
  },
  load() {
    try {
      const raw = localStorage.getItem(this.key)
      if (raw) Progress.data = JSON.parse(raw)
    } catch {}
  },
  markComplete(lessonId) {
    this.load()
    if (!Progress.data.completed) Progress.data.completed = []
    if (!Progress.data.completed.includes(lessonId)) Progress.data.completed.push(lessonId)
    if (!Progress.data.xp) Progress.data.xp = 0
    const lesson = Store.lessons.find(l => l.id === lessonId)
    Progress.data.xp += (lesson && lesson.durationMin) ? Math.max(5, Math.round(lesson.durationMin / 5)) : 10
    if (!Progress.data.streak) Progress.data.streak = 0
    Progress.data.streak += 1
    this.save()
  },
  reset() {
    Progress.data = {}
    localStorage.removeItem(this.key)
  }
}
if (typeof module !== 'undefined') module.exports = ProgressPersistence
