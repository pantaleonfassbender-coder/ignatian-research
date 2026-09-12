# -*- coding: utf-8 -*-
# Build data/caussade.json — Abandonment to Divine Providence, attributed to
# Jean-Pierre de Caussade (d. 1751), complete in the English of Ella J.
# McMahon: "Abandonment; or, Absolute Surrender to Divine Providence"
# (New York: Benziger Brothers, 1887; Internet Archive
# abandonmentorabs00caus), a pre-1930 US publication in the public domain.
#
# The book as Ramière shaped it and Benziger printed it is carried whole:
# his doctrinal preface (which is where the edition explains itself), the
# treatise in three books (9 + 12 + 12 chapters), and the appendix of five
# pieces by other hands (Surin, Bossuet twice, Francis de Sales, and the
# acts of abandonment of de Chantal, Bossuet and Pignatelli). The
# attribution to Caussade is debated in modern scholarship; the module
# states it as debated. Chapters are counted strictly sequentially, so a
# mangled roman numeral cannot mislead; book boundaries fall at the counts
# the table of contents fixes (9/12/12).
#
# Usage: python tools/build-caussade.py caussade1887.txt
import io, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = io.open(sys.argv[1], encoding='utf-8').read().splitlines()

def idx(pred, start=0):
    return next(i for i in range(start, len(lines)) if pred(lines[i]))

i_pref  = idx(lambda l: l.strip().startswith('There  is  no  truth'))
i_toc   = idx(lambda l: l.strip() == 'CONTENTS.')
i_body  = idx(lambda l: re.match(r'^\s*Book\s+first', l), i_toc)
i_app   = idx(lambda l: l.strip() == 'APPENDIX.', i_body)
i_end   = idx(lambda l: 'Printed  by  Benziger' in l, i_app)

NOISE = [
    re.compile(r'^\s*(Digitized|Google)\b'),
    re.compile(r'^\s*B[oO0][oO0]K\b', re.I),
    re.compile(r"^\s*[ivxlcIVXLC0-9 .,*^~•£_'\-]{1,10}\s*$"),
]
HEAD = re.compile(r'^\s*CHAPTE')

WORD_FIXES = {
    'whicli': 'which', 'tlieii': 'their', 'Sainl': 'Saint',
    'grateful to us foi': 'grateful to us for',
    'us  foi ': 'us  for ',
    'orderof': 'order of', 'vi^hither': 'whither', "v^'xW": 'will',
    'T!iy': 'Thy', 'tiiat': 'that', 'taith': 'faith', 'fiesh': 'flesh',
    'Him* self': 'Himself', '/>.,': 'i.e.,', 'Overshadoiued': 'Overshadowed',
    'wrongly interpreted-': 'wrongly interpreted.',
    'no truth however cleai': 'no truth however clear',
    '1 wish it': 'I wish it',
    'sanctify, us': 'sanctify us', 'Use ful': 'Useful', 'aQ ': 'an ',
    'c&n': 'can', 'Lighi': 'Light', 'gfives': 'gives',
    'ret ognize': 'recognize', 'Peace ol Heart': 'Peace of Heart',
    'to Soul who walk': 'to Souls who walk',
    # italic words the OCR shredded, restored from the page images
    'thisyf^/uttered': 'this fiat uttered',
    "one's %**^i with God": "one's self with God",
    'to do with sue what Thou wilt': 'to do with me what Thou wilt',
    '/» Thee, 0 Lord': 'In Thee, O Lord',
    '/irtue': 'virtue', '{Fiat lux)': '(Fiat lux)',
    'purgative wa\\.': 'purgative way.',
    'Dbey': 'obey', 'obUgations': 'obligations', 'thjjir': 'their',
    'witiiout': 'without', 'permittingourselvesthe': 'permitting ourselves the',
    'an(^': 'and', 'an<* eternity': 'and eternity', 'onlyThee': 'only Thee',
    'habet J sed': 'habet, sed', 'om7iia': 'omnia', '07ie': 'one',
    '4th„': '4th.', '4Lh.': '4th.', 'i2th.': '12th.',
    'loth. We should take': '10th. We should take',
    'nth. We should console': '11th. We should console',
    'gfocs': 'goes', 'wlmt': 'what',
    'that is> His part and action— arc': 'that is, His part and action — are',
    'ver> obscurity': 'very obscurity', 'o{ the senses': 'of the senses',
    '& dream': 'a dream', 'p&rseveringly': 'perseveringly',
    '%ults': 'faults', 'p yrfection': 'perfection', '2very kind': 'every kind',
    '^ease to love': 'cease to love',
    'shah overshadow': 'shall overshadow',
    "overshadow thee*' said": 'overshadow thee," said',
    "admirabi*' variety": 'admirable variety',
    # p. 147/148 page turn: "…they are all the real / subject of those
    # mystic histories" — the l of real lost in a smudge (page image checked)
    "all the re*'- subject": 'all the real subject',
    "all the re'- subject": 'all the real subject',
    'fidelty': 'fidelity', 'in Ihe depths': 'in the depths',
}

