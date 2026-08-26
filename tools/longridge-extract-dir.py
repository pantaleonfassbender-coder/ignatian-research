# Longridge 1919 Directory translation, parser v2: page-structured.
# Pages are delimited by running-head lines carrying the printed page number
# (269-350). Footnotes sit at the physical page end; paragraph numbers are
# matched against the expected sequence (with OCR digit confusions allowed).
import io, re, json

SRC = 'C:/Users/leofa/AppData/Local/Temp/longridge_djvu.txt'
t = io.open(SRC, encoding='utf-8', errors='replace').read()
seg = t[676029:860057]

EXPECT = {1:7,2:8,3:8,4:8,5:8,6:3,7:8,8:5,9:16,10:13,11:6,12:7,13:8,14:7,15:9,
          16:5,17:2,18:6,19:7,20:5,21:3,22:7,23:5,24:4,25:9,26:3,27:9,28:9,29:8,
          30:7,31:6,32:4,33:3,34:4,35:13,36:3,37:13,38:3,39:8,40:6}

def rom(n):
    s, m = '', n
    for v, r in [(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]:
        while m >= v: s += r; m -= v
    return s

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

# ---- 1. locate true chapter headings (digit-free CHAPTER lines, first per number)
heads = {}
for m in re.finditer(r'\n\s*(CHAPTER\s+([IVXLT]+)[^\n]*)\n', seg):
    if re.search(r'\d', m.group(1)): continue
    n = norm_roman(m.group(2))
    if n and 1 <= n <= 40 and n not in heads:
        heads[n] = m.start()
assert len(heads) == 40, heads.keys()

# ---- 2. split into pages by running-head / page-number lines
lines = seg.split('\n')
# absolute char offset of each line start
offs, pos = [], 0
for ln in lines:
    offs.append(pos); pos += len(ln)+1

def is_pagebreak(s):
    s = s.strip()
    if re.fullmatch(r'\d{3}', s) and 260 <= int(s) <= 352: return True
    if re.fullmatch(r'\d{3}\s+THE DIRECTORY.*', s): return True
    if re.fullmatch(r'THE DIRECTORY\s*[.,]?\s*\d{3}.*', s): return True
    if re.match(r'CHAPTER\s+[IVXLT0-9]+\S*\s+\S*\d', s): return True  # 'CHAPTER XI 299', 'CHAPTER XXVII | $25'
    if re.fullmatch(r'[IVX]+L?\.?\s*\d{3}\s*\S{0,2}', s): return True # signature 'IL. 271 U'
    return False

FN_CUE = re.compile(r'^(\d{1,2}|[!*™“”‘’\u2018\u2019]+)\s+\S')
PARA_DOT = re.compile(r'^(\d{1,2})[.,:]\s+\S')

def page_split():
    pages, cur = [], []
    for i, ln in enumerate(lines):
        if is_pagebreak(ln):
            pages.append(cur); cur = []
        else:
            cur.append((offs[i], ln))
    pages.append(cur)
    return pages

pages = page_split()

# ---- 3. within each page, split off the footnote suffix
OCR_ALT = {9:{2},8:{3},0:{6,9},5:{3},1:{1},7:{7},4:{4},2:{2},3:{3},6:{6}}
def could_be(v, e):
    return v == e or e in OCR_ALT.get(v, set())

body_stream = []   # (abs_offset, line)
fn_stream = []     # (abs_offset, line)
for page in pages:
    # find footnote zone: candidate = last run; take first FN-cue line index such
    # that no clear paragraph-dot line follows it on this page
    fn_start = None
    for i, (o, ln) in enumerate(page):
        s = ln.strip()
        if not s: continue
        if FN_CUE.match(s) and not PARA_DOT.match(s):
            later_para = any(PARA_DOT.match(l.strip()) for _, l in page[i+1:])
            if not later_para:
                fn_start = i
                break
    if fn_start is None:
        body_stream.extend(page)
    else:
        body_stream.extend(page[:fn_start])
        fn_stream.extend(page[fn_start:])

# ---- 4. walk the body stream chapter by chapter, paragraph by paragraph
# chapter boundaries by abs offset
chap_bounds = sorted((heads[n], n) for n in heads)
def chap_of(o):
    c = 0
    for start, n in chap_bounds:
        if o >= start: c = n
        else: break
    return c

chapters = {n: {'titel_lines': [], 'paras': [], 'fns': []} for n in range(0, 41)}
cur_chap, expected, cur_para, cur_lines = 0, 1, None, []

def flush():
    global cur_para, cur_lines
    if cur_para is not None and cur_lines:
        chapters[cur_chap]['paras'].append((cur_para, cur_lines))
    elif cur_lines and cur_chap > 0:
        chapters[cur_chap]['titel_lines'].extend(cur_lines)
    elif cur_lines:
        chapters[0]['titel_lines'].extend(cur_lines)
    cur_para, cur_lines = None, []

for o, ln in body_stream:
    s = ln.strip()
    c = chap_of(o)
    if c != cur_chap:
        flush()
        cur_chap, expected, cur_para = c, 1, None
    if not s:
        continue
    if s.startswith('CHAPTER'):
        continue
    m = re.match(r'^(\d{1,2})[.,:]?\s+(.*)', s)
    started = False
    if m:
        v = int(m.group(1))
        if could_be(v, expected):
            flush()
            cur_para = expected
            expected += 1
            cur_lines = [m.group(2)]
            started = True
    if not started:
        cur_lines.append(s)
flush()

for o, ln in fn_stream:
    s = ln.strip()
    if s:
        chapters[chap_of(o)]['fns'].append(s)

def join_text(ls):
    txt = ' '.join(l for l in ls if l.strip())
    txt = re.sub(r'(\w)[-\u00ad]\s+(\w)', r'\1\2', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    return txt

out = {'front_raw': seg[:heads[1]], 'chapters': {}}
bad = 0
for n in range(1, 41):
    ch = chapters[n]
    paras = [{'n': pn, 'en': join_text(pl)} for pn, pl in ch['paras']]
    ns = [p['n'] for p in paras]
    exp = list(range(1, EXPECT[n]+1))
    ok = ns == exp
    if not ok: bad += 1
    title = join_text(ch['titel_lines'])
    out['chapters'][f'c{n}'] = {'titel': title, 'paras': paras, 'fns': ch['fns']}
    print(f"c{n:<3d} {'OK ' if ok else 'BAD'} got={len(ns) if ok else ns} exp={EXPECT[n]} fn={len(ch['fns'])}  {title[:60]}")
print('mismatched chapters:', bad)
json.dump(out, io.open('C:/Users/leofa/AppData/Local/Temp/longridge/dir-draft2.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
