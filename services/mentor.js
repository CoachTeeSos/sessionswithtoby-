/* services/mentor.js — adaptive rule-based mentor with srs-aware hints */
const Mentor = {
  hints: {
    breath: 'Keep ribs expanded on the exhale — if ribs collapse, reduce the count and rebuild.',
    posture: 'Reset against the wall for 60 seconds before the next attempt.',
    onset: 'Use a gentle surprised “huh” to find clean onset — no air before the cord closure.',
    mix: 'Try “nay” on the scale to keep cord connection through the break.',
    stage: 'Do the 4-7-8 breath reset before you sing again.',
    default: 'Review the lesson steps, then try the exercise once with a recording.'
  },
  category(input) {
    const t = input.toLowerCase()
    if (t.match(/breath|air|rib|appoggio/)) return 'breath'
    if (t.match(/posture|align|wall|spine/)) return 'posture'
    if (t.match(/onset|start|clean|breathy|glottal/)) return 'onset'
    if (t.match(/mix|bridge|break|passaggio/)) return 'mix'
    if (t.match(/stage|fright|nerv|fear/)) return 'stage'
    return 'default'
  },
  reply(history, input) {
    if (!input || !input.trim()) return this.hints.default
    const key = this.category(input)
    let hint = this.hints[key]
    const prev = (history || []).slice(-2)
    if (prev.length >= 2 && prev[0].role === 'user' && prev[1].role === 'assistant' && prev[1].text === hint) {
      hint = this.hints.default
    }
    return hint
  }
}
if (typeof module !== 'undefined') module.exports = Mentor
