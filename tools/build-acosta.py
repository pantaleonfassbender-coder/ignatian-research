# -*- coding: utf-8 -*-
# Build data/acosta.json — José de Acosta, Historia natural y moral de las
# Indias (Seville 1590), in Edward Grimston's English of 1604 as reprinted by
# the Hakluyt Society (ed. Clements Markham, 2 vols., London 1880; Internet
# Archive naturalmoralhist01acos and naturalmoralhist61acosrich) — a 1604
# translation in an 1880 printing, public domain twice over.
#
# Eleven chapters, cut to the module's argument — a Jesuit empiricism before
# the word, observation set against the authorities: the Fathers may err on
# cosmography (I.1), Aristotle on the new world (I.9), the burning zone
# watered and temperate against the ancients (II.6, II.9 — "I laughed at
# Aristotle and his philosophy" — II.14), Potosí observed (IV.6–7), and the
# rationality of the Indians defended, letters or none (VI.1, VI.4, VI.7,
# VI.8 — the quipus). Grimston's orthography of 1604 is kept as printed;
# Markham's footnotes are omitted; chapters are counted strictly
# sequentially within each book, so a mangled roman numeral cannot mislead.
#
# Usage: python tools/build-acosta.py acosta1.txt acosta2.txt [--dropped]
import io, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vol1 = io.open(sys.argv[1], encoding='utf-8').read().splitlines()
vol2 = io.open(sys.argv[2], encoding='utf-8').read().splitlines()

