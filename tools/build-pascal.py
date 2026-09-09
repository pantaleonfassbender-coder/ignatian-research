# -*- coding: utf-8 -*-
# Build data/pascal.json — Blaise Pascal, Lettres provinciales, Letters V,
# VII and X complete, in Thomas M'Crie's translation of 1856 (Robert Carter
# & Brothers; Project Gutenberg #73959, public domain). English-only for
# now: the French original (the Vallée transcription on fr.wikisource keeps
# the seventeenth-century orthography) is named as source but not yet
# carried — the bilingualisation is a planned enhancement, since M'Crie's
# paragraphing is much finer than the French and needs hand alignment.
#
# Usage:
#   python tools/build-pascal.py            # fetch from Project Gutenberg
#   python tools/build-pascal.py pg.txt     # use a local dump
import io, json, os, re, sys, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PG = 'https://www.gutenberg.org/cache/epub/73959/pg73959.txt'

if len(sys.argv) > 1:
    raw = io.open(sys.argv[1], encoding='utf-8-sig').read()
else:
    req = urllib.request.Request(PG, headers={'User-Agent': 'ignatiana-build/1.0'})
    raw = urllib.request.urlopen(req, timeout=60).read().decode('utf-8-sig')

m = re.search(r'\*\*\* ?START OF[^\n]*\n(.*)\n\*\*\* ?END OF', raw, re.S)
assert m, 'PG START/END markers not found'
t = m.group(1)

def body(rom, nxt):
    starts = [x.start() for x in re.finditer(r'^ +LETTER %s\.(\[\d+\])?\s*$' % rom, t, re.M)]
    ends = [x.start() for x in re.finditer(r'^ +LETTER %s\.(\[\d+\])?\s*$' % nxt, t, re.M)]
    a = starts[-1]
    b = min(e for e in ends if e > a)
    seg = t[a:b]
    # the letter proper ends with M'Crie's rendering of Pascal's close;
    # everything after (his endnotes to the letter) is not carried
    sig = re.search(r'I am,? &c\.[^\n]*', seg)
    assert sig, f'letter {rom}: closing signature not found'
    seg = seg[:sig.end()]
    seg = re.sub(r'^ +LETTER [IVX]+\.(\[\d+\])?\s*$', '', seg, flags=re.M)
    paras = []
    for p in re.split(r'\n\s*\n', seg):
        p = re.sub(r'\[\d+\]', '', p)          # editorial footnote markers
        p = p.replace('_', '')                 # PG italics markers
        p = re.sub(r'\s+', ' ', p).strip()
        if len(p) > 2:
            paras.append(p)
    # drop the leading all-caps argument (it duplicates the section blurb)
    while paras and sum(c.isupper() for c in paras[0]) > 0.6 * sum(c.isalpha() for c in paras[0]):
        paras.pop(0)
    return paras

LETTERS = [
 ('l5', 'V', 'Letter V — The doctrine of probable opinions',
  "Design of the Jesuits in establishing a new system of morals; two sorts of casuists among them; the doctrine of probabilism explained; a multitude of modern authors substituted for the holy fathers; Escobar."),
 ('l7', 'VII', 'Letter VII — Directing the intention',
  "The method of directing the intention adopted by the casuists; permission to kill in defence of honour and property, extended even to priests and monks."),
 ('l10', 'X', 'Letter X — Devotion made easy',
  "Palliatives applied to the sacrament of penance: maxims on confession, satisfaction, absolution, proximate occasions of sin, and the love of God."),
]

out = {
 'id': 'pascal',
 'autor': 'Blaise Pascal',
 'titel': 'Lettres provinciales — Letters V, VII and X (1656–1657)',
 'jahr': 1656,
 'lang': 'en',
 'zitierweise': 'Prov. V [k] · Prov. VII [k] · Prov. X [k]',
 'quelle': ("The Provincial Letters of Blaise Pascal, a new translation by the Rev. Thomas "
            "M'Crie (New York: Robert Carter & Brothers, 1856), via the Project Gutenberg "
            "transcription #73959. Public domain. The French original is cited from the "
            "Vallée transcription on the French Wikisource (seventeenth-century orthography "
            "preserved there); it is not yet carried in this module."),
 'hinweis': ("Three letters complete, chosen for the counter-voice they state: probabilism "
             "(V), the direction of the intention (VII), and devotion made easy (X). "
             "Paragraph numbers are editorial, per letter; M'Crie's footnote markers are "
             "removed and his notes not reproduced. English only for now — the "
             "bilingualisation against the French, whose paragraphing is much coarser, is a "
             "planned enhancement. Not yet part of the concordance index (like the "
             "Longridge layers); the reader's search does not cover it either."),
 'sections': [],
}

n = 0
for sid, rom, titel, blurb in LETTERS:
    nxt = {'V': 'VI', 'VII': 'VIII', 'X': 'XI'}[rom]
    paras = body(rom, nxt)
    assert len(paras) > 20, f'letter {rom}: only {len(paras)} paragraphs'
    units = []
    for k, p in enumerate(paras, start=1):
        n += 1
        units.append({'n': n, 'k': k, 'en': p})
    out['sections'].append({'id': sid, 'titel': titel, 'blurb': blurb, 'zk': f'Prov. {rom}', 'units': units})
    print(f'{rom}: {len(paras)} paragraphs')

path = os.path.join(REPO, 'data', 'pascal.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', n, 'units')
