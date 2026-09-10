# -*- coding: utf-8 -*-
# Build data/monita.json — the Monita secreta (1614), the forged 'secret
# instructions' of the Society, carried as the debate it forced, not as
# truth. Latin and English from W. C. Brownlee's edition of 1857 (New York;
# Internet Archive instructiosecret00browrich, US public domain), which
# prints the Latin and an English translation on facing pages, chapter by
# chapter, with numbered articles on both sides — the alignment grid.
#
# The OCR of the 1857 stereotype print is serviceable; systematic ligature
# losses (ae -> se) and recurrent misreads are repaired by the fix lists
# below, residual errors emended against the sense. Running heads and page
# numbers are filtered out.
#
# Usage:
#   python tools/build-monita.py                # fetch the djvu OCR from IA
#   python tools/build-monita.py brownlee.txt   # use a local dump
import io, json, os, re, sys, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://archive.org/download/instructiosecret00browrich/instructiosecret00browrich_djvu.txt'

if len(sys.argv) > 1:
    raw = io.open(sys.argv[1], encoding='utf-8').read()
else:
    req = urllib.request.Request(URL, headers={'User-Agent': 'ignatiana-build/1.0'})
    raw = urllib.request.urlopen(req, timeout=120).read().decode('utf-8')

lines = raw.splitlines()
start = next(i for i, l in enumerate(lines) if 'SECEETA' in l or 'SECRETA' in l and 'MONITA' in l)
end = next(i for i, l in enumerate(lines) if i > start and 'MORALITY' in l and 'JESUITS' in l)
region = lines[start:end]

ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
         'XIII', 'XIV', 'XV', 'XVI', 'XVII']
r2i = {r: i + 1 for i, r in enumerate(ROMAN)}
def roman_to_int(tok):
    """r2i with repair of the OCR's I->L confusion (CAPUT XL for XI etc.)."""
    if tok in r2i:
        return r2i[tok]
    fixed = tok.replace('L', 'I')
    return r2i.get(fixed, 0)

NOISE = re.compile(r'^\s*(\d+|[A-Z][A-Z\'\s\.\,]{4,})\s*$')
HEAD_LA = re.compile(r'^\s*CAPUT\s+([IVXL]+)')
HEAD_EN = re.compile(r'^\s*CHAP(?:TER)?\.?\s+([IVXL]+)')
ART_LA = re.compile(r'^\s*(\d{1,2})\s*[.,]\s+(.*)')
ART_EN = re.compile(r'^\s*([IVXL]{1,5})\s*[.,]\s+(.*)')

def latinish(s):
    la = len(re.findall(r'\b(et|in|ad|ut|cum|quod|non|si|est|sunt|qui|quae|quse|ne|pro|ex|atque|vel|aut|sed|nisi|erga|apud)\b', s))
    en = len(re.findall(r'\b(the|and|of|to|that|with|which|they|be|shall|let|for|their|them|are|will|not|by)\b', s))
    return la > en

# walk: route paragraphs into per-chapter La/En article lists
cur = {'la': 0, 'en': 0}          # current chapter per side
arts = {'la': {}, 'en': {}}        # side -> chapter -> list of (artno, [text..])
open_art = {'la': None, 'en': None}
titles = {'la': {}, 'en': {}}
pending_title = {'la': None, 'en': None}

def flush_title(side):
    if pending_title[side] is not None and cur[side]:
        titles[side].setdefault(cur[side], pending_title[side])
        pending_title[side] = None

para = []
def emit(paragraph):
    text = ' '.join(paragraph).strip()
    if not text:
        return
    mla, men = HEAD_LA.match(text), HEAD_EN.match(text)
    if mla:
        cur['la'] = roman_to_int(mla.group(1)) or cur['la']
        open_art['la'] = None
        pending_title['la'] = ''
        return
    if men:
        cur['en'] = roman_to_int(men.group(1)) or cur['en']
        open_art['en'] = None
        pending_title['en'] = ''
        return
    side = 'la' if latinish(text) else 'en'
    if cur[side] == 0:
        return                                     # front matter before ch. 1
    m = (ART_LA if side == 'la' else ART_EN).match(text)
    if m:
        flush_title(side)
        no = int(m.group(1)) if side == 'la' else roman_to_int(m.group(1))
        if no:
            arts[side].setdefault(cur[side], []).append((no, [m.group(2)]))
            open_art[side] = (cur[side], no)
            return
    if pending_title[side] == '':
        pending_title[side] = text
        return
    tgt = open_art[side]
    if tgt and tgt[0] == cur[side] and arts[side].get(cur[side]):
        arts[side][cur[side]][-1][1].append(text)