# body start of each book: the half-title lines of the 1880 printing
BOOK_MARK = {
    1: (vol1, 'THE   FIRST   BOOKE'), 2: (vol1, 'THE   SECOND    BOOKE'),
    3: (vol1, 'THE   THIRD    BOOKE'), 4: (vol1, 'THE    FOVRTH    BOOKE'),
    5: (vol2, 'THE    FIFT    BOOKE'), 6: (vol2, 'THE    SIXT    BOOKE'),
    7: (vol2, 'THE   SEVENTH    BOOKE'),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
def find_mark(lines, mark):
    m = norm(mark)
    return next(i for i, l in enumerate(lines) if norm(l) == m)

SELECT = {1: [1, 9], 2: [6, 9, 14], 4: [6, 7], 6: [1, 4, 7, 8]}
ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV']

HEAD = re.compile(r'^\s*C[Hh][Aa][Pp]\b')
DROPPED = []
NOISE = [
    re.compile(r'^\s*(Digitized|Google)\b'),
    # running heads: caps-only line, page number before or after
    re.compile(r"^\s*\d{0,4}\s*[A-Z][A-Z0-9 .,'’&:;\-]{4,}\s*\d{0,4}\s*$"),
    # marginal LIB. N. fragments on their own line
    re.compile(r'^\s*[Ll][iI1l][bB][.,]?\s*[ivxlcIVXLC]{0,4}[.,]?\s*$'),
    re.compile(r"^\s*[ivxlcIVXLC0-9 .,*^~•£_'\-]{1,10}\s*$"),
    re.compile(r'^\s*[A-Za-z]{1,2}\s+[A-Za-z]?\s*\d\s*$'),   # quire signatures (d d 2, B 2)
]
FOOTNOTE = re.compile(r'^\s*\d{1,2}\s+(?:\*|u\s|[A-Z(“"])')

WORD_FIXES = {
    'TEOPICS': 'TROPICS', 'wrjting': 'writing',
    # Acosta's marginal source-citations, shredded by the OCR and glued into
    # the running text; the sentences are restored, the mangled references
    # dropped (the printed margin carries them, the text never did)
    'resolve, Aug., lib. ii, whether': 'resolve whether',
    "at. cG9'.a< ": '',
    "V'9 saith": 'I," saith',
    'doth id. Psai.': 'doth',
    'aaE^hesSt* ** seeme^h that': 'it seemeth that',
    'hb. 11, c. 4. ': '',
    'Tim. and critia. renowned': 'renowned',
    'critia. renowned': 'renowned',
    'deceived, not Biues, lib. that I will': 'deceived. Not that I will',
    'whereof emit., c. 21. the Scripture': 'whereof the Scripture',
    'and 1/ * the good': 'and the good',
    'memorable d d 2 _ things': 'memorable things',
    'quinua/ and': 'quinua, and',
    'thousand worth i?506 peeces': 'thousand peeces',
    'Theodoret. as the armes': 'as the armes',
    'Theophii. and Theophilus': 'and Theophilus',
    'at those Chrysost., which hold': 'at those which hold',
    'the amTxviUn holy Scripture': 'the holy Scripture',
    "Lact.,lib.iii, ° _ ' caVi24 inSt'' holding": 'holding',
    'in all m capitul. 8, ad Hebre. thinges. But': 'in all thinges. But',
    'or or registers': 'or registers',
    'Lli. II. although': 'although',
    'Astrologie and Linr-': 'Astrologie and',
}

def clean(t):
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)
    t = re.sub(r'\s+', ' ', t).strip()
    for a, b in WORD_FIXES.items():
        t = t.replace(a, b)
    # the printing's quotation marks and rules, broken by the OCR
    t = t.replace("/''", '."').replace("/'", '."')
    t = re.sub(r'(\w)-\s*/\s*(\w)', r'\1\2', t)       # dis- / covered
    t = re.sub(r'^[/\s]+', '', t)                      # marginal rule at para start
    t = re.sub(r'([a-z])/(?=\s)', r'\1', t)            # rule glued to a word
    t = re.sub(r'\s/\s*,?\s*(XXXV\.)?\s*', ' ', t)     # stray marginal rules
    # marginal "lib. ii." glued to the start of a page's first line
    t = re.sub(r'(?:^|\s)[Ll][iI1l][bB][.,]?\s+[ivxlc]{1,4}[.,]?(?=\s|$)', ' ', t)
    # footnote reference digits, printed superscript, glued to the word
    t = re.sub(r'([a-z.,;:!?’\'"])\d{1,2}(?=[\s.,;)]|$)', r'\1', t)
    t = re.sub(r'\b\d{1,2}(?=[a-z]{3,})', '', t)       # 5takes -> takes
    # the 1880 OCR misreads Grimston's "Iland(s)" as "Hand(s)"
    t = re.sub(r'\bHand(s?)\b', r'Iland\1', t)
    # two marginal glosses the fixes above cannot catch verbatim (odd glyphs)
    t = re.sub(r"Lact\.,?\s*lib\.\S*.{0,14}caVi\d*\s+inSt'{0,2}\s+holding", 'holding', t)
    t = re.sub(r'sixe rialls and a[,. \-]{0,12}fourth part, thousand', 'sixe thousand', t)
    t = t.replace('the Heavens a Hebre. Tabernacle', 'the Heavens a Tabernacle')
    t = re.sub(r'\S*[<>{}^]\S*[<>{}^]\S*', ' ', t)
    for ch in '■♦•«»^~*°_·':
        t = t.replace(ch, '')
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def chapters_of(lines, start, end):
    """walk one book's body, split at Chap. headings, count sequentially"""
    chs, cur = [], None
    for raw in lines[start + 1:end]:
        s = raw.rstrip()
        if HEAD.match(s):
            cur = {'no': len(chs) + 1, 'blocks': [[s.strip()]], 'inhead': True}
            chs.append(cur)
            continue
        if cur is None:
            continue
        if FOOTNOTE.match(s):
            cur['infn'] = True
            DROPPED.append(('fn', s.strip()[:70]))
            continue
        if cur.get('infn'):
            if not s.strip():
                cur['infn'] = False
            else:
                DROPPED.append(('fn+', s.strip()[:70]))
            continue
        if any(rx.match(s) for rx in NOISE):
            if s.strip():
                DROPPED.append(('noise', s.strip()[:70]))
            continue
        if not s.strip():
            if cur['blocks'][-1]:
                cur['blocks'].append([])
            cur['inhead'] = False
            continue
        if cur['inhead']:
            cur['blocks'][0].append(s.strip())
        else:
            cur['blocks'][-1].append(s.strip())
    return chs

# book -> chapter walk boundaries
marks = {}
for b, (lines, mark) in BOOK_MARK.items():
    marks[b] = (lines, find_mark(lines, mark))
ends = {}
for b in BOOK_MARK:
    lines, i = marks[b]
    later = [j for bb, (l2, j) in marks.items() if l2 is lines and j > i]
    ends[b] = min(later) if later else len(lines)

