#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply the same color dictionary to console.js / lookup.* plus JS-specific rules."""
import re, sys

src = open('scripts/restyle/apply_console_css.py', encoding='utf-8').read()
# extract D = [...] and R = [...] blocks
d_blk = re.search(r'^D = \[.*?\n^\]', src, re.S | re.M).group(0)
r_blk = re.search(r'^R = \[.*?\n^\]', src, re.S | re.M).group(0)
ns = {}
exec(d_blk, ns); exec(r_blk, ns)
D = ns['D']; R = ns['R']

FILES = [
    'internal/management/web/console.js',
    'internal/management/web/lookup.css',
    'internal/management/web/lookup.js',
    'internal/management/web/lookup.html',
]

for p in FILES:
    s = open(p, encoding='utf-8').read()
    orig = s
    for old, new in D:
        s = s.replace(old, new)
    for pat, new in R:
        s = re.sub(pat, new, s)
    open(p, 'w', encoding='utf-8').write(s)
    print(p.split('/')[-1], 'dict done, delta', len(s) - len(orig))

# ---- console.js specific (per spec) ----
p = FILES[0]; s = open(p, encoding='utf-8').read()
JS_MAP = [
    ("'rgba(15, 23, 42, .94)'", "'rgba(15, 23, 42, .94)'"),  # tooltip bg already mapped
    ("'rgba(26, 31, 28, .94)'", "'rgba(15, 23, 42, .94)'"),
    ("#cdd6cf", "#cbd5e1"),
    ("#c56b82", "#f59e0b"),
    ("#9ea9a1", "#94a3b8"),
    ("#dce5de", "#d8e5f2"),
    ("#edf1ee", "#eef4fa"),
    ("'#f0f4f1'", "'rgba(59,130,246,.08)'"),
    ("'#e56b8a'", "'#ef4444'"),
    ("'#f0a04b'", "'#f59e0b'"),
    ("#31,41,34", "#15,23,42"),  # rgba shadow
    ("rgba(31, 41, 34,", "rgba(15, 23, 42,"),
    ("#f0f4f1", "#eef4fa"),
]
for old, new in JS_MAP:
    if old in s:
        print('  js map:', old, '->', new)
        s = s.replace(old, new)
# MODEL_SHARE_COLORS: find the array and report
m = re.search(r'MODEL_SHARE_COLORS\s*=\s*\[[^\]]*\]', s)
print('MODEL_SHARE_COLORS:', m.group(0) if m else 'not found')
if m:
    new_arr = ('MODEL_SHARE_COLORS = [\'#3b82f6\', \'#60a5fa\', \'#22c55e\', \'#f59e0b\', '
               '\'#93c5fd\', \'#38bdf8\', \'#a5b4fc\', \'#f87171\']')
    s = s[:m.start()] + new_arr + s[m.end():]
    print('  replaced ->', new_arr)
open(p, 'w', encoding='utf-8').write(s)

# ---- lookup.css :root token block + structural ----
p = FILES[1]; s = open(p, encoding='utf-8').read()
m = re.search(r':root\s*\{[^}]*\}', s)
print('lookup :root:', m.group(0)[:400] if m else 'not found')
if m:
    new_root = (':root { --bg:#eff2f7; --panel:rgba(255,255,255,.9); --ink:#2c3e50; '
        '--muted:#5f6c7b; --line:rgba(15,23,42,.08); --accent:#3b82f6; --accent-dark:#2563eb; '
        '--accent-soft:rgba(59,130,246,.12); --warn:#f59e0b; --danger:#ef4444; '
        'font-family:var(--cpamp-plugin-font-family, Inter, -apple-system,BlinkMacSystemFont,'
        '"Segoe UI","Noto Sans SC",system-ui,sans-serif); }')
    s = s[:m.start()] + new_root + s[m.end():]
open(p, 'w', encoding='utf-8').write(s)

# ---- residual audit ----
print('=== residuals ===')
import subprocess
bad = re.compile(r'1eb787|7968ee|14a879|7fe0bd|087d5a|bfe9d7|e4f7ef|dce5de|c8d5cc|fafbf8|f7f9f6|173328|30,183,135|76d7b8|27c692|63d4ad|14926b|087b57')
for p in FILES:
    s = open(p, encoding='utf-8').read()
    for i, line in enumerate(s.splitlines(), 1):
        for mm in bad.finditer(line):
            print(f'{p.split("/")[-1]}:{i}: {mm.group(0)}')
# list all remaining hex colors for review
print('=== remaining hex colors ===')
for p in FILES:
    s = open(p, encoding='utf-8').read()
    hexes = sorted(set(re.findall(r'#[0-9a-fA-F]{3,8}\b', s)))
    print(p.split('/')[-1], len(hexes), hexes)

# ---- post-hoc extra sweeps (match manual fixups after first pass) ----
EXTRA = {
    'internal/management/web/console.js': [
        ("#6a766e", "#5f6c7b"),
    ],
    'internal/management/web/lookup.js': [
        ("rgba(26,31,28,.94)", "rgba(15,23,42,.94)"),
        ("#6a766e", "#5f6c7b"),
        ("#9ea9a1", "#94a3b8"),
        ("#dce5de", "#d8e5f2"),
        ("#edf1ee", "#eef4fa"),
        ("#c56b82", "#f59e0b"),
        ("#f0f4f1", "rgba(59,130,246,.08)"),
        ("#e56b8a", "#ef4444"),
        ("#f0a04b", "#f59e0b"),
        ("#20c997", "#22c55e"),
        ("#4dabf7", "#60a5fa"),
        ("#ff922b", "#fbbf24"),
        ("#cc5de8", "#a5b4fc"),
    ],
    'internal/management/web/lookup.css': [
        ("#dce5de", "#d8e0ea"),
        ("#9ad7bf", "#93c5fd"),
        ("#e8f3ef", "#eff6ff"),
        ("#4a6f61", "#2563eb"),
        ("#f3f8f5", "#f6faff"),
        ("#edf0ed", "#e8eef5"),
        ("#6c6a62", "#64748b"),
        ("#6a635b", "#64748b"),
        ("#6f6a64", "#64748b"),
        ("#6355d6", "#3b82f6"),
        ("#8a8379", "#8b9bb4"),
        ("#35312c", "#2b3242"),
        ("#3a3f46", "#39445c"),
    ],
}
for p, pairs in EXTRA.items():
    s = open(p, encoding='utf-8').read()
    for o, n in pairs:
        s = s.replace(o, n)
    open(p, 'w', encoding='utf-8').write(s)
    print('extra swept', p)

# dedup lookup.js palette after mapping
p = 'internal/management/web/lookup.js'
s = open(p, encoding='utf-8').read()
s = s.replace(
    "const palette=['#60a5fa','#3b82f6','#f59e0b','#ef4444','#60a5fa','#22c55e','#fbbf24','#a5b4fc'];",
    "const palette=['#3b82f6','#60a5fa','#f59e0b','#ef4444','#38bdf8','#22c55e','#fbbf24','#a5b4fc'];")
open(p, 'w', encoding='utf-8').write(s)
