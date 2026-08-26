# Memoriale B. Petri Fabri (ed. Bouix, Paris 1873) — extraction from IA OCR.
# Volume structure: Bouix preface | Prooemium (1506-1542) | Memoriale
# (VI.1542 - VII.1543, month running heads) | Epilogus (1543-1546) |
# Appendix (letters and counsels) | FINIS.
import io, re, json

t = io.open('C:/Users/leofa/AppData/Local/Temp/favre_memoriale_djvu.txt', encoding='utf-8', errors='replace').read()

# ---- anchors
p_arg = t.find('In hoc proæmio')
if p_arg < 0: p_arg = t.find('In hoc pro')
b_arg = t.find('In hoc Memoriali')
e_arg = t.find('In hoc Epilogo')
a_arg = t.find('Epistolæ quædam et monita')
fin   = t.find('FINIS')
assert -1 not in (p_arg, b_arg, e_arg, a_arg, fin), (p_arg, b_arg, e_arg, a_arg, fin)

# argument paragraphs end at the first blank-blank after them; body starts after
def after_argument(pos):
    m = re.compile(r'\n\s*\n\s*\n').search(t, pos)
    return m.end()

ARGS = {}
def argument_text(pos):
    end = re.compile(r'\n\s*\n\s*\n').search(t, pos).start()
    s = re.sub(r'\s+', ' ', t[pos:end]).strip()
    return s

ARGS['prooem'] = argument_text(p_arg)
ARGS['mem'] = argument_text(b_arg)
ARGS['epilog'] = argument_text(e_arg)

MONTHS = {'JANUARIO':'01','FEBRUARIO':'02','MARTIO':'03','APRILI':'04','MAIO':'05',
          'JUNIO':'06','JULIO':'07','AUGUSTO':'08','SEPTEMBRI':'09','OCTOBRI':'10',
          'NOVEMBRI':'11','DECEMBRI':'12'}
MONTH_DE = {'01':'Januar','02':'Februar','03':'März','04':'April','05':'Mai','06':'Juni',
            '07':'Juli','08':'August','09':'September','10':'Oktober','11':'November','12':'Dezember'}
MONTH_EN = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June',
            '07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}

def fuzzy_month(s):
    s = s.upper()
    best, bd = None, 3
    for name, num in MONTHS.items():
        # crude edit-similarity: shared prefix + length
        d = sum(1 for a, b in zip(s, name) if a != b) + abs(len(s) - len(name))
        if d < bd:
            best, bd = num, d
    return best

HEAD_ANNO = re.compile(r'^\W{0,4}(?:ANNO\s+)?(\d{3,4})\W{0,3}\s*MENSE\s+([A-Z]{4,12})')
def classify(line):
    """-> ('head', (yr, mo)) | ('head', None) | ('pagenum', None) | ('text', None)"""
    s = line.strip()
    if not s:
        return ('blank', None)
    if re.fullmatch(r'[\W\d]{1,8}', s):
        return ('pagenum', None)
    m = HEAD_ANNO.match(s)
    if m and s.upper() == s:
        yr = m.group(1)
        yr = '15' + yr[-2:] if len(yr) >= 3 else yr
        return ('head', (yr, fuzzy_month(m.group(2))))
    up = s.upper()
    letters = [c for c in s if c.isalpha()]
    upr = sum(1 for c in letters if c.isupper()) / max(1, len(letters))
    if upr > 0.8 and re.search(r'MEMORIALE|FABRI|EPILOGUS|APPENDIX|PROQ|PRO.EMIUM|SOCIETATIS|SOC\w*TAT', up):
        return ('head', None)
    if upr > 0.8 and re.search(r'\d{2,3}', s) and len(s) < 50:
        return ('head', None)          # damaged running head with page number
    if len(letters) < 4 and len(s) > 2:
        return ('junk', None)
    return ('text', None)

def extract_stream(lo, hi, init_ctx):
    """-> list of (ctx, paragraph_text); ctx = (yr, mo) or None"""
    lines = t[lo:hi].split('\n')
    paras, cur, ctx = [], [], init_ctx
    in_fn = False
    def flush():
        nonlocal cur
        if cur:
            s = ' '.join(cur)
            s = re.sub(r'(\w)[-\u00ad¬]\s+(\w)', r'\1\2', s)
            s = re.sub(r'\s+', ' ', s).strip()
            if len(s) > 3:
                paras.append((ctx, s))
        cur = []
    for ln in lines:
        kind, val = classify(ln)
        if kind == 'blank':
            flush(); in_fn = False
        elif kind == 'pagenum':
            in_fn = False
        elif kind == 'head':
            in_fn = False
            if val: ctx = val
        elif kind == 'junk':
            continue
        else:
            s = ln.strip()
            if re.match(r'^\d{1,2}\s+\S', s) and not re.match(r'^\d{1,2}\s+\d', s):
                in_fn = True
                continue
            if in_fn:
                continue
            cur.append(s)
    flush()
    # merge page-break splits: previous doesn't end a sentence, or next starts lowercase
    merged = []
    for ctx2, s in paras:
        if merged:
            prev = merged[-1][1]
            if (not re.search(r'[.!?»"\u201d]\s*$', prev)) or (s[:1].islower()):
                merged[-1] = (merged[-1][0], prev + ' ' + s)
                continue
        merged.append((ctx2, s))
    return merged