for l in region:
    s = l.strip()
    if not s:
        emit(para); para = []
        continue
    if NOISE.match(s) and not HEAD_LA.match(s) and not HEAD_EN.match(s) \
       and not ART_EN.match(s):
        continue                                   # running heads, page nos.
    para.append(s)
emit(para)

def dehyph(t):
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)
    t = re.sub(r'[\^°·]+', '', t)
    return re.sub(r'\s+', ' ', t).strip()

WORD_FIXES = {
    'lucruin': 'lucrum', 'etiarn': 'etiam', 'quern': 'quem', 'quibns': 'quibus',
    'potissitnum': 'potissimum', 'strunntur': 'struantur', 'certain': 'certum',
    'addietorum': 'addictorum', 'Indus': 'Indiis', 'capitals': 'capitale',
    'primaries': 'primarios', 'submin-istranint': 'subministrarint',
    'subministranint': 'subministrarint', 'gegris': 'aegris', 'gegros': 'aegros',
    'segris': 'aegris', 'segros': 'aegros', 'segrotos': 'aegrotos',
    'segroto': 'aegroto', 'segrotum': 'aegrotum', 'segrotis': 'aegrotis',
    'proe': 'prae', 'templaesedificantur': 'templa aedificantur',
    'UtiJiter': 'Utiliter', 'huinilia': 'humilia', 'prorapte': 'prompte',
    'dome-rum': 'domorum', 'preediorum': 'praediorum', 'bononim': 'bonorum',
    'gravammum': 'gravaminum', 'raoneat': 'moneat', 'coiietur': 'conetur',
    'etomni': 'et omni', 'efficaci-ssime': 'efficacissime',
    'divincicndi': 'divinciendi', 'aniniandi': 'animandi',
    'sucaesaerit': 'successerit', 'sucaesserit': 'successerit',
    'frequentendam': 'frequentandam',
    'nostroruin': 'nostrorum', 'moduin': 'modum', 'salvatorern': 'salvatorem',
    'Venotos': 'Venetos', 'utiiitatis': 'utilitatis',
    # verified in context after narrowing the ligature classes
    'sinssepe': 'sint saepe', 'ipssemet': 'ipsaemet',
    'lisereditatem': 'haereditatem', 'professes': 'professos',
    'expresses': 'expressos', 'morosse': 'morosae', 'professse': 'professae',
    'essse': 'esse', 'dessentiones': 'dissensiones',
    'prasseindere': 'praescindere', 'causse': 'causae',
    'prassertim': 'praesertim', 'prasstans': 'praestans',
    'Imjusmodi': 'hujusmodi', 'quue': 'quae', 'Prxter': 'Praeter',
    'pcccato': 'peccato', 'prcecipue': 'praecipue', 'dolerido': 'dolendo',
    'nee': 'nec', 'mognae': 'magnae', 'mognce': 'magnae',
    # chapter-heading debris, verified against the page images
    # (the print's own oddities — 'viduarem', 'devotorium' in c. VIII,
    # 'privatae' in c. X — are carried as printed, not emended)
    'viduce': 'viduae', 'filice': 'filiae',
    'conaervandae': 'conservandae', 'prcestare': 'praestare',
    'deleat': 'debeat', 'magnet turn': 'magnatum', 'gui': 'qui',
    'guamvis': 'quamvis', 'Qua commendata': 'Quae commendata',
    'utfilii': 'ut filii', 'etfilice': 'et filiae', 'Quomod6': 'Quomodo',
    'disciplines': 'disciplinae', 'rigore private': 'rigore privatae',
    'detectu': 'delectu', 'juvenuin': 'juvenum',
    'adinittendorum': 'admittendorum',
    'quce': 'quae', 'mahorneticce': 'mahometicae',
}

