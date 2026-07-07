# LMS Airtable Proxy
Free backend to keep your Airtable secret off the site.
Required: `node >= 18`

## Run locally
cat > .env <<EOF
AIRTABLE_TOKEN=...
AIRTABLE_BASE=app3N2MFPvfDSuYxk
AIRTABLE_TABLE=Leads
PORT=8787
EOF
npm install
npm run dev

## Deploy free
### Railway / Render
- Root: api-proxy
- Build: npm install
- Start: npm start
- Add env vars from `.env.example`

### Cloudflare Workers
Convert to worker fetch handler with same `/api/register` contract and env secrets.
