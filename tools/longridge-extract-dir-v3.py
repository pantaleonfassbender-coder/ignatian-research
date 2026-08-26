# v3: single sequential walk over page-structured lines; footnote suffix vs
# paragraph start decided with knowledge of the expected paragraph number.
import io, re, json

SRC = 'C:/Users/leofa/AppData/Local/Temp/longridge_djvu.txt'
t = io.open(SRC, encoding='utf-8', errors='replace').read()
seg = t[676029:860057]

EXPECT = {1:7,2:8,3:8,4:8,5:8,6:3,7:8,8:5,9:16,10:13,11:6,12:7,13:8,14:7,15:9,
          16:5,17:2,18:6,19:7,20:5,21:3,22:7,23:5,24:4,25:9,26:3,27:9,28:9,29:8,
          30:7,31:6,32:4,33:3,34:4,35:13,36:3,37:13,38:3,39:8,40:6}

def norm_roman(tok):
    tok = tok.strip(' .:|')
    if tok == 'XL': return 40
    fixed = tok.replace('T','I')
    if fixed.endswith('L') and fixed != 'XL': fixed = fixed[:-1]+'I'
    rmap = {'I':1,'V':5,'X':10,'L':50}
    val = 0
    for j,ch in enumerate(fixed):
        v = rmap.get(ch)
        if v is None: return None
        if j+1 < len(fixed) and rmap.get(fixed[j+1],0) > v: val -= v
        else: val += v
    return val

heads = {}
for m in re.finditer(r'\n\s*(CHAPTER\s+([IVXLT]+)[^\n]*)\n', seg):
    if re.search(r'\d', m.group(1)): continue
    n = norm_roman(m.group(2))
    if n and 1 <= n <= 40 and n not in heads:
        heads[n] = m.start()
assert len(heads) == 40

lines = seg.split('\n')
offs, pos = [], 0
for ln in lines:
    offs.append(pos); pos += len(ln)+1

def is_pagebreak(s):
    s = s.strip()
    if re.fullmatch(r'\d{3}', s) and 260 <= int(s) <= 352: return True
    if re.fullmatch(r'\d{3}\s+THE DIRECTORY.*', s): return True
    if re.fullmatch(r'THE DIRECTORY\s*[.,]?\s*\d{3}.*', s): return True
    if re.match(r'CHAPTER\s+[IVXLT0-9]+\S*\s+\S*\d', s): return True
    if re.fullmatch(r'[IVX]+L?\.?\s*\d{3}\s*\S{0,2}', s): return True
    return False

pages, cur = [], []
for i, ln in enumerate(lines):
    if is_pagebreak(ln):
        pages.append(cur); cur = []
    else:
        cur.append((offs[i], ln))
pages.append(cur)

chap_bounds = sorted((v, k) for k, v in heads.items())
def chap_of(o):
    c = 0
    for start, n in chap_bounds:
        if o >= start: c = n
        else: break
    return c

OCR_ALT = {9:{2},8:{3},0:{6,9},5:{3}}
def could_be(v, e):
    return v == e or e in OCR_ALT.get(v, set())

DOTTED = re.compile(r'^(\d{1,2})[.,:]\s+(.*)')
DOTLESS = re.compile(r'^(\d{1,2})\s+(\S.*)')

chapters = {n: {'titel_lines': [], 'paras': [], 'fns': []} for n in range(0, 41)}
cur_chap, expected, cur_para, cur_lines = 0, 1, None, []

def flush():
    global cur_para, cur_lines
    if cur_para is not None and cur_lines:
        chapters[cur_chap]['paras'].append((cur_para, cur_lines))
    elif cur_lines:
        chapters[cur_chap]['titel_lines'].extend(cur_lines)
    cur_para, cur_lines = None, []

for page in pages:
    in_fn = False
    for idx, (o, ln) in enumerate(page):
        s = ln.strip()
        c = chap_of(o)
        if c != cur_chap:
            flush()
            cur_chap, expected, cur_para = c, 1, None
            in_fn = False
        if not s:
            continue
        if s.startswith('CHAPTER'):
            continue
        if in_fn:
            chapters[cur_chap]['fns'].append(s)
            continue
        md, ml = DOTTED.match(s), DOTLESS.match(s)
        if md and could_be(int(md.group(1)), expected):
            flush(); cur_para = expected; expected += 1
            cur_lines = [md.group(2)]
        elif ml and could_be(int(ml.group(1)), expected) and int(ml.group(1)) != 1:
            # dotless paragraph number (OCR lost the period); exclude bare "1 "
            # which is nearly always a footnote when unexpected... but here it
            # matches expectation, so accept unless it looks like a citation
            flush(); cur_para = expected; expected += 1
            cur_lines = [ml.group(2)]
        elif ml and int(ml.group(1)) == 1 and could_be(1, expected) and not re.match(
                r'(See|Cf|I\.?e|T\.?e|Le\.|P\.|Tit\.|S\.|In his|["\u201c])', ml.group(2)):
            flush(); cur_para = expected; expected += 1
            cur_lines = [ml.group(2)]
        elif ml and not could_be(int(ml.group(1)), expected):
            # dotless digit line not matching expectation -> footnote suffix
            in_fn = True
            chapters[cur_chap]['fns'].append(s)
        elif ml:
            # value 1 with citation cue while expecting 1 -> footnote
            in_fn = True
            chapters[cur_chap]['fns'].append(s)
        else:
            cur_lines.append(s)
flush()

def join_text(ls):
    txt = ' '.join(l for l in ls if l.strip())
    txt = re.sub(r'(\w)[-\u00ad]\s+(\w)', r'\1\2', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

out = {'front_raw': seg[:heads[1]], 'chapters': {}}
bad = []
for n in range(1, 41):
    ch = chapters[n]
    paras = [{'n': pn, 'en': join_text(pl)} for pn, pl in ch['paras']]
    ns = [p['n'] for p in paras]
    ok = ns == list(range(1, EXPECT[n]+1))
    if not ok: bad.append(n)
    out['chapters'][f'c{n}'] = {'titel': join_text(ch['titel_lines']),
                                'paras': paras, 'fns': ch['fns']}
    print(f"c{n:<3d} {'OK ' if ok else 'BAD'} got={len(ns) if ok else ns} exp={EXPECT[n]} fn={len(ch['fns'])}")
print('mismatched:', bad)
json.dump(out, io.open('C:/Users/leofa/AppData/Local/Temp/longridge/dir-draft3.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
