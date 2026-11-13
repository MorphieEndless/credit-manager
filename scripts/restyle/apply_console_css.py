#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restyle console.css -> CPAMP blue-white glass design system."""
import re, sys

P = "internal/management/web/console.css"
s = open(P, encoding="utf-8").read()
orig = s
fails = []

def sub1(name, old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        fails.append(f"[{name}] expected {count}x, found {n}x :: {old[:90]!r}")
        return
    s = s.replace(old, new, count)

def rep(name, old, new):
    global s
    n = s.count(old)
    if n == 0:
        print(f"  {name:<28}   0x  (already covered) {old[:48]}")
        return
    s = s.replace(old, new)
    print(f"  {name:<28} {n:>3}x  {old[:48]} -> {new[:48]}")

# ============================================================
# 1. STRUCTURAL REWRITES (tokens, geometry, glass, controls)
# ============================================================

# --- :root token block -> CPAMP light defaults ---
sub1("root", """\
:root {
  color-scheme: light;
  --bg: #fafbf8;
  --panel: #ffffff;
  --panel-2: #f7f9f6;
  --line: #e7ebe5;
  --text: #1a1f1c;
  --muted: #5f6a61;
  --table-text: #1f2922;
  --table-muted: #4f5b53;
  --accent: #1eb787;
  --accent-soft: #e4f7ef;
  --accent-2: #7968ee;
  --purple-soft: #efedff;
  --warn: #e5a12d;
  --danger: #d95c51;
  --ok: #1eb787;
  --shadow: 0 8px 28px rgba(41, 57, 46, .07);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", system-ui, sans-serif;
}""", """\
:root {
  color-scheme: light;
  --bg: #eff2f7;
  --panel: rgba(255,255,255,.9);
  --panel-2: rgba(255,255,255,.62);
  --card-bg: rgba(255,255,255,.9);
  --control: rgba(255,255,255,.62);
  --control-hover: #ffffff;
  --table-head: #f6faff;
  --line: rgba(15,23,42,.08);
  --text: #2c3e50;
  --muted: #5f6c7b;
  --table-text: #2c3e50;
  --table-muted: #5f6c7b;
  --accent: #3b82f6;
  --accent-soft: rgba(59,130,246,.12);
  --accent-2: #60a5fa;
  --purple-soft: #eff6ff;
  --warn: #f59e0b;
  --danger: #ef4444;
  --ok: #22c55e;
  --shadow: 0 1px 2px rgba(15,23,42,.05);
  font-family: var(--cpamp-plugin-font-family, Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", system-ui, sans-serif);
}""")

# --- body gradient -> light blue glass ---
sub1("body-bg", """\
  background:
    radial-gradient(740px 300px at 45% -8%, rgba(90, 219, 176, .16), transparent 72%),
    radial-gradient(600px 300px at 100% 8%, rgba(121, 104, 238, .06), transparent 76%),
    var(--bg);""", """\
  background:
    radial-gradient(740px 300px at 45% -8%, rgba(122, 162, 255, .20), transparent 72%),
    radial-gradient(600px 300px at 100% 8%, rgba(125, 235, 220, .16), transparent 76%),
    linear-gradient(120deg, #f0f7ff 0%, #e7f2ff 50%, #edf7ff 100%);""")

# --- .card: radius 20 + glass ---
sub1("card", """\
.card {
   background: var(--card-bg, rgba(255,255,255,.9));
  border:1px solid var(--line);
  border-radius:14px;
  padding:18px;
  box-shadow: var(--shadow);
  margin-bottom:16px;
}""", """\
.card {
   background: var(--card-bg, rgba(255,255,255,.9));
  border:1px solid var(--line);
  border-radius:20px;
  padding:18px;
  box-shadow: var(--shadow);
  margin-bottom:16px;
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
}""")

# --- .stat: neutral glass surface, no diffuse shadow ---
sub1("stat", """\
.stat {
  position:relative;
  overflow:hidden;
  background: linear-gradient(135deg, #fff, #fbfdfb);
  border:1px solid var(--line);
  border-radius:12px;
  padding:14px 16px;
  box-shadow: 0 4px 15px rgba(41, 57, 46, .035);
}""", """\
.stat {
  position:relative;
  overflow:hidden;
  background: var(--panel-2);
  border:1px solid var(--line);
  border-radius:12px;
  padding:14px 16px;
  box-shadow: 0 1px 2px rgba(15,23,42,.04);
}""")

# --- .stat top bars / icons: blue sequence ---
sub1("stat-bar2", ".stat:nth-child(2n)::before { background:var(--accent-2); }",
     ".stat:nth-child(2n)::before { background:#60a5fa; }")
sub1("stat-bar3", ".stat:nth-child(3n)::before { background:var(--warn); }",
     ".stat:nth-child(3n)::before { background:#f59e0b; }")
sub1("stat-icon2", ".stat:nth-child(2n) .stat-icon { background:var(--purple-soft); color:#5f4fd0; }",
     ".stat:nth-child(2n) .stat-icon { background:#e0edff; color:#3b82f6; }")

# --- buttons / tabs: 12px radius, 14px 600, min-height 40 for .btn ---
sub1("btn-base", """\
.tab, button, .btn {
  appearance:none;
  border:1px solid var(--line);
   background: var(--panel);
  color:var(--text);
  border-radius:8px;
  padding:8px 13px;
  cursor:pointer;
  font:inherit;
  font-size:.86rem;
  transition: background .16s ease, border-color .16s ease, box-shadow .16s ease, transform .16s ease;
}""", """\
.tab, button, .btn {
  appearance:none;
  border:1px solid var(--line);
   background: var(--panel);
  color:var(--text);
  border-radius:12px;
  padding:8px 14px;
  cursor:pointer;
  font:inherit;
  font-size:.875rem;
  font-weight:600;
  transition: background .16s ease, border-color .16s ease, box-shadow .16s ease, transform .16s ease;
}
.btn { min-height:40px; }
.btn.sm, .row-actions .btn, .pricing-actions .btn { min-height:32px; }
.price-tier-remove { min-height:28px; }""")

sub1("btn-hover", ".tab:hover, button:hover, .btn:hover { border-color:#cbd5cc; box-shadow:0 4px 12px rgba(41,57,46,.07); }",
     ".tab:hover, button:hover, .btn:hover { border-color:rgba(59,130,246,.4); box-shadow:0 1px 2px rgba(15,23,42,.05); }")

sub1("btn-primary", ".btn.primary { background: var(--accent); border-color: var(--accent); color: #fff; box-shadow:0 5px 12px rgba(30,183,135,.19); }",
     ".btn.primary { background: var(--accent); border-color: var(--accent); color: #fff; box-shadow:0 5px 12px rgba(59,130,246,.19); }")
sub1("btn-primary-hover", ".btn.primary:hover { background:#14a879; border-color:#14a879; }",
     ".btn.primary:hover { background:#60a5fa; border-color:#60a5fa; transform:translateY(-1px); box-shadow:0 8px 18px -14px rgba(59,130,246,.72); }\nhtml[data-palette=\"dark\"] .btn.primary:hover { background:#93c5fd; border-color:#93c5fd; }")

sub1("btn-ok", ".btn.ok { background:#202421; border-color:#202421; color:#fff; }",
     ".btn.ok { background:var(--panel-2); border-color:var(--line); color:var(--text); }")
sub1("btn-danger", ".btn.danger { background:#fff7f5; border-color:#f2d0cb; color:#bd443b; }",
     ".btn.danger { background:rgba(239,68,68,.08); border-color:rgba(239,68,68,.3); color:#ef4444; }")
sub1("btn-ghost", ".btn.ghost { background:rgba(255,255,255,.58); }",
     ".btn.ghost { background:var(--panel-2); }")
sub1("btn-iconish", ".btn.iconish { min-width:38px; width:38px; height:38px; min-height:38px; padding:0; gap:0; }",
     ".btn.iconish { min-width:40px; width:40px; height:40px; min-height:40px; padding:0; gap:0; }")
sub1("btn-soft-hover", ".btn.soft:hover { background:#d7f3e7; border-color:#b4e5d2; }",
     ".btn.soft:hover { background:#dbeafe; border-color:#93c5fd; }")

# --- inputs: radius 12, min-height 40, blue focus ring ---
sub1("input-base", """\
input, select, textarea {
  width:100%;
  border:1px solid #e2e7e1;
   background:var(--control, #fcfdfb);
  color:var(--text);
  border-radius:8px;
  padding:9px 10px;
  font:inherit;
  outline:none;
  transition:border-color .16s ease, box-shadow .16s ease, background .16s ease;
}""", """\
input, select, textarea {
  width:100%;
  border:1px solid var(--line);
   background:var(--control, rgba(255,255,255,.62));
  color:var(--text);
  border-radius:12px;
  padding:9px 12px;
  font:inherit;
  outline:none;
  transition:border-color .16s ease, box-shadow .16s ease, background .16s ease;
}
input:not([type="checkbox"]):not([type="radio"]):not(.native-control), select, textarea { min-height:40px; }
.custom-time-field .custom-time-input, .custom-date-text, .auth-warmup-task-name { min-height:0; }
.native-control { min-height:0 !important; }""")

sub1("input-hover", "input:not(:disabled):hover, select:not(:disabled):hover, textarea:not(:disabled):hover {\n  border-color:#c8d6cb;",
     "input:not(:disabled):hover, select:not(:disabled):hover, textarea:not(:disabled):hover {\n  border-color:#b4c3d8;")

sub1("select-h", "select {\n  appearance:none;\n  min-height:38px;", "select {\n  appearance:none;\n  min-height:40px;")
sub1("dt-h", 'input[type="datetime-local"] {\n  min-height:38px;', 'input[type="datetime-local"] {\n  min-height:40px;')
sub1("dt-scheme", 'input[type="datetime-local"] {\n  min-height:40px;\n  padding-right:9px;\n  color-scheme:light;',
     'input[type="datetime-local"] {\n  min-height:40px;\n  padding-right:9px;\n  color-scheme:light dark;')

sub1("focus", "input:focus, select:focus, textarea:focus { border-color:#76d7b8; background:#fff; box-shadow:0 0 0 3px rgba(30,183,135,.12); }",
     "input:focus, select:focus, textarea:focus { border-color:var(--accent); background:#fff; box-shadow:0 0 0 3px rgba(59,130,246,.15); }")
sub1("ctrl-open", ".custom-control.open > .custom-control-trigger { border-color:#76d7b8; background:#fff; box-shadow:0 0 0 3px rgba(30,183,135,.12); }",
     ".custom-control.open > .custom-control-trigger { border-color:var(--accent); background:#fff; box-shadow:0 0 0 3px rgba(59,130,246,.15); }")
sub1("keysearch-open", ".key-search-control.open input { border-color:#76d7b8; background:#fff; box-shadow:0 0 0 3px rgba(30,183,135,.12); }",
     ".key-search-control.open input { border-color:var(--accent); background:#fff; box-shadow:0 0 0 3px rgba(59,130,246,.15); }")
sub1("keymat-focus", ".key-material-field:focus-within .key-material-prefix { border-color:#76d7b8; box-shadow:0 0 0 3px rgba(30,183,135,.12); }",
     ".key-material-field:focus-within .key-material-prefix { border-color:var(--accent); box-shadow:0 0 0 3px rgba(59,130,246,.15); }")

sub1("trigger", """\
.custom-control-trigger {
  display:flex;
  align-items:center;
  justify-content:space-between;
  width:100%;
  min-height:38px;
  padding:8px 10px;
  border:1px solid #e2e7e1;
  border-radius:8px;
  background:#fcfdfb;""", """\
.custom-control-trigger {
  display:flex;
  align-items:center;
  justify-content:space-between;
  width:100%;
  min-height:40px;
  padding:8px 12px;
  border:1px solid var(--line);
  border-radius:12px;
  background:var(--control);""")
sub1("trigger-hover", ".custom-control-trigger:hover:not(:disabled) { border-color:#c8d6cb; background:#fff; box-shadow:none; }",
     ".custom-control-trigger:hover:not(:disabled) { border-color:#b4c3d8; background:var(--control-hover); box-shadow:none; }")

# --- dropdown panels: blue glass ---
sub1("cc-panel", """\
  padding:6px;
  border:1px solid #dbe7df;
  border-radius:11px;
  background:#fff;
  box-shadow:0 16px 36px rgba(29, 49, 37, .16), 0 3px 10px rgba(29, 49, 37, .07);
}
.custom-control-panel[hidden] { display:none; }""", """\
  padding:6px;
  border:1px solid var(--line);
  border-radius:12px;
  background:rgba(255,255,255,.92);
  box-shadow:0 10px 15px -3px rgba(15,23,42,.12), 0 3px 8px rgba(15,23,42,.06);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
}
.custom-control-panel[hidden] { display:none; }""")
sub1("tl-panel", """\
  padding:6px;
  border:1px solid #dbe7df;
  border-radius:11px;
  background:#fff;
  box-shadow:0 16px 36px rgba(29, 49, 37, .16), 0 3px 10px rgba(29, 49, 37, .07);
}
.token-limit-panel .custom-option""", """\
  padding:6px;
  border:1px solid var(--line);
  border-radius:12px;
  background:rgba(255,255,255,.92);
  box-shadow:0 10px 15px -3px rgba(15,23,42,.12), 0 3px 8px rgba(15,23,42,.06);
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
}
.token-limit-panel .custom-option""")

sub1("date-panel", ".custom-date-panel { width:312px; padding:14px; border-color:#cfe7da; border-radius:14px; background:linear-gradient(180deg, #fff, #fbfdfb); box-shadow:0 20px 44px rgba(29, 49, 37, .17), 0 4px 12px rgba(29, 49, 37, .06); }",
     ".custom-date-panel { width:312px; padding:14px; border-color:var(--line); border-radius:14px; background:linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,.82)); box-shadow:0 10px 15px -3px rgba(15,23,42,.12), 0 4px 10px rgba(15,23,42,.06); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); }")
sub1("time-panel", ".custom-time-panel { width:168px; padding:8px; border-color:#cfe7da; border-radius:14px; background:linear-gradient(180deg, #fff, #fbfdfb); box-shadow:0 20px 44px rgba(29, 49, 37, .17), 0 4px 12px rgba(29, 49, 37, .06); }",
     ".custom-time-panel { width:168px; padding:8px; border-color:var(--line); border-radius:14px; background:linear-gradient(180deg, rgba(255,255,255,.95), rgba(255,255,255,.82)); box-shadow:0 10px 15px -3px rgba(15,23,42,.12), 0 4px 10px rgba(15,23,42,.06); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); }")

# --- modal backdrop + connection modal: CPAMP glass ---
sub1("backdrop", ".modal-backdrop { position:fixed; z-index:20; inset:0; display:grid; place-items:center; padding:20px; background:rgba(24, 35, 28, .32); backdrop-filter:blur(5px); opacity:0; pointer-events:none; transition:opacity .18s ease; }",
     ".modal-backdrop { position:fixed; z-index:20; inset:0; display:grid; place-items:center; padding:20px; background:rgba(15,23,42,.32); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); opacity:0; pointer-events:none; transition:opacity .18s ease; }")
sub1("modal-1", ".connection-modal { width:min(610px, 100%); max-height:calc(100vh - 40px); overflow:auto; background:var(--panel); border:1px solid rgba(255,255,255,.72); border-radius:16px; box-shadow:0 24px 70px rgba(21, 37, 26, .25); transform:scale(.96); transition:transform .36s cubic-bezier(.32, .72, 0, 1); }",
     ".connection-modal { width:min(610px, 100%); max-height:calc(100vh - 40px); overflow:auto; background:var(--panel); border:1px solid rgba(255,255,255,.45); border-radius:12px; box-shadow:0 10px 15px -3px rgba(15,23,42,.14); backdrop-filter:blur(20px); -webkit-backdrop-filter:blur(20px); transform:scale(.96); transition:transform .36s cubic-bezier(.32, .72, 0, 1); }")
sub1("modal-2", ".connection-modal { border-radius:16px; }", "")
sub1("modal-shadow", ".connection-modal {\n  background:var(--panel);\n  box-shadow:0 28px 80px rgba(16, 28, 22, .28), 0 0 0 1px rgba(255,255,255,.55) inset;\n}",
     ".connection-modal {\n  background:var(--panel);\n  box-shadow:0 10px 15px -3px rgba(15,23,42,.14), 0 0 0 1px rgba(255,255,255,.4) inset;\n}")
sub1("backdrop-mat", ".modal-backdrop {\n  background:rgba(18, 24, 21, .42);\n  backdrop-filter:blur(18px) saturate(140%);",
     ".modal-backdrop {\n  background:rgba(15,23,42,.42);\n  backdrop-filter:blur(18px) saturate(140%);")

# --- modal-section glass ---
sub1("modal-section", """\
.modal-section {
  display:grid;
  gap:12px;
  padding:16px;
  border:1px solid #e8eee8;
  border-radius:12px;
  background:linear-gradient(180deg, #fcfdfb, #f7faf7);
}""", """\
.modal-section {
  display:grid;
  gap:12px;
  padding:16px;
  border:1px solid var(--line);
  border-radius:12px;
  background:linear-gradient(180deg, rgba(255,255,255,.72), rgba(255,255,255,.5));
  backdrop-filter:blur(20px);
  -webkit-backdrop-filter:blur(20px);
}""")

# --- flash stays glass ---
sub1("flash", "  border-radius: 12px;\n  border: 1px solid var(--line);\n  background: #fff;\n  box-shadow: 0 14px 40px rgba(28, 42, 33, .14);",
     "  border-radius: 12px;\n  border: 1px solid var(--line);\n  background: rgba(255,255,255,.9);\n  box-shadow: 0 10px 15px -3px rgba(15,23,42,.14);")

# --- empty states ---
sub1("empty", ".empty-state { display:grid; place-items:center; min-height:112px; padding:22px 16px; text-align:center; color:var(--muted); background:linear-gradient(135deg, #fbfdfb, #f6faf7); border:1px dashed #dce7de; border-radius:10px; font-size:.82rem; }",
     ".empty-state { display:grid; place-items:center; min-height:112px; padding:22px 16px; text-align:center; color:var(--muted); background:linear-gradient(135deg, rgba(255,255,255,.7), rgba(244,248,253,.6)); border:1px dashed rgba(59,130,246,.28); border-radius:12px; font-size:.82rem; }")

# --- filter card / table scroll ---
sub1("filter-card", ".filter-card { border-color:#ccebdd; box-shadow:0 8px 24px rgba(30,183,135,.06); }",
     ".filter-card { border-color:rgba(59,130,246,.22); box-shadow:0 8px 24px rgba(59,130,246,.06); }")
sub1("table-scroll", ".table-scroll { overflow-x:auto; border:1px solid #edf0eb; border-radius:10px; }",
     ".table-scroll { overflow-x:auto; border:1px solid var(--line); border-radius:12px; }")
sub1("table-scroll-bg", ".table-scroll { background:#fff; }", ".table-scroll { background:var(--panel); }")

# --- table head / cell borders on tokens ---
sub1("th-border", "th, td { border-bottom:1px solid #e8ece6;", "th, td { border-bottom:1px solid var(--line);")
sub1("th-bg", "th { color:var(--table-muted); background:#f7faf7;", "th { color:var(--table-muted); background:var(--table-head);")
sub1("keys-th", ".keys-table th { position:sticky; top:0; z-index:1; background:#f7faf7;",
     ".keys-table th { position:sticky; top:0; z-index:1; background:var(--table-head);")

# --- unit-switch active: accent-soft + accent ---
sub1("unit-active", """\
.unit-switch button.active {
  background:var(--accent-soft);
  color:var(--text);
  box-shadow:none;
}""", """\
.unit-switch button.active {
  background:var(--accent-soft);
  color:var(--accent);
  box-shadow:none;
}""")

# --- list search geometry ---
sub1("list-search", ".list-search { position:relative; display:block; flex:0 1 288px; width:288px; min-width:220px; height:38px; min-height:38px; margin:0; border:1px solid var(--line); border-radius:10px; background:var(--panel-2);",
     ".list-search { position:relative; display:block; flex:0 1 288px; width:288px; min-width:220px; height:40px; min-height:40px; margin:0; border:1px solid var(--line); border-radius:12px; background:var(--panel-2);")
sub1("list-search-input", ".list-search input, .list-search input:hover, .list-search input:focus { display:block; width:100%; height:36px; min-height:36px; padding:8px 41px 8px 37px; border:0; border-radius:9px;",
     ".list-search input, .list-search input:hover, .list-search input:focus { display:block; width:100%; height:38px; min-height:38px; padding:8px 41px 8px 37px; border:0; border-radius:10px;")

# --- overview guide: dark card stays dark, goes blue ---
sub1("guide", ".overview-guide { min-height:100%; background:linear-gradient(145deg, #202421, #38463b); border-color:#202421; color:#fff; }",
     ".overview-guide { min-height:100%; background:linear-gradient(145deg, #1d2b45, #0f1e38); border-color:#1d2b45; color:#fff; }")
sub1("guide-hint", ".overview-guide .hint { color:#d2dbd3; }", ".overview-guide .hint { color:#c3d3e8; }")
sub1("guide-mark", ".overview-guide .guide-mark { display:grid; place-items:center; width:32px; height:32px; margin-bottom:20px; border-radius:10px; background:rgba(30,183,135,.18); color:#76dfbc; font-weight:800; }",
     ".overview-guide .guide-mark { display:grid; place-items:center; width:32px; height:32px; margin-bottom:20px; border-radius:10px; background:rgba(96,165,250,.2); color:#93c5fd; font-weight:800; }")
sub1("guide-dark", "html[data-palette=\"dark\"] .overview-guide { background:linear-gradient(145deg, #211e1b, #39332d); border-color:#39332d; }",
     "html[data-palette=\"dark\"] .overview-guide { background:linear-gradient(145deg, #131c30, #1b2a4a); border-color:#26334f; }")

# --- brand rails: keep distinct brand hues, but retire mint/violet hexes ---
sub1("rail-ag", '.auth-quota-card[data-provider="antigravity"] { --auth-rail:#1eb787; }',
     '.auth-quota-card[data-provider="antigravity"] { --auth-rail:#3186ff; }')
sub1("rail-kimi", '.auth-quota-card[data-provider="kimi"] { --auth-rail:#7968ee; }',
     '.auth-quota-card[data-provider="kimi"] { --auth-rail:#6366f1; }')

# --- auth quota card: 20px radius (spec: card = --app-radius-lg) ---
sub1("aq-radius", ".auth-quota-card { --auth-rail: var(--accent); position:relative; display:flex; flex-direction:column; align-self:stretch; height:100%; min-height:299px; margin:0; overflow:visible; padding:0; border-radius:12px;",
     ".auth-quota-card { --auth-rail: var(--accent); position:relative; display:flex; flex-direction:column; align-self:stretch; height:100%; min-height:299px; margin:0; overflow:visible; padding:0; border-radius:20px;")
sub1("aq-rail-radius", ".auth-quota-card::before { content:\"\"; position:absolute; top:0; bottom:0; left:0; width:3px; border-radius:12px 0 0 12px; background:var(--auth-rail); }",
     ".auth-quota-card::before { content:\"\"; position:absolute; top:0; bottom:0; left:0; width:3px; border-radius:20px 0 0 20px; background:var(--auth-rail); }")

# --- small geometry touch-ups per spec (12px controls) ---
sub1("btn-sm-radius", ".btn.sm { padding:5px 10px; font-size:.78rem; border-radius:7px; line-height:1.25; }",
     ".btn.sm { padding:5px 10px; font-size:.78rem; border-radius:10px; line-height:1.25; }")
sub1("scope-card-radius", "padding:11px; border:1px solid var(--line); border-radius:11px; background:var(--panel-2); color:var(--text);",
     "padding:11px; border:1px solid var(--line); border-radius:12px; background:var(--panel-2); color:var(--text);")
sub1("confirm-note-radius", ".auth-quota-batch-confirm-note { display:flex; align-items:flex-start; gap:10px; padding:11px 12px; border:1px solid var(--line); border-radius:11px; background:var(--panel-2); }",
     ".auth-quota-batch-confirm-note { display:flex; align-items:flex-start; gap:10px; padding:11px 12px; border:1px solid var(--line); border-radius:12px; background:var(--panel-2); }")

# --- glass off under mobile/reduced prefs (spec behaviour) ---
sub1("glass-off", """\
@media (prefers-contrast: more) {""", """\
@media (max-width: 768px), (prefers-reduced-motion: reduce), (prefers-reduced-transparency: reduce) {
  .card, .connection-modal, .custom-control-panel, .flash, .modal-section {
    backdrop-filter:none;
    -webkit-backdrop-filter:none;
  }
}
@media (prefers-contrast: more) {""")

# --- reduced transparency: cover the new glass surfaces too ---
sub1("reduced-transp", """\
@media (prefers-reduced-transparency: reduce) {
  .tabs, .usage-pagination, .unit-switch, .flash, .modal-backdrop {
    backdrop-filter:none;
    -webkit-backdrop-filter:none;
  }
  .tabs, .usage-pagination, .unit-switch, .flash { background:var(--panel); }
  .modal-backdrop { background:rgba(18, 24, 21, .62); }
}""", """\
@media (prefers-reduced-transparency: reduce) {
  .tabs, .usage-pagination, .unit-switch, .flash, .modal-backdrop, .card, .connection-modal, .custom-control-panel, .modal-section {
    backdrop-filter:none;
    -webkit-backdrop-filter:none;
  }
  .tabs, .usage-pagination, .unit-switch, .flash { background:var(--panel); }
  .card, .connection-modal, .custom-control-panel, .modal-section { background:#fff; }
  .modal-backdrop { background:rgba(15,23,42,.62); }
}""")

# ============================================================
# 2. PALETTE TOKEN BLOCKS
# ============================================================
sub1("pal-white", """\
html[data-palette="white"] {
  color-scheme:light;
  --bg:#ffffff; --panel:#ffffff; --panel-2:#f8f8f8; --card-bg:rgba(255,255,255,.94);
  --control:#ffffff; --control-hover:#ffffff; --table-head:#f7f7f7; --line:#e6e6e6;
  --text:#242424; --muted:#686868; --table-text:#282828; --table-muted:#5f5f5f;
  --accent:#5c8776; --accent-soft:#e8f3ef; --accent-2:#8274c9; --purple-soft:#f0edfa;
  --warn:#b77b1d; --danger:#c15b52; --ok:#4d9475; --shadow:0 8px 28px rgba(30,30,30,.07);
}
html[data-palette="light"] {
  color-scheme:light;
  --bg:#f0eee8; --panel:#fffdf9; --panel-2:#f6f4ee; --card-bg:rgba(255,253,249,.92);
  --control:#fffdf9; --control-hover:#ffffff; --table-head:#f6f4ee; --line:#e3e1db;
  --text:#2d2a26; --muted:#6d6760; --table-text:#2d2a26; --table-muted:#6d6760;
  --accent:#8b8680; --accent-soft:#ebe8e1; --accent-2:#8573bd; --purple-soft:#eeebf5;
  --warn:#d97706; --danger:#c65746; --ok:#168b63; --shadow:0 10px 24px rgba(70,63,55,.09);
}
html[data-palette="dark"] {
  color-scheme:dark;
  --bg:#151412; --panel:#1d1b18; --panel-2:#25221f; --card-bg:rgba(29,27,24,.96);
  --control:#25221f; --control-hover:#302d29; --table-head:#282521; --line:#3a3530;
  --text:#f6f4f1; --muted:#b6afa3; --table-text:#f6f4f1; --table-muted:#c2bbb2;
  --accent:#b3aaa0; --accent-soft:#36312d; --accent-2:#b5a5e9; --purple-soft:#312c40;
  --warn:#efb860; --danger:#ef8779; --ok:#58be91; --shadow:0 12px 30px rgba(0,0,0,.3);
}""", """\
html[data-palette="white"], html[data-palette="light"] {
  color-scheme:light;
  --bg:#eff2f7; --panel:rgba(255,255,255,.9); --panel-2:rgba(255,255,255,.62); --card-bg:rgba(255,255,255,.9);
  --control:rgba(255,255,255,.62); --control-hover:#ffffff; --table-head:#f6faff; --line:rgba(15,23,42,.08);
  --text:#2c3e50; --muted:#5f6c7b; --table-text:#2c3e50; --table-muted:#5f6c7b;
  --accent:#3b82f6; --accent-soft:rgba(59,130,246,.12); --accent-2:#60a5fa; --purple-soft:#eff6ff;
  --warn:#f59e0b; --danger:#ef4444; --ok:#22c55e; --shadow:0 1px 2px rgba(15,23,42,.05);
}
html[data-palette="dark"] {
  color-scheme:dark;
  --bg:#0a0a0a; --panel:rgba(24,28,40,.9); --panel-2:rgba(255,255,255,.08); --card-bg:rgba(24,28,40,.92);
  --control:#1b1f2a; --control-hover:#232836; --table-head:rgba(255,255,255,.06); --line:rgba(255,255,255,.08);
  --text:#e5e5e5; --muted:#a3a3a3; --table-text:#e5e5e5; --table-muted:#a3a3a3;
  --accent:#60a5fa; --accent-soft:rgba(96,165,250,.18); --accent-2:#93c5fd; --purple-soft:rgba(96,165,250,.16);
  --warn:#f59e0b; --danger:#f87171; --ok:#4ade80; --shadow:0 1px 3px rgba(0,0,0,.3);
}""")

sub1("pal-body", """\
html[data-palette="light"] body { background:radial-gradient(740px 300px at 45% -8%, rgba(139,134,128,.13), transparent 72%),radial-gradient(600px 300px at 100% 8%, rgba(133,115,189,.06), transparent 76%),var(--bg); }
html[data-palette="dark"] body { background:radial-gradient(740px 300px at 45% -8%, rgba(148,134,119,.12), transparent 72%),radial-gradient(600px 300px at 100% 8%, rgba(181,165,233,.07), transparent 76%),var(--bg); }
html[data-palette="light"] .stat { background:linear-gradient(135deg, #fffdf9, #f6f4ee); }
html[data-palette="dark"] .stat { background:linear-gradient(135deg, #282521, #1d1b18); }""", """\
html[data-palette="white"] body, html[data-palette="light"] body { background:radial-gradient(740px 300px at 45% -8%, rgba(122,162,255,.20), transparent 72%),radial-gradient(600px 300px at 100% 8%, rgba(125,235,220,.16), transparent 76%),linear-gradient(120deg, #f0f7ff 0%, #e7f2ff 50%, #edf7ff 100%); }
html[data-palette="dark"] body { background:radial-gradient(740px 300px at 45% -8%, rgba(27,42,85,.35), transparent 72%),radial-gradient(600px 300px at 100% 8%, rgba(15,61,89,.30), transparent 76%),linear-gradient(120deg, #0b1324 0%, #0a1426 50%, #091521 100%); }
html[data-palette="dark"] .stat { background:linear-gradient(135deg, rgba(255,255,255,.08), rgba(255,255,255,.03)); }""")

# ============================================================
# 3. PER-PALETTE RULE REWRITES (warm -> blue/slate)
# ============================================================
def sr(name, old, new):  # exact single replacement required
    sub1(name, old, new)

sr("pal-trow-l", 'html[data-palette="light"] tbody tr:hover td, html[data-palette="light"] .keys-table tbody tr:hover td { background:#f4f1eb; }',
   'html[data-palette="white"] tbody tr:hover td, html[data-palette="white"] .keys-table tbody tr:hover td, html[data-palette="light"] tbody tr:hover td, html[data-palette="light"] .keys-table tbody tr:hover td { background:rgba(59,130,246,.06); }')
sr("pal-trow-d", 'html[data-palette="dark"] tbody tr:hover td, html[data-palette="dark"] .keys-table tbody tr:hover td { background:#2d2925; }',
   'html[data-palette="dark"] tbody tr:hover td, html[data-palette="dark"] .keys-table tbody tr:hover td { background:rgba(255,255,255,.05); }')
sr("pal-tr-mobile", """\
  html[data-palette="light"] .keys-table tbody tr, html[data-palette="light"] .pricing-table tbody tr { background:#fffdf9; border-color:#e3e1db; }
  html[data-palette="dark"] .keys-table tbody tr, html[data-palette="dark"] .pricing-table tbody tr { background:#1d1b18; border-color:#3a3530; }
  html[data-palette="light"] .keys-table tbody tr:hover, html[data-palette="light"] .pricing-table tbody tr:hover { border-color:#d8d3ca; }
  html[data-palette="dark"] .keys-table tbody tr:hover, html[data-palette="dark"] .pricing-table tbody tr:hover { border-color:#5a534b; }""", """\
  html[data-palette="light"] .keys-table tbody tr, html[data-palette="light"] .pricing-table tbody tr, html[data-palette="white"] .keys-table tbody tr, html[data-palette="white"] .pricing-table tbody tr { background:rgba(255,255,255,.8); border-color:var(--line); }
  html[data-palette="dark"] .keys-table tbody tr, html[data-palette="dark"] .pricing-table tbody tr { background:#181c28; border-color:rgba(255,255,255,.1); }
  html[data-palette="light"] .keys-table tbody tr:hover, html[data-palette="light"] .pricing-table tbody tr:hover, html[data-palette="white"] .keys-table tbody tr:hover, html[data-palette="white"] .pricing-table tbody tr:hover { border-color:rgba(59,130,246,.35); }
  html[data-palette="dark"] .keys-table tbody tr:hover, html[data-palette="dark"] .pricing-table tbody tr:hover { border-color:rgba(96,165,250,.4); }""")
sr("pal-modsec", 'html[data-palette="light"] .modal-section, html[data-palette="light"] .custom-date-panel, html[data-palette="light"] .custom-time-panel { background:linear-gradient(180deg, #fffdf9, #f6f4ee); border-color:var(--line); }',
   'html[data-palette="white"] .modal-section, html[data-palette="white"] .custom-date-panel, html[data-palette="white"] .custom-time-panel, html[data-palette="light"] .modal-section, html[data-palette="light"] .custom-date-panel, html[data-palette="light"] .custom-time-panel { background:linear-gradient(180deg, rgba(255,255,255,.9), rgba(244,248,253,.85)); border-color:var(--line); }')
sr("pal-modsec-d", 'html[data-palette="dark"] .modal-section, html[data-palette="dark"] .custom-date-panel, html[data-palette="dark"] .custom-time-panel { background:linear-gradient(180deg, #282521, #1d1b18); border-color:var(--line); }',
   'html[data-palette="dark"] .modal-section, html[data-palette="dark"] .custom-date-panel, html[data-palette="dark"] .custom-time-panel { background:linear-gradient(180deg, #202636, #181c28); border-color:var(--line); }')
sr("pal-active", 'html[data-palette="light"] .tab.active, html[data-palette="light"] .unit-switch button.active, html[data-palette="light"] .filter-state, html[data-palette="light"] .overview-filter-state { color:#57524c; border-color:#d8d3ca; }',
   'html[data-palette="white"] .tab.active, html[data-palette="white"] .unit-switch button.active, html[data-palette="white"] .filter-state, html[data-palette="white"] .overview-filter-state,\nhtml[data-palette="light"] .tab.active, html[data-palette="light"] .unit-switch button.active, html[data-palette="light"] .filter-state, html[data-palette="light"] .overview-filter-state { color:var(--accent); border-color:rgba(59,130,246,.3); }')
sr("pal-active-d", 'html[data-palette="dark"] .tab.active, html[data-palette="dark"] .unit-switch button.active, html[data-palette="dark"] .filter-state, html[data-palette="dark"] .overview-filter-state { color:#f0ece6; border-color:#504940; }',
   'html[data-palette="dark"] .tab.active, html[data-palette="dark"] .unit-switch button.active, html[data-palette="dark"] .filter-state, html[data-palette="dark"] .overview-filter-state { color:var(--accent); border-color:rgba(96,165,250,.4); }')
sr("pal-usw", """\
html[data-palette="light"] .unit-switch { background:#eeece6; border-color:#d8d4cc; box-shadow:none; }
html[data-palette="light"] .unit-switch button:hover { background:#e2dfd8; }
html[data-palette="light"] .unit-switch button.active { background:#817b73; color:#fffdf9; }
html[data-palette="light"] .rate-field { background:#eeece6; border-color:#d8d4cc; box-shadow:none; color:#756e66; }
html[data-palette="light"] .rate-field b { color:#2d2a26; }
html[data-palette="dark"] .unit-switch { background:#282521; border-color:#49433c; box-shadow:none; }
html[data-palette="dark"] .unit-switch-label { color:#b9b1a7; }
html[data-palette="dark"] .unit-switch button { color:#c8c0b6; }
html[data-palette="dark"] .unit-switch button:hover { background:#37322d; color:#f6f4f1; }
html[data-palette="dark"] .unit-switch button.active { background:#6f675f; color:#fffdf9; }
html[data-palette="dark"] .rate-field { background:#282521; border-color:#49433c; box-shadow:none; color:#b9b1a7; }
html[data-palette="dark"] .rate-field b { color:#f6f4f1; }""", """\
html[data-palette="light"] .unit-switch { background:rgba(255,255,255,.62); border-color:var(--line); box-shadow:none; }
html[data-palette="light"] .unit-switch button:hover { background:#ffffff; }
html[data-palette="light"] .unit-switch button.active { background:var(--accent-soft); color:var(--accent); }
html[data-palette="light"] .rate-field { background:rgba(255,255,255,.62); border-color:var(--line); box-shadow:none; color:#5f6c7b; }
html[data-palette="light"] .rate-field b { color:#2c3e50; }
html[data-palette="dark"] .unit-switch { background:#1b1f2a; border-color:rgba(255,255,255,.1); box-shadow:none; }
html[data-palette="dark"] .unit-switch-label { color:#a3a3a3; }
html[data-palette="dark"] .unit-switch button { color:#a3a3a3; }
html[data-palette="dark"] .unit-switch button:hover { background:#232836; color:#e5e5e5; }
html[data-palette="dark"] .unit-switch button.active { background:var(--accent-soft); color:var(--accent); }
html[data-palette="dark"] .rate-field { background:#1b1f2a; border-color:rgba(255,255,255,.1); box-shadow:none; color:#a3a3a3; }
html[data-palette="dark"] .rate-field b { color:#e5e5e5; }""")
sr("pal-select-d", """\
html[data-palette="dark"] select {
  background-color:#25221f !important;
  color:#f6f4f1 !important;
  border-color:#4a443c !important;
  color-scheme:dark;
}
html[data-palette="dark"] select:hover { background-color:#2d2925 !important; }
html[data-palette="dark"] select:focus {
  background-color:#2d2925 !important;
  border-color:#797066 !important;
  box-shadow:0 0 0 3px rgba(179,170,160,.16) !important;
  outline:none;
}
html[data-palette="dark"] select option { background:#25221f; color:#f6f4f1; }
html[data-palette="dark"] .custom-control-trigger,
html[data-palette="dark"] .custom-control-trigger:hover:not(:disabled) {
  background:#25221f !important;
  color:#f6f4f1 !important;
  border-color:#4a443c !important;
}
html[data-palette="dark"] .custom-control.open > .custom-control-trigger {
  background:#2d2925 !important;
  border-color:#797066 !important;
  box-shadow:0 0 0 3px rgba(179,170,160,.16) !important;
}""", """\
html[data-palette="dark"] select {
  background-color:#1b1f2a !important;
  color:#e5e5e5 !important;
  border-color:rgba(255,255,255,.12) !important;
  color-scheme:dark;
}
html[data-palette="dark"] select:hover { background-color:#232836 !important; }
html[data-palette="dark"] select:focus {
  background-color:#232836 !important;
  border-color:#60a5fa !important;
  box-shadow:0 0 0 3px rgba(96,165,250,.16) !important;
  outline:none;
}
html[data-palette="dark"] select option { background:#1b1f2a; color:#e5e5e5; }
html[data-palette="dark"] .custom-control-trigger,
html[data-palette="dark"] .custom-control-trigger:hover:not(:disabled) {
  background:#1b1f2a !important;
  color:#e5e5e5 !important;
  border-color:rgba(255,255,255,.12) !important;
}
html[data-palette="dark"] .custom-control.open > .custom-control-trigger {
  background:#232836 !important;
  border-color:#60a5fa !important;
  box-shadow:0 0 0 3px rgba(96,165,250,.16) !important;
}""")
sr("pal-panels-d", """\
html[data-palette="dark"] .custom-select-panel,
html[data-palette="dark"] .custom-date-panel,
html[data-palette="dark"] .custom-time-panel,
html[data-palette="dark"] .key-search-panel { background:#25221f !important; border-color:#4a443c !important; }
html[data-palette="light"] .custom-time-col { background:#f3f0e9; }
html[data-palette="dark"] .custom-time-col { background:#1b1916; }
html[data-palette="dark"] .custom-time-option { color:#f0ece6; }
html[data-palette="dark"] .custom-time-option:hover, html[data-palette="dark"] .custom-time-option:focus-visible { background:#37322d; color:#fffdf9; }
html[data-palette="dark"] .custom-select-option, html[data-palette="dark"] .custom-option { color:#f6f4f1 !important; }
html[data-palette="dark"] .custom-select-option:hover,
html[data-palette="dark"] .custom-select-option.selected,
html[data-palette="dark"] .custom-option:hover,
html[data-palette="dark"] .custom-option:focus-visible,
html[data-palette="dark"] .key-search-option:hover,
html[data-palette="dark"] .key-search-option:focus-visible { background:#37322d !important; color:#fffdf9 !important; }
html[data-palette="dark"] .key-search-option { color:#f6f4f1 !important; }""", """\
html[data-palette="dark"] .custom-select-panel,
html[data-palette="dark"] .custom-date-panel,
html[data-palette="dark"] .custom-time-panel,
html[data-palette="dark"] .key-search-panel { background:#1b1f2a !important; border-color:rgba(255,255,255,.12) !important; }
html[data-palette="light"] .custom-time-col { background:#f2f7fd; }
html[data-palette="dark"] .custom-time-col { background:#12161f; }
html[data-palette="dark"] .custom-time-option { color:#e5e5e5; }
html[data-palette="dark"] .custom-time-option:hover, html[data-palette="dark"] .custom-time-option:focus-visible { background:#2b3242; color:#ffffff; }
html[data-palette="dark"] .custom-select-option, html[data-palette="dark"] .custom-option { color:#e5e5e5 !important; }
html[data-palette="dark"] .custom-select-option:hover,
html[data-palette="dark"] .custom-option:hover,
html[data-palette="dark"] .custom-option:focus-visible,
html[data-palette="dark"] .key-search-option:hover,
html[data-palette="dark"] .key-search-option:focus-visible { background:#2b3242 !important; color:#ffffff !important; }
html[data-palette="dark"] .custom-select-option.selected, html[data-palette="dark"] .custom-option.selected { background:rgba(96,165,250,.18) !important; color:#93c5fd !important; }
html[data-palette="dark"] .key-search-option { color:#e5e5e5 !important; }""")
sr("pal-badge-d", """\
html[data-palette="dark"] .badge, html[data-palette="dark"] .model-chip, html[data-palette="dark"] .quota-bar { background:#2b2824; border-color:#48423b; color:var(--text); }
html[data-palette="dark"] .badge.ok, html[data-palette="dark"] .model-chip.all, html[data-palette="dark"] .token-limit-chip { background:#203b30; border-color:#35614f; color:#94dfbb; }""", """\
html[data-palette="dark"] .badge, html[data-palette="dark"] .model-chip, html[data-palette="dark"] .quota-bar { background:#232836; border-color:rgba(255,255,255,.1); color:var(--text); }
html[data-palette="dark"] .badge.ok { background:rgba(74,222,128,.14); border-color:rgba(74,222,128,.35); color:#4ade80; }
html[data-palette="dark"] .model-chip.all, html[data-palette="dark"] .token-limit-chip { background:rgba(96,165,250,.16); border-color:rgba(96,165,250,.4); color:#93c5fd; }""")
sr("pal-tlfb", """\
html[data-palette="light"] .token-limit-fallback { background:#fffdf9; }
html[data-palette="light"] .token-limit-fallback.is-disabled { border-color:#e4cfc8; background:#fff8f6; }
html[data-palette="light"] .token-limit-mode { background:#eeece6; border-color:#d8d4cc; }
html[data-palette="light"] .token-limit-mode button { color:#57524c; }
html[data-palette="light"] .token-limit-mode button.active { background:#fff; color:#2d2a26; }
html[data-palette="light"] .key-expiry-copy strong, html[data-palette="light"] .key-expiry-copy span { color:#756e66; }
html[data-palette="dark"] .token-limit-fallback { background:#25221f; }
html[data-palette="dark"] .token-limit-fallback.is-disabled { border-color:#5a3d38; background:#2a221f; }
html[data-palette="dark"] .token-limit-row { border-color:#3a3530; background:#1d1b18; box-shadow:inset 3px 0 0 #58be91; }
html[data-palette="dark"] .token-limit-mode { background:#282521; border-color:#49433c; }
html[data-palette="dark"] .token-limit-mode button { color:#c8c0b6; }
html[data-palette="dark"] .token-limit-mode button.active { background:#3a3530; color:#fffdf9; }
html[data-palette="dark"] .key-expiry-copy strong, html[data-palette="dark"] .key-expiry-copy span { color:#b9b1a7; }
html[data-palette="dark"] .key-expiry-field.is-expired .key-expiry-copy span { color:#ee9088; }
html[data-palette="dark"] .key-expiry-field.is-soon .key-expiry-copy span { color:#f0c56b; }
html[data-palette="dark"] .token-limit-panel { background:#25221f !important; border-color:#4a443c !important; }
html[data-palette="dark"] .badge.bad, html[data-palette="dark"] .btn.danger { background:#422522; border-color:#70413b; color:#ffb5aa; }
html[data-palette="dark"] .badge.warn { background:#44341e; border-color:#70582f; color:#f4ca80; }""", """\
html[data-palette="light"] .token-limit-fallback { background:rgba(255,255,255,.62); }
html[data-palette="light"] .token-limit-fallback.is-disabled { border-color:rgba(239,68,68,.3); background:#fef2f2; }
html[data-palette="light"] .token-limit-mode { background:#e7edf6; border-color:var(--line); }
html[data-palette="light"] .token-limit-mode button { color:#475569; }
html[data-palette="light"] .token-limit-mode button.active { background:#fff; color:#2563eb; }
html[data-palette="light"] .key-expiry-copy strong, html[data-palette="light"] .key-expiry-copy span { color:#5f6c7b; }
html[data-palette="dark"] .token-limit-fallback { background:#1b1f2a; }
html[data-palette="dark"] .token-limit-fallback.is-disabled { border-color:#5f3a3f; background:#2a1f26; }
html[data-palette="dark"] .token-limit-row { border-color:rgba(255,255,255,.08); background:#181c28; box-shadow:inset 3px 0 0 #60a5fa; }
html[data-palette="dark"] .token-limit-mode { background:#141824; border-color:rgba(255,255,255,.1); }
html[data-palette="dark"] .token-limit-mode button { color:#a3a3a3; }
html[data-palette="dark"] .token-limit-mode button.active { background:#232836; color:#93c5fd; }
html[data-palette="dark"] .key-expiry-copy strong, html[data-palette="dark"] .key-expiry-copy span { color:#a3a3a3; }
html[data-palette="dark"] .key-expiry-field.is-expired .key-expiry-copy span { color:#f87171; }
html[data-palette="dark"] .key-expiry-field.is-soon .key-expiry-copy span { color:#fbbf24; }
html[data-palette="dark"] .token-limit-panel { background:#1b1f2a !important; border-color:rgba(255,255,255,.12) !important; }
html[data-palette="dark"] .badge.bad, html[data-palette="dark"] .btn.danger { background:rgba(248,113,113,.12); border-color:rgba(248,113,113,.4); color:#f87171; }
html[data-palette="dark"] .badge.warn { background:rgba(245,158,11,.14); border-color:rgba(245,158,11,.4); color:#fbbf24; }""")
sr("pal-ksw", """\
html[data-palette="light"] .key-switch-ui { background:#d8d4cc; }
html[data-palette="light"] .key-switch input:checked + .key-switch-ui { background:#817b73; }
html[data-palette="dark"] .key-switch-ui { background:#49433c; }
html[data-palette="dark"] .key-switch input:checked + .key-switch-ui { background:#58be91; }
html[data-palette="dark"] .empty-state { background:linear-gradient(135deg, #24211e, #1c1a17); border-color:#49433c; }
html[data-palette="dark"] .chart-empty-icon { background:#2a2723; border-color:#49433c; color:#b9b1a7; }
html[data-palette="light"] .chart-empty-icon { background:#eeece6; border-color:#d8d4cc; color:#756e66; }""", """\
html[data-palette="light"] .key-switch-ui { background:#d5dcea; }
html[data-palette="light"] .key-switch input:checked + .key-switch-ui { background:#3b82f6; }
html[data-palette="dark"] .key-switch-ui { background:#3a4358; }
html[data-palette="dark"] .key-switch input:checked + .key-switch-ui { background:#60a5fa; }
html[data-palette="dark"] .empty-state { background:linear-gradient(135deg, #1a1f2e, #12161f); border-color:rgba(255,255,255,.1); }
html[data-palette="dark"] .chart-empty-icon { background:rgba(96,165,250,.14); border-color:rgba(96,165,250,.3); color:#93c5fd; }
html[data-palette="light"] .chart-empty-icon { background:var(--accent-soft); border-color:rgba(59,130,246,.28); color:var(--accent); }""")
sr("pal-trend", """\
html[data-palette="light"] .trend-metric { background:#f6f4ee; border-color:#e3e1db; }
html[data-palette="dark"] .trend-metric { background:#24211e; border-color:#3a3530; }
html[data-palette="dark"] .trend-metric:hover { border-color:#5a534b; background:#2d2925; }
html[data-palette="light"] .share-legend-item:hover, html[data-palette="light"] .share-legend-item:focus-visible { background:#f4f1eb; border-color:#e3e1db; }
html[data-palette="dark"] .share-legend-item:hover, html[data-palette="dark"] .share-legend-item:focus-visible { background:#2d2925; border-color:#49433c; }
html[data-palette="light"] .model-rank-item { background:linear-gradient(180deg, #fffdf9, #f6f4ee); border-color:#e3e1db; }
html[data-palette="light"] .model-rank-item:hover, html[data-palette="light"] .model-rank-item:focus-visible { background:#f4f1eb; border-color:#d8d3ca; }
html[data-palette="light"] .model-rank-bar { background:#ece8e1; }
html[data-palette="dark"] .model-rank-item { background:linear-gradient(180deg, #26231f, #1d1b18); border-color:#49433c; }
html[data-palette="dark"] .model-rank-item:hover, html[data-palette="dark"] .model-rank-item:focus-visible { background:#2d2925; border-color:#5a534b; }
html[data-palette="dark"] .model-rank-bar { background:#3a3530; }""", """\
html[data-palette="light"] .trend-metric { background:rgba(255,255,255,.62); border-color:var(--line); }
html[data-palette="dark"] .trend-metric { background:rgba(255,255,255,.08); border-color:rgba(255,255,255,.08); }
html[data-palette="dark"] .trend-metric:hover { border-color:rgba(96,165,250,.4); background:rgba(255,255,255,.12); }
html[data-palette="light"] .share-legend-item:hover, html[data-palette="light"] .share-legend-item:focus-visible { background:rgba(59,130,246,.06); border-color:var(--line); }
html[data-palette="dark"] .share-legend-item:hover, html[data-palette="dark"] .share-legend-item:focus-visible { background:rgba(255,255,255,.06); border-color:rgba(255,255,255,.12); }
html[data-palette="light"] .model-rank-item { background:linear-gradient(180deg, rgba(255,255,255,.9), rgba(255,255,255,.62)); border-color:var(--line); }
html[data-palette="light"] .model-rank-item:hover, html[data-palette="light"] .model-rank-item:focus-visible { background:#ffffff; border-color:rgba(59,130,246,.4); }
html[data-palette="light"] .model-rank-bar { background:#e8eef5; }
html[data-palette="dark"] .model-rank-item { background:linear-gradient(180deg, #202636, #181c28); border-color:rgba(255,255,255,.08); }
html[data-palette="dark"] .model-rank-item:hover, html[data-palette="dark"] .model-rank-item:focus-visible { background:#232836; border-color:rgba(96,165,250,.4); }
html[data-palette="dark"] .model-rank-bar { background:#232836; }""")
sr("pal-reset-d", """\
html[data-palette="dark"] .reset-spend-scope input:checked + .reset-spend-scope-card .reset-spend-scope-mark { border-color:#7fe0bd; background:#7fe0bd; }
html[data-palette="dark"] .reset-spend-scope input:checked + .reset-spend-scope-card .reset-spend-scope-mark::after { border-color:#173328; }
html[data-palette="dark"] .reset-spend-note-icon { background:rgba(126,224,189,.14); color:#7fe0bd; }""", """\
html[data-palette="dark"] .reset-spend-scope input:checked + .reset-spend-scope-card .reset-spend-scope-mark { border-color:#60a5fa; background:#60a5fa; }
html[data-palette="dark"] .reset-spend-scope input:checked + .reset-spend-scope-card .reset-spend-scope-mark::after { border-color:#0b1526; }
html[data-palette="dark"] .reset-spend-note-icon { background:rgba(96,165,250,.14); color:#93c5fd; }""")

sr("pal-batch-icon", 'html[data-palette="dark"] .auth-quota-batch-confirm-icon { background:rgba(126,224,189,.14); color:#7fe0bd; }',
   'html[data-palette="dark"] .auth-quota-batch-confirm-icon { background:rgba(96,165,250,.14); color:#93c5fd; }')

sr("pal-rowact-d", """\
html[data-palette="dark"] .row-actions { border-color:#48423b; background:#24211e; }
html[data-palette="dark"] .row-actions .btn + .btn { border-left-color:#48423b; }
html[data-palette="dark"] .row-actions .btn.soft,
html[data-palette="dark"] .row-actions .btn.primary { color:#7fe0bd; }
html[data-palette="dark"] .row-actions .btn.soft:hover,
html[data-palette="dark"] .row-actions .btn.primary:hover { background:rgba(126,224,189,.12); }
html[data-palette="dark"] .row-actions .btn.danger:hover { background:#422522; }
html[data-palette="dark"] .keys-table tbody tr.is-selected td { background:rgba(126,224,189,.1); }
html[data-palette="dark"] .key-select-ui { border-color:#5c665f; background:#25221f; }
html[data-palette="dark"] .key-select input:checked + .key-select-ui { border-color:#7fe0bd; background:#7fe0bd; }
html[data-palette="dark"] .key-select input:checked + .key-select-ui::after { border-color:#173328; }
html[data-palette="dark"] .key-select input:indeterminate + .key-select-ui { border-color:#7fe0bd; background:rgba(126,224,189,.14); }
html[data-palette="dark"] .key-select input:indeterminate + .key-select-ui::after { background:#7fe0bd; }""", """\
html[data-palette="dark"] .row-actions { border-color:rgba(255,255,255,.1); background:#1b1f2a; }
html[data-palette="dark"] .row-actions .btn + .btn { border-left-color:rgba(255,255,255,.1); }
html[data-palette="dark"] .row-actions .btn.soft,
html[data-palette="dark"] .row-actions .btn.primary { color:#93c5fd; }
html[data-palette="dark"] .row-actions .btn.soft:hover,
html[data-palette="dark"] .row-actions .btn.primary:hover { background:rgba(96,165,250,.14); }
html[data-palette="dark"] .row-actions .btn.danger:hover { background:rgba(248,113,113,.14); }
html[data-palette="dark"] .keys-table tbody tr.is-selected td { background:rgba(96,165,250,.12); }
html[data-palette="dark"] .key-select-ui { border-color:#47536b; background:#1b1f2a; }
html[data-palette="dark"] .key-select input:checked + .key-select-ui { border-color:#60a5fa; background:#60a5fa; }
html[data-palette="dark"] .key-select input:checked + .key-select-ui::after { border-color:#0b1526; }
html[data-palette="dark"] .key-select input:indeterminate + .key-select-ui { border-color:#60a5fa; background:rgba(96,165,250,.16); }
html[data-palette="dark"] .key-select input:indeterminate + .key-select-ui::after { background:#60a5fa; }""")

sr("pal-listsearch", """\
html[data-palette="dark"] .list-search { border-color:#48423b; background:#25221f; }
html[data-palette="dark"] .list-search:hover, html[data-palette="dark"] .list-search:focus-within { border-color:#5d896f; background:#2b2824; }""", """\
html[data-palette="dark"] .list-search { border-color:rgba(255,255,255,.1); background:rgba(255,255,255,.08); }
html[data-palette="dark"] .list-search:hover, html[data-palette="dark"] .list-search:focus-within { border-color:rgba(96,165,250,.45); background:#1b1f2a; }""")

sr("pal-tabs-d", """\
html[data-palette="dark"] .tabs { border-color:#48423b; background:rgba(30,29,27,.6); box-shadow:none; }
html[data-palette="dark"] .tab { color:#a49d92; }
html[data-palette="dark"] .tab:hover { background:rgba(126,224,189,.08); color:#e8ece9; }
html[data-palette="dark"] .tab.active { background:#24211e; color:#7fe0bd; box-shadow:0 2px 8px rgba(0,0,0,.3), 0 0 0 1px rgba(126,224,189,.24) inset; }""", """\
html[data-palette="dark"] .tabs { border-color:rgba(255,255,255,.1); background:rgba(24,28,40,.72); box-shadow:none; }
html[data-palette="dark"] .tab { color:#a3a3a3; }
html[data-palette="dark"] .tab:hover { background:rgba(96,165,250,.1); color:#e5e5e5; }
html[data-palette="dark"] .tab.active { background:rgba(96,165,250,.16); color:#93c5fd; box-shadow:0 2px 8px rgba(0,0,0,.3), 0 0 0 1px rgba(96,165,250,.3) inset; }""")

sr("pal-heading-d", """\
html[data-palette="dark"] .heading-icon { background:rgba(126,224,189,.14); color:#7fe0bd; }
html[data-palette="dark"] .heading-icon.danger { background:rgba(217,92,81,.22); color:#ffb5aa; }""", """\
html[data-palette="dark"] .heading-icon { background:rgba(96,165,250,.14); color:#93c5fd; }
html[data-palette="dark"] .heading-icon.danger { background:rgba(248,113,113,.2); color:#f87171; }""")

sr("pal-staticon-d", """\
html[data-palette="dark"] .stat { border-color:#48423b; }
html[data-palette="dark"] .stat-icon { background:rgba(126,224,189,.14); color:#7fe0bd; }
html[data-palette="dark"] .stat:nth-child(2n) .stat-icon { background:rgba(121,104,238,.2); color:#b7aefe; }
html[data-palette="dark"] .stat:nth-child(3n) .stat-icon { background:rgba(229,161,45,.18); color:#ecc06a; }""", """\
html[data-palette="dark"] .stat { border-color:rgba(255,255,255,.1); }
html[data-palette="dark"] .stat-icon { background:rgba(96,165,250,.14); color:#93c5fd; }
html[data-palette="dark"] .stat:nth-child(2n) .stat-icon { background:rgba(147,197,253,.16); color:#93c5fd; }
html[data-palette="dark"] .stat:nth-child(3n) .stat-icon { background:rgba(245,158,11,.18); color:#fbbf24; }""")

sr("pal-emptyicon-d", 'html[data-palette="dark"] .empty-state .empty-icon, html[data-palette="dark"] .chart-empty-icon { background:rgba(126,224,189,.13); color:#7fe0bd; }',
   'html[data-palette="dark"] .empty-state .empty-icon, html[data-palette="dark"] .chart-empty-icon { background:rgba(96,165,250,.14); color:#93c5fd; }')
sr("pal-modalclose-d", 'html[data-palette="dark"] .modal-close:hover { background:rgba(126,224,189,.12); color:#7fe0bd; }',
   'html[data-palette="dark"] .modal-close:hover { background:rgba(96,165,250,.14); color:#93c5fd; }')

sr("pal-warmup-d", """\
html[data-palette="dark"] .auth-warmup-task, html[data-palette="dark"] .auth-warmup-advanced { border-color:#48423b; background:#1d1b18; box-shadow:none; }
html[data-palette="dark"] .auth-warmup-task.is-disabled { border-color:#4d514d; background:#1b1d1b; }
html[data-palette="dark"] .auth-warmup-empty { border-color:#4b5c52; background:#202a24; }
html[data-palette="light"] .auth-warmup-task-toggle i { background:#d8d4cc; }
html[data-palette="dark"] .auth-warmup-task-toggle i { background:#5a534c; box-shadow:none; }
html[data-palette="dark"] .auth-warmup-task .icon-btn { background:#25221f; color:#c8c0b6; }
html[data-palette="dark"] .auth-warmup-task .icon-btn:hover { background:#3e2825; }
html[data-palette="dark"] .auth-warmup-settings-footer { border-color:#48423b; background:color-mix(in srgb, #1d1b18 72%, var(--panel)); }
html[data-palette="dark"] .auth-warmup-settings-footer .btn.ghost { background:#25221f; }""", """\
html[data-palette="dark"] .auth-warmup-task, html[data-palette="dark"] .auth-warmup-advanced { border-color:rgba(255,255,255,.1); background:#181c28; box-shadow:none; }
html[data-palette="dark"] .auth-warmup-task.is-disabled { border-color:#39445c; background:#151a28; }
html[data-palette="dark"] .auth-warmup-empty { border-color:rgba(96,165,250,.35); background:#16202f; }
html[data-palette="light"] .auth-warmup-task-toggle i { background:#d5dcea; }
html[data-palette="dark"] .auth-warmup-task-toggle i { background:#3a4358; box-shadow:none; }
html[data-palette="dark"] .auth-warmup-task .icon-btn { background:#1b1f2a; color:#a3a3a3; }
html[data-palette="dark"] .auth-warmup-task .icon-btn:hover { background:#3a2530; }
html[data-palette="dark"] .auth-warmup-settings-footer { border-color:rgba(255,255,255,.1); background:color-mix(in srgb, #181c28 72%, var(--panel)); }
html[data-palette="dark"] .auth-warmup-settings-footer .btn.ghost { background:#1b1f2a; }""")

sr("pal-quota-d", """\
html[data-palette="dark"] .auth-quota-card { background:#24211e; box-shadow:0 10px 24px rgba(0,0,0,.18); }
html[data-palette="dark"] .auth-quota-cost { border-color:#48423b; background:#1d1b18; }
html[data-palette="dark"] .auth-quota-window-grid { background:linear-gradient(180deg, rgba(21,20,18,.5), rgba(21,20,18,.28)); }
html[data-palette="dark"] .auth-quota-group { border-color:#48423b; background:#24211e; box-shadow:none; }
html[data-palette="dark"] .auth-quota-window-card { border-color:#48423b; background:#24211e; box-shadow:none; }
html[data-palette="dark"] .auth-quota-window-card:hover { border-color:#6c8979; box-shadow:0 8px 16px rgba(0,0,0,.22); }
html[data-palette="dark"] .auth-quota-bar { background:#3a403b; }
html[data-palette="dark"] .auth-quota-bar.unknown { --quota-color:#5a635d; }
html[data-palette="dark"] .auth-quota-error { border-color:#70413b; background:#422522; color:#ffb5aa; }
html[data-palette="dark"] .auth-quota-period-trigger { border-color:#4b5c52; background:linear-gradient(180deg, #272b28, #222622); color:#e8ece9; box-shadow:none; }
html[data-palette="dark"] .auth-quota-period-trigger:hover, html[data-palette="dark"] .auth-quota-period-picker.is-open .auth-quota-period-trigger { border-color:#629a82; background:#29362f; }
html[data-palette="dark"] .auth-quota-period-menu { border-color:#4b5c52; background:rgba(34,38,35,.98); box-shadow:0 14px 30px rgba(0,0,0,.38); }
html[data-palette="dark"] .auth-quota-period-option { color:#e8ece9; }
html[data-palette="dark"] .auth-quota-period-option:hover, html[data-palette="dark"] .auth-quota-period-option:focus-visible { background:#2b3931; }
html[data-palette="dark"] .auth-quota-period-option.is-selected { background:#294738; color:#9be5c5; }
html[data-palette="dark"] .auth-quota-period-chevron { color:#aabbb1; }
html[data-palette="dark"] .auth-quota-period-option::before { background:#5a6b61; }
html[data-palette="dark"] .auth-quota-period-option.is-partial::before { background:repeating-linear-gradient(to bottom, #dfad53 0 3px, transparent 3px 5px); }
html[data-palette="dark"] .auth-quota-period-option.is-partial .auth-quota-period-option-mark { background:#dfad53; }""", """\
html[data-palette="dark"] .auth-quota-card { background:#181c28; box-shadow:0 10px 24px rgba(0,0,0,.24); }
html[data-palette="dark"] .auth-quota-cost { border-color:rgba(255,255,255,.1); background:#12161f; }
html[data-palette="dark"] .auth-quota-window-grid { background:linear-gradient(180deg, rgba(13,17,28,.5), rgba(13,17,28,.28)); }
html[data-palette="dark"] .auth-quota-group { border-color:rgba(255,255,255,.1); background:#1b1f2a; box-shadow:none; }
html[data-palette="dark"] .auth-quota-window-card { border-color:rgba(255,255,255,.1); background:#1b1f2a; box-shadow:none; }
html[data-palette="dark"] .auth-quota-window-card:hover { border-color:rgba(96,165,250,.45); box-shadow:0 8px 16px rgba(0,0,0,.28); }
html[data-palette="dark"] .auth-quota-bar { background:#232836; }
html[data-palette="dark"] .auth-quota-bar.unknown { --quota-color:#4b5563; }
html[data-palette="dark"] .auth-quota-error { border-color:rgba(248,113,113,.4); background:rgba(248,113,113,.12); color:#f87171; }
html[data-palette="dark"] .auth-quota-period-trigger { border-color:rgba(255,255,255,.1); background:linear-gradient(180deg, #1b1f2a, #161b27); color:#e5e5e5; box-shadow:none; }
html[data-palette="dark"] .auth-quota-period-trigger:hover, html[data-palette="dark"] .auth-quota-period-picker.is-open .auth-quota-period-trigger { border-color:rgba(96,165,250,.45); background:#232e45; }
html[data-palette="dark"] .auth-quota-period-menu { border-color:rgba(255,255,255,.1); background:rgba(24,28,40,.96); box-shadow:0 14px 30px rgba(0,0,0,.38); }
html[data-palette="dark"] .auth-quota-period-option { color:#e5e5e5; }
html[data-palette="dark"] .auth-quota-period-option:hover, html[data-palette="dark"] .auth-quota-period-option:focus-visible { background:#232e45; }
html[data-palette="dark"] .auth-quota-period-option.is-selected { background:rgba(96,165,250,.16); color:#93c5fd; }
html[data-palette="dark"] .auth-quota-period-chevron { color:#8b9bb4; }
html[data-palette="dark"] .auth-quota-period-option::before { background:#3a4358; }
html[data-palette="dark"] .auth-quota-period-option.is-partial::before { background:repeating-linear-gradient(to bottom, #f59e0b 0 3px, transparent 3px 5px); }
html[data-palette="dark"] .auth-quota-period-option.is-partial .auth-quota-period-option-mark { background:#f59e0b; }""")

sr("pal-period-pill", 'html[data-palette="dark"] .auth-quota-period { border-color:#4a5c52; background:#24302a; color:#9dc4b2; }',
   'html[data-palette="dark"] .auth-quota-period { border-color:rgba(96,165,250,.3); background:rgba(96,165,250,.12); color:#93c5fd; }')

sr("pal-routing", """\
html[data-palette="dark"] .auth-routing-list { background:#25221f; }
html[data-palette="dark"] .auth-routing-control { background:#2b2824; }""", """\
html[data-palette="dark"] .auth-routing-list { background:#1b1f2a; }
html[data-palette="dark"] .auth-routing-control { background:#232836; }""")

sr("pal-pagination-d", 'html[data-palette="dark"] .usage-pagination { border-color:#48423b; background:rgba(30,29,27,.6); }',
   'html[data-palette="dark"] .usage-pagination { border-color:rgba(255,255,255,.1); background:rgba(24,28,40,.72); }')
sr("pal-flash-d", 'html[data-palette="dark"] .flash { background:rgba(29,27,24,.88); }',
   'html[data-palette="dark"] .flash { background:rgba(24,28,40,.9); }')
sr("pal-mats-d", """\
html[data-palette="dark"] .tabs,
html[data-palette="dark"] .usage-pagination,
html[data-palette="dark"] .unit-switch {
  background:rgba(30,29,27,.72);""", """\
html[data-palette="dark"] .tabs,
html[data-palette="dark"] .usage-pagination,
html[data-palette="dark"] .unit-switch {
  background:rgba(24,28,40,.72);""")
sr("pal-provider-d", """\
html[data-palette="dark"] .auth-quota-provider-icon { background:#2a2723; color:#f6f4f1; }
html[data-palette="dark"] .auth-quota-card[data-provider="codex"] .auth-quota-provider-icon,
html[data-palette="dark"] .auth-quota-card[data-provider="kimi"] .auth-quota-provider-icon { background:#fff; }
html[data-palette="dark"] .auth-quota-card[data-provider="xai"] .auth-quota-provider-icon { background:#3a3530; color:#f6f4f1; }
html[data-palette="dark"] .auth-quota-card[data-provider="claude"] .auth-quota-provider-icon { background:#3a2e28; }
html[data-palette="dark"] .auth-quota-card[data-provider="antigravity"] .auth-quota-provider-icon { background:#243044; color:#7ab4ff; }
html[data-palette="dark"] .auth-quota-week-icon { color:#9aa89f; }""", """\
html[data-palette="dark"] .auth-quota-provider-icon { background:#232836; color:#e5e5e5; }
html[data-palette="dark"] .auth-quota-card[data-provider="codex"] .auth-quota-provider-icon,
html[data-palette="dark"] .auth-quota-card[data-provider="kimi"] .auth-quota-provider-icon { background:#fff; }
html[data-palette="dark"] .auth-quota-card[data-provider="xai"] .auth-quota-provider-icon { background:#2c3547; color:#e5e5e5; }
html[data-palette="dark"] .auth-quota-card[data-provider="claude"] .auth-quota-provider-icon { background:#3a2e28; }
html[data-palette="dark"] .auth-quota-card[data-provider="antigravity"] .auth-quota-provider-icon { background:#243044; color:#7ab4ff; }
html[data-palette="dark"] .auth-quota-week-icon { color:#94a3b8; }""")
sr("pal-eyebrow", """\
html[data-palette="light"] .eyebrow { color:#6a655e; }
html[data-palette="dark"] .eyebrow { color:#9ae8c9; }""", """\
html[data-palette="light"] .eyebrow { color:#2563eb; }
html[data-palette="dark"] .eyebrow { color:#93c5fd; }""")

# ============================================================
# 4. COLOR DICTIONARY SWEEP (exact substrings, order matters)
# ============================================================
print("== dictionary sweep ==")
D = [
  # mint / green accents -> blue
  ("#087d5a", "var(--accent)"),
  ("#1eb787", "#3b82f6"),
  ("#14a879", "#2563eb"),
  ("#27c692", "#60a5fa"),
  ("#63d4ad", "#93c5fd"),
  ("#76d7b8", "var(--accent)"),
  ("#7fe0bd", "#93c5fd"),
  ("#76dfbc", "#93c5fd"),
  ("#4cc59b", "#60a5fa"),
  ("#74cfae", "#60a5fa"),
  ("#a9dfc8", "#93c5fd"),
  ("#a9d9c4", "#93c5fd"),
  ("#8acfb0", "#93c5fd"),
  ("#bfe9d7", "#bfdbfe"),
  ("#c8eddd", "#bfdbfe"),
  ("#d3eee3", "#bfdbfe"),
  ("#ccebdd", "#bfdbfe"),
  ("#bce9d5", "#bfdbfe"),
  ("#b4e5d2", "#93c5fd"),
  ("#e4f7ef", "#eff6ff"),
  ("#eaf8f1", "#eff6ff"),
  ("#eaf8f0", "#eff6ff"),
  ("#eff9f4", "#eff6ff"),
  ("#f1faf5", "#f6faff"),
  ("#f1f8f4", "#f6faff"),
  ("#f4fbf7", "#f6faff"),
  ("#f4faf6", "#f6faff"),
  ("#f6fcf8", "#f6faff"),
  ("#f7fcf9", "#f6faff"),
  ("#f7fbf8", "#f6faff"),
  ("#f6fbf8", "#f6faff"),
  ("#fafdfb", "#f7faff"),
  ("#f7faf7", "#f7faff"),
  ("#fbfdfb", "#f7faff"),
  ("#f6faf7", "#f7faff"),
  ("#fcfdfb", "#f7faff"),
  ("#d7f3e7", "#dbeafe"),
  ("#dbe7df", "#d8e5f2"),
  ("#dce7de", "#d8e5f2"),
  ("#cfe7da", "#d8e5f2"),
  ("#cfe1d6", "#d8e5f2"),
  ("#d7e8de", "#d8e5f2"),
  ("#d7e4dc", "#d8e5f2"),
  ("#d2e2d7", "#d8e5f2"),
  ("#e3eee7", "#d8e5f2"),
  ("#dff0e8", "#d8e5f2"),
  ("#e8eee8", "#e2eaf3"),
  ("#e5ece6", "#e2eaf3"),
  ("#edf2ee", "#e8eef5"),
  ("#e8efea", "#e8eef5"),
  ("#edf1ed", "#e8eef5"),
  ("#e8ece6", "#e8eef5"),
  ("#e8ece9", "#e5e5e5"),
  ("#d8e0da", "#d8e0ea"),
  ("#d7e8de", "#d8e5f2"),
  ("#d5e0d9", "#cbd5e1"),
  ("#c9d5cc", "#cbd5e1"),
  ("#c9d4cb", "#cbd5e1"),
  ("#cbd5cc", "#cbd5e1"),
  ("#c8d5cc", "#cbd5e1"),
  ("#c8d6cb", "#cbd5e1"),
  ("#bdc9c0", "#b9c6d8"),
  ("#c9d0cc", "#cbd5e1"),
  ("#c5cfc8", "#cbd5e1"),
  ("#c2cbc3", "#cbd5e1"),
  ("#c1c9c3", "#b6c2d1"),
  ("#cfd8d2", "#d5dcea"),
  ("#b8cbc0", "#b9c6d8"),
  ("#a9b8ad", "#a9b8cf"),
  ("#98a69d", "#94a3b8"),
  ("#8c9991", "#94a3b8"),
  ("#7b887f", "#64748b"),
  ("#6d8174", "#64748b"),
  ("#65746a", "#5f6c7b"),
  ("#5e6b62", "#64748b"),
  ("#567064", "#64748b"),
  ("#5f6a61", "#5f6c7b"),
  ("#4f5b53", "#5f6c7b"),
  ("#4d5a51", "#475569"),
  ("#4a6759", "#475569"),
  ("#4a564e", "#475569"),
  ("#3f6554", "#475569"),
  ("#3d4a42", "#334155"),
  ("#26342b", "#334155"),
  ("#1f2922", "#2c3e50"),
  ("#1a1f1c", "#2c3e50"),
  ("#3f6b56", "#2563eb"),
  ("#146b4d", "#166534"),
  ("#087b57", "#2563eb"),
  ("#0b7d5c", "var(--accent)"),
  # purple accents -> blue
  ("#7968ee", "#60a5fa"),
  ("#efedff", "#eff6ff"),
  ("#f0edfa", "#eff6ff"),
  ("#eeebf5", "#eff6ff"),
  ("#5f4fd0", "#3b82f6"),
  ("#8573bd", "#60a5fa"),
  ("#8274c9", "#60a5fa"),
  ("#b5a5e9", "#93c5fd"),
  ("#b7aefe", "#93c5fd"),
  # reds -> spec danger
  ("#bd443b", "#ef4444"),
  ("#9d3b33", "#ef4444"),
  ("#b14b43", "#ef4444"),
  ("#7d342d", "#dc2626"),
  ("#d95c51", "#ef4444"),
  ("#e07a6a", "#ef4444"),
  ("#c15b52", "#ef4444"),
  ("#c65746", "#ef4444"),
  ("#ef8779", "#f87171"),
  ("#ee9088", "#f87171"),
  ("#ffb5aa", "#f87171"),
  ("#f1d3cf", "#fecaca"),
  ("#f2d0cb", "#fecaca"),
  ("#f0d4d0", "#fecaca"),
  ("#ead7d3", "#fecaca"),
  ("#e4cfc8", "#fecaca"),
  ("#fff7f5", "#fef2f2"),
  ("#fff8f7", "#fef2f2"),
  ("#fff8f6", "#fef2f2"),
  ("#fff6f4", "#fef2f2"),
  ("#fff6f5", "#fef2f2"),
  ("#fff4f2", "#fef2f2"),
  ("#fdeceb", "#fee2e2"),
  ("#efd0cd", "#fecaca"),
  ("#422522", "#3a2530"),
  ("#70413b", "#5f3a3f"),
  ("#5a3d38", "#5f3a3f"),
  ("#3e2825", "#3a2530"),
  ("#2a221f", "#2a1f26"),
  # ambers -> spec warn
  ("#e5a12d", "#f59e0b"),
  ("#d8942b", "#f59e0b"),
  ("#dfad53", "#f59e0b"),
  ("#a66b07", "#b45309"),
  ("#9a6a1c", "#b45309"),
  ("#b57a10", "#b45309"),
  ("#a86f0e", "#b45309"),
  ("#b77b1d", "#b45309"),
  ("#f0c56b", "#fbbf24"),
  ("#ecc06a", "#fbbf24"),
  ("#f4ca80", "#fbbf24"),
  ("#efb860", "#fbbf24"),
  ("#fff8e9", "#fffbeb"),
  ("#fff2dc", "#fffbeb"),
  ("#f8eee3", "#fffbeb"),
  ("#f5dfaf", "#fde68a"),
  ("#44341e", "#453514"),
  ("#70582f", "#75601f"),
  # warm-light palette neutrals -> blue-white
  ("#fffdf9", "#ffffff"),
  ("#f6f4ee", "#f2f6fc"),
  ("#f6f4f1", "#e5e5e5"),
  ("#f0eee8", "#eff2f7"),
  ("#eeece6", "#e7edf6"),
  ("#f4f1eb", "#eaf0f8"),
  ("#f3f0e9", "#f2f7fd"),
  ("#ece8e1", "#e8eef5"),
  ("#ebe8e1", "#e7edf6"),
  ("#e3e1db", "#e2eaf3"),
  ("#e2dfd8", "#d8e5f2"),
  ("#d8d4cc", "#d8e0ea"),
  ("#d8d3ca", "#cbd5e1"),
  ("#f0ece6", "#e5e5e5"),
  ("#2d2a26", "#2c3e50"),
  ("#6d6760", "#5f6c7b"),
  ("#756e66", "#5f6c7b"),
  ("#57524c", "#475569"),
  ("#8b8680", "#94a3b8"),
  ("#817b73", "#64748b"),
  ("#6f675f", "#64748b"),
  ("#6a655e", "#64748b"),
  # warm-dark browns -> slate blue darks
  ("#151412", "#0a0a0a"),
  ("#1d1b18", "#181c28"),
  ("#1b1916", "#12161f"),
  ("#1c1a17", "#12161f"),
  ("#211e1b", "#131c30"),
  ("#26231f", "#202636"),
  ("#25221f", "#1b1f2a"),
  ("#282521", "#202636"),
  ("#2a2723", "#232836"),
  ("#2b2824", "#232836"),
  ("#2d2925", "#232836"),
  ("#302d29", "#232836"),
  ("#24211e", "#1b1f2a"),
  ("#37322d", "#2b3242"),
  ("#3a3530", "#2c3547"),
  ("#48423b", "#39445c"),
  ("#4a443c", "#39445c"),
  ("#49433c", "#39445c"),
  ("#5a534b", "#47536b"),
  ("#5a534c", "#47536b"),
  ("#504940", "#3a4460"),
  ("#39332d", "#26334f"),
  ("#36312d", "#26334f"),
  ("#312c40", "#26334f"),
  ("#797066", "#60a5fa"),
  ("#a49d92", "#a3a3a3"),
  ("#b9b1a7", "#a3a3a3"),
  ("#c8c0b6", "#a3a3a3"),
  ("#b6afa3", "#a3a3a3"),
  ("#c2bbb2", "#a3a3a3"),
  ("#b3aaa0", "#94a3b8"),
  ("#7a736b", "#8b9bb4"),
  ("#5f5f5f", "#5f6c7b"),
  ("#282828", "#2c3e50"),
  ("#242424", "#2c3e50"),
  ("#686868", "#5f6c7b"),
  ("#f7f7f7", "#f6faff"),
  ("#f8f8f8", "#f6faff"),
  ("#e6e6e6", "#dfe7f0"),
  # dark mint accents -> dark blue accents
  ("#58be91", "#60a5fa"),
  ("#4d9475", "#22c55e"),
  ("#168b63", "#22c55e"),
  ("#5c8776", "#5f6c7b"),
  ("#173328", "#0b1526"),
  ("#5c665f", "#47536b"),
  ("#5d896f", "#60a5fa"),
  ("#629a82", "#60a5fa"),
  ("#6c8979", "#60a5fa"),
  ("#4b5c52", "#39445c"),
  ("#4a5c52", "#39445c"),
  ("#4d514d", "#39445c"),
  ("#5a6b61", "#3a4358"),
  ("#203b30", "#1e2d4a"),
  ("#35614f", "#2f4a75"),
  ("#94dfbb", "#93c5fd"),
  ("#9be5c5", "#93c5fd"),
  ("#9ae8c9", "#93c5fd"),
  ("#9dc4b2", "#93c5fd"),
  ("#24302a", "#1e2d4a"),
  ("#202a24", "#16202f"),
  ("#29362f", "#232e45"),
  ("#2b3931", "#232e45"),
  ("#294738", "#1e2d4a"),
  ("#272b28", "#1b1f2a"),
  ("#222622", "#161b27"),
  ("#1b1d1b", "#151a28"),
  ("#aabbb1", "#8b9bb4"),
  ("#9aa89f", "#94a3b8"),
  ("#3a403b", "#232836"),
  ("#5a635d", "#4b5563"),
  ("#202421", "#1b2a4a"),
  ("#38463b", "#1d2b45"),
  ("#d2dbd3", "#c3d3e8"),
  ("#3d4540", "#334155"),
  # remaining greenish neutrals -> blue greys
  ("#e2e7e1", "#dfe7f0"),
  ("#e7ebe5", "#dfe7f0"),
  ("#edf0eb", "#e8eef5"),
  ("#f3f6f3", "#eef4fa"),
  ("#e4eae4", "#dfe7f0"),
  ("#e4ece6", "#dfe7f0"),
  ("#e2eae3", "#dfe7f0"),
  ("#f3f5f2", "#eef4fa"),
  ("#f5f7f5", "#eef4fa"),
  ("#f8faf8", "#f7faff"),
  ("#fafbfa", "#f7faff"),
  ("#fafcf9", "#f7faff"),
  ("#f7f9f6", "#f2f7fd"),
  ("#fafbf8", "#eff2f7"),
  ("#eef2ef", "#e8eef5"),
  ("#e4ebe6", "#dfe7f0"),
  ("#d7ddd6", "#cbd5e1"),
  ("#d5e8dc", "#bfdbfe"),
  ("#a4ada6", "#9aa7b8"),
  ("#e6ebe7", "#dfe7f0"),
  ("#eef1ef", "#e8eef5"),
  # svg-embedded greys
  ("%236d786f", "%235f6c7b"),
  ("%235f6a61", "%235f6c7b"),
  ("%23087d5a", "%233b82f6"),
]
for old, new in D:
    rep("dict", old, new)

# ============================================================
# 5. rgba() SWEEP — preserve alpha, swap hue
# ============================================================
print("== rgba sweep ==")
R = [
  (r"rgba\(30,\s*183,\s*135,", "rgba(59,130,246,"),
  (r"rgba\(126,\s*224,\s*189,", "rgba(96,165,250,"),
  (r"rgba\(121,\s*104,\s*238,", "rgba(96,165,250,"),
  (r"rgba\(217,\s*92,\s*81,", "rgba(239,68,68,"),
  (r"rgba\(224,\s*122,\s*106,", "rgba(239,68,68,"),
  (r"rgba\(229,\s*161,\s*45,", "rgba(245,158,11,"),
  (r"rgba\(179,\s*170,\s*160,", "rgba(96,165,250,"),
  (r"rgba\(90,\s*219,\s*176,", "rgba(122,162,255,"),
  (r"rgba\(181,\s*165,\s*233,", "rgba(96,165,250,"),
  (r"rgba\(148,\s*134,\s*119,", "rgba(96,165,250,"),
  (r"rgba\(139,\s*134,\s*128,", "rgba(122,162,255,"),
  (r"rgba\(133,\s*115,\s*189,", "rgba(96,165,250,"),
  (r"rgba\(41,\s*57,\s*46,", "rgba(15,23,42,"),
  (r"rgba\(29,\s*49,\s*37,", "rgba(15,23,42,"),
  (r"rgba\(21,\s*37,\s*26,", "rgba(15,23,42,"),
  (r"rgba\(28,\s*42,\s*33,", "rgba(15,23,42,"),
  (r"rgba\(35,\s*53,\s*42,", "rgba(15,23,42,"),
  (r"rgba\(32,\s*57,\s*42,", "rgba(15,23,42,"),
  (r"rgba\(27,\s*52,\s*38,", "rgba(15,23,42,"),
  (r"rgba\(16,\s*28,\s*22,", "rgba(15,23,42,"),
  (r"rgba\(18,\s*24,\s*21,", "rgba(15,23,42,"),
  (r"rgba\(24,\s*35,\s*28,", "rgba(15,23,42,"),
  (r"rgba\(30,\s*30,\s*30,", "rgba(15,23,42,"),
  (r"rgba\(70,\s*63,\s*55,", "rgba(15,23,42,"),
  (r"rgba\(29,\s*27,\s*24,", "rgba(24,28,40,"),
  (r"rgba\(30,\s*29,\s*27,", "rgba(24,28,40,"),
  (r"rgba\(34,\s*38,\s*35,", "rgba(24,28,40,"),
  (r"rgba\(21,\s*20,\s*18,", "rgba(13,17,28,"),
  (r"rgba\(247,\s*250,\s*247,", "rgba(246,250,255,"),
  (r"rgba\(255,\s*253,\s*249,", "rgba(255,255,255,"),
  (r"rgba\(38,\s*49,\s*61,", "rgba(15,23,42,"),
]
for pat, newp in R:
    s, n = re.subn(pat, newp, s)
    print(f"  {pat:<38} {n:>3}x -> {newp}")

# ============================================================
# 6. POST FIXUPS that must see swept values
# ============================================================
# Design-overhaul .tab.active: spec wants accent-soft bg + accent text.
sub1("tab-active2", ".tab.active { border:0; background:#fff; color:var(--accent); font-weight:700; box-shadow:0 2px 8px rgba(15,23,42,.08), 0 0 0 1px rgba(59,130,246,.28) inset; }",
     ".tab.active { border:0; background:var(--accent-soft); color:var(--accent); font-weight:700; box-shadow:0 0 0 1px rgba(59,130,246,.28) inset; }")

# ============================================================
# 7. AUDIT leftovers
# ============================================================
hexes = re.findall(r"#[0-9a-fA-F]{3,8}\b", s)
from collections import Counter
cnt = Counter(h.lower() for h in hexes)
print("\n== remaining hex colors ==")
for h, c in sorted(cnt.items(), key=lambda x: -x[1]):
    print(f"  {c:>3} {h}")
rgbas = re.findall(r"rgba?\([0-9., ]+\)", s)
cnt2 = Counter(rgbas)
print("\n== remaining rgba colors ==")
for h, c in sorted(cnt2.items(), key=lambda x: -x[1]):
    print(f"  {c:>3} {h}")

if fails:
    print("\n!! FAILURES:")
    for f in fails: print("  " + f)
    sys.exit(1)

open(P, "w", encoding="utf-8").write(s)
print(f"\nWrote {P}: {len(orig)} -> {len(s)} bytes")
