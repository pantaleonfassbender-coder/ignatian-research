# -*- coding: utf-8 -*-
# Build data/ricci.json — Ricci/Trigault, De Christiana expeditione apud
# Sinas (Augsburg 1615), in the English reception of 1625: Samuel Purchas's
# digest "taken out of Ricius and Trigautius" in Purchas his Pilgrimes,
# carried from the MacLehose reprint (Glasgow 1906, vol. XII; Internet
# Archive hakluytusposthum12purc) — a 1625 translation-digest in a 1906
# printing, public domain twice over.
#
# Eight sections, cut to the module's argument — inculturation argued at
# the court of China: from the mission narrative (Purchas XII, ch. V)
# Ruggieri and Ricci's entry (§ 3), the alteration of habit from bonze to
# literatus (§ 4), and Nanquin with Ricci's Booke of Friendship (§ 5);
# from the systematic discourse (ch. VII) the name and greatness of the
# kingdom (§ 1), characters, studies and degrees (§ 2), the three sects
# (§ 5), and strangers and foreign religions (§ 6); and from ch. VIII the
# death of Ricci with Pantoja's petition for a burial place, to the church
# built at Nanquin in 1611. Purchas abridges and reworks Trigault — the
# transmission chain of 1625, carried as it stands, in its own orthography.
# Sections are counted strictly sequentially within each chapter, so a
# mangled section numeral cannot mislead; a marker repeated at a page
# boundary is deduplicated by distance.
#
# Usage: python tools/build-ricci.py purchas12.txt [--dropped]
import io, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = io.open(sys.argv[1], encoding='utf-8').read().splitlines()

def find_line(rx, start=0):
    r = re.compile(rx)
    return next(i for i in range(start, len(lines)) if r.match(lines[i]))

# body chapter heads (the table of contents is all before line 700)
i_c5 = find_line(r'^\s*Chap\.\s+V\.?\s*$', 1000)
i_c7 = find_line(r'^\s*Chap\.\s+VII\b', i_c5)
i_c8 = find_line(r'^\s*Chap\.\s+VIII\b', i_c7)
i_end = find_line(r'.*Riccis\s+death.*', 0) and len(lines)

MARK = re.compile(r"^\s*\[?§['’.•]{0,2}\s*[IVXLivxlH1|acmrn\-]{0,6}[.\-]?\]?\s*$")
SELECT = {'c5': [3, 4, 5], 'c7': [1, 2, 5, 6]}
CHAPTER = {'c5': ('V', i_c5, i_c7), 'c7': ('VII', i_c7, i_c8)}

DROPPED = []
NOISE = [
    re.compile(r'^\s*(Digitized|Google)\b'),
    # running heads: PURCHAS HIS PILGRIMES / THE JESUITS IN CHINA, with
    # page numbers or the reprint's a.d. margin caption on either side
    re.compile(r"^\s*(?:[aA]\.?[dD]\.?\s*)?\d{0,4}\s*[A-Z][A-Z .,'’&:;\-]{5,}\s*(?:[aA]\.?[dD]\.?)?\s*\d{0,4}\s*$"),
    re.compile(r"^\s*[ivxlcIVXLC0-9 .,*^~•£_'\-]{1,10}\s*$"),
    re.compile(r'^\s*[A-Za-z]{1,2}\s+[A-Za-z]?\s*\d\s*$'),
    re.compile(r'^\s*\[?[iInl]{1,3}\.\s*[iI]{1,2}\.\s*\d{1,4}\.?\]?\s*$'),   # [III. ii. 380.]
    re.compile(r'^\s*[cC]\.?\s*1?\d{3}\.?[\-—]?\s*$'),                        # c. 1604. / 1579-
]

WORD_FIXES = {
    'JNanquin': 'Nanquin',
    'Lanchin: fcr they': 'Lanchin: for they',
    # marginal glosses the gap-rules cannot reach, restored sentence by
    # sentence against the source
    'Legation #. goetk into from the Pope': 'Legation from the Pope',
    'the com1>aredvnth Streets': 'the Streets',
    '&rJ:at a^tar, Chinois': 'Chinois',
    'had comne from': 'had come from',
    'Christ 6$.': 'Christ 65.',
    'stand \'"&\' ten times': 'stand ten times',
    '1587. Converts.': '1587.',
    'and M.Paris \\$c freed': 'and freed',
}

