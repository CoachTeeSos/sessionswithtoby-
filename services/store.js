/* services/store.js — minimal data loader with proxy-ready API + FormSubmit fallback */
const Store = {
  data: null,
  apiBase: '',
  formsubmitUrl: '', // e.g. 'https://formsubmit.co/you@example.com'
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
  async postJSON(url, payload) {
    const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
    return r.ok;
  },
  async submitEmail(payload) {
    if (!payload.email) return false;
    const base = (this.apiBase || '').replace(/\/$/, '');
    try {
      if (base && await this.postJSON(base + '/api/register', {fields: payload})) { this.clearQueue(); return true; }
    } catch {}
    try {
      const fs = (this.formsubmitUrl || '').replace(/\/$/, '');
      if (fs && await this.postJSON(fs, payload)) return true;
    } catch {}
    this.enqueue(payload);
    return false;
  },
  async flushQueue() {
    const q = JSON.parse(localStorage.getItem('swt_email_queue')||'[]');
    if (!q.length) return;
    const base = (this.apiBase || '').replace(/\/$/, '');
    const fs = (this.formsubmitUrl || '').replace(/\/$/, '');
    const out = [];
    for (const item of q) {
      const p = {fields: item.payload};
      let ok = false;
      if (base) ok = await this.postJSON(base + '/api/register', p).catch(()=>false);
      if (!ok && fs) ok = await this.postJSON(fs, item.payload).catch(()=>false);
      if (ok) out.push(item);
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
