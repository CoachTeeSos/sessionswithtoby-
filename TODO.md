# Sessions with Toby — LMS Todo
## Priority order
1. Email capture working
2. Berklee alignment/audit
3. LMS build polish

## 1 Email capture
- [ ] Choose backend: Railway free worker OR Cloudflare Worker OR direct frontend Airtable with explicit UX warning
- [ ] If proxy: set `AIRTABLE_TOKEN`, `AIRTABLE_BASE`, `AIRTABLE_TABLE` in host env; verify `/api/health` responds
- [ ] Set `Store.apiBase` in `lms.html` to proxy URL, or restore `directAirtable` flag
- [ ] End-to-end test: submit gate email → Airtable row appears or proxy logs receipt
- [ ] Remove any inline tokens from repo history; rotate PAT if exposed

## 2 Berklee alignment
- [ ] Audit `data/lessons.json`: auto-detect lessons with empty `outcomes`
- [ ] Add lesson metadata: `domain` (technique/theory/ear/performance/musicianship/business), `level` (beginner/intermediate/advanced/pro), `credits`
- [ ] Update `data/berklee-benchmark.md` with exact measurable criteria per level
- [ ] Wire `services/progress-engine.js` to enforce level prerequisites before lesson unlock
- [ ] Wire `services/assessor.js` with rubric thresholds tied to benchmark criteria
- [ ] Add certificate issuance logic tied to completed credits and assessment mastery
- [ ] Optional: add “alignment score” to user progress dashboard

## 3 LMS build polish
- [ ] Add `lms/pages/*.html` fragments for: dashboard, learn, assessments, mentor, practice, community, coach
- [ ] Replace placeholder practice/assessments shells in `lms/router.js` with real UI
- [ ] Add lesson detail view renderer in router
- [ ] Add progress persistence checks + offline fallback messaging
- [ ] QA script: validate all required IDs exist in HTML before push

## Notes
- Current blocking issue: GitHub secret scanning blocked push due to historical Airtable PAT in repo history; either unblock on GitHub or rewrite/purge that commit from upstream history.
- Fastest working path for email: use existing `api-proxy/` code + Railway deploy with env vars, then `Store.apiBase = 'https://...railway.app'`.
- GA property already included: `G-J9V395RPDH` in `lms/bootstrap.js`.
