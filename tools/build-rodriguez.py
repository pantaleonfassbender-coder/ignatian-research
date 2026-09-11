# -*- coding: utf-8 -*-
# Build data/rodriguez.json — Alonso Rodríguez, Practice of Christian
# Perfection, the Eighth Treatise of the First Part: "Of Conformity to the
# Will of God", complete in the anonymous English translation of the
# three-volume edition of 1861 (Dublin: James Duffy; London, 1861 - made, as
# its title page states, from the French of the Abbe Regnier-Desmarais;
# Internet Archive
# PracticeOfChristianAndReligiousPerfectionV1, US public domain).
#
# The Ejercicio de perfección (Seville 1609) was the daily curriculum of
# Jesuit formation for three centuries; this treatise — its most celebrated
# — is the school of discernment as doctrine of life, and the direct
# ancestor of the Abandonment attributed to Caussade. Rodríguez is cited by
# treatise and chapter; the paragraph numbers within each chapter are this
# site's own. The OCR of the 1861 printing is good; running heads, page
# numbers and scanner artefacts are stripped, damaged chapter headings
# repaired against the table of contents (chapters are strictly sequential,
# so a mangled roman numeral cannot mislead), and the printing's broken
# opening quotation marks (**, *', 44, u) restored.
#
# Usage: python tools/build-rodriguez.py rodr1861.txt
import io, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = io.open(sys.argv[1], encoding='utf-8').read().splitlines()

# Treatise VIII body: from its half-title to the volume colophon
start = next(i for i in range(20000, len(lines)) if 'THE  EIGHTH  TREATISE' in lines[i])
end = next(i for i in range(start, len(lines)) if 'END  OF  VOLUME' in lines[i])
body = lines[start + 1:end]

NOISE = [
    re.compile(r'^\s*(Digitized|Google)\b'),
    re.compile(r'^\s*\d{0,4}\s*[„"]?\s*(OF|OP|0F)\s+C[O0]NF'),  # recto head, w/ page no.
    re.compile(r'^\s*TH[EB]\s+W\S{0,5}\s+OF\b'),                 # THE WILL OF GOD + kin
    re.compile(r'^\s*THE\s+EIGHTH\s+TREATISE'),
    re.compile(r'^\s*CONFORMITY\s+TO\s+THE\s+WILL'),             # the half-title
    re.compile(r'^\s*VOL\.?\s*I\b'),                             # quire signatures
    re.compile(r'^\s*[0-9]{1,3}\s*$'),
    re.compile(r"^\s*[ivxlcIVXLC0-9 .,*^~•£_'\-]{1,10}\s*$"),
]
HEAD = re.compile(r'^\s*CHAPTE\S*')

# Chapter titles the OCR damaged beyond word repair, restored from the
# volume's own table of contents:
TITLE_FIX = {
    31: ('The Conformity we are to have to the Will of God, in the Gifts '
         'of Glory.'),
}

WORD_FIXES = {
    'Cmforrnity': 'Conformity', 'Religions should': 'Religious should',
    'Religions is': 'Religious is', 'example.\',': 'example."',
    'tie sand': 'ties and', 'profit* able': 'profitable',
    'nt>t': 'not', '\\>e': 'be', 'cxviii. Z%': 'cxviii. 32',
    'm^erit': 'merit', 'these^': 'these', '■were': 'were',
    '♦explains': 'explains', '•f good': 'of good', '• passage': 'passage',
    'earth;~and': 'earth; and',
    'ov$r': 'over', 'som%': 'some', 'barra/mess': 'barrenness',
    # a quire signature glued into the running text at a page turn
    'con- voi». i. 2 o tinue': 'continue',
    'C^sarius': 'Caesarius', 'WUl': 'Will',
    'TnAT this': 'That this', 'asSt.': 'as St.',
    'the man T spoke': 'the man I spoke',
    "John, six. '11.": 'John, xix. 11.',
    "die,*'": 'die,"',
    'to reduce. by frequent': 'to reduce, by frequent',
}

