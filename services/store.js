/* services/store.js — minimal data loader with proxy-ready API */
const Store = {
  data: null,
  apiBase: '',
  queue: [],
  async init() {
    const res = await fetch('data/lessons.json', {cache: 'no-store'});
    const lessons = await res.json();
    const cRes = await fetch('data/courses.json', {cache: 'no-store'});
    const courses = await cRes.json();
    const xRes = await fetch('data/certifications.json', {cache: 'no-store'});
    const certs = await xRes.json();
    const aRes = await fetch('data/assessments-v1.json', {cache: 'no-store'});
    const assessments = await aRes.json();
    this.data = {schemaVersion: 1, lessons, courses, certifications: certs, assessments};
    this.loadQueue();
    return this.data;
  },
  get lessons() { return this.data?.lessons || []; },
  get courses() { return this.data?.courses || []; },
  get certifications() { return this.data?.certifications || []; },
  get assessments() { return this.data?.assessments || {}; },
  enqueue(payload) {
    try {
      const q = JSON.parse(localStorage.getItem('swt_email_queue')||'[]');
      q.push({payload, ts: Date.now()});
      localStorage.setItem('swt_email_queue', JSON.stringify(q.slice(-50)));
    } catch {}
  },
  loadQueue() {
    this.queue = JSON.parse(localStorage.getItem('swt_email_queue')||'[]');
  },
  async submitEmail(payload) {
    if (!payload.email) return false;
    const base = (this.apiBase || '').replace(/\/$/, '');
    try {
      if (base) {
        const r = await fetch(base + '/api/register', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({fields: payload})
        });
        if (r.ok) { this.clearQueue(); return true; }
      }
    } catch {}
    this.enqueue(payload);
    return false;
  },
  async flushQueue() {
    const q = JSON.parse(localStorage.getItem('swt_email_queue')||'[]');
    if (!q.length) return;
    const base = (this.apiBase || '').replace(/\/$/, '');
    if (!base) return;
    const out = [];
    for (const item of q) {
      try {
        const r = await fetch(base + '/api/register', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({fields: item.payload})
        });
        if (r.ok) out.push(item);
      } catch {}
    }
    if (out.length) this.clearQueue(out.length);
  },
  clearQueue(keep=0) {
    try {
      const q = keep ? JSON.parse(localStorage.getItem('swt_email_queue')||'[]').slice(keep) : [];
      localStorage.setItem('swt_email_queue', JSON.stringify(q));
    } catch {}
  }
};
window.Store = Store;