sections, total = [], 0
for b, wanted in SELECT.items():
    lines, i = marks[b]
    chs = chapters_of(lines, i, ends[b])
    for c in chs:
        if c['no'] not in wanted:
            continue
        blocks = [bl for bl in c['blocks'] if bl]
        head = clean(' '.join(blocks[0]))
        # "Chap. ix. — Title." -> title
        m = re.match(r'^C[Hh][Aa][Pp]\S{0,2}\s*[ivxlc]{0,5}\S{0,2}\s*[—\-]+\s*(.+)$', head)
        title = clean(m.group(1)) if m else head
        paras = [clean(' '.join(bl)) for bl in blocks[1:]]
        paras = [p for p in paras if len(p) > 4 or re.search(r'[a-z]{2}', p)]
        # stray second lines of Markham's Spanish-verse footnotes (the blank
        # line inside the note ends the footnote-block drop too early)
        paras = [p for p in paras if not p.startswith(('A inquirir de Nilo',
                                                       'Que ignora el mundo'))]
        # a short lowercase-opening first paragraph is the title's runover
        while paras and len(paras[0]) < 45 and paras[0][:1].islower():
            title = clean(title.rstrip('.') + ' ' + paras.pop(0))
        merged = []
        for p in paras:
            if merged and (p[:1].islower() or p[:1] in ')(' or p[:1].isdigit()):
                merged[-1] = clean(merged[-1] + ' ' + p)
            else:
                merged.append(p)
        # a paragraph broken at a page turn can end on its conjunction: stitch
        i2 = 0
        while i2 < len(merged) - 1:
            if merged[i2].endswith(' and'):
                merged[i2] = clean(merged[i2] + ' ' + merged.pop(i2 + 1))
            else:
                i2 += 1
        # the printed note after II.14 becomes a labelled unit, not a stray line
        labels = {}
        merged2 = []
        for p in merged:
            if p.rstrip('.') == 'An advertisement to the Reader':
                labels[len(merged2)] = 'An advertisement to the Reader'
                continue
            merged2.append(p)
        merged = merged2
        units = []
        for k, p in enumerate(merged, start=1):
            u = {'n': k, 'k': k, 'en': p}
            if labels.get(k - 1):
                u['label'] = labels[k - 1]
            units.append(u)
        total += len(units)
        sections.append({
            'id': f'b{b}c{c["no"]}',
            'zk': f'Acosta {ROMAN[b-1]}, c. {c["no"]}',
            'titel': f'Book {ROMAN[b-1]}, Chapter {c["no"]} — {title.rstrip(".")}',
            'units': units,
        })

assert len(sections) == sum(len(v) for v in SELECT.values()), \
    f'expected {sum(len(v) for v in SELECT.values())} chapters, got {len(sections)}'

out = {
 'id': 'acosta',
 'autor': 'José de Acosta',
 'titel': 'The Natural and Moral History of the Indies (1590, selections)',
 'jahr': '1590',
 'lang': 'en',
 'zitierweise': 'Acosta B, c. N [k]',
 'quelle': ("English: Edward Grimston's translation of 1604, as reprinted by the Hakluyt "
            "Society — The Natural & Moral History of the Indies, ed. Clements R. Markham, "
            "2 vols. (London, 1880; Internet Archive naturalmoralhist01acos and "
            "naturalmoralhist61acosrich) — a 1604 translation in an 1880 printing, in the "
            "United States public domain twice over. Eleven chapters are carried, cut to "
            "the module's argument: I.1 and I.9 on the authorities and the new world, "
            "II.6, II.9 and II.14 on the burning zone, IV.6–7 on Potosí, and VI.1, VI.4, "
            "VI.7 and VI.8 on the reason, writing and reckoning of the Indians. "
            "Grimston's orthography of 1604 is kept as printed; Markham's editorial "
            "footnotes are omitted; obvious OCR slips are emended against the sense. The "
            "Spanish original (Historia natural y moral de las Indias, Seville 1590) is "
            "named as source but not yet carried."),
 'hinweis': ("A Jesuit empiricism before the word: Acosta crossed the equator, felt cold "
             "where Aristotle promised uninhabitable fire, and wrote it down — 'What "
             "could I else do then but laugh?' The world line's counterpart to Xavier: "
             "where the letters carry the mission, the Historia carries the observation, "
             "down to its defence of the rationality of peoples who reckon without "
             "letters. Cited by book and chapter of the 1590 arrangement as the 1604 "
             "English prints it; the paragraph numbers are this site's own. Part of the "
             "concordance and the citation-bound dialogue; not part of the linguistic "
             "statistics, which describe the core corpus only."),
 'sections': sections,
}

path = os.path.join(REPO, 'data', 'acosta.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', total, 'units in', len(sections), 'chapters')
for s in sections:
    print(' ', s['zk'], '|', len(s['units']), '¶ |', s['titel'][:72])
if '--dropped' in sys.argv:
    print('--- dropped lines ---')
    for kind, l in DROPPED:
        print('  ', kind, '|', repr(l))