def fix(s):
    s = s.replace('æ', 'ae').replace('Æ', 'Ae').replace('œ', 'oe').replace('Œ', 'Oe')
    s = re.sub(r'[|©®™_`~^«»§]+', ' ', s)
    s = re.sub(r'\s{2,}', ' ', s)
    s = re.sub(r'\s+([,.;:!?])', r'\1', s)
    s = re.sub(r'\bDer\b(?=\s+gloria)', 'Dei', s)
    return s.strip()

# ---- Prooemium (context: none — retrospective)
prooem = extract_stream(after_argument(p_arg), b_arg, None)
# ---- Memoriale body (context from running heads; entries before first head = VI.1542)
body = extract_stream(after_argument(b_arg), e_arg, ('1542', '06'))
# ---- Epilogus
epilog = extract_stream(after_argument(e_arg), a_arg, None)

# ---- number units and group into sections
sections = []
n = 0
def add_section(sid, label_de, units, arg=''):
    sections.append({'id': sid, 'titel': label_de, 'arg': arg,
                     'units': units})

units = []
for ctx, s in prooem:
    n += 1
    units.append({'n': n, 'la': fix(s)})
add_section('prooem', 'Prooemium (1506–1542)', units, ARGS['prooem'])

from collections import OrderedDict
bymonth = OrderedDict()
for ctx, s in body:
    key = ctx if ctx and ctx[1] else ('1542', '06')
    bymonth.setdefault(key, [])
    n += 1
    bymonth[key].append({'n': n, 'la': fix(s)})
for (yr, mo), us in bymonth.items():
    add_section(f'm{yr}{mo}', f'{MONTH_EN[mo]} {yr}', us,
                ARGS['mem'] if not sections or sections[-1]['id'] == 'prooem' else '')

units = []
for ctx, s in epilog:
    n += 1
    units.append({'n': n, 'la': fix(s)})
add_section('epilog', 'Epilogus (1543–1546)', units, ARGS['epilog'])

# ---- Appendix items
ITEMS = [
 (407136, 'a1', 'Monita, Parma 1540'),
 (414638, 'a2', 'Ad S. Ignatium et socios, 1541'),
 (421997, 'a3', 'Ad scholasticos Parisienses, 1541'),
 (428688, 'a4', 'Ad Iacobum Laynium (I)'),
 (430591, 'a5', 'Ad Iacobum Laynium (II)'),
 (437488, 'a6', 'Epistola, 1543'),
 (442843, 'a7', 'Monita communitati religiosae, 1543'),
]
app_sections = []
for i, (pos, sid, short) in enumerate(ITEMS):
    end = ITEMS[i+1][0] if i+1 < len(ITEMS) else fin
    # heading = lines up to '(Anno ...)' or first blank-blank
    hm = re.compile(r'\n\s*\n\s*\n').search(t, pos)
    head_txt = re.sub(r'\s+', ' ', t[pos:hm.start()]).strip()
    stream = extract_stream(hm.end(), end, None)
    us = []
    for ctx, s in stream:
        n += 1
        us.append({'n': n, 'la': fix(s)})
    app_sections.append({'id': sid, 'titel': short, 'arg': fix(head_txt), 'units': us})

out = {'sections': sections, 'appendix': app_sections}
json.dump(out, io.open('C:/Users/leofa/AppData/Local/Temp/longridge/favre-draft.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('memoriale sections:')
for s in sections:
    ch = sum(len(u['la']) for u in s['units'])
    print(f"  {s['id']:8s} {len(s['units']):4d} units {ch:7d} chars  {s['titel']}")
print('appendix items:')
for s in app_sections:
    ch = sum(len(u['la']) for u in s['units'])
    print(f"  {s['id']:4s} {len(s['units']):3d} units {ch:6d} chars  {s['arg'][:70]}")
print('total units:', n)
PY_EOF = True
