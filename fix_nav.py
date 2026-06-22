import re

with open('index.html') as f:
    content = f.read()

# ============================================================
# 1. ADD CSS for top-right search + compact bottom nav
# ============================================================
new_css = """
/* TOP SEARCH ICON (fixed on all pages) */
.tb-search {
  width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: var(--bg2); border: 1px solid var(--border);
  color: var(--tx3); cursor: pointer; flex-shrink: 0;
  transition: all .15s; margin-left: 8px;
}
.tb-search:hover { color: var(--tx); border-color: var(--pri); background: var(--pri-glow); }
.tb-search svg { width: 18px; height: 18px; stroke-width: 1.8; }

/* SEARCH OVERLAY (full screen) */
.srch-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 200;
  background: oklch(0.10 0.01 260 / 0.95);
  backdrop-filter: blur(8px);
  display: none; flex-direction: column;
}
.srch-overlay.on { display: flex; }
.srch-top {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 16px; border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.srch-top input {
  flex: 1; background: var(--bg2); border: 1px solid var(--border);
  color: var(--tx); padding: 10px 14px; border-radius: var(--r);
  font-size: 0.9rem; outline: none; font-family: inherit;
}
.srch-top input::placeholder { color: var(--tx3); }
.srch-top input:focus { border-color: var(--pri); }
.srch-top .srch-cls {
  background: none; border: none; color: var(--tx3); cursor: pointer;
  font-size: 1.4rem; padding: 4px 8px; line-height: 1; flex-shrink: 0;
}
.srch-results {
  flex: 1; overflow-y: auto; padding: 8px 0;
}
.srch-res-item {
  padding: 12px 16px; border-bottom: 1px solid var(--border);
  cursor: pointer; display: flex; align-items: center; gap: 12px;
  font-size: 0.85rem;
}
.srch-res-item:hover { background: var(--bg2); }
.srch-res-item .srch-ic {
  width: 32px; height: 32px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
}
.srch-res-item .srch-ic.mod { background: var(--pri-glow); color: var(--pri); }
.srch-res-item .srch-ic.song { background: oklch(0.30 0.02 200 / 0.3); color: var(--ok); }
.srch-res-item .srch-info { flex: 1; min-width: 0; }
.srch-res-item .srch-title { font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.srch-res-item .srch-meta { font-size: 0.75rem; color: var(--tx3); margin-top: 2px; }
.srch-res-item .srch-hi { color: var(--pri); font-weight: 700; }
.srch-no { padding: 30px 20px; text-align: center; color: var(--tx3); font-size: 0.85rem; }

/* COMPACT BOTTOM NAV */
.bn { height: 56px; }
.bn-in { justify-content: flex-start; overflow-x: auto; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
.bn-in::-webkit-scrollbar { display: none; }
.bn-i { min-width: 52px; min-height: 44px; padding: 4px 8px; gap: 2px; font-size: 0.65rem; }
.bn-ic { width: 20px; height: 20px; margin-bottom: 0; }
.bn-ic svg { width: 18px; height: 18px; stroke-width: 1.6; }
"""

style_end = content.find('</style>')
content = content[:style_end] + new_css + content[style_end:]
print("CSS added")

# ============================================================
# 2. ADD search icon to every screen's top bar
# ============================================================
# Pattern: <div class="tb-t">TITLE</div>
# Add search icon after each tb-t
search_icon_html = '<button class="tb-search" onclick="openSearch()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg></button>'

# Add after every </div> that follows tb-t
# Pattern: <div class="tb-t">...</div>  →  <div class="tb-t">...</div><button class="tb-search"...>
content = content.replace(
    '<div class="tb-t">Singer OS</div>\n    <div class="tb-r"',
    '<div class="tb-t">Singer OS</div>' + search_icon_html + '\n    <div class="tb-r"'
)

# For all other screens (no tb-r), pattern is: <div class="tb-t">TITLE</div>\n  </div>
# Add search icon before the closing </div> of tb
tb_titles = ['Learn', 'Practice', 'Instruments', 'Songs', 'Music Theory', 'Musician Quiz', 'Your Progress', 'Profile', 'Auth']
for title in tb_titles:
    old = f'<div class="tb-t">{title}</div>\n  </div>'
    new = f'<div class="tb-t">{title}</div>{search_icon_html}\n  </div>'
    content = content.replace(old, new)

