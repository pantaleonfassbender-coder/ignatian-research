# Final assembly of Longridge's Directory translation:
# v2 draft as base, v3 for c15, targeted re-extraction for c4/c29/c37,
# front matter (Preface + Introduction) extracted here.
import io, re, json

DIR = 'C:/Users/leofa/AppData/Local/Temp/longridge/'
v2 = json.load(io.open(DIR+'dir-draft2.json', encoding='utf-8'))
v3 = json.load(io.open(DIR+'dir-draft3.json', encoding='utf-8'))

EXPECT = {1:7,2:8,3:8,4:8,5:8,6:3,7:8,8:5,9:16,10:13,11:6,12:7,13:8,14:7,15:9,
          16:5,17:2,18:6,19:7,20:5,21:3,22:7,23:5,24:4,25:9,26:3,27:9,28:9,29:8,
          30:7,31:6,32:4,33:3,34:4,35:13,36:3,37:13,38:3,39:8,40:6}

def join_text(ls):
    txt = ' '.join(l for l in ls if l.strip())
    txt = re.sub(r'(\w)[-\u00ad]\s+(\w)', r'\1\2', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

def is_pagebreak(s):
    s = s.strip()
    if re.fullmatch(r'\d{3}', s) and 260 <= int(s) <= 352: return True
    if re.fullmatch(r'\d{3}\s+THE DIRECTORY.*', s): return True
    if re.fullmatch(r'THE DIRECTORY\s*[.,]?\s*\d{3}.*', s): return True
    if re.match(r'CHAPTER\s+[IVXLT0-9]+\S*\s+\S*\d', s): return True
    if re.fullmatch(r'[IVX]+L?\.?\s*\d{3}\s*\S{0,2}', s): return True
    return False

PSTART = re.compile(r'^(?:[^\dA-Za-z(]*(?:[A-Za-z]{1,2}[\s.]+)?[^\dA-Za-z(]*)(\d{1,2})[.,:]?\s+(\S.*)')
OCR_ALT = {9:{2},8:{3},2:{2,3},0:{6,9},5:{3}}
def could_be(v, e):
    return v == e or e in OCR_ALT.get(v, set())

def extract_chapter(raw, nch, fn_lines_expected=()):
    """Extract paragraphs 1..EXPECT from a raw chapter dump using expected-
    number-driven matching; footnote blocks are skipped page-suffix-wise."""
    lines = raw.split('\n')
    paras, cur, cur_n, expected = [], [], None, 1
    title_lines = []
    skip_fn = False
    for ln in lines:
        s = ln.strip()
        if not s:
            skip_fn = False
            continue
        if is_pagebreak(s) or s.startswith('CHAPTER'):
            skip_fn = False
            continue
        m = PSTART.match(s)
        if m and could_be(int(m.group(1)), expected):
            if cur_n is not None: paras.append((cur_n, cur))
            elif cur: title_lines.extend(cur)
            cur_n, cur = expected, [m.group(2)]
            expected += 1
            skip_fn = False
        elif m and int(m.group(1)) < expected and '.' not in s[:3] and cur_n is not None:
            # dotless digit line, number below expectation -> footnote suffix
            skip_fn = True
        elif skip_fn:
            continue
        else:
            cur.append(s)
    if cur_n is not None: paras.append((cur_n, cur))
    elif cur: title_lines.extend(cur)
    return join_text(title_lines), [{'n': pn, 'en': join_text(pl)} for pn, pl in paras]

final = {'chapters': {}}
for n in range(1, 41):
    key = f'c{n}'
    if n in (4, 29, 37):
        raw = io.open(DIR+f'raw-c{n}.txt', encoding='utf-8').read()
        titel, paras = extract_chapter(raw, n)
        final['chapters'][key] = {'titel': titel or v2['chapters'][key]['titel'], 'paras': paras}
    elif n == 15:
        final['chapters'][key] = {'titel': v3['chapters'][key]['titel'],
                                  'paras': v3['chapters'][key]['paras']}
    else:
        final['chapters'][key] = {'titel': v2['chapters'][key]['titel'],
                                  'paras': v2['chapters'][key]['paras']}

# ---- front matter: preface + translator's note + introduction 1..12
front = v2['front_raw']
i_pref = front.find('PREFACE')
i_tn = front.find('TRANSLATOR')
i_intro = front.find('INTRODUCTION')
pref_raw = front[i_pref+len('PREFACE'):i_tn]
tn_raw = front[i_tn:i_intro]
tn_raw = tn_raw[tn_raw.find('\n'):]
intro_raw = front[i_intro+len('INTRODUCTION'):]

def clean_block(raw):
    out = []
    for ln in raw.split('\n'):
        s = ln.strip()
        if not s: out.append(''); continue
        if is_pagebreak(s): continue
        if re.fullmatch(r'THE DIRECTORY.*', s): continue
        if re.fullmatch(r'TO THE SPIRITUAL EXERCISES', s): continue
        if re.fullmatch(r'PART I', s): continue
        out.append(s)
    return out

# preface: split on blank-line groups into paragraphs (2 expected: text + dateline/signature)
pref_lines = clean_block(pref_raw)
pref_text = join_text(pref_lines)
# introduction: numbered 1..12 with footnotes
def extract_numbered(raw, upto):
    lines = clean_block(raw)
    paras, cur, cur_n, expected = [], [], None, 1
    skip_fn = False
    for s in lines:
        if not s:
            skip_fn = False
            continue
        m = PSTART.match(s)
        if m and expected <= upto and could_be(int(m.group(1)), expected):
            if cur_n is not None: paras.append((cur_n, cur))
            cur_n, cur = expected, [m.group(2)]
            expected += 1
            skip_fn = False
        elif m and cur_n is not None and int(m.group(1)) < expected and '.' not in s[:3]:
            skip_fn = True
        elif skip_fn:
            continue
        elif cur_n is not None:
            cur.append(s)
    if cur_n is not None: paras.append((cur_n, cur))
    return [{'n': pn, 'en': join_text(pl)} for pn, pl in paras]

intro_title = 'Of the excellence and utility of the Exercises, and of the need of a Directory'
# strip title line from intro_raw before numbering
intro_paras = extract_numbered(intro_raw, 12)
final['praef'] = {'text': pref_text}
final['prooem'] = {'titel': intro_title, 'paras': intro_paras}
final['translator_note'] = join_text([l for l in clean_block(tn_raw) if l])

print('praef chars:', len(pref_text))
print('prooem paras:', [p['n'] for p in intro_paras])
for n in (4, 29, 37):
    ns = [p['n'] for p in final['chapters'][f'c{n}']['paras']]
    print(f"c{n} paras:", ns, 'OK' if ns == list(range(1, EXPECT[n]+1)) else 'BAD')
tot = sum(len(final['chapters'][f'c{n}']['paras']) for n in range(1,41))
print('total chapter paras:', tot, '(expected 286 = 287 - praef2 - prooem12 + ... check: 273 chapter paras)')
exp_ch = sum(EXPECT.values())
print('expected chapter paras:', exp_ch, '; c40 delivers', len(final['chapters']['c40']['paras']))
json.dump(final, io.open(DIR+'dir-final.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('translator note:', final['translator_note'][:150])
