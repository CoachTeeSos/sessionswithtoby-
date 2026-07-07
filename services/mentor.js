/* services/mentor.js — lightweight rule-based mentor responses */
const Mentor = {
  reply(history, input) {
    const text = input.toLowerCase();
    if (text.includes('breath') || text.includes('air')) return 'Try the Farinelli Cycle from the Breath course, then apply it to a 20-second sustain.';
    if (text.includes('pitch')) return 'Use pitch-matching exercise + slow playback. Record and check with a tuner.';
    if (text.includes('stage fright') || text.includes('confidence')) return 'Build an exposure ladder: record yourself, then 1 person, then 3, then 5.';
    if (text.includes('practice') || text.includes('routine')) return 'Set a 30-minute focused session: 10 min exercises, 15 min songs, 5 min cool-down.';
    if (text.includes('vocal dna') || text.includes('assessment')) return 'Start with Vocal DNA so I can map your weak spots before recommending a lesson path.';
    return 'Good question. Start with the lesson assigned for today, then tell me which part tripped you.';
  }
};
window.Mentor = Mentor;