print("Search icons added to all top bars")

# ============================================================
# 3. REMOVE old search bar HTML (the one that was before <nav>)
# ============================================================
old_search_html = """<!-- SEARCH BAR -->
<div class="srch-bar" id="srchBar">
  <button class="srch-cls" onclick="closeSearch()">&times;</button>
  <input type="text" id="srchInput" placeholder="Search modules, songs, lessons..." oninput="doSearch()" onkeydown="if(event.key==='Enter')goFirstResult()">
</div>
<div class="srch-res" id="srchRes"></div>

"""
content = content.replace(old_search_html, '')
print("Old search bar removed")

# ============================================================
# 4. ADD new full-screen search overlay (before </body>)
# ============================================================
search_overlay = """
<!-- SEARCH OVERLAY -->
<div class="srch-overlay" id="srchOverlay">
  <div class="srch-top">
    <input type="text" id="srchInput" placeholder="Search modules, songs, lessons..." oninput="doSearch()" onkeydown="if(event.key==='Enter')goFirstResult()">
    <button class="srch-cls" onclick="closeSearch()">&times;</button>
  </div>
  <div class="srch-results" id="srchResults"></div>
</div>
"""
content = content.replace('</body>', search_overlay + '</body>')
print("Search overlay added")

# ============================================================
# 5. REDUCE bottom nav to 5 tabs (remove Search, Quiz, Progress)
# ============================================================
# Remove the Search button from nav
content = content.replace("""    <button class="bn-i" id="n-search" onclick="openSearch()">
      <span class="bn-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg></span>
      Search
    </button>
""", '')

# Remove Quiz button
content = content.replace("""    <button class="bn-i" id="n-quiz" onclick="go('quiz')">
      <span class="bn-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></span>
      Quiz
    </button>
""", '')

# Remove Progress button
content = content.replace("""    <button class="bn-i" id="n-progress" onclick="go('progress')">
      <span class="bn-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></span>
      Progress
    </button>
""", '')

print("Bottom nav reduced to 5 tabs: Home, Learn, Practice, Songs, Theory")

