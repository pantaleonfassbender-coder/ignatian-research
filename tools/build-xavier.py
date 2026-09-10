# -*- coding: utf-8 -*-
# Build data/xavier.json — Francis Xavier, Letters from India and Japan
# (selections), in the English of H. J. Coleridge, The Life and Letters of
# St. Francis Xavier, 2 vols. (London: Burns and Oates, 1872; Internet
# Archive lifelettersofstf01cole / lifelettersofstf02cole, public domain).
#
# Coleridge quotes the letters complete inside a running biography, with
# long small-type footnotes. The two volumes need different handling:
# vol. I's PDF text layer is line-granular, so the letter there is cut from
# the djvu text (whose blank lines carry the paragraphing) with the numbered
# footnotes dropped; vol. II's PDF text layer has paragraph blocks with
# usable font sizes, so its letters are cut from body-type blocks (median
# size separates body cleanly from footnotes and running heads). In the
# great Kagoshima letter the book interrupts the text once for commentary —
# the two installments are rejoined.
#
# Usage: python tools/build-xavier.py cole1.txt cole2.pdf
import io, json, os, re, statistics, sys
import fitz

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
v1 = io.open(sys.argv[1], encoding='utf-8').read().splitlines()
doc2 = fitz.open(sys.argv[2])

def norm(t):
    return re.sub(r'\s+', ' ', t).strip()

# ------------------------------------------------------------- vol. I (djvu)
NOISE = re.compile(r"^\s*[l\dI\s*'~•_]{1,10}$"
                   r"|^\s*\d{0,3}\s*(St\s*[.,]?\s*Franc\w*\s*Xav\w*|Among\s+the\s+Paravas)"
                   r"\s*[.,]?\s*[l\d]{0,3}\s*$")
FOOT = re.compile(r'^\d{1,2}\s+\S')   # numbered footnote at paragraph start

def paras_v1(lines):
    out, cur = [], []
    for l in lines:
        if NOISE.match(l):
            continue
        if re.match(r'^\d{1,2}\s{2}\S', l):   # footnote line glued mid-paragraph
            continue
        if not l.strip():
            if cur:
                out.append(' '.join(cur)); cur = []
            continue
        cur.append(l.strip())
    if cur:
        out.append(' '.join(cur))
    keep = []
    for p in out:
        if FOOT.match(p) or '(Orig.)' in p:
            continue
        if 'deturbatur' in p:      # stray continuation line of a Latin footnote
            continue
        keep.append(p)
    return keep

def segment_v1(start, end):
    i = next(k for k, l in enumerate(v1) if start in l)
    j = next(k for k in range(i + 1, len(v1)) if end in v1[k])
    return v1[i:j + 1]

# ------------------------------------------------------------ vol. II (PDF)
def body_blocks(page, y_min=None, y_max=None):
    out = []
    for b in page.get_text('dict')['blocks']:
        spans = [s for l in b.get('lines', []) for s in l['spans']]
        if not spans:
            continue
        if y_min is not None and b['bbox'][1] < y_min:
            continue
        if y_max is not None and b['bbox'][1] >= y_max:
            continue
        med = statistics.median([s['size'] for s in spans])
        txt = norm(' '.join(s['text'] for s in spans))
        txt = re.sub(r'^[\s_\-{}\[\]|~•]+', '', txt)   # leading OCR junk, so
        # a running head glued to the top of a page-turn block: a short
        # capitalized phrase + page number, then the lowercase continuation
        txt = re.sub(r'^[A-Z][A-Za-z ]{2,30}[,.]\s*\d{1,3}(\s\d{1,2})?\s+(?=[a-z])', '', txt)
        if 6.7 <= med <= 8.9 and len(txt) > 2:         # join() sees the case
            out.append(txt)
    return out

def find_page(needle, lo=0):
    for i in range(lo, len(doc2)):
        if needle in norm(doc2[i].get_text()):
            return i
    raise SystemExit(f'anchor not found: {needle!r}')