# Latin chapter headings the OCR lost entirely or damaged beyond word fixes,
# each transcribed from the rendered page images of the 1857 printing
# (accents of the print dropped, as everywhere in this transcription):
LA_TITLES = {
    2:  "Quomodo principum, magnatum et primariorum PP. societatis "
        "familiaritatem acquirent et conservabunt.",
    6:  "De conciliandis societati viduis opulentis.",
    9:  "De reditibus collegiorum augendis.",
    11: "Qualiter se nostri unanimiter praestabunt contra dimissos e societate.",
    12: "Quinam conservari ac foveri in societate debeant.",
    14: "De casibus reservatis, et causa dimittendi e societate.",
    16: "De contemptu divitiarum palam prae se ferendo.",
    17: "De mediis promovendi societatem.",
}
def fix_la(t):
    t = dehyph(t)
    t = t.replace('qu&', 'quae')
    for a, b in WORD_FIXES.items():
        t = re.sub(r'\b' + re.escape(a) + r'\b', b, t)
    t = re.sub(r'\bprse', 'prae', t).replace('Prse', 'Prae')
    t = re.sub(r'\bquse', 'quae', t).replace('Quse', 'Quae')
    t = re.sub(r'\bcse', 'cae', t).replace('Cse', 'Cae')
    t = re.sub(r'\bsse', 'sae', t).replace('Sse', 'Sae')   # ssepe, sseculares
    # 'ce' for 'æ' after a consonant at word end ('distrahendce', 'viduce'
    # via 'uce'? no — only consonant class): no Latin word ends consonant+ce,
    # except -sce (hujusce), so 's' and 'c' stay out of the class
    t = re.sub(r'(?<=[bdfgklmnprtv])ce\b', 'ae', t)
    # ligature loss ae -> se after a consonant, word-internal or final.
    # 's' is deliberately absent from the classes: genuine -sse- (esse,
    # necesse, possessiones ...) must not be turned into -sae-.
    t = re.sub(r'(?<=[bcdfghklmnpqrtvx])s(?=e\b)', 'a', t)
    t = re.sub(r'(?<=[bcdfghklmnpqrtvx])se(?=[dmnrst]\b|[dmnrst][a-z])',
               lambda m: 'ae', t)
    for a, b in WORD_FIXES.items():   # second pass: some keys only surface
        t = re.sub(r'\b' + re.escape(a) + r'\b', b, t)
    return t

def fix_en(t):
    return dehyph(t)

# ---------------------------------------------------------------- repairs
# Seventeen article boundaries were damaged in the OCR (numbers lost at page
# breaks or line damage, the article's text glued to its neighbour). Each
# repair below was verified against the page images of the 1857 printing:
# SPLITS cuts the glued text out of the host article at a marker that opens
# the lost article; ADDS supplies text lost entirely at a page break, with
# TRUNCS removing its glued tail from the host.
SPLITS = [   # (side, chapter, host_k, new_k, [markers], prefix lost at page break)
    ('en', 1, 7, 8,  ['In every province, let none'], ''),
    ('en', 6, 1, 2,  ['And let the same confessors persuade them'], ''),
    ('en', 7, 10, 11, ['Let this be deeply imprinted'], ''),
    ('en', 7, 17, 18, ['But since our expectations'], ''),
    ('en', 11, 1, 2, ['Let it be immediately published'], ''),
    ('en', 11, 7, 8, ['Let the misfortunes'], ''),
    ('en', 14, 1, 2, ['But if any one at the sacrament'], ''),
    ('en', 17, 7, 8, ['But if our hopes'], ''),
    ('la', 9, 2, 3,  ['affinibus, parentibus'],
     'Non negligant confessarii interrogare poenitentes suos (opportune tamen) de nomine, familia, '),
    ('la', 9, 4, 5,  ['titiam domorum', 'titiam dome', 'domorum, hortorum'],
     'Rectores collegiorum conabuntur habere no'),
    ('la', 14, 5, 6, ['Retinendi etiam'], ''),
]
ADDS = {     # (side, chapter, k) -> full text, hand-transcribed from the scan
    ('la', 1, 7): "Summum pretium a viduis semper extorquendum, inculcata illis summa nostra necessitate.",
    ('la', 2, 9): "Tam principes quam praelati aliique omnes qui societati favorem extraordinarium praestare possunt, participes faciendi sunt omnium meritorum societatis, exposito illis momento hujus summi privilegii.",
    ('la', 13, 5): "Munusculis ac privilegiis variis, aetati illorum conformibus, divinciendi sunt, et maxime colloquiis spiritualibus sunt animandi.",
    ('en', 2, 6): "How much the Society has benefited from their engagements in marriage treaties, the house of Austria and Bourbon; Poland and other kingdoms, are experimental evidences. Wherefore let such matches be with prudence picked out, whose parents are our friends, and firmly attached to our interests.",
    ('en', 2, 11): "It will be very proper to give invitations to such to attend our sermons and fellowships, to hear our orations and declamations, as also to compliment them with verses and theses; to address them in a genteel and complaisant manner, and at proper opportunities to give them handsome entertainments.",
    ('en', 3, 1): "All that has been before mentioned, may, in a great measure, be applied to these; and we must also be industrious to procure their favor against every one that opposes us.",
    ('en', 5, 1): "We must not be discouraged or beat down by this sort of men, but take proper opportunities, demonstrably to convince princes, and others in authority, who are in any way attached to our interest, that our order contains the perfection of all others, excepting only their cant and outward austerity of life and dress; but if another order should claim pre-eminence in any particular, that it is ours which shines with the greatest lustre in the Church of God.",
    ('en', 13, 8): "The more earnestly they desire admission into our Society, the longer let the grant of such favor be deferred, provided at the same time they seem stedfast in their resolution; but if their minds appear to be wavering, let all proper methods be used for the immediate firing of them.",
}
TRUNCS = [   # (side, chapter, host_k, [markers]) — cut host at marker, drop tail
    ('la', 2, 8, ['possunt, participes', 'possunt, parficipes']),
    ('la', 13, 4, ['conformibus, divin']),
    ('en', 2, 5, ['How much the Society', 'from their engagements in marriage']),
    ('en', 2, 10, ['It will be very proper', 'ons to such to attend our sermons']),
    ('en', 13, 7, ['The more earnestly', 'esire admission into our Society']),
]