# ============================================================
# 6. UPDATE JS search functions for new overlay
# ============================================================
# Replace old openSearch/closeSearch/doSearch with new versions
old_js_search = content.find('// ============================================================\n// SEARCH\n// ============================================================')
if old_js_search > 0:
    # Find the end of the search JS block (next // === block or end of script)
    next_block = content.find('\n// ============================================================\n', old_js_search + 50)
    if next_block == -1:
        next_block = content.rfind('</script>')
    
    new_search_js = """// ============================================================
// SEARCH
// ============================================================
function openSearch() {
  var overlay = document.getElementById('srchOverlay');
  overlay.classList.add('on');
  setTimeout(function(){ document.getElementById('srchInput').focus(); }, 100);
  doSearch();
}

function closeSearch() {
  var overlay = document.getElementById('srchOverlay');
  overlay.classList.remove('on');
  document.getElementById('srchInput').value = '';
  document.getElementById('srchResults').innerHTML = '';
}

function doSearch() {
  var q = document.getElementById('srchInput').value.trim().toLowerCase();
  var res = document.getElementById('srchResults');
  if (!q) { res.innerHTML = '<div class="srch-no">Type to search modules and songs</div>'; return; }

  var results = [];

  // Search CURRICULUM modules
  for (var s in CURRICULUM) {
    var section = CURRICULUM[s];
    if (!section.modules) continue;
    for (var i = 0; i < section.modules.length; i++) {
      var m = section.modules[i];
      var title = (m.title || '').toLowerCase();
      var outcome = (m.outcome || '').toLowerCase();
      var text = (m.content || '').replace(/<[^>]*>/g, '').toLowerCase();
      if (title.indexOf(q) >= 0 || outcome.indexOf(q) >= 0 || text.indexOf(q) >= 0) {
        var snippet = '';
        var idx = text.indexOf(q);
        if (idx >= 0) {
          var start = Math.max(0, idx - 40);
          var end = Math.min(text.length, idx + q.length + 50);
          snippet = (start > 0 ? '...' : '') + text.substring(start, end) + (end < text.length ? '...' : '');
        } else {
          snippet = outcome.substring(0, 100);
        }
        results.push({
          type: 'module', section: section.title, sectionId: s,
          stage: m.stage, title: highlightMatch(m.title, q),
          snippet: snippet, xp: m.xp
        });
      }
    }
  }

  // Search SONGS
  if (typeof SONGS !== 'undefined') {
    for (var si = 0; si < SONGS.length; si++) {
      var song = SONGS[si];
      var title = (song.title || '').toLowerCase();
      var artist = (song.artist || '').toLowerCase();
      var tags = (song.tags || []).join(' ').toLowerCase();
      var focus = (song.focus || '').toLowerCase();
      if (title.indexOf(q) >= 0 || artist.indexOf(q) >= 0 || tags.indexOf(q) >= 0 || focus.indexOf(q) >= 0) {
        results.push({
          type: 'song', title: highlightMatch(song.title, q),
          artist: highlightMatch(song.artist, q),
          level: song.level, tags: song.tags || [],
          focus: (song.focus || '').substring(0, 100), index: si
        });
      }
    }
  }

  // Render
  if (results.length === 0) {
    res.innerHTML = '<div class="srch-no">No results for "' + esc(q) + '"</div>';
  } else {
    var h = '';
    for (var r of results.slice(0, 20)) {
      if (r.type === 'module') {
        h += '<div class="srch-res-item" onclick="goModule(\\'' + r.sectionId + '\\')">';
        h += '<span class="srch-ic mod">' + r.stage + '</span>';
        h += '<div class="srch-info">';
        h += '<div class="srch-title">' + r.title + '</div>';
        h += '<div class="srch-meta">' + r.section + ' \u00b7 Stage ' + r.stage + ' \u00b7 ' + r.xp + ' XP</div>';
        h += '<div class="srch-meta">' + esc(r.snippet) + '</div>';
        h += '</div></div>';
      } else {
        h += '<div class="srch-res-item" onclick="goSong(' + r.index + ')">';
        h += '<span class="srch-ic song">' + (r.level === 1 ? 'B' : r.level === 2 ? 'I' : 'A') + '</span>';
        h += '<div class="srch-info">';
        h += '<div class="srch-title">' + r.title + ' \u2014 ' + r.artist + '</div>';
        h += '<div class="srch-meta">Level ' + r.level + ' \u00b7 ' + (r.tags || []).join(', ') + '</div>';
        h += '<div class="srch-meta">' + esc(r.focus) + '</div>';
        h += '</div></div>';
      }
    }
    if (results.length > 20) {
      h += '<div class="srch-no">Showing 20 of ' + results.length + ' results</div>';
    }
    res.innerHTML = h;
  }
}

function highlightMatch(text, q) {
  if (!q) return esc(text);
  var lower = text.toLowerCase();
  var idx = lower.indexOf(q);
  if (idx < 0) return esc(text);
  var before = text.substring(0, idx);
  var match = text.substring(idx, idx + q.length);
  var after = text.substring(idx + q.length);
  return esc(before) + '<span class="srch-hi">' + esc(match) + '</span>' + esc(after);
}

function goModule(sectionId) {
  closeSearch();
  go(sectionId);
}

function goSong(index) {
  closeSearch();
  go('songs');
}

function goFirstResult() {
  var items = document.querySelectorAll('.srch-res-item');
  if (items.length > 0) items[0].click();
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeSearch();
});
"""
    content = content[:old_js_search] + new_search_js + content[next_block:]
    print("Search JS updated")

# ============================================================
# 7. REMOVE old search button from home screen (now in top bar)
# ============================================================
content = content.replace(
    "  h += '<button class=\"btn btn-s\" style=\"margin-top:var(--s3);width:auto;padding:var(--s2) var(--s4);min-height:36px\" onclick=\"openSearch()\">&#128269; Search Modules &amp; Songs</button>';\n",
    ""
)
print("Old home search button removed")

with open('index.html', 'w') as f:
    f.write(content)

print(f"Done! File: {len(content)} chars")
