/* lms/pages.js — page render shells for current SPA data-page nodes */
const LMSPages = {
  init() {
    ['dashboard','learn','practice','assessments','mentor','coach','feedback','insights','community','resources'].forEach(page => {
      document.getElementById(`page-${page}`)?.addEventListener('click', (e) => {
        e.preventDefault()
        LMS.nav(page)
      })
    })
  },
  showDashboard() {
    const completed = Progress.data?.completed || []
    document.getElementById('lesson-list').innerHTML = Store.lessons.slice(0,8).map(l => {
      const done = completed.includes(l.id)
      return `<div class="lesson" data-id="${l.id}">
        <div class="title">${done ? '✅ ' : ''}${l.title}</div>
        <div class="meta">${l.course} · ${l.durationMin} min · ${l.level || 'Beginner'}</div>
      </div>`
    }).join('')
  },
  showLearn(lessonId) {
    const lesson = Store.lessons.find(l => l.id === (lessonId || 1))
    if (!lesson) return this.showDashboard()
    document.getElementById('lesson-title').textContent = lesson.title
    document.getElementById('lesson-content').innerHTML = lesson.steps.map((s,i) => `
      <div class="step step-${s.type}">
        <div class="step-title">${i+1}. ${s.title}</div>
        <div class="step-body">${s.body}</div>
      </div>
    `).join('')
    document.getElementById('lesson-nav').innerHTML = `<button id="start-assessment" data-id="${lesson.id}">Start Assessment</button>`
    document.getElementById('start-assessment')?.addEventListener('click', () => this.showAssessment(lesson.id))
  },
  showAssessment(lessonId) {
    const lesson = Store.lessons.find(l => l.id === lessonId)
    if (!lesson) return
    document.getElementById('lesson-title').textContent = 'Assessment'
    document.getElementById('lesson-content').innerHTML = `
      <div class="assessment">
        <div class="prompt">Record a demonstration of: <strong>${lesson.title}</strong></div>
        <div class="rubric">
          <h4>Rubric</h4>
          <ul>
            ${(lesson.performanceTask && lesson.performanceTask.rubric ? lesson.performanceTask.rubric : []).map(r =>
              `<li>${r.criterion} — ${Math.round((r.weight||0)*100)}%</li>`
            ).join('')}
          </ul>
        </div>
        <button id="submit-assessment" data-id="${lesson.id}">Submit</button>
      </div>
    `
    document.getElementById('submit-assessment')?.addEventListener('click', () => {
      const result = Assessor.grade({type: lesson.performanceTask?.type || 'audio', response: {}, correctCount: 4, totalItems: 5})
      ProgressPersistence.markComplete(lesson.id)
      document.getElementById('lesson-content').innerHTML = `<div class="result">Score: ${result.score} — ${result.feedback}</div>`
      setTimeout(() => this.showDashboard(), 1800)
    })
  },
  showMentor() {
    const log = document.getElementById('mentor-log')
    const input = document.getElementById('mentor-input')
    const send = () => {
      const text = (input?.value || '').trim()
      if (!text) return
      const userMsg = {role:'user', text}
      const reply = window.MentorLLM ? window.MentorLLM.reply((MentorLLM._history||[]), text) : require('./mentor').reply([], text)
      (MentorLLM._history = MentorLLM._history || []).push(userMsg, {role:'assistant', text: reply})
      input.value = ''
      if (log) { log.innerHTML += `<div><b>You:</b> ${userMsg.text}</div><div><b>Toby:</b> ${reply}</div>`; log.scrollTop = log.scrollHeight }
    }
    log && log.innerHTML && (log.innerHTML = '')
    input && (input.onkeydown = (e) => { if (e.key === 'Enter') send() })
    document.getElementById('mentor-send')?.addEventListener('click', send)
  }
}
if (typeof module !== 'undefined') module.exports = LMSPages