def clean(t):
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)
    t = re.sub(r'\s+', ' ', t).strip()
    for a, b in WORD_FIXES.items():
        t = t.replace(a, b)
    # running heads glued mid-paragraph at page turns (with page number,
    # in any state of decay), and tokens shredded past recognition
    t = re.sub(r'(?:^|\s)\d{0,4}\s*[„"]?\s*[0OQy)(]{0,3}[PF]?\s*C[O0]NFORMITY\s+T[O0](?:\s*[yj]?TH[EB]?\b)?[^.]{0,25}[).]?', ' ', t)
    t = re.sub(r'\S*[<>{}^]\S*[<>{}^]\S*', ' ', t)
    # the printing's quotation marks, broken by the OCR
    t = re.sub(r'(^|\s)(\*\*|\*[•\'’]|\'\*|\*|44|4t|4<|<4|<\{|<£|£<|\'<|4\\|c<|6<|<\(|<c|fi€|["\'’]?«["\'’]?|„)\s*(?=[A-Za-z])', r'\1"', t)
    t = re.sub(r'(\s)u\s+(?=\w)', r'\1"', t)
    t = t.replace("/ '", '." ').replace("/*", '."').replace("/'", '."')
    # asterisk as a broken full stop or as glue between words
    t = re.sub(r"([a-z]),?\*\\?['’]?\s*(?=[A-Z\"])", r'\1. ', t)
    t = re.sub(r'([a-z]),\*(?=[a-z])', r'\1, ', t)
    t = re.sub(r'([a-z])\*(?=[a-z])', r'\1 ', t)
    t = re.sub(r'([a-z])\*(?=[\s.,])', r'\1', t)
    t = re.sub(r'([?!.])\*(?=\s|$)', r'\1', t)   # footnote asterisks
    t = re.sub(r'([a-z])\*$', r'\1.', t)         # asterisk as a broken full stop
    t = re.sub(r'\s%\s', ' ', t)
    for ch in '■♦•«»^~':
        t = t.replace(ch, '')
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

# walk: split into chapters at CHAPTE* lines (strictly sequential), then
# title = first block after the heading, paragraphs = blank-line blocks
chapters = []          # list of (no, title_lines, [para_lines...])
cur = None
for l in body:
    s = l.rstrip()
    if HEAD.match(s):
        cur = {'no': len(chapters) + 1, 'blocks': [[]]}
        chapters.append(cur)
        continue
    if cur is None:
        continue                       # half-title matter before chapter I
    if any(rx.match(s) for rx in NOISE):
        continue
    if not s.strip():
        if cur['blocks'][-1]:
            cur['blocks'].append([])
        continue
    cur['blocks'][-1].append(s.strip())

assert len(chapters) == 34, f'expected 34 chapters, found {len(chapters)}'

# The OCR shuffled the page at the head of chapter IX: the chapter's title
# ("Of some other Helps...") and the opening lines of its first paragraph
# were emitted BEFORE the "CHAPTER IX." line — so they land at the end of
# chapter VIII — while the block that follows the heading is that first
# paragraph's continuation. Put the page back together.
b8 = [b for b in chapters[7]['blocks'] if b]
b9 = [b for b in chapters[8]['blocks'] if b]
assert 'easy' in ' '.join(b8[-2]) and 'TnAT' in ' '.join(b8[-1])[:8], \
    'chapter IX shuffle not where expected'
assert ' '.join(b9[0]).lstrip().startswith('to  us'), \
    'chapter IX continuation not where expected'
chapters[8]['blocks'] = [b8[-2], b8[-1] + b9[0]] + b9[1:]
chapters[7]['blocks'] = b8[:-2]

ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII',
         'XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII','XXIII','XXIV',
         'XXV','XXVI','XXVII','XXVIII','XXIX','XXX','XXXI','XXXII','XXXIII','XXXIV']

# the volume's final page carries a library stamp that shredded the OCR;
# the closing sentences were re-transcribed from the page image (p. 522)
END_REPAIR = ('earth what we are hereafter to repeat for eternity in heaven. It is here we '
              'must begin to enkindle in ourselves the fire of the love of God. But since '
              'this "divine fire has its source in Sion and its furnace in Jerusalem" '
              '(Isa. xxxi. 9), it will never attain the perfection of a full blaze till we '
              'arrive in the heavenly Jerusalem, i. e., till we attain the felicity of glory.')