def extract2(start, end):
    """Body blocks from the block containing `start` down to the printed
    `end` (the dateline may sit in small type: blocks below its y are cut)."""
    p0 = find_page(start)
    p1 = find_page(end, lo=p0)
    if p1 == p0:
        t0 = norm(doc2[p0].get_text())
        if t0.index(end) < t0.index(start):   # a previous letter's dateline
            p1 = find_page(end, lo=p0 + 1)
    # the dateline's vertical position on its page, via its first words
    probe = end.split(',')[0]
    rects = doc2[p1].search_for(probe)
    y_end = rects[-1].y0 + 1 if rects else None
    blocks = []
    for i in range(p0, p1 + 1):
        for t in body_blocks(doc2[i], y_max=(y_end if i == p1 else None)):
            if i == p0 and not blocks and start not in t:
                continue
            if i == p0 and not blocks:
                t = t[t.index(start):]
            if end in t:
                blocks.append(t[:t.index(end) + len(end)])
                return blocks
            blocks.append(t)
    return blocks

def join(blocks):
    out = []
    for t in blocks:
        if out and (t[:1].islower() or out[-1].endswith('-')):
            out[-1] = (out[-1][:-1] + t) if out[-1].endswith('-') else (out[-1] + ' ' + t)
        else:
            out.append(t)
    return out

# ---------------------------------------------------------------- cleaning
WORD_FIXES = {
    'fapan': 'Japan', 'Fapan': 'Japan', 'fapanese': 'Japanese',
    'Fesus': 'Jesus', 'Sfesus': 'Jesus', 'fesus': 'Jesus',
    'Fanuary': 'January', 'buils': 'bulls', 'prought': 'brought',
    'af the people': 'if the people', 'So hy the': 'So by the',
    'rtien': 'men',
}
def clean(t):
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)
    for a, b in WORD_FIXES.items():
        t = t.replace(a, b)
    t = t.replace('{', '').replace('[', '').replace(']', '').replace('|', '').replace('~', '')
    # running heads and quire signatures glued mid-paragraph
    t = re.sub(r'(?:^|\s)(?:\d{1,3}[;,.]?\s+)?S[tf]\s*[.,]?\s*Franc\w*\s*Xav\w*\s*[.,]?(?:\s*l?\d{1,3}[;,.]?)?\s', ' ', t)
    t = re.sub(r'(?:^|\s)[®©»°]?\s*(?:Among\s+the\s+Paravas|Security\s+in\s+Religion|Hopes\s+for\s+the\s+Future)\s*[.,]?\s*[l\d]{0,3}(\s\d{1,2})?(?=\s)', ' ', t)
    t = re.sub(r'\sVOL[,.]\s*I+L?[,.]?\s*R?\s*t?\s*\d{1,3}[;,.]?\s', ' ', t)
    # OCR symbol debris: footnote daggers and superscripts, broken exclamations
    t = t.replace(',!°', ',').replace('!®', '!').replace('.!®', '.')
    t = t.replace('€x', 'ex').replace(' /’', '!’').replace(' / ', ' ! ')
    for ch in '®©»°$€^':
        t = t.replace(ch, '')
    t = t.replace('*', ' ')
    t = t.replace('to facel It', 'to face! It')
    # footnote reference digits glued to a word or its closing punctuation
    # (never after a digit or space, so years and dates survive)
    t = re.sub(r"([.,;:!?\'’”])\d{1,2}(\s|$)", r'\1\2', t)
    t = re.sub(r'([a-z])\d{1,2}(\s)', r'\1\2', t)
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    return norm(t)

def finish(paras, dateline):
    ps = [clean(p) for p in paras]
    ps = [p for p in ps if len(p) > 2]
    ps = [p for p in ps if not re.fullmatch(r'[-\s.,rt]*(FRANCIS|Francis)\s*[.,]?', p)]
    # page numbers, volume signatures and running heads left as whole units
    ps = [p for p in ps if not re.fullmatch(
        r"[il\dIo ]{2,6}|VOL[.,]?\s*I*L?[.,]?|\d{0,3}\s*S[tf][.,]?\s*Franc\w*\s*Xav\w*[.,]?\s*l?\d{0,3}[.,]?", p)]
    # fold signature + dateline into one closing unit
    while ps and (dateline in ps[-1] and len(norm(ps[-1])) < len(dateline) + 30):
        ps.pop()
    if ps:   # junk left where the dateline was cut away ('.., f')
        ps[-1] = re.sub(r'[\s,;|]+[a-z]?$', '', ps[-1])
    ps.append(f'Francis. — {dateline}.')
    return ps

