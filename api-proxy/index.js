const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();
const app = express();
app.use(cors());
app.use(express.json());
const AIRTABLE_TOKEN = process.env.AIRTABLE_TOKEN || '';
const AIRTABLE_BASE = process.env.AIRTABLE_BASE || 'app3N2MFPvfDSuYxk';
const AIRTABLE_TABLE = process.env.AIRTABLE_TABLE || 'Leads';
const API = `https://api.airtable.com/v0/${AIRTABLE_BASE}/${AIRTABLE_TABLE}`;
function headers() { return {'Authorization': `Bearer ${AIRTABLE_TOKEN}`, 'Content-Type': 'application/json'}; }
app.post('/api/register', async (req, res) => {
  try {
    const fields = req.body && req.body.fields ? req.body.fields : req.body;
    if (!fields.Name || !fields.Plan) return res.status(400).json({error: 'Name and Plan required'});
    const out = await axios.post(API, {fields}, {headers: headers(), timeout: 15});
    return res.status(201).json({success: true, id: out.data.id});
  } catch (e) { return res.status(500).json({error: 'Registration failed'}); }
});
app.get('/api/health', (req, res) => res.json({ok: true}));
const port = process.env.PORT || 8787;
app.listen(port, () => console.log(`proxy on ${port}`));