def clean(t):
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)
    t = re.sub(r'\s+', ' ', t).strip()
    for a, b in WORD_FIXES.items():
        t = t.replace(a, b)
    # the printing's italics, broken glyph by glyph
    t = re.sub(r"(^|\s)(\*\*|\*')\s*(?=[A-Za-z])", r'\1"', t)
    t = t.replace('v/', 'w')
    t = re.sub(r'\bt[li]ie\b', 'the', t)
    t = re.sub(r'\b0(?=\s+[A-Z])', 'O', t)
    t = re.sub(r'rowing\s+\S*l\S*\s+the\s+tide', 'rowing with the tide', t)
    t = re.sub(r'follow\s+the\s+[\\/|]{2,}\s+of\s+God', 'follow the will of God', t)
    t = re.sub(r"the\\+'?\s+are\s+nothing", 'they are nothing', t)
    # running heads glued mid-paragraph at page turns
    t = re.sub(r'(?:^|\s)[\\0-9iIlJoOS$!]{1,4}\s*(?:Holy\s+Ab[a-z7]\S{0,12}|Appendix)[.,]?(?=\s|$)', ' ', t)
    t = re.sub(r'\S*[<>{}^]\S*[<>{}^]\S*', ' ', t)
    for ch in '■♦•«»^~*':
        t = t.replace(ch, '')
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

# page furniture survives as its own short block between blank lines:
# a page number, alone or glued to a decayed running head on either side
PSEUDO_NUM = r'[\\0-9iIlJoOS$!][\\0-9iIlJoOSy$!]{0,3}'
def is_furniture(p):
    if re.fullmatch(r'\d{1,4}', p):
        return True
    if len(p) < 60 and re.search(r'\d', p) and (
            re.match(rf'^{PSEUDO_NUM}\s', p) or
            re.search(rf'\s{PSEUDO_NUM}[.,]?$', p)):
        return True
    # a head whose page number decayed into letters (Tio Holy Abandonment)
    if len(p) < 45 and re.match(
            r'^\S{0,4}\s*(Holy\s+Aban\S{0,10}|Preface|Appendix)[.,]?\s*\S{0,4}$', p):
        return True
    return False

def blocks_of(seg):
    """blank-line paragraph blocks, NOISE lines dropped"""
    out, cur = [], []
    for l in seg:
        s = l.rstrip()
        if any(rx.match(s) for rx in NOISE):
            continue
        if not s.strip():
            if cur:
                out.append(cur); cur = []
            continue
        cur.append(s.strip())
    if cur:
        out.append(cur)
    return out

DROPPED = []
def paras_of(blocks):
    """clean, drop furniture, merge page-turn continuations"""
    paras = []
    for b in blocks:
        p = clean(' '.join(b))
        if len(p) <= 2:
            continue
        if is_furniture(p):
            DROPPED.append(p)
            continue
        paras.append(p)
    merged = []
    for p in paras:
        if merged and (p[:1].islower() or p[:1] in ')('):
            merged[-1] = clean(merged[-1] + ' ' + p)
        else:
            merged.append(p)
    return merged

ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
sections = []
total = 0
def push(sid, zk, titel, paras, labels=None):
    global total
    units = []
    for k, p in enumerate(paras, start=1):
        u = {'n': k, 'k': k, 'en': p}
        if labels and labels.get(k - 1):
            u['label'] = labels[k - 1]
        units.append(u)
    total += len(units)
    sections.append({'id': sid, 'zk': zk, 'titel': titel, 'units': units})

