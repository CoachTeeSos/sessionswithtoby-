/* services/store.js — minimal data loader with schema version guard + proxy-ready API */
const Store = {
  data: null,
  apiBase: '', // set to proxy URL, e.g. 'https://sessionswithtoby-proxy.up.railway.app'
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
    return this.data;
  },
  get lessons() { return this.data?.lessons || []; },
  get courses() { return this.data?.courses || []; },
  get certifications() { return this.data?.certifications || []; },
  get assessments() { return this.data?.assessments || {}; },
  async submitEmail(payload) {
    const base = (this.apiBase || '').replace(/\/$/, '');
    if (!base) throw new Error('missing apiBase');
    const res = await fetch(base + '/api/register', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({fields: payload})
    });
    if (!res.ok) throw new Error('submitEmail failed');
    return true;
  }
};
window.Store = Store;
