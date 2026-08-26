# Merge translations into the edition, restructure the appendix into its
# thirteen pieces, renumber, validate, and write data/memoriale.json.
import io, json, re, glob, os

D = 'C:/Users/leofa/AppData/Local/Temp/longridge/'
d = json.load(io.open(D+'favre-fixed.json', encoding='utf-8'))

tr = {}
for f in glob.glob(D+'tr/*.json'):
    for k, v in json.load(io.open(f, encoding='utf-8')).items():
        tr[int(k)] = v

# strip embedded headings / datelines from certain Latin units
STRIP = {
 390: r'^DE OBEDIENTIA ET CHARITATE RELIGIOSA\s*',
 394: r'^Beatus Petrus Faber ad amicum quemdam.*?\(Anno \d{4}\)\s*',
 400: r'^Beati Petri Fabri aureum praeceptum.*?traditum:\s*',
 401: r'^Praecepta [gq]uaedam Cornelio Wishavaeo tradita.*?\(Anno \d{4}\)\s*',
 405: r'^Beati Petri Fabri monitum ad Societatem vocatum.*?\(Anno \d{4}\)\s*',
 406: r'^\(Matriti, 12 Martii, anno \d{4}\.?\)\s*',
}

allunits = {}
for s in d['sections'] + d['appendix']:
    for u in s['units']:
        allunits[u['n']] = u

for n, u in allunits.items():
    t = tr.get(n)
    if t is None:
        continue
    if t.get('la'):
        u['la'] = t['la']
    if n in STRIP:
        u['la'] = re.sub(STRIP[n], '', u['la'], flags=re.S).strip()
    u['en'] = t.get('en', '')

# drop empties (315 and any others)
for s in d['sections'] + d['appendix']:
    s['units'] = [u for u in s['units'] if u.get('en') and len(u['la']) > 3]

# restructure appendix into thirteen pieces
def units_range(sid, lo, hi):
    src = [x for x in d['appendix'] if x['id'] == sid][0]
    return [u for u in src['units'] if lo <= u['n'] <= hi]

APP = [
 ('a1',  'Monita sodalitati Charitatis, Parma 1540', units_range('a1', 355, 365)),
 ('a2',  'Ad S. Ignatium et Petrum Codacium, Spira, 23. Ian. 1541', units_range('a2', 366, 375)),
 ('a3',  'Ad scholasticos Parisienses, Ratisbona, 12. Maii 1541', units_range('a3', 376, 379)),
 ('a4',  'Ad Iacobum Laynium: de bonis a Deo acceptis', units_range('a4', 380, 380)),
 ('a5',  'Ad Iacobum Laynium: de agendi ratione cum haereticis', units_range('a5', 381, 389)),
 ('a6',  'De obedientia et charitate religiosa', units_range('a6', 390, 393)),
 ('a7',  'Ad amicum: de adversariis comitate devinciendis, 1543', units_range('a6', 394, 395)),
 ('a8',  'Monita communitati religiosae vitae ineundae, 1543', units_range('a7', 396, 399)),
 ('a9',  'Aureum praeceptum de castitate in hospitiis tuenda', units_range('a7', 400, 400)),
 ('a10', 'Praecepta de confessionibus excipiendis (Cornelio Wishaveo), 1543', units_range('a7', 401, 404)),
 ('a11', 'Monitum ad vocatum in Societatem, 1544', units_range('a7', 405, 405)),
 ('a12', 'Ad Gerardum Hammontanum, priorem Carthusiae Coloniensis, Matriti 1546', units_range('a8', 406, 406)),
 ('a13', 'Adhortatio ad doctum quemdam ad Societatem accedentem', units_range('a9', 407, 411)),
]

# renumber sequentially
n = 0
for s in d['sections']:
    for u in s['units']:
        n += 1
        u['n'] = n
appendix = []
for sid, titel, us in APP:
    for u in us:
        n += 1
        u['n'] = n
    appendix.append({'id': sid, 'titel': titel, 'units': us})

out = {
 'titel': 'Memoriale Beati Petri Fabri',
 'quelle': ('Memoriale Beati Petri Fabri, primi sacerdotis Societatis Iesu, ed. Marcel Bouix SJ '
            '(Paris: Gauthier-Villars, 1873). First public edition; in the United States public domain. '
            'Reconstructed from the OCR of the Internet Archive scan memorialebeatipe0000sign.'),
 'provenienz': ("Favre's autograph is lost. Bouix printed the Latin text transmitted within the Society "
                'of Jesus through autographic printings (an internal printing is recorded for 1853), '
                'emending corrupt passages, omitting a few words he judged beyond repair, and rendering '
                'into Latin a handful of Spanish words embedded in the text. The critical edition of the '
                'original — largely Spanish — appeared only in the Monumenta Historica Societatis Iesu '
                '(Fabri Monumenta, Madrid 1914), whose canonical paragraph numbering (MF 1-443) this '
                'edition therefore cannot reproduce: the paragraph numbers here are this site\'s own, '
                'assigned to the 1873 text.'),
 'uebersetzung': ('The English is an unofficial machine-generated working translation made for this site '
                  'directly from the 1873 Latin, consulting no copyrighted translation. Cite the Latin.'),
 'sections': d['sections'],
 'appendix': appendix,
}

# validation
bad = []
tot = 0
for s in out['sections'] + out['appendix']:
    for u in s['units']:
        tot += 1
        if not u.get('la') or not u.get('en'):
            bad.append((s['id'], u['n']))
print('total units:', tot, 'missing la/en:', bad)
ns = [u['n'] for s in out['sections'] + out['appendix'] for u in s['units']]
print('numbering contiguous:', ns == list(range(1, len(ns)+1)))

# simple stats for the works entry
la_all = ' '.join(u['la'] for s in out['sections'] + out['appendix'] for u in s['units'])
words = re.findall(r"[A-Za-z']+", la_all)
sents = re.split(r'[.!?]+\s', la_all)
wl = sum(len(w) for w in words) / len(words)
long_w = sum(1 for w in words if len(w) > 6) / len(words)
sl = len(words) / len(sents)
lix = round(sl + 100 * long_w, 1)
ttr = round(len(set(w.lower() for w in words)) / len(words), 3)
print(f"tokens={len(words)} sents={len(sents)} satzlaenge={sl:.1f} wortlaenge={wl:.2f} lix={lix} ttr={ttr}")

json.dump(out, io.open('C:/Users/leofa/OneDrive/Desktop/Ignatius/ignatian-research/data/memoriale.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('written; size:', os.path.getsize('C:/Users/leofa/OneDrive/Desktop/Ignatius/ignatian-research/data/memoriale.json'))