# ---- the preface -------------------------------------------------------
pref = paras_of(blocks_of(lines[i_pref:i_toc]))
push('pref', 'Ab. Pref.',
     'Preface by the Rev. H. Ramière, S.J. — Foundation and True Nature of '
     'the Virtue of Abandonment',
     pref)

# ---- the treatise: three books, chapters strictly sequential -----------
# an ornamental book heading (however the OCR decayed its blackletter) is
# followed by the book's subtitle: skip both until the next CHAPTER line
BOOKLINE = re.compile(r'^\s*(B[oO0][oO0]K|Book|\S{0,2}3ook)\b')
chapters, cur, skipping = [], None, False
for l in lines[i_body:i_app]:
    s = l.rstrip()
    if HEAD.match(s):
        skipping = False
        cur = {'no': len(chapters) + 1, 'blocks': [[]]}
        chapters.append(cur)
        continue
    if BOOKLINE.match(s):
        skipping = True
        continue
    if skipping or cur is None:
        continue
    if any(rx.match(s) for rx in NOISE):
        continue
    if not s.strip():
        if cur['blocks'][-1]:
            cur['blocks'].append([])
        continue
    cur['blocks'][-1].append(s.strip())
assert len(chapters) == 33, f'expected 33 chapters, found {len(chapters)}'

BOOK_OF = lambda n: 1 if n <= 9 else (2 if n <= 21 else 3)
CHAP_OF = lambda n: n if n <= 9 else (n - 9 if n <= 21 else n - 21)

for c in chapters:
    blocks = [b for b in c['blocks'] if b]
    title = clean(' '.join(blocks[0]))
    paras = paras_of(blocks[1:])
    # a short lowercase-opening first paragraph is the title's runover
    while paras and len(paras[0]) < 45 and paras[0][:1].islower():
        title = clean(title.rstrip('.') + ' ' + paras.pop(0))
    b, n = BOOK_OF(c['no']), CHAP_OF(c['no'])
    push(f'b{b}c{n}', f'Ab. {ROMAN[b-1]}, c. {n}',
         f'Book {ROMAN[b-1]}, Chapter {ROMAN[n-1]} — {title.rstrip(".")}',
         paras)

# ---- the appendix: five pieces by other hands --------------------------
NUMERAL = re.compile(r'^(I|II|III|IV|V)\s*[.,]?\s*$')
ACT_HEAD = re.compile(r'^(Another\s+)?Acts?\s+of\s+Abandonment[.,]?$', re.I)

# split at the standalone numeral lines BEFORE the noise filter sees them
app_segs, seg = [[]], []
for l in lines[i_app + 1:i_end]:
    if NUMERAL.match(l.strip()):
        app_segs.append([])
        continue
    app_segs[-1].append(l)
note, pieces = blocks_of(app_segs[0]), [blocks_of(s) for s in app_segs[1:]]
assert len(pieces) == 5, f'expected 5 appendix pieces, found {len(pieces)}'