def units(ps):
    return [{'n': k, 'k': k, 'en': p} for k, p in enumerate(ps, start=1)]

# ---------------------------------------------------------------- letters
seg1 = paras_v1(segment_v1('It  is  now  the  third  year  since  I left',
                           'From  Cochin,  Dec.  31,  1543'))
l1 = finish(seg1, 'From Cochin, Dec. 31, 1543')

k1 = extract2('I wrote to you at great length from Malacca',
              'by the rest of the people of the place.')
k2 = extract2('We shall write to you about Japan',
              'Cagoxima, Nov. 11, 1549')
l2 = finish(join(k1) + join(k2), 'Cagoxima, Nov. 11, 1549')

l3 = finish(join(extract2('I have just received at Malacca, on my return from Japan',
                          'Cochin, Jan. 29, 1552')),
            'Cochin, Jan. 29, 1552')

l4 = finish(join(extract2('By this letter I expressly command',
                          'Port of San Chan, November 13, 1552')),
            'Port of San Chan, November 13, 1552')

SECTIONS = [
 {'id': 'cochin1543', 'zk': 'FX I',
  'titel': 'To the Society at Rome — Cochin, 31 December 1543',
  'blurb': ("The great letter from the Fishery Coast: the Comorin mission, the "
            "catechism translated into Malabar, the baptisms — and the famous "
            "reproach to the learned of Europe, that multitudes are not made "
            "Christians 'because there is no one to make them Christians'."),
  'units': units(l1)},
 {'id': 'cagoxima1549', 'zk': 'FX II',
  'titel': 'To the Society at Goa — Cagoxima (Kagoshima), November 1549',
  'blurb': ("The first letter from Japan: the voyage on the pirate coast, the "
            "landing at Kagoshima on the Assumption of 1549, and the celebrated "
            "estimate of the Japanese. Coleridge prints the letter in two "
            "installments around his own commentary; they are rejoined here. "
            "His closing dateline reads November 11; the letter is usually "
            "dated November 5."),
  'units': units(l2)},
 {'id': 'cochin1552', 'zk': 'FX III',
  'titel': 'To Father Ignatius at Rome — Cochin, 29 January 1552',
  'blurb': ("Back from Japan: 'O, my true Father!' — the report to Ignatius, "
            "the turn toward China, and the tenderest surviving statement of "
            "the bond between the two men."),
  'units': units(l3)},
 {'id': 'sancian1552', 'zk': 'FX IV',
  'titel': 'To Fathers Perez and Baertz — Sancian, 13 November 1552',
  'blurb': ("The last letter. Barred from the Chinese mainland at Sancian "
            "island, Xavier demands the canonical penalty against the man who "
            "blocked the mission; three weeks later he was dead within sight "
            "of the coast."),
  'units': units(l4)},
]

out = {
 'id': 'xavier',
 'autor': 'Francis Xavier',
 'titel': 'Letters from India and Japan (selections)',
 'jahr': '1543–1552',
 'lang': 'en',
 'zitierweise': 'FX I–IV [k]',
 'quelle': ("English: H. J. Coleridge, The Life and Letters of St. Francis "
            "Xavier, 2 vols. (London: Burns and Oates, 1872), which quotes the "
            "letters complete inside a running biography; Internet Archive "
            "scans, public domain. Four letters are carried, cut at their "
            "printed openings and datelines; Coleridge's commentary and "
            "footnotes are omitted. The Latin and Spanish originals are in the "
            "Monumenta Xaveriana (1899–1912), not yet carried."),
 'hinweis': ("A selection, not an edition: four letters out of Coleridge's "
             "hundred and forty, chosen as the classic anthology pieces of the "
             "mission to the East — Comorin, Japan, the report to Ignatius, "
             "and the last letter from Sancian. Paragraph numbers are this "
             "site's own, per letter. Part of the concordance and the citation-bound dialogue; not part of the linguistic statistics, which describe the core corpus only."),
 'sections': SECTIONS,
}

path = os.path.join(REPO, 'data', 'xavier.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', sum(len(s['units']) for s in SECTIONS), 'units:',
      {s['zk']: len(s['units']) for s in SECTIONS})
