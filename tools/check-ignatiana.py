# -*- coding: utf-8 -*-
"""Consistency check for the Ignatiana apparatus.

The apparatus is hybrid: four locked works ship structure and anchors but no
text, so — unlike a fully public-domain corpus — a registry entry without a
text file can be legitimate. The check therefore verifies:

  1. works.json: seven entries, required fields present, every `linie` valid;
  2. programme.json: planned entries well-formed, lines valid;
  3. the open editions parse and their unit counts hold
     (exercitia 370 canonical paragraphs, directorium 287, letters 24,
     memoriale sections + appendix non-empty, Longridge layers well-formed);
  4. every reading-path station in app.js resolves to an existing reader
     anchor (exercitia/directorium/memoriale section ids, letter numbers);
  5. the nav carries every route and every route is defined;
  6. SOURCES.md names every open edition; LICENSES.md exists.

Run from anywhere: python tools/check-ignatiana.py
Exit code 0 = clean; 1 = errors (warnings alone do not fail the check).
"""
import json, io, os, re, sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(REPO)

errors, warns = [], []
LINIEN = {'kern', 'schule', 'welt', 'spee', 'kritik'}

# 1. works.json
works = json.load(io.open('data/works.json', encoding='utf-8'))
if len(works) != 7:
    warns.append(f'works.json has {len(works)} entries (expected 7) — extend this check if the corpus grew')
for w in works:
    for f in ('id', 'kurz', 'zk', 'titel', 'zitierweise', 'rechte', 'linie'):
        if not w.get(f):
            errors.append(f"works.json {w.get('id','?')}: field {f} empty")
    if w.get('linie') not in LINIEN:
        errors.append(f"works.json {w['id']}: unknown linie {w.get('linie')}")

# 2. programme.json
prog = json.load(io.open('data/programme.json', encoding='utf-8'))
for p in prog:
    for f in ('id', 'linie', 'status', 'autor', 'jahr', 'titel', 'warum', 'quelle'):
        if not p.get(f):
            errors.append(f"programme.json {p.get('id','?')}: field {f} empty")
    if p.get('linie') not in LINIEN:
        errors.append(f"programme.json {p['id']}: unknown linie {p.get('linie')}")
ids = [x['id'] for x in works] + [x['id'] for x in prog]
if len(ids) != len(set(ids)):
    errors.append('duplicate ids across works.json and programme.json')

# 3. open editions
exx = json.load(io.open('data/exercitia.json', encoding='utf-8'))
ns = [u['n'] for s in exx['sections'] for u in s['units']]
if sorted(ns) != list(range(1, 371)):
    errors.append(f'exercitia: canonical grid broken ({len(ns)} units, expected [1]-[370] complete)')
exx_ids = {s['id'] for s in exx['sections']}

dirj = json.load(io.open('data/directorium.json', encoding='utf-8'))
dir_parts = list(dirj['vorspann']) + list(dirj['kapitel'])
dir_ids = {c['id'] for c in dir_parts}
dn = sum(len(c['paras']) for c in dir_parts)
if dn != 287:
    errors.append(f'directorium: {dn} paragraphs (expected 287)')

letters = json.load(io.open('data/letters.json', encoding='utf-8'))
if len(letters) != 24:
    errors.append(f'letters: {len(letters)} letters (expected 24)')
letter_ns = {l['n'] for l in letters}

mem = json.load(io.open('data/memoriale.json', encoding='utf-8'))
mem_ids = {s['id'] for s in mem['sections']} | {a['id'] for a in mem['appendix']}
if not mem['sections'] or not mem['appendix']:
    errors.append('memoriale: sections or appendix empty')

for name in ('longridge_exx', 'longridge_dir', 'anchors', 'corpus', 'network', 'terms',
             'keyness', 'glossary', 'lexicon', 'discernment', 'persons', 'places',
             'itinerary', 'introductions', 'sections'):
    try:
        json.load(io.open(f'data/{name}.json', encoding='utf-8'))
    except Exception as e:
        errors.append(f'data/{name}.json unreadable: {e}')

# 4. reading-path stations resolve
app = io.open('app.js', encoding='utf-8').read()
for href in re.findall(r'href: "(#/[a-z]+/[^"]+)"', app):
    kind, _, rest = href[2:].partition('/')
    tgt = rest.split('/')[0]
    ok = True
    if kind == 'exercitia':
        ok = tgt in exx_ids
    elif kind == 'directorium':
        ok = tgt in dir_ids
    elif kind == 'memoriale':
        ok = tgt in mem_ids
    elif kind == 'letters':
        ok = tgt.isdigit() and int(tgt) in letter_ns
    elif kind == 'works':
        ok = tgt in {w['id'] for w in works}
    if not ok:
        errors.append(f'path/link target does not resolve: {href}')

# 5. nav <-> routes
idx = io.open('index.html', encoding='utf-8').read()
nav = set(re.findall(r'data-v="(\w+)"', idx))
routes = set(re.findall(r'(\w+):', re.search(r'const ROUTES = \{(.*?)\n\};', app, re.S).group(1)))
for r in ('paths', 'coda'):
    if r not in nav:
        errors.append(f'route {r} missing from the nav')
for r in nav - routes:
    errors.append(f'nav points to undefined route: {r}')

# 6. docs
sources = io.open('SOURCES.md', encoding='utf-8').read().lower()
for key in ('exercitia', 'directorium', 'memoriale', 'letters'):
    if key.rstrip('s') not in sources and key not in sources:
        errors.append(f'{key} missing in SOURCES.md')
if not os.path.exists('LICENSES.md'):
    errors.append('LICENSES.md missing')

print(f'works: {len(works)} shipped · {len(prog)} planned · exercitia {len(ns)} ¶ · directorium {dn} ¶ · letters {len(letters)}')
print()
print('ERRORS:', len(errors))
for e in errors:
    print('  !!', e)
print('WARNINGS:', len(warns))
for w in warns:
    print('  ?', w)
sys.exit(1 if errors else 0)