for no, blocks in enumerate(pieces, start=1):
    labels = {}
    if no == 5:
        title, rest = 'Acts of Abandonment', blocks
    else:
        title = clean(' '.join(blocks[0])).rstrip('.')
        rest = blocks[1:]
        if rest and clean(' '.join(rest[0])).startswith('By '):
            by = clean(' '.join(rest[0])).rstrip('.,')
            title += f' ({by[3:]})'
            rest = rest[1:]
    paras, pending = [], None
    i = 0
    while i < len(rest):
        joined = clean(' '.join(rest[i]))
        # act headers: "(Another) Act of Abandonment. By N." in one block or
        # two; the fourth header, blackletter "An Act of Confidence in God.",
        # defeated the OCR entirely and leaves only its standalone By-line —
        # the title is restored from the page image (printed p. 191)
        m = re.match(r'^(?:An(?:other)?\s+)?Acts?\s+of\s+Abandonment[.,]?'
                     r'(?:\s+By\s+(.+?))?[.,]?$', joined)
        if m:
            by = m.group(1)
            if not by and i + 1 < len(rest) and \
                    clean(' '.join(rest[i + 1])).startswith('By '):
                by = clean(' '.join(rest[i + 1]))[3:]
                i += 1
            pending = 'Act of abandonment — ' + (by or '').rstrip('.,')
            i += 1
            continue
        if re.match(r'^By\s+[A-Z]', joined) and len(joined) < 60:
            title5 = ('An Act of Confidence in God'
                      if 'Colombiere' in joined else 'Act')
            pending = title5 + ' — ' + joined[3:].rstrip(',')
            i += 1
            continue
        p = joined
        i += 1
        if len(p) <= 2:
            continue
        if is_furniture(p):
            DROPPED.append(p)
            continue
        if paras and pending is None and (p[:1].islower() or p[:1] in ')('):
            paras[-1] = clean(paras[-1] + ' ' + p)
            continue
        if pending:
            labels[len(paras)] = pending
            pending = None
        paras.append(p)
    if no == 1 and note:
        note_paras = paras_of(note)
        labels = {k + len(note_paras): v for k, v in labels.items()}
        for j, p in enumerate(reversed(note_paras)):
            paras.insert(0, p)
        labels[0] = "The editor's note to the appendix"
    push(f'app{no}', f'Ab. App. {ROMAN[no-1]}',
         f'Appendix {ROMAN[no-1]} — {title}', paras, labels)

out = {
 'id': 'caussade',
 'autor': 'attributed to Jean-Pierre de Caussade',
 'titel': 'Abandonment to Divine Providence (before 1751 · transmitted 1861)',
 'jahr': '1861',
 'lang': 'en',
 'zitierweise': 'Ab. B, c. N [k]',
 'quelle': ("English: Ella J. McMahon's translation, Abandonment; or, Absolute Surrender "
            "to Divine Providence (New York: Benziger Brothers, 1887; Internet Archive "
            "abandonmentorabs00caus), a pre-1930 US publication in the public domain. "
            "The book is carried whole as Henri Ramière shaped it in 1861 and Benziger "
            "printed it: Ramière's doctrinal preface, the treatise in three books "
            "(9 + 12 + 12 chapters), and the appendix of pieces by other hands — Surin, "
            "Bossuet, Francis de Sales, the acts of abandonment of Jane Frances de "
            "Chantal, Bossuet and Pignatelli, and La Colombière's act of confidence in "
            "God. The French original (L'abandon à la "
            "providence divine, ed. H. Ramière, Lyon 1861) is named as source but not "
            "yet carried. The attribution to Caussade, who died in 1751, is debated in "
            "modern scholarship (the text survives through manuscript copies circulated "
            "among the Visitation nuns of Nancy); this module states the book as what "
            "it demonstrably is — the text Ramière published under Caussade's name."),
 'hinweis': ("The end of the school line: the discernment the Directory regulates and "
             "Rodríguez curricularizes is here distilled to a single motion — the "
             "present moment as the sacrament of God's will, embraced by abandonment. "
             "Written before the suppression and printed long after it (the Favre "
             "pattern of transmission), the book reached the nineteenth century as the "
             "testament of the old Society's school of prayer. Cited by book and "
             "chapter in Ramière's arrangement; the paragraph numbers are this site's "
             "own. Part of the concordance and the citation-bound dialogue; not part "
             "of the linguistic statistics, which describe the core corpus only."),
 'sections': sections,
}

path = os.path.join(REPO, 'data', 'caussade.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', total, 'units in', len(sections), 'sections')
for s in sections:
    print(' ', s['zk'], '|', len(s['units']), '¶ |', s['titel'][:70])
if '--dropped' in sys.argv:
    print('--- dropped as furniture ---')
    for p in DROPPED:
        print('  ', repr(p))
