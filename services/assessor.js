/* services/assessor.js — rubric-based lesson/quiz assessment */
const Assessor = {
  grade({type, response, rubric, correctCount, totalItems}) {
    if (rubric && Array.isArray(rubric)) {
      const score = Math.round((correctCount / totalItems) * 100)
      return {
        score,
        passed: score >= 80,
        feedback: score >= 90 ? 'Excellent mastery.' : score >= 80 ? 'Competent. Review missed items.' : 'Retry lesson steps first.'
      }
    }
    return { score: 0, passed: false, feedback: 'No rubric configured.' }
  }
}
if (typeof module !== 'undefined') module.exports = Assessor