def trim_margin(s):
    """the reprint's right-hand marginal glosses attach to a text line
    across ONE wide gap (3+ spaces, against the djvu's uniform double
    space): cut the short capitalised tail off. Lines with several wide
    gaps are spread type (drop-cap indentation) and are left alone."""
    s = re.sub(r'^\[[^\]]{0,16}\]\s*', '', s)          # folio refs [III. ii. 409.]
    runs = re.findall(r'[^\S\n]{3,}', s)
    if len(runs) != 1:
        return s
    left, right = re.split(r'[^\S\n]{3,}', s, maxsplit=1)
    if len(right) <= 25 and len(left) > len(right):
        return left
    if len(left) <= 25 and not left.rstrip().endswith(':') and (
            len(right) >= 25 or (len(right) >= 12 and right[:1].islower())):
        return right
    return s

def clean(t):
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)
    t = re.sub(r'\s+', ' ', t).strip()
    for a, b in WORD_FIXES.items():
        t = t.replace(a, b)
    t = re.sub(r'\[\s*[IiNnl1]{1,3}\.\s*[iI1l]{1,2}\.?\s*\d{1,4}\.?\s*\]', ' ', t)
    t = re.sub(r"\S{0,4}J&,\.1P\s+i-'\s+\S*Rka(?=giving)", '', t)
    t = re.sub(r'([a-z.,;:!?’\'"])\d{1,2}(?=[\s.,;)]|$)', r'\1', t)
    t = re.sub(r'\b\d{1,2}(?=[a-z]{3,})', '', t)
    t = re.sub(r'\S*[<>{}^]\S*[<>{}^]\S*', ' ', t)
    for ch in '■♦•«»^~*°_·<>':
        t = t.replace(ch, '')
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def blocks_of(seg):
    """paragraph blocks with margin trimming; a block whose longest line is
    narrow is the margin column itself and is dropped whole"""
    out, cur = [], []
    for raw in seg:
        s = raw.rstrip()
        if any(rx.match(s) for rx in NOISE):
            if s.strip():
                DROPPED.append(('noise', s.strip()[:70]))
            continue
        if not s.strip():
            if cur:
                out.append(cur); cur = []
            continue
        cur.append(trim_margin(s.strip()))
    if cur:
        out.append(cur)
    kept = []
    for b in out:
        if max(len(l) for l in b) < 30 and sum(len(l) for l in b) < 120:
            DROPPED.append(('margin', ' | '.join(b)[:70]))
            continue
        kept.append(b)
    return kept

def paras_of(blocks):
    paras = []
    for b in blocks:
        p = clean(' '.join(b))
        if len(p) > 4 or re.search(r'[a-z]{2}', p):
            paras.append(p)
    merged = []
    for p in paras:
        if merged and (p[:1].islower() or p[:1] in ')(' or p[:1].isdigit()):
            merged[-1] = clean(merged[-1] + ' ' + p)
        else:
            merged.append(p)
    return merged

def split_sections(start, end):
    """standalone §-marker lines, counted sequentially, page-boundary
    duplicates dropped by distance"""
    marks = []
    for i in range(start + 1, end):
        if MARK.match(lines[i].rstrip()):
            if marks and i - marks[-1] < 30:
                continue
            marks.append(i)
    out = {}
    for n, i in enumerate(marks, start=1):
        j = marks[n] if n < len(marks) else end
        out[n] = (i + 1, j)
    return out

# drop-cap letters the 1906 printing loses at section openings, restored
DROPCAP = {
    'c5s3': ('T is a custome', 'It is a custome'),
    'c5s4': ('Icius cals', 'Ricius cals'),
    'c5s5': ('Anquin or Nanchin', 'Nanquin or Nanchin'),
    'c7s1': ('His utmost Empire', 'This utmost Empire'),
    'c7s2': ('Ow, for', 'Now, for'),
    'c7s5': ('O superstition', 'No superstition'),
    'c7s6': ('jlOw inhospitall', 'How inhospitall'),
}

sections, total = [], 0
def push(sid, zk, titel, paras):
    global total
    units = [{'n': k, 'k': k, 'en': p} for k, p in enumerate(paras, start=1)]
    total += len(units)
    sections.append({'id': sid, 'zk': zk, 'titel': titel, 'units': units})

