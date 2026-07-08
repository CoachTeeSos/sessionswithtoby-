/* services/mentor-llm.js — configurable LLM mentor stub with offline fallback */
const Mentor = require('./mentor')

const MentorLLM = {
  enabled: false,
  async init({apiKey, endpoint, model}) {
    if (apiKey && endpoint && model) {
      this.enabled = true
      this.config = {apiKey, endpoint: endpoint.replace(/\/$/, ''), model}
      return true
    }
    this.enabled = false
    return false
  },
  async reply(history, input) {
    if (!this.enabled) return Mentor.reply(history, input)
    try {
      const body = {
        model: this.config.model,
        messages: [
          ...(history || []).map(m => ({role: m.role === 'assistant' ? 'assistant' : 'user', content: m.text})),
          {role: 'user', content: input}
        ]
      }
      const res = await fetch(this.config.endpoint + '/chat/completions', {
        method: 'POST',
        headers: {'Content-Type':'application/json','Authorization':'Bearer ' + this.config.apiKey},
        body: JSON.stringify(body)
      })
      if (!res.ok) throw new Error('LLM request failed')
      const data = await res.json()
      const text = data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content
      if (typeof text === 'string' && text.trim()) return text.trim()
    } catch {}
    return Mentor.reply(history, input)
  }
}
if (typeof module !== 'undefined') module.exports = MentorLLM
