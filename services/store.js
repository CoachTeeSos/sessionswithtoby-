/* services/store.js — minimal data loader with schema version guard + API base */
const Store = {
  data: null,
  apiBase: '', // set this to your proxy URL, e.g. 'https://sessionswithtoby-proxy.up.railway.app'
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
    const url = base ? base + '/api/register' : 'https://api.airtable.com/v0/app3N2MFPvfDSuYxk/Leads';
    const headers = {'Content-Type':'application/json'};
    if (!base) {
      const token = (window.__SWT_AIRTABLE_TOKEN || (typeof process !== 'undefined' && process.env && process.env.AIRTABLE_TOKEN) || '').toString();
      if (!token) throw new Error('missing Airtable token');
      headers['Authorization'] = 'Bearer ' + token;
    }
    const res = await fetch(url, {method:'POST', headers, body: JSON.stringify({fields: payload})});
    if (!res.ok) throw new Error('submitEmail failed');
    return true;
  }
};
window.Store = Store;