def apply_repairs(la, en, c):
    both = {'la': la, 'en': en}
    for side, ch, host, new, markers, prefix in SPLITS:
        if ch != c: continue
        d = both[side]
        t = d.get(host)
        if not t:
            print(f'!! split {side} c{c} {host}->{new}: host missing'); continue
        pos = next((t.find(m) for m in markers if t.find(m) >= 0), -1)
        if pos < 0:
            print(f'!! split {side} c{c} {host}->{new}: marker not found'); continue
        tail = re.sub(r'^[A-Za-z]{1,5}[.,]\s+', '', t[pos:]).strip() if not prefix else t[pos:].strip()
        if prefix:
            tail = prefix + tail if (prefix[-1].isalnum() and tail[:1].islower()) else prefix.rstrip() + ' ' + tail
        d[host] = t[:pos].rstrip().rstrip('.,;') + '.'
        d[new] = tail
    for (side, ch, k), text in ADDS.items():
        if ch != c: continue
        both[side][k] = text
    for side, ch, host, markers in TRUNCS:
        if ch != c: continue
        d = both[side]
        t = d.get(host)
        if not t: continue
        pos = next((t.find(m) for m in markers if t.find(m) >= 0), -1)
        if pos >= 0:
            d[host] = t[:pos].rstrip().rstrip('.,;') + '.'

# assemble aligned units
sections = []
n = 0
for c in range(1, 18):
    la = {no: fix_la(' '.join(px)) for no, px in arts['la'].get(c, [])}
    en = {no: fix_en(' '.join(px)) for no, px in arts['en'].get(c, [])}
    apply_repairs(la, en, c)
    nos = sorted(set(la) | set(en))
    units = []
    for k in nos:
        n += 1
        u = {'n': n, 'k': k}
        if la.get(k): u['orig'] = la[k]
        if en.get(k): u['en'] = en[k]
        if not la.get(k): u['note'] = 'Latin article not recovered from the OCR; see the scan.'
        if not en.get(k): u['note'] = 'English article not recovered from the OCR; see the scan.'
        units.append(u)
    sections.append({
        'id': f'c{c}', 'zk': f'MS c. {ROMAN[c-1]}',
        'titel': fix_en(titles['en'].get(c) or '') or f'Chapter {ROMAN[c-1]}',
        'blurb': LA_TITLES.get(c) or fix_la(titles['la'].get(c) or ''),
        'units': units,
    })
    only_la = sorted(set(la) - set(en)); only_en = sorted(set(en) - set(la))
    print(f'c{c}: la {len(la)} / en {len(en)} -> {len(units)} units'
          + (f' | nur-LA: {only_la}' if only_la else '')
          + (f' | nur-EN: {only_en}' if only_en else ''))

out = {
 'id': 'monita',
 'autor': 'Monita secreta (forgery, 1614)',
 'titel': "Monita secreta — the forged 'secret instructions' (1614)",
 'jahr': 1614,
 'lang': 'la',
 'zitierweise': 'MS c. N [k]',
 'quelle': ("The Monita secreta first appeared in Kraków in 1614, the work of the dismissed "
            "Jesuit Hieronim Zahorowski; text here after W. C. Brownlee's edition (New York, "
            "1857; Internet Archive scan), which prints the Latin and an English translation "
            "on facing pages with numbered articles. Both sides public domain."),
 'hinweis': ("Carried as the debate it forced, not as truth: the Monita are a forgery, "
             "condemned as such by the Church in 1616 and refuted from Gretser (1618) "
             "onward, yet reprinted for three centuries as the Society's 'secret "
             "instructions' — the apparatus's counterpart to the chess-playing Turk. The "
             "chapter and article numbering of the 1857 printing is kept as the citation "
             "grid; running heads are removed, hyphenation joined, and the systematic "
             "ligature losses of the OCR (ae) repaired, residual errors emended against "
             "the sense. Part of the concordance and the citation-bound dialogue; not part of the linguistic statistics, which describe the core corpus only."),
 'sections': sections,
}

path = os.path.join(REPO, 'data', 'monita.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', n, 'units')
