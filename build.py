#!/usr/bin/env python3
"""Build complete SessionswithToby single-page app"""
import re

# Read the committed file to extract lessons data
with open('index.html', 'r') as f:
    src = f.read()

# Extract lessons array
ls = src.find('  lessons: [', src.find('const DATA = {'))
end = src.find('      ]}\n  ],\n  assessmentQuestions:', ls)
if end > 0:
    end = end + len('      ]}\n  ],')
lessons_raw = src[ls:end]

# Extract assessment questions
aq_s = src.find('assessmentQuestions:', end)
aq_e = src.find('\n  ]\n};', aq_s)
if aq_e == -1:
    aq_e = src.find('\n  ]\n\n', aq_s)
assessment_raw = src[aq_s:aq_e+len('\n  ]')]

# Build the complete HTML
html = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>SessionswithToby — Artist Operating System</title>
<meta name="description" content="AI-powered vocal coach. Personalized lessons, practice tools, real-time feedback.">
<meta name="theme-color" content="#0A0A0B">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300..900&family=Clash+Display:wght@400;500;600;700;800&family=Geist+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--midnight:#0A0A0B;--ivory:#FAFAF7;--gold:#D4AF37;--gold-dark:#B8960F;--indigo:#4F46E5;--indigo-l:#6366F1;--emerald:#10B981;--gray-50:#F9FAFB;--gray-100:#F3F4F6;--gray-200:#E5E7EB;--gray-300:#D1D5DB;--gray-400:#9CA3AF;--gray-500:#6B7280;--gray-600:#4B5563;--gray-700:#374151;--gray-800:#1F2937;--gray-900:#111827;--gray-950:#030712;--bg:var(--midnight);--text:var(--ivory);--muted:var(--gray-400);--surface:#141419;--surface2:#1a1a1f;--border:rgba(255,255,255,.08);--border-l:rgba(255,255,255,.15);--font-sans:'Inter',-apple-system,sans-serif;--font-d:'Clash Display','Inter',sans-serif;--font-m:'Geist Mono','SF Mono',monospace;--r-sm:8px;--r-md:12px;--r-lg:16px;--r-xl:24px;--r-full:9999px;--ease:cubic-bezier(.16,1,.3,1);--nav-h:60px;--side-w:240px}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased;text-size-adjust:100%}
body{font-family:var(--font-sans);background:var(--bg);color:var(--text);line-height:1.6;overflow-x:hidden;min-height:100vh;min-height:100dvh}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
button{font-family:inherit;cursor:pointer;border:none;background:none;-webkit-tap-highlight-color:transparent;color:inherit}
input,textarea,select{font-family:inherit;color:inherit}
ul,ol{list-style:none}
#emailScreen{position:fixed;inset:0;z-index:99999;background:var(--midnight);display:flex;align-items:center;justify-content:center;transition:opacity .5s var(--ease),transform .5s var(--ease)}
#emailScreen.gone{opacity:0;transform:scale(1.05);pointer-events:none}
.email-card{width:100%;max-width:420px;padding:32px 24px;text-align:center}
.email-logo{font-family:var(--font-d);font-size:clamp(1.5rem,5vw,2.25rem);font-weight:800;letter-spacing:-.03em;margin-bottom:8px}
.email-logo span{color:var(--gold)}
.email-tag{color:var(--muted);font-size:clamp(.85rem,2vw,.95rem);margin-bottom:28px;line-height:1.5}
.email-progress{display:flex;gap:6px;justify-content:center;margin-bottom:20px}
.ep-dot{width:8px;height:8px;border-radius:50%;background:var(--border);transition:background .3s}
.ep-dot.on{background:var(--gold)}
.ep-dot.done{background:var(--gold);opacity:.4}
.es-step{display:none}.es-step.active{display:block}
.es-h{font-family:var(--font-d);font-size:clamp(1.05rem,3vw,1.3rem);font-weight:700;margin-bottom:20px}
.es-sub{font-size:.85rem;color:var(--muted);margin-bottom:16px}
.es-opt{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:var(--r-md);border:1.5px solid var(--border);background:var(--surface);text-align:left;font-size:.9rem;font-weight:500;transition:all .2s;width:100%;cursor:pointer;margin-bottom:8px}
.es-opt:hover{border-color:var(--border-l)}
.es-opt.sel{border-color:var(--gold);background:rgba(212,175,55,.08)}
.es-opt .oi{font-size:1.25rem;flex-shrink:0}
.es-frm{margin-bottom:16px;text-align:left}
.es-frm label{display:block;font-size:.7rem;font-weight:600;color:var(--muted);margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}
.es-input{width:100%;padding:14px 16px;background:var(--surface);border:1.5px solid var(--border);border-radius:var(--r-md);font-size:1rem;outline:none;transition:border-color .2s;color:var(--ivory)}
.es-input:focus{border-color:var(--gold)}
.es-input::placeholder{color:#4B5563}
.es-textarea{width:100%;padding:14px 16px;background:var(--surface);border:1.5px solid var(--border);border-radius:var(--r-md);font-size:.9rem;resize:vertical;min-height:80px;outline:none;color:var(--ivory)}
.es-textarea:focus{border-color:var(--gold)}
.es-btn{width:100%;padding:14px;background:var(--gold);color:#000;font-weight:700;font-size:1rem;border-radius:var(--r-md);transition:all .2s}
.es-btn:hover{filter:brightness(1.1)}
.es-btn:active{transform:scale(.98)}
.es-btn:disabled{opacity:.5;cursor:not-allowed}
.es-skip{margin-top:14px;font-size:.8rem;color:#6B7280;text-decoration:underline;cursor:pointer}
.es-skip:hover{color:var(--text)}
#lmsApp{display:none;min-height:100vh;min-height:100dvh}
.lms-nav{position:fixed;top:0;left:0;right:0;height:var(--nav-h);background:rgba(10,10,11,.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);z-index:1000}
.lms-nav-in{display:flex;align-items:center;justify-content:space-between;height:var(--nav-h);max-width:1200px;margin:0 auto;padding:0 16px}
.lms-logo{font-family:var(--font-d);font-weight:700;font-size:clamp(.85rem,2.5vw,1.05rem);letter-spacing:-.02em}
.lms-logo span{color:var(--gold)}
.lms-user{display:flex;align-items:center;gap:10px}
.lms-av{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,var(--indigo),var(--gold));display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700}
.lms-user span{font-size:.85rem;font-weight:600;display:none}
.lms-out{font-size:.8rem;color:var(--muted);padding:4px 10px;border:1px solid var(--border);border-radius:var(--r-sm);transition:all .2s}
.lms-out:hover{color:var(--text);border-color:var(--border-l)}
.lms-side{position:fixed;left:0;top:var(--nav-h);bottom:0;width:var(--side-w);background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow-y:auto;z-index:500}
.lms-side-nav{flex:1;padding:12px 10px}
.lms-slink{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:var(--r-md);font-size:.875rem;color:var(--muted);font-weight:500;transition:all .2s;white-space:nowrap;margin-bottom:2px}
.lms-slink:hover{background:rgba(255,255,255,.04);color:var(--text)}
.lms-slink.active{background:rgba(212,175,55,.08);color:var(--gold)}
.lms-slink svg{width:18px;height:18px;flex-shrink:0}
.lms-side-ft{padding:12px 10px;border-top:1px solid var(--border)}
.coach-card{padding:12px;border-radius:var(--r-md);background:rgba(255,255,255,.03);border:1px solid var(--border);cursor:pointer;transition:border-color .2s}
.coach-card:hover{border-color:var(--border-l)}
.coach-ch{display:flex;align-items:center;gap:8px;margin-bottom:4px}
.coach-av{width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,var(--gold),#F59E0B);display:flex;align-items:center;justify-content:center;font-size:.8rem}
.coach-nm{font-size:.8rem;font-weight:600}
.coach-tt{font-size:.7rem;color:var(--muted)}
.coach-exp{margin-top:8px;font-size:.78rem;color:var(--muted);line-height:1.5;display:none}
.coach-card.open .coach-exp{display:block}
.lms-main{margin-left:var(--side-w);margin-top:var(--nav-h);padding:24px 20px 100px;min-height:calc(100vh - var(--nav-h))}
.dash-h{margin-bottom:28px}
.dash-h h1{font-family:var(--font-d);font-size:clamp(1.5rem,4vw,2.25rem);font-weight:800;letter-spacing:-.03em;line-height:1.1;margin-bottom:6px}
.dash-h p{color:var(--muted);font-size:.95rem}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px}
.sc{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-md);padding:16px;text-align:center}
.sc-v{font-family:var(--font-d);font-size:clamp(1.3rem,4vw,2rem);font-weight:700;letter-spacing:-.02em;line-height:1}
.sc-l{font-size:.7rem;color:var(--muted);margin-top:4px;text-transform:uppercase;letter-spacing:.05em}
.xp-wrap{margin-bottom:28px}
.xp-lbl{display:flex;justify-content:space-between;font-size:.8rem;color:var(--muted);margin-bottom:6px}
.xp-bar{height:8px;background:var(--surface);border-radius:var(--r-full);overflow:hidden}
.xp-fill{height:100%;background:linear-gradient(90deg,var(--gold),#F59E0B);border-radius:var(--r-full);transition:width .5s var(--ease)}
.daily-rec{background:linear-gradient(135deg,rgba(79,70,229,.15),rgba(212,175,55,.08));border:1px solid rgba(212,175,55,.2);border-radius:var(--r-lg);padding:20px;margin-bottom:28px}
.dr-lbl{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:var(--gold);margin-bottom:6px}
.dr-t{font-family:var(--font-d);font-weight:700;font-size:1.15rem;margin-bottom:6px}
.dr-d{font-size:.875rem;color:var(--muted)}
.grid{display:grid;gap:12px}
.g2{grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr))}
.lg{margin-bottom:32px}
.lg-t{font-family:var(--font-d);font-weight:700;font-size:1.2rem;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.lcard{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-md);padding:16px;transition:all .2s;cursor:pointer}
.lcard:hover{border-color:var(--border-l);transform:translateY(-2px)}
.lcard.done{border-color:rgba(16,185,129,.3)}
.lct{display:flex;justify-content:space-between;align-items:start;margin-bottom:8px}
.lcm{font-size:.75rem;color:var(--muted)}
.lcm-c{color:var(--gold);font-weight:500}
.lcn{font-weight:600;font-size:.95rem;margin-bottom:6px;line-height:1.3}
.lcd{font-size:.85rem;color:var(--muted);line-height:1.5;margin-bottom:12px}
.lcb{font-size:.85rem;padding:8px 16px;border-radius:var(--r-sm);font-weight:600;background:rgba(212,175,55,.15);color:var(--gold);border:1px solid rgba(212,175,55,.3);transition:background .2s}
.lcb:hover{background:rgba(212,175,55,.25)}
.lcb.rev{background:rgba(79,70,229,.1);color:var(--indigo-l);border-color:rgba(79,70,229,.2)}
.pgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,160px),1fr));gap:12px;margin-bottom:28px}
.pc{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-md);padding:20px 16px;text-align:center;cursor:pointer;transition:all .2s}
.pc:hover{border-color:var(--border-l);transform:translateY(-2px)}
.pc-ic{font-size:2rem;margin-bottom:8px}
.pc-t{font-weight:600;font-size:.9rem;margin-bottom:4px}
.pc-d{font-size:.75rem;color:var(--muted)}
.pa{margin-top:28px;background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:24px}
.viz{height:100px;display:flex;align-items:flex-end;justify-content:center;gap:3px;margin:20px 0}
.vb{width:8px;border-radius:4px 4px 0 0;background:var(--gold);transition:height .05s;flex-shrink:0}
.mentor{display:flex;flex-direction:column;height:calc(100vh - var(--nav-h) - 48px)}
.ment-msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}
.mm{max-width:80%;padding:12px 16px;border-radius:var(--r-lg);font-size:.9rem;line-height:1.6}
.mbot{background:var(--surface);border:1px solid var(--border);align-self:flex-start;border-bottom-left-radius:4px}
.muser{background:var(--indigo);color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.mbot a{color:var(--gold);text-decoration:underline;cursor:pointer}
.ment-sug{display:flex;flex-wrap:wrap;gap:8px;padding:0 16px 12px}
.ment-sug-btn{font-size:.8rem;padding:6px 12px;border-radius:var(--r-full);background:var(--surface);border:1px solid var(--border);color:var(--muted);cursor:pointer;transition:all .2s}
.ment-sug-btn:hover{color:var(--text);border-color:var(--border-l)}
.ment-inp{display:flex;gap:10px;padding:12px 16px;border-top:1px solid var(--border)}
.ment-inp input{flex:1;padding:12px 16px;background:var(--surface);border:1px solid var(--border);border-radius:var(--r-md);font-size:.9rem;outline:none;color:var(--ivory)}
.ment-inp input:focus{border-color:var(--border-l)}
.ment-send{padding:12px 20px;background:var(--gold);color:#000;font-weight:700;border-radius:var(--r-md);transition:all .2s}
.ment-send:active{transform:scale(.96)}
.bgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin-bottom:28px}
.bi{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-md);padding:16px 12px;text-align:center}
.bi.earned{border-color:var(--gold);background:rgba(212,175,55,.05)}
.bi-ic{font-size:2rem;margin-bottom:6px}
.bi-n{font-size:.8rem;font-weight:500}
.bi-n.locked{color:#4B5563}
.lst{display:inline-block;padding:4px 12px;border-radius:var(--r-full);font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px}
.stg-t{background:rgba(79,70,229,.15);color:var(--indigo-l)}
.stg-e{background:rgba(16,185,129,.15);color:var(--emerald)}
.stg-p{background:rgba(245,158,11,.15);color:#F59E0B}
.stg-tip{background:rgba(139,92,246,.15);color:#A78BFA}
.lst-title{font-family:var(--font-d);font-size:1.25rem;font-weight:700;margin-bottom:16px;line-height:1.2}
.lst-body{font-size:.92rem;line-height:1.8;color:#D1D5DB;margin-bottom:24px}
.lst-body strong{color:var(--text)}
.lst-act{display:flex;gap:10px}
.btn-a{padding:12px 24px;background:var(--gold);color:#000;font-weight:700;border-radius:var(--r-md);font-size:.9rem;transition:all .2s;display:inline-block;text-align:center}
.btn-a:active{transform:scale(.96)}
.btn-ghost{padding:12px 24px;background:var(--surface);border:1px solid var(--border);border-radius:var(--r-md);font-size:.9rem;font-weight:600;transition:all .2s}
.btn-ghost:hover{border-color:var(--border-l)}
.book-float{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:800;display:flex;align-items:center;gap:8px;padding:12px 20px;background:linear-gradient(135deg,var(--gold),#F59E0B);color:#000;font-weight:700;font-size:.9rem;border-radius:var(--r-full);box-shadow:0 8px 32px rgba(0,0,0,.4);cursor:pointer;transition:all .2s;white-space:nowrap}
.book-float:active{transform:translateX(-50%) scale(.96)}
.fb-btn{position:fixed;bottom:24px;right:24px;width:48px;height:48px;border-radius:50%;background:var(--gold);color:#000;font-size:1.2rem;box-shadow:0 4px 12px rgba(0,0,0,.4);z-index:800;display:flex;align-items:center;justify-content:center;transition:all .2s;cursor:pointer}
.fb-btn:active{transform:scale(.9)}
.toast{position:fixed;bottom:80px;left:50%;transform:translateX(-50%) translateY(20px);background:var(--surface);color:var(--text);padding:12px 24px;border-radius:var(--r-full);font-size:.9rem;font-weight:500;z-index:99999;opacity:0;pointer-events:none;transition:all .3s var(--ease);border:1px solid var(--border-l);white-space:nowrap}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
.mo{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:9998;display:none;align-items:center;justify-content:center;backdrop-filter:blur(4px)}
.mo.open{display:flex}
.modal{background:var(--surface2);border:1px solid var(--border);border-radius:var(--r-xl);padding:28px 24px;max-width:560px;width:92%;max-height:85vh;overflow-y:auto}
@media(max-width:820px){
  :root{--side-w:0px}
  .lms-side{position:fixed;bottom:0;left:0;right:0;top:auto;height:56px;flex-direction:row;border-right:none;border-top:1px solid var(--border);background:rgba(20,20,25,.95);backdrop-filter:blur(20px);padding:0 4px env(safe-area-inset-bottom);z-index:1000}
  .lms-side-nav{display:flex;flex-direction:row;padding:0;flex:1;justify-content:space-around;align-items:center}
  .lms-slink{flex-direction:column;padding:6px 8px;gap:2px;font-size:.6rem;border-radius:var(--r-sm);flex:1}
  .lms-slink svg{width:20px;height:20px}
  .lms-slink span{white-space:normal;text-align:center;line-height:1.1}
  .lms-side-ft{display:none}
  .lms-main{margin-left:0;padding-bottom:calc(56px + 24px)}
  .stats{grid-template-columns:repeat(2,1fr)}
  .book-float{bottom:72px}
  .fb-btn{bottom:72px;right:16px}
}
@media(max-width:480px){
  .pgrid{grid-template-columns:repeat(2,1fr)}
  .stats{grid-template-columns:repeat(2,1fr);gap:8px}
  .sc{padding:12px}
}
.lms-side-nav::-webkit-scrollbar{width:0}
.lms-main::-webkit-scrollbar{width:6px}
.lms-main::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
</style>
</head>
<body>

<!-- EMAIL CAPTURE -->
<div id="emailScreen">
  <div class="email-card">
    <div class="email-logo">Sessions<span>with</span>Toby</div>
    <div class="email-tag">Your Artist Operating System</div>
    <div class="es-step active" data-step="1">
      <div class="es-h">What is your email?</div>
      <div class="es-sub">We will save your progress and personalize your experience</div>
      <div class="es-frm"><input class="es-input" type="email" id="emailInput" placeholder="you@example.com" onkeydown="if(event.key===\'Enter\')app.submitEmail()"></div>
      <button class="es-btn" id="emailBtn" onclick="app.submitEmail()">Continue</button>
    </div>
    <div class="es-step" data-step="2">
      <div class="email-progress"><div class="ep-dot done"></div><div class="ep-dot on"></div><div class="ep-dot"></div><div class="ep-dot"></div></div>
      <div class="es-h">What do you want to achieve?</div>
      <button class="es-opt" onclick="app.selGoal(this,\'worship\')"><span class="oi">🙏</span> Lead worship or minister</button>
      <button class="es-opt" onclick="app.selGoal(this,\'record\')"><span class="oi">🎙️</span> Record and release songs</button>
      <button class="es-opt" onclick="app.selGoal(this,\'perform\')"><span class="oi">🎤</span> Perform live confidently</button>
      <button class="es-opt" onclick="app.selGoal(this,\'technique\')"><span class="oi">📈</span> Improve my technique</button>
      <button class="es-opt" onclick="app.selGoal(this,\'beginner\')"><span class="oi">🌱</span> Start from scratch</button>
    </div>
    <div class="es-step" data-step="3">
      <div class="email-progress"><div class="ep-dot done"></div><div class="ep-dot done"></div><div class="ep-dot on"></div><div class="ep-dot"></div></div>
      <div class="es-h">Your current level?</div>
      <button class="es-opt" onclick="app.selLevel(this,\'beginner\')"><span class="oi">🌱</span> Complete beginner</button>
      <button class="es-opt" onclick="app.selLevel(this,\'some\')"><span class="oi">🎵</span> Some experience</button>
      <button class="es-opt" onclick="app.selLevel(this,\'intermediate\')"><span class="oi">🎶</span> Intermediate (years)</button>
      <button class="es-opt" onclick="app.selLevel(this,\'advanced\')"><span class="oi">⭐</span> Advanced (performing)</button>
    </div>
    <div class="es-step" data-step="4">
      <div class="email-progress"><div class="ep-dot done"></div><div class="ep-dot done"></div><div class="ep-dot done"></div><div class="ep-dot on"></div></div>
      <div class="es-h">Your primary genre?</div>
      <button class="es-opt" onclick="app.selGenre(this,\'gospel\')"><span class="oi">✝️</span> Gospel / Worship</button>
      <button class="es-opt" onclick="app.selGenre(this,\'afrobeats\')"><span class="oi">🥁</span> Afrobeats</button>
      <button class="es-opt" onclick="app.selGenre(this,\'rnb\')"><span class="oi">🎹</span> R&B / Soul</button>
      <button class="es-opt" onclick="app.selGenre(this,\'pop\')"><span class="oi">🎵</span> Pop</button>
      <button class="es-opt" onclick="app.selGenre(this,\'other\')"><span class="oi">🎸</span> Other / Multiple</button>
    </div>
    <div class="es-step" data-step="5">
      <div class="es-h">Anything specific to fix?</div>
      <div class="es-sub">Optional — tell us about your voice goals</div>
      <div class="es-frm"><textarea class="es-textarea" id="surveyWants" rows="3" placeholder="e.g. I go flat on high notes..."></textarea></div>
      <button class="es-btn" onclick="app.finishSurvey()">Start My Journey</button>
      <div class="es-skip" onclick="app.finishSurvey()">Skip and explore →</div>
    </div>
  </div>
</div>

<!-- LMS APP -->
<div id="lmsApp">
  <nav class="lms-nav">
    <div class="lms-nav-in">
      <div class="lms-logo">Sessions<span>with</span>Toby</div>
      <div class="lms-user">
        <div class="lms-av" id="lmsAv"></div>
        <span id="lmsNm"></span>
        <button class="lms-out" onclick="app.logout()">Logout</button>
      </div>
    </div>
  </nav>
  <aside class="lms-side">
    <div class="lms-side-nav">
      <a class="lms-slink active" data-p="dashboard" onclick="app.go(\'dashboard\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg><span>Dashboard</span></a>
      <a class="lms-slink" data-p="learn" onclick="app.go(\'learn\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg><span>Learn</span></a>
      <a class="lms-slink" data-p="practice" onclick="app.go(\'practice\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg><span>Practice</span></a>
      <a class="lms-slink" data-p="mentor" onclick="app.go(\'mentor\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg><span>AI Mentor</span></a>
      <a class="lms-slink" data-p="coach" onclick="app.go(\'coach\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg><span>Coach</span></a>
      <a class="lms-slink" data-p="feedback" onclick="app.go(\'feedback\')"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg><span>Feedback</span></a>
    </div>
    <div class="lms-side-ft">
      <div class="coach-card" onclick="this.classList.toggle(\'open\')">
        <div class="coach-ch"><div class="coach-av">👨‍🏫</div><div><div class="coach-nm">Coach Toby</div><div class="coach-tt">NYVC Method</div></div></div>
        <div class="coach-exp">10+ years training singers across 15 countries. NYVC method = what singers actually feel: jaw drops, tongue glides, throat opens, air flows steady.<br><br>🔥 <strong>Book a 1-on-1 session</strong> for personalized feedback.</div>
      </div>
    </div>
  </aside>
  <main class="lms-main" id="lmsMain"></main>
</div>

<div class="book-float" onclick="app.bookSession()">📞 Book a Session</div>
<div class="fb-btn" onclick="app.go(\'feedback\')" title="Feedback">💬</div>
<div class="toast" id="toast"></div>
<div class="mo" id="modal"><div class="modal" id="modalC"></div></div>

<script>
const DATA = {
''' + lessons_raw + '''
''' + assessment_raw + '''
};

let S = { user:null, xp:0, streak:0, lessonsCompleted:[], badges:[], voiceProfile:null, mentorHistory:[] };
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3000)}
function modal(html){document.getElementById('modalC').innerHTML=html;document.getElementById('modal').classList.add('open')}
document.getElementById('modal').addEventListener('click',e=>{if(e.target.id==='modal')document.getElementById('modal').classList.remove('open')});
function closeModal(){document.getElementById('modal').classList.remove('open')}

let surveyData = {};
const app = {
  init() { this.showStep(1); },
  showStep(n) {
    document.querySelectorAll('.es-step').forEach((el,i) => el.classList.toggle('active', i === n-1));
    document.querySelectorAll('.ep-dot').forEach((el,i) => { el.classList.toggle('on', i === n-2); el.classList.toggle('done', i < n-2); });
    if (n === 1) setTimeout(() => document.getElementById('emailInput')?.focus(), 100);
  },
  submitEmail() {
    const email = document.getElementById('emailInput').value.trim();
    if (!email.includes('@')) { toast('Enter a valid email'); return; }
    surveyData.email = email;
    this.pushToSheet({ email, type:'email_captured', ts: Date.now() });
    this.showStep(2);
  },
  selGoal(el, val) { document.querySelectorAll('.es-step[data-step="2"] .es-opt').forEach(e => e.classList.remove('sel')); el.classList.add('sel'); surveyData.goal = val; setTimeout(() => this.showStep(3), 200); },
  selLevel(el, val) { document.querySelectorAll('.es-step[data-step="3"] .es-opt').forEach(e => e.classList.remove('sel')); el.classList.add('sel'); surveyData.level = val; setTimeout(() => this.showStep(4), 200); },
  selGenre(el, val) { document.querySelectorAll('.es-step[data-step="4"] .es-opt').forEach(e => e.classList.remove('sel')); el.classList.add('sel'); surveyData.genre = val; setTimeout(() => this.showStep(5), 200); },
  finishSurvey() {
    const wants = document.getElementById('surveyWants');
    if (wants) surveyData.wants = wants.value.trim();
    this.pushToSheet({ ...surveyData, type:'survey', ts: Date.now() });
    S.user = { email: surveyData.email, name: surveyData.email.split('@')[0], ...surveyData };
    this.enterLMS();
  },
  pushToSheet(data) {
    const webhook = localStorage.getItem('swt_sheets_webhook');
    if (!webhook) return false;
    fetch(webhook, { method:'POST', mode:'no-cors', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) }).catch(()=>{});
    return true;
  },
  enterLMS() {
    document.getElementById('emailScreen').classList.add('gone');
    document.getElementById('lmsApp').style.display = 'block';
    document.getElementById('lmsAv').textContent = S.user.name[0].toUpperCase();
    document.getElementById('lmsNm').textContent = S.user.name;
    this.go('dashboard');
  },
  logout() {
    S = { user:null, xp:0, streak:0, lessonsCompleted:[], badges:[], voiceProfile:null, mentorHistory:[] };
    document.getElementById('lmsApp').style.display = 'none';
    document.getElementById('emailScreen').classList.remove('gone');
    surveyData = {}; this.init();
  },
  bookSession() {
    const msg = encodeURIComponent('Hi Coach Toby! I am ' + (S.user?.name||'a singer') + ' and I would like to book a session.');
    window.open('https://wa.me/2349160106084?text=' + msg, '_blank');
  },
  go(page) {
    document.querySelectorAll('.lms-slink').forEach(el => el.classList.toggle('active', el.dataset.p === page));
    const main = document.getElementById('lmsMain');
    if (page === 'dashboard') main.innerHTML = this.dash();
    else if (page === 'learn') main.innerHTML = this.learn();
    else if (page === 'practice') main.innerHTML = this.practice();
    else if (page === 'mentor') main.innerHTML = this.mentor();
    else if (page === 'coach') main.innerHTML = this.coach();
    else if (page === 'feedback') main.innerHTML = this.feedback();
  },
  dash() {
    const xp = S.xp, level = Math.floor(xp/100)+1, progress = xp%100;
    const badges = ['🌱 First Step','🔥 7-Day Streak','🎯 Pitch Pro','🫁 Breath Master','⭐ 500 XP','👑 1000 XP'];
    const earned = badges.slice(0, Math.floor(xp/100)+1);
    return '<div class="dash-h"><h1>Welcome, ' + S.user.name + ' 👋</h1><p>Level ' + level + ' · ' + xp + ' XP · ' + S.lessonsCompleted.length + ' lessons</p></div>' +
    '<div class="xp-wrap"><div class="xp-lbl"><span>Level ' + level + '</span><span>' + (100-progress) + ' XP to Level ' + (level+1) + '</span></div><div class="xp-bar"><div class="xp-fill" style="width:' + progress + '%"></div></div></div>' +
    '<div class="stats"><div class="sc"><div class="sc-v">' + xp + '</div><div class="sc-l">XP</div></div><div class="sc"><div class="sc-v">' + S.streak + '</div><div class="sc-l">Streak</div></div><div class="sc"><div class="sc-v">' + S.lessonsCompleted.length + '</div><div class="sc-l">Lessons</div></div><div class="sc"><div class="sc-v">' + level + '</div><div class="sc-l">Level</div></div></div>' +
    '<div class="daily-rec"><div class="dr-lbl">Recommended</div><div class="dr-t">' + (S.lessonsCompleted.length===0?'Start Your First Lesson':'Keep Your Streak Alive') + '</div><div class="dr-d">' + (S.lessonsCompleted.length===0?'Jump into Lesson 1 — Posture & Alignment.': 'You have completed ' + S.lessonsCompleted.length + ' lessons. Progress is real.') + '</div></div>' +
    '<div class="lg"><div class="lg-t">🏅 Badges</div><div class="bgrid">' + badges.map((b,i) => '<div class="bi ' + (i<earned.length?'earned':'') + '"><div class="bi-ic">' + b.split(' ')[0] + '</div><div class="bi-n ' + (i>=earned.length?'locked':'') + '">' + b.split(' ').slice(1).join(' ') + '</div></div>').join('') + '</div></div>';
  },
  learn() {
    const grouped = {};
    DATA.lessons.forEach(l => { if (!grouped[l.course]) grouped[l.course] = []; grouped[l.course].push(l); });
    return '<div class="dash-h"><h1>Learn</h1><p>' + DATA.lessons.length + ' lessons across ' + Object.keys(grouped).length + ' courses. Complete each to earn XP.</p></div>' +
    Object.entries(grouped).map(([course, lessons]) => '<div class="lg"><div class="lg-t">' + course + ' <span style="font-size:.8rem;color:var(--muted);font-weight:400">' + lessons.length + ' lessons</span></div><div class="g2">' + lessons.map(l => {const done=S.lessonsCompleted.includes(l.id);return '<div class="lcard ' + (done?'done':'') + '" onclick="app.viewLesson(' + l.id + ')"><div class="lct"><div class="lcm"><span class="lcm-c">' + l.course + '</span> · ' + l.duration + '</div>' + (done?'✅':'') + '</div><div class="lcn">' + l.title + '</div><div class="lcd">' + (l.content||'').substring(0,80) + '…</div><div class="lcb ' + (done?'rev':'') + '">' + (done?'Review →':'Start Lesson →') + '</div></div>';}).join('') + '</div></div>';}).join('');
  },
  viewLesson(id) {
    const lesson = DATA.lessons.find(l => l.id === id);
    if (!lesson) return;
    const steps = lesson.steps || [];
    if (steps.length === 0) { modal('<h3>' + lesson.title + '</h3><p style="margin:16px 0">' + lesson.content + '</p><button class="btn-a" style="width:100%;text-align:center" onclick="app.completeLesson(' + id + ')">Complete +15 XP</button>'); return; }
    let cur = 0;
    const render = () => {
      const s = steps[cur];
      const colors = {teach:'stg-t',exercise:'stg-e',practice:'stg-p',tip:'stg-tip'};
      const icons = {teach:'📖',exercise:'🎯',practice:'🏋️',tip:'💡'};
      const labels = {teach:'Teaching',exercise:'Exercise',practice:'Practice',tip:'Pro Tip'};
      const body = (s.body||'').replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>').replace(/\\n/g,'<br>');
      const progress = ((cur+1)/steps.length*100).toFixed(0);
      const back = cur>0 ? '<button class="btn-ghost" style="flex:1" onclick="app._navLesson(' + id + ',-1)">← Back</button>' : '';
      const next = cur<steps.length-1 ? '<button class="btn-a" style="flex:1" onclick="app._navLesson(' + id + ',1)">Next →</button>' : '<button class="btn-a" style="flex:1" onclick="app.completeLesson(' + id + ')">✓ Complete +15 XP</button>';
      modal('<span class="lst ' + colors[s.type] + '">' + icons[s.type] + ' ' + labels[s.type] + '</span><h2 class="lst-title">' + lesson.title + '</h2><p style="color:var(--muted);margin-bottom:12px;font-size:.85rem">' + lesson.course + ' · ' + lesson.duration + '</p><div style="height:4px;background:var(--border);border-radius:99px;margin-bottom:20px"><div style="height:4px;background:var(--gold);border-radius:99px;width:' + progress + '%"></div></div><h4 style="font-family:var(--font-d);font-weight:600;margin-bottom:12px">' + s.title + '</h4><div class="lst-body">' + body + '</div><div class="lst-act">' + back + next + '</div>');
    };
    app._navLesson = (lid, dir) => { if (lid !== id) return; cur = Math.max(0, Math.min(steps.length-1, cur+dir)); render(); };
    render();
  },
  completeLesson(id) {
    if (!S.lessonsCompleted.includes(id)) { S.lessonsCompleted.push(id); S.xp += 15; toast('+15 XP!'); }
    closeModal(); this.go('learn');
  },
  practice() {
    return '<div class="dash-h"><h1>Practice Tools</h1><p>Real-time audio analysis powered by Web Audio API.</p></div>' +
    '<div class="pgrid">' +
    '<div class="pc" onclick="app.pracTool(\'pitch\')"><div class="pc-ic">🎯</div><div class="pc-t">Pitch Detector</div><div class="pc-d">Real-time pitch and notes</div></div>' +
    '<div class="pc" onclick="app.pracTool(\'ear\')"><div class="pc-ic">👂</div><div class="pc-t">Ear Training</div><div class="pc-d">Interval recognition</div></div>' +
    '<div class="pc" onclick="app.pracTool(\'breath\')"><div class="pc-ic">🫁</div><div class="pc-t">Breath Coach</div><div class="pc-d">Visual breathing timer</div></div>' +
    '<div class="pc" onclick="app.pracTool(\'warmup\')"><div class="pc-ic">🔥</div><div class="pc-t">Warm-Up</div><div class="pc-d">5-step vocal warmup</div></div>' +
    '<div class="pc" onclick="app.pracTool(\'voicelab\')"><div class="pc-ic">🔬</div><div class="pc-t">Voice Lab</div><div class="pc-d">Spectrum and volume</div></div>' +
    '<div class="pc" onclick="app.pracTool(\'range\')"><div class="pc-ic">📏</div><div class="pc-t">Range Finder</div><div class="pc-d">Find your vocal range</div></div>' +
    '</div><div class="pa" id="pracArea" style="display:none"></div>';
  },
  pracTool(tool) {
    const area = document.getElementById('pracArea');
    area.style.display = 'block';
    area.scrollIntoView({behavior:'smooth',block:'start'});
    if (tool === 'pitch') {
      area.innerHTML = '<h3 style="font-family:var(--font-d);font-weight:700;margin-bottom:16px">🎯 Pitch Detector</h3><div class="viz" id="pitchViz"></div><div style="text-align:center;font-family:var(--font-m);font-size:3rem;font-weight:700;color:var(--indigo)" id="pitchHz">--</div><div style="text-align:center;font-weight:600" id="pitchNote">Sing to detect</div><div style="text-align:center;color:var(--muted);margin-top:4px;font-family:var(--font-m)" id="pitchCents"></div><button class="btn-a" style="margin:20px auto 0;display:block" id="pitchBtn" onclick="app.startPitch()">Start →</button>';
      this.initPitchViz();
    } else if (tool === 'ear') {
      area.innerHTML = '<h3 style="font-family:var(--font-d);font-weight:700;margin-bottom:16px">👂 Ear Training</h3><div style="text-align:center;margin:20px 0"><div style="font-size:1.1rem;font-weight:600;margin-bottom:20px" id="earStatus">Press Play to start</div><div class="g2" style="max-width:400px;margin:0 auto 20px" id="earOpts"></div><div style="color:var(--muted)">Score: <strong id="earScore">0</strong> · Streak: <strong id="earStreak">0</strong></div></div><button class="btn-a" style="margin:20px auto 0;display:block" id="earBtn" onclick="app.startEar()">Play Interval →</button>';
      this.earScore = 0; this.earStreak = 0;
    } else if (tool === 'breath') {
      area.innerHTML = '<h3 style="font-family:var(--font-d);font-weight:700;margin-bottom:16px">🫁 Breath Coach</h3><div style="text-align:center;margin:24px 0"><div style="width:200px;height:200px;border-radius:50%;border:4px solid var(--indigo);margin:0 auto;display:flex;align-items:center;justify-content:center;transition:all .3s linear" id="breathCircle"><span style="font-family:var(--font-m);font-size:2rem;font-weight:700;color:var(--gold)" id="breathTimer">4</span></div><div style="margin-top:16px;font-size:1.1rem;font-weight:600;color:var(--gold)" id="breathPhase">Tap Start</div></div><button class="btn-a" style="margin:0 auto;display:block" id="breathBtn" onclick="app.startBreath()">Start Breathing →</button>';
    } else if (tool === 'warmup') {
      area.innerHTML = '<h3 style="font-family:var(--font-d);font-weight:700;margin-bottom:16px">🔥 Warm-Up Protocol</h3><div style="text-align:center;margin:20px 0"><div style="font-family:var(--font-m);font-size:2.5rem;font-weight:700;color:var(--gold)" id="wupTimer">30</div><div style="font-weight:600;font-size:1.1rem;margin-bottom:8px" id="wupCurrent">Step 1: Deep Breathing</div></div><button class="btn-a" style="margin:0 auto;display:block" id="wupBtn" onclick="app.startWarmup()">Start Warm-Up →</button>';
      this.wupStep = 0; this.wupCount = 30; this.wupTimer = null;
    } else if (tool === 'voicelab') {
      area.innerHTML = '<h3 style="font-family:var(--font-d);font-weight:700;margin-bottom:16px">🔬 Voice Lab</h3><div class="viz" id="vlSpectrum" style="height:120px"></div><div style="display:flex;justify-content:space-around;text-align:center;margin-top:16px"><div><div style="font-family:var(--font-m);font-size:1.5rem;font-weight:700;color:var(--indigo)" id="vlVol">--</div><div style="font-size:.75rem;color:var(--muted)">dB</div></div><div><div style="font-family:var(--font-m);font-size:1.5rem;font-weight:700;color:var(--emerald)" id="vlStab">--</div><div style="font-size:.75rem;color:var(--muted)">Stability</div></div></div><button class="btn-a" style="margin:20px auto 0;display:block" id="vlBtn" onclick="app.startVoiceLab()">Analyze →</button>';
    } else if (tool === 'range') {
      area.innerHTML = '<h3 style="font-family:var(--font-d);font-weight:700;margin-bottom:16px">📏 Range Finder</h3><p style="color:var(--muted);margin-bottom:20px">Sing as <strong>low</strong> as you can, then as <strong>high</strong> as you can.</p><div style="display:flex;justify-content:space-around;margin:24px 0"><div style="text-align:center"><div style="font-size:.75rem;color:var(--muted);margin-bottom:6px">Low</div><div style="font-family:var(--font-m);font-size:2rem;font-weight:700;color:var(--indigo)" id="rangeLow">--</div></div><div style="text-align:center"><div style="font-size:.75rem;color:var(--muted);margin-bottom:6px">High</div><div style="font-family:var(--font-m);font-size:2rem;font-weight:700;color:var(--emerald)" id="rangeHigh">--</div></div></div><button class="btn-a" style="margin:0 auto;display:block" id="rangeBtn" onclick="app.startRange()">Start →</button>';
      this.rangeDetecting = false; this.rangeMin = Infinity; this.rangeMax = 0;
    }
  },
  audioCtx:null, analyser:null, micStream:null,
  getAudio() {
    if (this.audioCtx) return Promise.resolve();
    return navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {
      this.micStream = stream;
      this.audioCtx = new (window.AudioContext||window.webkitAudioContext)();
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 2048;
      this.audioCtx.createMediaStreamSource(stream).connect(this.analyser);
    });
  },
  hzToNote(hz) {
    const n=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
    const semi=12*Math.log2(hz/440); const midi=Math.round(semi)+69;
    return {name:n[midi%12]+(Math.floor(midi/12)-1),cents:(semi-Math.round(semi))*100};
  },
  autocorrelate(buf,sr) {
    let bestOff=-1,bestCor=0,rms=0;
    for(let i=0;i<buf.length;i++) rms+=buf[i]*buf[i];
    rms=Math.sqrt(rms/buf.length); if(rms<0.01) return -1;
    for(let off=20;off<1000;off++){let cor=0;for(let j=0;j<1000;j++)cor+=Math.abs(buf[j]-buf[j+off]);cor=1-cor/1000;if(cor>bestCor){bestCor=cor;bestOff=off;}}
    return bestCor>0.3?sr/bestOff:-1;
  },
  initPitchViz() { const v=document.getElementById('pitchViz'); v.innerHTML=''; for(let i=0;i<32;i++){const b=document.createElement('div');b.className='vb';b.style.height='4px';v.appendChild(b);} },
  startPitch() {
    this.pitchActive=true;
    document.getElementById('pitchBtn').textContent='Listening...';
    document.getElementById('pitchBtn').disabled=true;
    const bars=document.getElementById('pitchViz').children;
    this.getAudio().then(()=>{
      const buf=new Float32Array(this.analyser.fftSize);
      const detect=()=>{
        this.analyser.getFloatTimeDomainData(buf);
        const pitch=this.autocorrelate(buf,this.audioCtx.sampleRate);
        if(pitch>50&&pitch<2000){const note=this.hzToNote(pitch);document.getElementById('pitchHz').textContent=Math.round(pitch);document.getElementById('pitchNote').textContent=note.name;document.getElementById('pitchCents').textContent=(note.cents>0?'+':'')+Math.round(note.cents)+'¢';}
        let rms=0;for(let i=0;i<buf.length;i++)rms+=buf[i]*buf[i];rms=Math.sqrt(rms/buf.length);
        for(let i=0;i<bars.length;i++)bars[i].style.height=Math.max(4,Math.min(100,Math.round(rms*500)))+'%';
        if(this.pitchActive) requestAnimationFrame(detect);
      };
      detect();
    }).catch(()=>toast('Microphone access needed'));
  },
  earScore:0, earStreak:0, earCurrent:null,
  startEar() {
    this.getAudio().then(()=>{
      const ctx=this.audioCtx;
      const idx=Math.floor(Math.random()*8);
      this.earCurrent=idx;
      const names=['Unison','Major 2nd','Major 3rd','Perfect 4th','Perfect 5th','Major 6th','Major 7th','Octave'];
      const ratios=[1,9/8,5/4,4/3,3/2,5/3,15/8,2];
      const g=ctx.createGain();g.gain.value=0.2;g.connect(ctx.destination);
      const o1=ctx.createOscillator();o1.frequency.value=220;
      const o2=ctx.createOscillator();o2.frequency.value=220*ratios[idx];
      o1.connect(g);o2.connect(g);o1.start();o2.start();
      setTimeout(()=>{o1.stop();o2.stop();},1500);
      document.getElementById('earStatus').textContent='What interval did you hear?';
      document.getElementById('earOpts').innerHTML=names.map((n,i)=>'<button class="btn-ghost" style="text-align:left;width:100%" onclick="app.checkEar('+i+')">'+n+'</button>').join('');
      document.getElementById('earBtn').style.display='none';
      setTimeout(()=>{document.getElementById('earBtn').style.display='block';document.getElementById('earBtn').textContent='Next →';},2000);
    }).catch(()=>toast('Audio needed'));
  },
  checkEar(idx) {
    if(idx===this.earCurrent){this.earScore+=10;this.earStreak++;toast('✓ +10 XP');}
    else{this.earStreak=0;toast('✗ It was '+['Unison','Major 2nd','Major 3rd','Perfect 4th','Perfect 5th','Major 6th','Major 7th','Octave'][this.earCurrent]);}
    document.getElementById('earScore').textContent=this.earScore;
    document.getElementById('earStreak').textContent=this.earStreak;
  },
  startBreath() {
    let phase=0,count=4;
    const phases=['Inhale...','Hold...','Exhale...','Hold...'];
    const circle=document.getElementById('breathCircle');
    document.getElementById('breathBtn').style.display='none';
    const tick=()=>{
      document.getElementById('breathTimer').textContent=count;
      document.getElementById('breathPhase').textContent=phases[phase];
      circle.style.transform=(phase===0)?'scale(1.3)':(phase===2)?'scale(0.7)':'scale(1)';
      count--;
      if(count<0){phase=(phase+1)%4;count=4;}
      setTimeout(tick,1000);
    };
    tick();
    setTimeout(()=>{document.getElementById('breathBtn').style.display='block';toast('Complete! +10 XP');},60000);
  },
  wupStep:0, wupCount:30, wupTimer:null,
  startWarmup() {
    const steps=['Deep Breathing — 30s','Humming Scales — 30s','Lip Trills — 30s','Sirens — 30s','Arpeggio — 30s'];
    document.getElementById('wupBtn').style.display='none';
    this.wupStep=0;this.wupCount=30;
    const tick=()=>{
      if(this.wupStep>=steps.length){document.getElementById('wupTimer').textContent='✓';document.getElementById('wupCurrent').textContent='Complete! +15 XP';document.getElementById('wupBtn').style.display='block';return;}
      document.getElementById('wupTimer').textContent=this.wupCount;
      document.getElementById('wupCurrent').textContent='Step '+(this.wupStep+1)+': '+steps[this.wupStep];
      this.wupCount--;
      if(this.wupCount<0){this.wupStep++;this.wupCount=30;}
      this.wupTimer=setTimeout(tick,1000);
    };
    tick();
  },
  startVoiceLab() {
    document.getElementById('vlBtn').textContent='Analyzing...';
    this.getAudio().then(()=>{
      const buf=new Uint8Array(this.analyser.frequencyBinCount);
      const timeBuf=new Float32Array(this.analyser.fftSize);
      const bars=document.getElementById('vlSpectrum');
      bars.innerHTML='';
      for(let i=0;i<32;i++){const b=document.createElement('div');b.className='vb';b.style.height='4px';bars.appendChild(b);}
      const children=bars.children;
      let prevVol=0,samples=0,stable=0;
      const analyze=()=>{
        this.analyser.getByteFrequencyData(buf);
        this.analyser.getFloatTimeDomainData(timeBuf);
        let sum=0;for(let i=0;i<buf.length;i++)sum+=buf[i];
        const vol=Math.round(20*Math.log10(Math.max(sum/buf.length,1)/255));
        document.getElementById('vlVol').textContent=isFinite(vol)?vol:0;
        let rms=0;for(let i=0;i<timeBuf.length;i++)rms+=timeBuf[i]*timeBuf[i];rms=Math.sqrt(rms/timeBuf.length);
        samples++;if(Math.abs(rms-prevVol)<0.01&&rms>0.01)stable++;prevVol=rms;
        document.getElementById('vlStab').textContent=samples>5?Math.min(99,Math.round(stable/samples*100))+'%':'...';
        for(let i=0;i<32;i++)children[i].style.height=Math.max(4,buf[i*8]/2)+'%';
        if(document.getElementById('vlBtn').textContent==='Analyzing...')requestAnimationFrame(analyze);
      };
      analyze();
    }).catch(()=>toast('Microphone access needed'));
  },
  rangeDetecting:false, rangeMin:Infinity, rangeMax:0,
  startRange() {
    document.getElementById('rangeBtn').disabled=true;
    document.getElementById('rangeBtn').textContent='Sing LOW then HIGH';
    this.rangeDetecting=true;this.rangeMin=Infinity;this.rangeMax=0;
    this.getAudio().then(()=>{
      const buf=new Float32Array(this.analyser.fftSize);
      const detect=()=>{
        this.analyser.getFloatTimeDomainData(buf);
        const pitch=this.autocorrelate(buf,this.audioCtx.sampleRate);
        if(pitch>50&&pitch<2000){
          if(pitch<this.rangeMin)this.rangeMin=pitch;
          if(pitch>this.rangeMax)this.rangeMax=pitch;
          document.getElementById('rangeLow').textContent=this.hzToNote(this.rangeMin).name;
          document.getElementById('rangeHigh').textContent=this.hzToNote(this.rangeMax).name;
        }
        if(this.rangeDetecting)requestAnimationFrame(detect);
      };
      detect();
      setTimeout(()=>{this.rangeDetecting=false;document.getElementById('rangeBtn').disabled=false;document.getElementById('rangeBtn').textContent='Find My Range →';if(this.rangeMin!==Infinity)toast('Range: '+this.hzToNote(this.rangeMin).name+' – '+this.hzToNote(this.rangeMax).name);},15000);
    }).catch(()=>toast('Microphone access needed'));
  },
  mentor() {
    return '<div class="dash-h"><h1>AI Vocal Mentor</h1><p>I search through all 33 lessons to find answers about singing.</p></div>' +
    '<div class="mentor"><div class="ment-msgs" id="mentMsgs"><div class="mm mbot">Hey! I have read all 33 lessons in the curriculum. Ask me about: <strong>pitch</strong>, <strong>breath</strong>, <strong>vibrato</strong>, <strong>range</strong>, <strong>stage fright</strong>, or <strong>warmups</strong>.</div></div>' +
    '<div class="ment-sug"><div class="ment-sug-btn" onclick="app.askMentor(\'How do I fix pitch problems?\')">🎯 Fix pitch</div><div class="ment-sug-btn" onclick="app.askMentor(\'How to expand my range?\')">📏 Expand range</div><div class="ment-sug-btn" onclick="app.askMentor(\'How to stop stage fright?\')">🎭 Stage fright</div><div class="ment-sug-btn" onclick="app.askMentor(\'Best warmup routine?\')">🔥 Warmup</div></div>' +
    '<div class="ment-inp"><input type="text" id="mentInp" placeholder="Ask about singing..." onkeydown="if(event.key===\'Enter\')app.askMentor()"><button class="ment-send" onclick="app.askMentor()">Send</button></div></div>';
  },
  askMentor(text) {
    const input=document.getElementById('mentInp');
    if(!text){text=input.value.trim();if(!text)return;}
    input.value='';
    const msgs=document.getElementById('mentMsgs');
    msgs.innerHTML+='<div class="mm muser">'+text+'</div>';
    setTimeout(()=>{
      const response=this.mentorRespond(text);
      msgs.innerHTML+='<div class="mm mbot">'+response+'</div>';
      msgs.scrollTop=msgs.scrollHeight;
    },500+Math.random()*500);
  },
  mentorRespond(text) {
    const t=text.toLowerCase();
    const keywords=t.split(/\\s+/).filter(w=>w.length>3);
    const stopWords=['what','how','why','when','where','which','there','their','about','would','could','should','have','this','that','with','from','your','just','more','some','like','into','other','whats','dont','cant'];
    const query=keywords.filter(k=>!stopWords.includes(k));
    let results=[];
    query.forEach(qw=>{DATA.lessons.forEach(l=>{const c=(l.content+' '+(l.steps||[]).map(s=>s.body).join(' ')).toLowerCase();if(c.includes(qw)){const ex=this.getExcerpt(l,qw);if(ex)results.push({lesson:l,excerpt:ex});}})});
    const phrases={'stage fright':['confidence','fear','stage','nervous'],'pitch problems':['pitch','flat','sharp','intonation'],'tone quality':['tone','resonance','mask','placement'],'range expansion':['range','expand','semitone'],'warm up':['warmup','humming','lip trills','sirens'],'breath support':['breath','support','diaphragm','solar']};
    Object.entries(phrases).forEach(([phrase,words])=>{if(t.includes(phrase)){words.forEach(qw=>{DATA.lessons.forEach(l=>{const c=(l.content+' '+(l.steps||[]).map(s=>s.body).join(' ')).toLowerCase();if(c.includes(qw)){const ex=this.getExcerpt(l,qw);if(!results.find(r=>r.excerpt===ex))results.push({lesson:l,excerpt:ex});}});});}});
    if(results.length===0) return 'Great question! Great singing comes down to three fundamentals: breath support, vowel shaping, and resonance placement. Master those and everything gets easier. Try asking about pitch, breath, vibrato, or range.';
    const top=results.slice(0,3);
    return 'I found relevant content from '+top.length+' lesson'+(top.length>1?'s':'')+':<br><br>'+top.map(r=>'<strong>'+r.excerpt.title+'</strong><br>"'+r.excerpt.text+'"<br>→ <a onclick="app.viewLesson('+r.lesson.id+');closeModal()" style="color:var(--gold);text-decoration:underline;font-weight:600">Read Lesson '+r.lesson.id+': '+r.lesson.title+'</a>').join('<br><br>');
  },
  getExcerpt(lesson,keyword) {
    for(const step of (lesson.steps||[])){const idx=(step.body||'').toLowerCase().indexOf(keyword);if(idx!==-1)return{title:'📋 '+step.title,text:(step.body||'').substring(idx,idx+150)+'...'};}
    const idx=(lesson.content||'').toLowerCase().indexOf(keyword);
    if(idx!==-1)return{title:'📋 '+lesson.title,text:(lesson.content||'').substring(idx,idx+120)+'...'};
    return null;
  },
  coach() {
    const msg=encodeURIComponent("Hi Coach Toby! I'd like to book a session.");
    const wa='https://wa.me/2349160106084?text='+msg;
    return '<div class="dash-h"><h1>Coach Toby</h1><p>The human behind the method. Vocal coach, artist, and mentor.</p></div>' +
    '<div class="card" style="max-width:600px">' +
    '<div style="display:flex;align-items:center;gap:24px;margin-bottom:24px;flex-wrap:wrap"><div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,var(--gold),#F59E0B);display:flex;align-items:center;justify-content:center;font-size:2.5rem;flex-shrink:0">🎤</div><div style="flex:1;min-width:200px"><h3 style="font-family:var(--font-d);font-size:1.5rem;letter-spacing:-.02em;margin-bottom:4px">Toby — Coach & Founder</h3><p style="color:var(--muted);font-size:.9rem">10+ years · 15 countries · 1000+ singers transformed</p></div></div>' +
    '<div style="margin-bottom:24px;padding:20px;background:rgba(212,175,55,.05);border-radius:var(--r-md);border:1px solid rgba(212,175,55,.15)"><h4 style="font-weight:600;margin-bottom:8px;color:var(--gold)">The NYVC Method</h4><p style="color:var(--muted);line-height:1.7;font-size:.9rem">New York Vocal Coaching — built on what singers <em>actually feel</em>. No generic pedagogy. Every exercise targets a real sensation: jaw drops, tongue glides, throat opens, air flows steady, mask resonance buzzes.</p></div>' +
    '<div class="g3" style="margin-bottom:24px"><div style="text-align:center;padding:16px;background:var(--gray-50);border-radius:var(--r-md)"><div style="font-size:1.5rem;font-family:var(--font-d);font-weight:700;color:var(--indigo)">9</div><div style="font-size:.7rem;color:var(--muted)">Courses</div></div><div style="text-align:center;padding:16px;background:var(--gray-50);border-radius:var(--r-md)"><div style="font-size:1.5rem;font-family:var(--font-d);font-weight:700;color:var(--indigo)">33</div><div style="font-size:.7rem;color:var(--muted)">Lessons</div></div><div style="text-align:center;padding:16px;background:var(--gray-50);border-radius:var(--r-md)"><div style="font-size:1.5rem;font-family:var(--font-d);font-weight:700;color:var(--emerald)">4</div><div style="font-size:.7rem;color:var(--muted)">Cert Levels</div></div></div>' +
    '<h4 style="font-family:var(--font-d);font-weight:600;margin-bottom:8px">Book a 1-on-1 Session</h4><p style="color:var(--muted);line-height:1.6;margin-bottom:16px;font-size:.9rem">Get your voice evaluated personally by Toby. Receive a custom training plan, specific exercises for your weaknesses, and expert feedback on a recording.</p>' +
    '<div class="g2" style="margin-bottom:24px"><div style="padding:20px;background:var(--gray-50);border-radius:var(--r-md);border:1px solid rgba(212,175,55,.2)"><div style="font-family:var(--font-d);font-weight:700;margin-bottom:4px">Free Discovery</div><div style="font-family:var(--font-d);font-size:1.75rem;font-weight:800;color:var(--gold);margin-bottom:4px">$0</div><ul style="font-size:.85rem;color:var(--muted);line-height:1.8"><li>15-min voice evaluation</li><li>Your strengths & weaknesses</li><li>No commitment</li></ul></div><div style="padding:20px;background:linear-gradient(135deg,rgba(212,175,55,.1),rgba(245,158,11,.05));border-radius:var(--r-md);border:1px solid rgba(212,175,55,.3);position:relative"><div style="position:absolute;top:-8px;right:8px;background:var(--gold);color:var(--midnight);font-size:.65rem;font-weight:700;padding:2px 10px;border-radius:var(--r-full)">Popular</div><div style="font-family:var(--font-d);font-weight:700;margin-bottom:4px">1-on-1 Coaching</div><div style="font-family:var(--font-d);font-size:1.75rem;font-weight:800;color:var(--gold);margin-bottom:4px">$200<span style="font-size:.8rem;font-weight:400;color:var(--muted)">/hour</span></div><ul style="font-size:.85rem;color:var(--muted);line-height:1.8"><li>Full vocal assessment</li><li>Custom training plan</li><li>Recording feedback</li><li>WhatsApp follow-up</li></ul></div></div>' +
    '<a href="'+wa+'" target="_blank" class="btn btn-gold btn-lg btn-block" style="text-align:center">Book via WhatsApp →</a></div>';
  },
  feedback() {
    const existing=JSON.parse(localStorage.getItem('swt_feedback')||'[]');
    let html='<div class="dash-h"><h1>Feedback</h1><p>Your voice shapes this platform. Tell us what to improve.</p></div>' +
    '<div class="card" style="max-width:600px;margin-bottom:32px"><h3 style="font-family:var(--font-d);font-weight:700;margin-bottom:16px">Share your thoughts</h3>' +
    '<div class="form-group"><label class="form-label">What do you want us to improve add or fix?</label><textarea class="form-input" id="fbText" rows="5" placeholder="Tell me anything..." style="resize:vertical"></textarea></div>' +
    '<div class="form-group"><label class="form-label">Rate your experience</label><div style="display:flex;gap:8px;margin-top:4px;flex-wrap:wrap">';
    for(let n=1;n<=5;n++) html+='<button class="btn btn-secondary btn-sm" id="fbRate'+n+'" onclick="document.getElementById(\'fbRating\').value='+n+';[].forEach.call(document.querySelectorAll(\'[id^=fbRate]\'),function(e){e.style.borderColor=\'var(--gray-200)\'});this.style.borderColor=\'var(--gold)\';return false">'+'⭐'.repeat(n)+'</button>';
    html+='</div><input type="hidden" id="fbRating" value="5"></div>' +
    '<button class="btn btn-gold btn-lg btn-block" onclick="app.submitFeedback()" style="text-align:center;margin-top:16px">Send Feedback →</button></div>';
    if(existing.length>0){
      html+='<div><h3 style="font-family:var(--font-d);font-weight:600;margin-bottom:16px;font-size:1.1rem">Your past feedback ('+existing.length+')</h3><div class="card" style="padding:0;overflow:hidden">';
      existing.slice().reverse().slice(0,10).forEach(f=>{html+='<div style="padding:16px;border-bottom:1px solid var(--gray-100)"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="font-size:.7rem;color:var(--muted)">'+new Date(f.ts).toLocaleDateString()+'</span><span>'+'⭐'.repeat(f.rating)+'</span></div><div style="font-size:.9rem">'+f.text+'</div></div>';});
      html+='</div></div>';
    }
    return html;
  },
  submitFeedback() {
    const text=document.getElementById('fbText').value.trim();
    let rating=parseInt(document.getElementById('fbRating').value);
    if(isNaN(rating))rating=5;
    if(!text){toast('Write something first');return;}
    const fb={text,rating,ts:Date.now()};
    const existing=JSON.parse(localStorage.getItem('swt_feedback')||'[]');
    existing.push(fb);
    localStorage.setItem('swt_feedback',JSON.stringify(existing));
    this.pushToSheet({...fb,email:S.user?.email,type:'feedback'});
    toast('Thank you! Feedback logged.');
    this.go('feedback');
  }
};
app.init();
</script>
</body></html>'''

# Write the file
with open('index.html', 'w') as f:
    f.write(html)

print(f"Written {len(html)} chars ({len(html)/1024:.1f} KB)")
