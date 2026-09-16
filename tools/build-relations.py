# -*- coding: utf-8 -*-
# Build data/relations.json — the Jesuit Relations from New France, in
# R. G. Thwaites's edition and English translation: The Jesuit Relations
# and Allied Documents, 73 vols. (Cleveland: Burrows Brothers, 1896–1901),
# a pre-1930 publication in the United States public domain. The English
# text is taken from the electronic transcription of Thwaites's edition
# hosted by Creighton University (moses.creighton.edu/kripke/jesuitrelations,
# transcriber Thom Mentrak) — a transcription of a public-domain text adds
# nothing licensable — and spot-verified against the Internet Archive scans
# of the Burrows printing (jesuitsNNjesuuoft). Thwaites's own page numbers,
# which the transcription preserves as [page N] markers, are carried as
# unit labels: the citation grid the scholarship actually uses.
#
# Four sections, cut to the module's argument — mission, ethnography and
# martyrdom, the three registers of the genre: Le Jeune wintering with the
# Montagnais (JR 7, ch. XII of the Relation of 1634, which opens with
# Epictetus); Brébeuf's Instructions for the Fathers who shall be sent to
# the Hurons, as Le Jeune printed them (JR 12, Relation of 1637) — the
# accommodation rulebook of New France, mirror to Ricci's China; and from
# Ragueneau's Relation of 1649 the capture of Saint-Ignace and the deaths
# of Brébeuf and Lalemant (JR 34, chs. III–IV).
#
# Usage: python tools/build-relations.py jr07.html jr12.html jr34.html
import io, json, os, re, sys
from html import unescape

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(path):
    raw = io.open(path, 'rb').read()
    try:
        t = raw.decode('windows-1252')
    except UnicodeDecodeError:
        t = raw.decode('utf-8', errors='replace')
    # paragraph boundaries at closing p-tags, all other markup dropped
    t = re.sub(r'(?i)</p\s*>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = unescape(t).replace('\xa0', ' ')
    return t

V7, V12, V34 = load(sys.argv[1]), load(sys.argv[2]), load(sys.argv[3])

# (id, volume-text, vol no, begin anchor, end anchor, zk, title)
CUTS = [
 ('jr7c12', V7, 7,
  'WHAT ONE MUST SUFFER IN', 'CHAPTER XIII',
  'JR 7, c. 12',
  'What one must suffer in wintering with the Savages — Le Jeune, '
  'Relation of 1634, chapter XII'),
 ('jr12instr', V12, 12,
  'Let us say a few words more before concluding this chapter',
  'CHAPTER XV',
  'JR 12, Instr.',
  "Brébeuf's Instructions for the Fathers of our Society who shall be "
  'sent to the Hurons — as Le Jeune printed them, Relation of 1637'),
 ('jr34c3', V34, 34,
  'OF THE CAPTURE OF THE VILLAGES', 'CHAPTER IV',
  'JR 34, c. 3',
  'Of the capture of the villages of the mission of Saint-Ignace — '
  'Ragueneau, Relation of 1649, chapter III'),
 ('jr34c4', V34, 34,
  'OF THE BLESSED DEATHS', 'CHAPTER V',
  'JR 34, c. 4',
  'Of the blessed deaths of Father Jean de Brébeuf and Father Gabriel '
  'Lalemant — Ragueneau, Relation of 1649, chapter IV'),
]

WORD_FIXES = {
    'Lallement': 'Lalemant',
    'HE Fathers and Brethren whom God': 'The Fathers and Brethren whom God',
    'try to cat their sagamité': 'try to eat their sagamité',
}

# drop-cap letters swallowed with the chapter heading, restored per section
OPEN_FIX = {
    'jr34c3': ('HE progress', 'The progress'),
    'jr34c4': ('S early', 'As early'),
}

PAGE = re.compile(r'\[page\s+(\d+)\]')

def clean(t):
    t = re.sub(r'\s+', ' ', t).strip()
    for a, b in WORD_FIXES.items():
        t = t.replace(a, b)
    # the transcription's bracketed original-pagination and repairs
    t = re.sub(r'\[\d{1,4}(\s+i\.e\.,?\s*\d{1,4})?\]', ' ', t)
    # print line-break hyphens the transcription carried into words
    t = re.sub(r'([a-z])-\s+([a-z])', r'\1\2', t)
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

sections, total = [], 0
for sid, vol, vno, a, b, zk, titel in CUTS:
    i = vol.rfind(a)      # the volume preface repeats the headings: take the body
    j = vol.find(b, i)
    assert i >= 0 and j > i, sid
    # page number in force at the cut's start
    before = [int(m.group(1)) for m in PAGE.finditer(vol[:i])]
    page = before[-1] if before else None
    seg = vol[i:j]
    units, k = [], 0
    for para in seg.split(' '):
        pages_here = [int(m.group(1)) for m in PAGE.finditer(para)]
        p = clean(PAGE.sub(' ', para))
        if pages_here:
            page = pages_here[-1]
        if re.fullmatch(r'[A-Z]', p):
            # the drop-cap letter stands as its own paragraph: keep it for
            # the rejoin below
            units.append({'p': p, 'page': pages_here[0] if pages_here else page})
            continue
        if len(p) <= 2 or not re.search(r'[a-z]{2}', p):
            continue
        if re.fullmatch(r"[A-Z0-9 .,;:'’\-]+", p):      # the chapter heading
            continue
        units.append({'p': p, 'page': pages_here[0] if pages_here else page})
        k += 1
    # rejoin the drop-cap letter with its paragraph and fold the printed
    # small-caps opening of each chapter to normal case
    out = []
    for u in units:
        if out == [] and len(u['p']) == 1:
            out.append(u); continue
        if out and len(out[-1]['p']) == 1:
            joined = out[-1]['p'] + u['p']
            m = re.match(r"^([A-Z][A-Z ,'’\-]{2,}?)(?=\s[a-z])", joined)
            if m:
                run = m.group(1)
                joined = run[0] + run[1:].lower() + joined[len(run):]
            out[-1] = {'p': joined, 'page': out[-1]['page'] or u['page']}
            continue
        out.append(u)
    fix = OPEN_FIX.get(sid)
    if fix and out and out[0]['p'].startswith(fix[0]):
        out[0]['p'] = fix[1] + out[0]['p'][len(fix[0]):]
    uu = []
    for n, u in enumerate(out, start=1):
        e = {'n': n, 'k': n, 'en': u['p']}
        if u['page']:
            e['label'] = f'Thwaites, p. {u["page"]}'
        uu.append(e)
    total += len(uu)
    sections.append({'id': sid, 'zk': zk, 'titel': titel, 'units': uu})

out = {
 'id': 'relations',
 'autor': 'The Jesuit Relations from New France',
 'titel': 'The Jesuit Relations (selections: 1634 · 1637 · 1649)',
 'jahr': '1632–1673',
 'lang': 'en',
 'zitierweise': 'JR vol., c. N [k]',
 'quelle': ("English: Reuben Gold Thwaites's edition and translation, The Jesuit "
            "Relations and Allied Documents, 73 vols. (Cleveland: Burrows Brothers, "
            "1896–1901), a pre-1930 publication in the United States public domain; "
            "the text follows the electronic transcription of that edition hosted by "
            "Creighton University, spot-verified against the Internet Archive scans "
            "of the Burrows printing, with Thwaites's page numbers carried on each "
            "paragraph — the citation grid the scholarship uses. Four selections in "
            "the genre's three registers: Le Jeune wintering with the Montagnais "
            "(Relation of 1634, ch. XII; JR 7), Brébeuf's Instructions for the "
            "Fathers who shall be sent to the Hurons as Le Jeune printed them "
            "(Relation of 1637; JR 12), and from Ragueneau's Relation of 1649 the "
            "capture of Saint-Ignace and the deaths of Brébeuf and Lalemant (JR 34, "
            "chs. III–IV). The French originals stand on the facing pages of the "
            "same public-domain volumes, named as source but not yet carried."),
 'hinweis': ("The order's annual world-reporting of mission, ethnography and "
             "martyrdom — the genre the Society made. Le Jeune opens the wintering "
             "chapter with Epictetus, as Acosta crossed the equator with Aristotle; "
             "Brébeuf's Instructions are the accommodation rulebook of New France, "
             "the canoe-borne mirror of Ricci's change of habit; and Ragueneau's "
             "chapters carry the register the genre was named for. Cited by "
             "Thwaites's volume and the document's chapter, with his page under "
             "every paragraph. Part of the concordance and the citation-bound "
             "dialogue; not part of the linguistic statistics, which describe the "
             "core corpus only."),
 'sections': sections,
}

path = os.path.join(REPO, 'data', 'relations.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', total, 'units in', len(sections), 'sections')
for s in sections:
    print(' ', s['zk'], '|', len(s['units']), '¶ |', s['titel'][:70])
