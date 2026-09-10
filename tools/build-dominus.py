# -*- coding: utf-8 -*-
# Build data/dominus.json — Clement XIV, Dominus ac Redemptor (21 July 1773),
# the brief of suppression: the corpus's closing text.
#
# Latin after the edition of Augustin Theiner, Clementis XIV. Pont. Max.
# Epistolae et Brevia (Paris 1852; Internet Archive clementisxivpon00clemgoog,
# US public domain), doc. CCCXVII, which prints the brief with numbered
# paragraphs — the citation grid carried here. The OCR of the 1852 typesetting
# is serviceable; systematic ligature losses (ae) and recurrent misreads are
# repaired below, residual errors emended against the sense. The English is
# this site's unofficial machine-generated working translation, made directly
# from the Latin (no full public-domain English translation of the brief was
# located; the contemporary and modern translations were not consulted).
#
# Usage:
#   python tools/build-dominus.py theiner2.txt [--dump]
#     --dump prints the cleaned Latin paragraphs (for translation drafting)
import io, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

src = sys.argv[1]
raw = io.open(src, encoding='utf-8').read()
i = raw.find('1. Dominus, ac Redemptor')
assert i > 0
m_end = re.search(r'Datum\s+Rom[a-z]*[^\n]*\n[^\n]*\n[^\n]*', raw[i:])
seg = raw[i:i + m_end.end()]

# join lines, keep paragraph numbers at line starts as split points, in
# strictly increasing order (page numbers and OCR noise are thereby skipped)
lines = [l.strip() for l in seg.splitlines()]
numbered, cur, curno, expect = [], None, 1, 1
NUM = re.compile(r'^(\d{1,2})\s*\.\s+(.*)')
LOST = {12: 'Pariter ip'}     # printed number destroyed; opening verified on p. 389
for l in lines:
    if not l:
        continue
    if re.fullmatch(r'\d+|[A-Z .\'’„-]{6,}', l):    # page nos., running heads
        continue
    m = NUM.match(l)
    # tolerate up to two lost numbers in sequence (recovered by POSTS below)
    if m and expect <= int(m.group(1)) <= expect + 2:
        if cur is not None:
            numbered.append((curno, cur))
        curno, cur = int(m.group(1)), m.group(2)
        expect = curno + 1
        continue
    lost = LOST.get(expect)
    if lost:
        pos = l.find(lost)
        if 0 <= pos <= 8:
            if cur is not None:
                numbered.append((curno, cur))
            curno, cur = expect, l[pos:]
            expect += 1
            continue
    cur = l if cur is None else cur + ' ' + l
numbered.append((curno, cur))

# paragraphs whose printed number the OCR destroyed entirely: split them out
# of their host by the openings verified against the page images (p. 390)
POSTS = [   # (host_no, new_no, fuzzy split regex at the opening)
    (13, 14, r'\b1\s*4\s*\.\s*(?=In his vero)'),
    (13, 15, r'\bis\.\s*(?=His\s*igitur)'),
    (14, 15, r'\bis\.\s*(?=His\s*igitur)'),
]
for host, new, rx in POSTS:
    for idx, (no, text) in enumerate(numbered):
        if no != host:
            continue
        m = re.search(rx, text)
        if m:
            head = text[:m.start()].rstrip()
            tail = re.sub(rx, '', text[m.start():], count=1).strip()
            numbered[idx] = (no, head)
            numbered.insert(idx + 1, (new, tail))
            break

ks = [no for no, _ in numbered]
assert ks == list(range(1, len(ks) + 1)), f'numbering broken: {ks}'
paras = [t for _, t in numbered]
print(f'{len(paras)} paragraphs extracted, numbering continuous 1..{len(paras)}')

