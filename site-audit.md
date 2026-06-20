# SITE AUDIT — Sessions with Toby

## Current State: 42 HTML files, too many pages, no clear funnel

---

## PAGE INVENTORY

### KEEP (core funnel pages)
| Page | Purpose | Status |
|---|---|---|
| index.html | Main landing page (quiz funnel) | Good, keep |
| home.html | Secondary landing page | MERGE into index.html |
| lead-magnet.html | Free 5 exercises guide | Good, keep |
| quiz.html | "Which Singer Are You?" quiz | Good, keep |
| pricing.html | Pricing plans | Good, keep |
| book.html | Book a session | Good, keep |
| about.html | Your story | Good, keep |
| links.html | Linktree-style links | Good, keep |
| thank-you.html | Post-payment confirmation | Good, keep |

### DELETE (redundant / no clear purpose)
| Page | Reason |
|---|---|
| content.html | Resources page — merge into blog |
| content.html | Duplicate of blog |
| blog.html | Has daily content subfolder — keep the daily posts, delete the blog listing page |
| community.html | Empty shell — you use WhatsApp groups |
| abuja-community.html | 788 lines, mostly empty — delete |
| student-details.html | Airtable handles this now |
| schedule-session.html | Google Calendar handles this |
| vocal-pain.html | Content page — merge into blog/geo |
| linkedin.html | Just a profile page — not needed on site |
| verify.html | Certificate verification — keep only if you actually issue certs |
| certification.html | Cert submission — keep only if active |
| google3cba4f0713525b29.html | Google verification — keep (don't delete) |
| core/ | Internal docs — not public, delete from repo |
| huggingface/ | Internal docs — not public, delete from repo |
| references/ | Internal docs — not public, delete from repo |
| content/geo/ | 5 SEO articles — KEEP these, they drive Google traffic |
| content/daily/ | 7 daily posts — KEEP for blog |
| content/docs/ | 2 doc pages — merge or delete |
| content/pedagogy/ | 3 internal docs — delete from repo |
| content/teaching/ | 1 internal doc — delete from repo |

### MERGE
| Pages | Into |
|---|---|
| home.html | index.html |
| content.html | blog.html (then rename to content/) |
| vocal-pain.html | content/geo/ or blog |

---

## THE SIMPLIFIED STRUCTURE

```
sessions-with-toby/
├── index.html              ← MAIN LANDING (quiz funnel + lead magnet)
├── about.html              ← Your story
├── pricing.html            ← Plans + Paystack
├── book.html               ← Book session
├── quiz.html               ← "Which Singer Are You?" quiz
├── lead-magnet.html        ← Free 5 exercises guide
├── links.html              ← All links (linktree)
├── thank-you.html          ← Post-payment
├── blog.html               ← Blog listing (daily posts)
├── google3cba4f0713525b29.html ← Google verification (KEEP)
├── content/
│   ├── daily/              ← Daily blog posts (7 articles)
│   └── geo/                ← SEO articles (5 articles)
│       ├── index.html
│       ├── how-to-improve-singing-voice.html
│       ├── how-to-overcome-stage-fright.html
│       ├── life-coaching-vs-therapy.html
│       ├── online-vocal-coaching-nigeria.html
│       └── voice-coach-vs-singing-teacher.html
└── assets/
    ├── css/
    └── js/
```

**From 42 pages → 12 pages + 12 content articles**

---

## THE FUNNEL — How Traffic Becomes Students

```
Google Search / Social Media / WhatsApp Status
        │
        ▼
   index.html (landing page)
        │
        ├──→ Quiz (quiz.html) → captures email → nurture → book call
        │
        ├──→ Lead Magnet (lead-magnet.html) → captures email → nurture → book call
        │
        ├──→ WhatsApp CTA → direct chat → book call
        │
        └──→ Pricing (pricing.html) → Paystack payment
```

Every page has ONE job: move the visitor toward booking a session or giving you their email/WhatsApp.

---

## GOOGLE TRAFFIC STRATEGY

### The Problem
Google Pages (GitHub Pages) is a static host. Google can index it, but you need to actively build authority.

### What You Already Have Working
- ✅ Google site verification (google-site-verification meta tag)
- ✅ Google Analytics (G-J9V395RPDH)
- ✅ Plausible analytics
- ✅ Schema.org structured data (Organization + AggregateRating)
- ✅ Open Graph + Twitter cards
- ✅ Canonical URLs
- ✅ 5 SEO articles in content/geo/
- ✅ 7 daily blog posts

### What's Missing for Google Rankings

1. **SITEMAP.XML** — Tell Google exactly what pages exist
2. **ROBOTS.TXT** — Guide Google's crawler
3. **INTERNAL LINKING** — Your pages don't link to each other
4. **BACKLINKS** — No external sites link to you (this is the #1 ranking factor)
5. **CONSISTENT PUBLISHING** — Google rewards fresh content weekly, not once a month
6. **PAGE SPEED** — Your pages are heavy (some 20KB+), need to optimize
7. **MOBILE OPTIMIZATION** — Most of your traffic will be mobile (Nigeria)

### Action Plan for Google Rankings

**Week 1: Foundation**
- Create sitemap.xml with all pages
- Create robots.txt
- Add internal links between all pages (nav footer on every page)
- Submit sitemap to Google Search Console (you already have verification)

**Week 2-4: Content Engine**
- Publish 1 blog post per week (minimum) — write about vocal coaching topics
- Each post links back to your landing page and pricing page
- Target long-tail keywords: "how to stop cracking voice when singing," "vocal coach Abuja," "singing lessons Nigeria"

**Ongoing: Backlinks**
- Guest post on Nigerian music blogs
- Get listed in "best vocal coaches in Nigeria" directories
- Share on Reddit (r/singing, r/nigeria)
- YouTube videos linking back to your site
- Podcast appearances

**Ongoing: Social Signals**
- Share every blog post on X, Instagram, WhatsApp status
- Create short-form content (TikTok/Reels) with tips → link in bio to site

---

## GOOGLE PAGES (Peniel Voices) — Separate Issue

The Peniel Voices Google Sheet is Divine's project in Garoua, Cameroon — it's a completely different site/project. For driving traffic there:

1. Share the Google Sheet link in church/choir WhatsApp groups
2. Share on Facebook groups for choir singers in Cameroon
3. Ask Divine to share with her network
4. The form is simple — make sure the link is easy to share (shortened URL)

---

## IMMEDIATE ACTION ITEMS

1. Delete redundant pages (list above)
2. Merge home.html into index.html
3. Create sitemap.xml
4. Create robots.txt
5. Add consistent nav/footer with internal links to every page
6. Set up a blog posting schedule (1x/week minimum)
7. Start building backlinks (guest posts, directories, social shares)