JUNK = [
    re.compile(r'^[0-9]{1,3}[A-Za-z]?\.?$'),                      # page numbers (4G0, 39S)
    re.compile(r'^vo[li]\.?\s*[ix.,]{0,4}\s*\d?\s*[a-z]?\.?$', re.I),   # quire signatures
    re.compile(r'^[„"]?\s*[0O]?[PF]?\s*C\w{0,12}TY\s+T[O0]\b.*$'),      # running heads,
    re.compile(r'^T\S{0,3}\s+W\S{0,5}\s+OF\s+G\S{0,4}\.?$'),            # however decayed
]

sections = []
total = 0
for c in chapters:
    blocks = [b for b in c['blocks'] if b]
    title = TITLE_FIX.get(c['no']) or clean(' '.join(blocks[0]))
    paras = [clean(' '.join(b)) for b in blocks[1:]]
    if c['no'] in TITLE_FIX:
        # the damaged page also mangles the printed title block: drop it
        paras = [p for p in paras if len(p) > 60 or not re.search(r'[\^~]', p)]
    if c['no'] == 34:
        paras = [END_REPAIR if 'divine fire has its sour' in p else p for p in paras]
    paras = [p for p in paras if len(p) > 2 and not any(rx.match(p) for rx in JUNK)]
    # a short lowercase-opening first block is the chapter title's runover
    while paras and len(paras[0]) < 45 and paras[0][:1].islower():
        title = title.rstrip('.') + ' ' + paras.pop(0)
        title = clean(title)
    # a paragraph that opens lowercase (or as a citation tail) continues its
    # predecessor across a page turn
    merged = []
    for p in paras:
        if merged and (p[:1].islower() or p[:1] in ')('):
            merged[-1] = clean(merged[-1] + ' ' + p)
        else:
            merged.append(p)
    paras = merged
    units = [{'n': k, 'k': k, 'en': p} for k, p in enumerate(paras, start=1)]
    total += len(units)
    sections.append({
        'id': f'c{c["no"]}',
        'zk': f'Rodr. VIII, c. {c["no"]}',
        'titel': f'Chapter {ROMAN[c["no"]-1]} — {title.rstrip(".")}',
        'units': units,
    })

out = {
 'id': 'rodriguez',
 'autor': 'Alonso Rodríguez',
 'titel': 'Of Conformity to the Will of God — the Eighth Treatise (1609)',
 'jahr': '1609',
 'lang': 'en',
 'zitierweise': 'Rodr. VIII, c. N [k]',
 'quelle': ("English: the anonymous translation printed in The Practice of Christian and "
            "Religious Perfection, vol. I (Dublin: James Duffy; London, 1861; Internet Archive "
            "PracticeOfChristianAndReligiousPerfectionV1), in the United States public "
            "domain — made, as its title page states, not from the Spanish but from the "
            "French version of the Abbé Régnier-Desmarais of the Académie française: the "
            "classic transmission chain of this book, carried here as it stands. The "
            "treatise is carried complete, all thirty-four chapters; damaged "
            "chapter headings were repaired against the volume's own table of contents, "
            "and the printing's quotation marks restored where the OCR broke them. The "
            "Spanish original (Ejercicio de perfección y virtudes cristianas, Seville "
            "1609, part I, treatise VIII) is named as source but not yet carried; the "
            "1609 first printing and several 19th-century Spanish editions are on the "
            "Internet Archive."),
 'hinweis': ("The school of discernment as a daily curriculum: Rodríguez's Ejercicio de "
             "perfección (1609) was read aloud in Jesuit novitiates for three centuries, "
             "and this, its most celebrated treatise, is the one the tradition kept "
             "closest — conformity to the will of God carried through content and "
             "calamity, sickness, aridity in prayer, and death. It is the direct ancestor "
             "of the Abandonment attributed to Caussade, which the programme names as a "
             "later module. Rodríguez is cited by treatise and chapter; the paragraph "
             "numbers within each chapter are this site's own. Part of the concordance "
             "and the citation-bound dialogue; not part of the linguistic statistics, "
             "which describe the core corpus only."),
 'sections': sections,
}

path = os.path.join(REPO, 'data', 'rodriguez.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', total, 'units in', len(sections), 'chapters')
for s in sections[:5]:
    print(' ', s['zk'], '|', len(s['units']), '¶ |', s['titel'][:70])