WORD_FIXES = {
    'prsemuntiatus': 'praenuntiatus', 'cselos': 'caelos', 'cslis': 'caelis',
    'reconcihavisset': 'reconciliavisset', 'reconciljationis': 'reconciliationis',
    'goniti': 'geniti', 'go niti': 'geniti', 'soliiciti': 'solliciti',
    'vocationb': 'vocationis', 'utinquitS': 'ut inquit S', 'onmes': 'omnes',
    'Romce': 'Romae', 'Uajorem': 'Majorem', 'Pnedecessor': 'Praedecessor',
    'pnedecessor': 'praedecessor', 'HI.': 'III.', 'Hl.': 'III.',
    'sseculi': 'saeculi', 'sseculo': 'saeculo', 'sspedict': 'saepedict',
    'ssepedict': 'saepedict', 'lOBS': '1668', 'imbiium': 'habitum',
    'novilios': 'novitios', 'Sociotati': 'Societati',
    'prssentium': 'praesentium', 'prssentibus': 'praesentibus',
    'longtus': 'longius', 'pnv bisque': 'probisque',
    'dosignabi': 'designabi', 'circumsoripsisset': 'circumscripsisset',
    # 'sB' is the OCR's rendering of 'æ' in this face
    'clesisB': 'clesiae', 'poenitentisB': 'poenitentiae',
    'prsBStare': 'praestare', 'sententisB': 'sententiae',
    'nostrsB': 'nostrae', 'CardinalisBorromei': 'Cardinalis Borromei',
    '\\1tio': 'vitio', 'nov8e': 'novae', 'Praedeces$ore': 'Praedecessore',
    'memorise': 'memoriae', 'GregoriusPP.': 'Gregorius PP.',
    'litterassub': 'litteras sub', 'a ic. memoriae': 'a rec. memoriae',
    'JuUo': 'Julio', 'acrelationibus adrecol.': 'ac relationibus ad recol.',
    'charitaiem': 'charitatem', 'conaervandam': 'conservandam',
    'exortisseditionibus': 'exortis seditionibus', 'autalio': 'aut alio',
    'pericuiosissimis': 'periculosissimis',
    # 'U' for 'll'/'li', 'H' for 'll' and kin, each verified in context
    'aUquid': 'aliquid', 'aUud': 'aliud', 'aiixiHum': 'auxilium',
    'ccMisequi': 'consequi', 'coUigati': 'colligati',
    'difSciliora': 'difficiliora', 'etMonasteria': 'et Monasteria',
    'inSocietate': 'in Societate', 'noUe': 'nolle', 'nuHos': 'nullos',
    'nuUam': 'nullam', 'nuUoque': 'nulloque', 'nuUo': 'nullo',
    'ofQcium': 'officium', 'poUent': 'pollent',
    'praedictiOrdinis': 'praedicti Ordinis', 'puUuIassc': 'pullulasse',
    'pubUcis': 'publicis', 'quaeUbet': 'quaelibet', 'rMuxit': 'reduxit',
    'saepedictaB': 'saepedictae', 'siMctae': 'sanctae', 'suUata': 'sublata',
    'suadibiUs': 'suadibilis', 'uUorum': 'ullorum', 'uUus': 'ullus',
    'uUo': 'ullo', 'utilitaU etconunodi': 'utilitatis et commodi',
    'accessionibuSp': 'accessionibus,', 'viTieam': 'vineam',
    'Terree': 'Terrae', 'scmina': 'semina', 'ajmulationum': 'aemulationum',
    'Prs&r decessore': 'Praedecessore', 'turbuientiora': 'turbulentiora',
    'Sedjs': 'Sedis', 'Apostolics': 'Apostolicae', '£a enim': 'Ea enim',
    'suoqu6': 'suoque', 'contentiombusy et': 'contentionibus, et',
    'pertm*bationes': 'perturbationes', 'deci*cta': 'decreta',
    'Ponlificis': 'Pontificis', 'MagnuS;': 'Magnus,',
    'LusitaniS;': 'Lusitaniae', 'RegniS;': 'Regnis,',
    'Rs Fidelissimi': 'Regis Fidelissimi', 'decemendam': 'decernendam',
    'obiius': 'obitus', 'coniigii': 'contigit', 'praeier': 'praeter',
    'expecialionem': 'expectationem', 'Tridentmi': 'Tridentini',
    '£t ': 'Et ', '£,Gardinales': 'E. Cardinales',
}
def clean(t):
    t = re.sub(r'(\w)-\*\s*(\w)', r'\1\2', t)   # 'po-* tissimum'
    t = re.sub(r'(\w)\*\s+(?=[a-z])', r'\1', t)  # 'sa* pientia' (all 7 * in
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)      # this text are word splits)
    t = re.sub(r'[\^°·]+', '', t)     # stray marks, BEFORE the fixes match
    t = re.sub(r'\s+', ' ', t).strip()
    # running heads of the 1852 edition, glued in mid-paragraph at page turns.
    # Both heads come through the OCR heavily mangled (CLEMKJNTIS, DOCUM£IMTA,
    # OOCUMENTA ...), so the match is fuzzy — but the verso head always carries
    # its page number, which keeps genuine 'Benedicto Papae XIV' etc. safe; and
    # the head is deleted WITHOUT a space, because where it is glued to lowercase
    # on both sides it interrupted a word split at the page break (suo|rumque).
    t = re.sub(r'\s*\d{2,3}[A-Za-z»$£]?\s+C[A-Za-z£]{5,12}\s+XIV\s*\.?\s*', ' ', t)
    t = re.sub(r'[DO]O?C[A-Za-z£]{3,10}\s+VA[A-Za-z]{2,5}\s*\.?\s*\d{0,3}[»$£]?\s*', '', t)
    for a, b in WORD_FIXES.items():
        t = re.sub(re.escape(a), b, t)
    t = re.sub(r'\bprse', 'prae', t).replace('Prse', 'Prae')
    t = re.sub(r'\bquse', 'quae', t).replace('Quse', 'Quae')
    t = re.sub(r'\bqus\b', 'quae', t)
    t = re.sub(r'\bcse', 'cae', t).replace('Cse', 'Cae')
    # 's' deliberately absent from the classes: genuine -sse- (esse, fuisse,
    # posse, dissensio ...) must not be turned into -sae-
    t = re.sub(r'(?<=[bcdfghklmnpqrtvx])s(?=e\b)', 'a', t)
    t = re.sub(r'(?<=[bcdfghklmnpqrtvx])se(?=[dmnrst]\b|[dmnrst][a-z])', 'ae', t)
    for a, b in WORD_FIXES.items():   # second pass: some keys only surface
        t = re.sub(re.escape(a), b, t)  # after the ligature repairs above
    t = re.sub(r'[\^°·]+', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

LA = [clean(p) for p in paras]

if '--dump' in sys.argv:
    for k, p in enumerate(LA, start=1):
        print(f'\n[{k}] {p}')
    sys.exit(0)

# English working translations, one per numbered paragraph, keyed 1..N.
# (Filled in by hand against the cleaned Latin; unofficial, CC0.)
EN = {}
try:
    from dominus_en import EN          # tools/dominus_en.py, generated below
except Exception:
    pass

units = []
for k, p in enumerate(LA, start=1):
    u = {'n': k, 'k': k, 'orig': p}
    if EN.get(k):
        u['en'] = EN[k]
    units.append(u)

out = {
 'id': 'dominus',
 'autor': 'Clement XIV',
 'titel': 'Dominus ac Redemptor — the brief of suppression (21 July 1773)',
 'jahr': 1773,
 'lang': 'la',
 'zitierweise': 'DaR [k]',
 'quelle': ("Latin after Augustin Theiner, Clementis XIV. Pont. Max. Epistolae et Brevia "
            "(Paris, 1852), doc. CCCXVII, whose paragraph numbering is carried as the "
            "citation grid; Internet Archive scan, OCR emended against the sense. Public "
            "domain (brief of 1773; edition 1852)."),
 'hinweis': ("The corpus's closing text, complete: the brief by which Clement XIV "
             "suppressed the Society of Jesus on 21 July 1773 — the apparatus ends, "
             "deliberately, here. The English is this site's unofficial machine-generated "
             "working translation, made directly from the Latin; no full public-domain "
             "English translation was located, and none was consulted — cite the Latin. "
             "Not yet part of the concordance index."),
 'sections': [{
   'id': 'brief', 'zk': 'DaR',
   'titel': 'The brief, in Theiner’s numbering',
   'blurb': 'Forty-odd numbered paragraphs: the long recital of precedents, the grounds, the operative suppression, and the provisions for persons and property.',
   'units': units,
 }],
}

path = os.path.join(REPO, 'data', 'dominus.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
missing = [k for k in range(1, len(LA) + 1) if not EN.get(k)]
print('wrote', path, '-', len(units), 'units; untranslated:', missing if missing else 'none')