for cid, wanted in SELECT.items():
    roman, start, end = CHAPTER[cid]
    secs = split_sections(start, end)
    for n in wanted:
        s0, s1 = secs[n]
        blocks = blocks_of(lines[s0:s1])
        title = clean(' '.join(blocks[0])).rstrip('.')
        paras = paras_of(blocks[1:])
        while paras and len(paras[0]) < 45 and paras[0][:1].islower():
            title = clean(title.rstrip('.') + ' ' + paras.pop(0))
        fix = DROPCAP.get(f'{cid}s{n}')
        if fix and paras and paras[0].startswith(fix[0]):
            paras[0] = fix[1] + paras[0][len(fix[0]):]
        push(f'{cid}s{n}', f'RT {roman}, § {n}',
             f'Chapter {roman}, § {n} — {title}', paras)

# ch. VIII: the death of Ricci, from the paragraph that announces it to the
# church built at Nanquin in 1611
d0 = find_line(r'^\s*Wee\s+are\s+now\s+come\s+to\s+the\s+Death\s+of\s+Father\s+Ricius', i_c8)
d1 = find_line(r'.*They\s+built\s+a\s+Church\s+at\s+Nanquin.*', d0)
d1 = d1 + 2
death = paras_of(blocks_of(lines[d0:d1]))
# the closing year stands alone on its line and falls to the number filter
if death and death[-1].endswith('Nanquin, Anno'):
    death[-1] += ' 1611.'
push('c8death', 'RT VIII (death)',
     'Chapter VIII — The Death of Father Ricius, and his buriall place '
     'obtayned of the King', death)

out = {
 'id': 'ricci',
 'autor': 'Matteo Ricci / Nicolas Trigault',
 'titel': 'De Christiana expeditione apud Sinas — in Purchas his Pilgrimes (1615 · Englished 1625)',
 'jahr': '1615',
 'lang': 'en',
 'zitierweise': 'RT c, § n [k]',
 'quelle': ("English: Samuel Purchas's digest of 1625 — 'A Discourse of the Kingdome of "
            "China, taken out of Ricius and Trigautius', with the mission narrative and "
            "the death of Ricci, in Purchas his Pilgrimes, book III — as reprinted by "
            "James MacLehose and Sons (Hakluytus Posthumus, vol. XII, Glasgow 1906; "
            "Internet Archive hakluytusposthum12purc): a 1625 translation-digest in a "
            "1906 printing, in the United States public domain twice over. Purchas "
            "abridges and reworks Trigault's Latin — the transmission chain of 1625, "
            "carried as it stands, in its own orthography; the reprint's marginal "
            "glosses and page furniture are not carried. Eight sections are cut to the "
            "module's argument: from the narrative (ch. V) the entry of Ruggieri and "
            "Ricci, the alteration of habit, and Nanquin with the Booke of Friendship; "
            "from the discourse (ch. VII) the kingdom's name and greatness, its "
            "characters, studies and degrees, the three sects, and the strangers and "
            "forraine religions; and from ch. VIII the death of Ricci with Pantoja's "
            "petition. The Latin original (Trigault, Augsburg 1615) is on the Internet "
            "Archive, named as source but not yet carried; the modern translation "
            "(Gallagher, 1953) is in copyright and was not consulted."),
 'hinweis': ("Inculturation argued at the court of China: the boldest application of "
             "Ignatian adaptability, read here through the eyes of a Protestant "
             "compiler of 1625 — a double transmission that is itself part of the "
             "story. The Jesuits learn the court tongue, change their habit from "
             "bonze to literatus, write a Booke of Friendship in Chinese, and are "
             "buried at last by imperial grant. Cited by Purchas's chapter and "
             "section; the paragraph numbers are this site's own. Part of the "
             "concordance and the citation-bound dialogue; not part of the linguistic "
             "statistics, which describe the core corpus only."),
 'sections': sections,
}

path = os.path.join(REPO, 'data', 'ricci.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', total, 'units in', len(sections), 'sections')
for s in sections:
    print(' ', s['zk'], '|', len(s['units']), '¶ |', s['titel'][:74])
if '--dropped' in sys.argv:
    print('--- dropped ---')
    for kind, l in DROPPED:
        print('  ', kind, '|', repr(l))
