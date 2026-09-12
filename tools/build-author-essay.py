# -*- coding: utf-8 -*-
# Convert an author-essay .docx into the JSON the author page renders
# (the schema of data/pilgrim_profile.json: titel, untertitel, autor, datum,
# copyright, sections [{level, titel, inhalt: [{t:'p', s} | {t:'table',
# caption, header, rows}]}], references [str]).
#
# The essays are the author's own work, all rights reserved — deliberately
# outside the open licences of the rest of the repository, and outside the
# concordance, the statistics and the dialogue.
#
# Usage: python tools/build-author-essay.py <manuscript.docx> <out.json>
import io, json, re, sys, zipfile
from html import unescape

src, out = sys.argv[1], sys.argv[2]
xml = zipfile.ZipFile(src).read('word/document.xml').decode('utf-8')
body = re.search(r'<w:body>(.*)</w:body>', xml, re.S).group(1)
elems = re.findall(r'(<w:p\b.*?</w:p>|<w:tbl>.*?</w:tbl>)', body, re.S)

def ptext(e):
    return unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', e))).strip()

def pstyle(e):
    m = re.search(r'<w:pStyle w:val="([^"]+)"', e)
    return m.group(1) if m else ''

HEAD = {'Heading1': 1, 'berschrift1': 1, 'Heading2': 2, 'berschrift2': 2}

# title block: the first paragraphs before the table of contents
tb = [ptext(e) for e in elems[:24] if not e.startswith('<w:tbl>')]
tb = [t for t in tb if t]
titel, untertitel = tb[0], tb[1]
autor = tb[2] + (f' {tb[3]}' if tb[3].startswith('(') else '')
datum = next(t for t in tb if re.fullmatch(r'[A-Z][a-z]+ \d{4}', t))
copyright_ = next(t for t in tb if t.startswith('©')).replace(' – ', ' ') + \
    ('' if next(t for t in tb if t.startswith('©')).rstrip().endswith('.') else '.') \
    + ' All rights reserved.'
copyright_ = re.sub(r'\.? All rights reserved\.$', '. All rights reserved.', copyright_)

# body: from the first Heading1 on; TOC paragraphs never carry Heading styles
sections, refs, cur, in_refs = [], [], None, False
i = next(k for k, e in enumerate(elems)
         if pstyle(e) in HEAD and ptext(e) and 'TOC' not in pstyle(e))
while i < len(elems):
    e = elems[i]
    if e.startswith('<w:tbl>'):
        rows = [[ptext(c) for c in re.findall(r'<w:tc\b.*?</w:tc>', r, re.S)]
                for r in re.findall(r'<w:tr\b.*?</w:tr>', e, re.S)]
        cap = ''
        if cur and cur['inhalt'] and cur['inhalt'][-1]['t'] == 'p' \
                and cur['inhalt'][-1]['s'].startswith('Table '):
            cap = cur['inhalt'].pop()['s']
        cur['inhalt'].append({'t': 'table', 'caption': cap,
                              'header': rows[0], 'rows': rows[1:]})
        i += 1
        continue
    st, t = pstyle(e), ptext(e)
    i += 1
    if not t:
        continue
    if st in HEAD:
        if t.lower() == 'references':
            in_refs = True
            continue
        in_refs = False
        cur = {'level': HEAD[st], 'titel': t, 'inhalt': []}
        sections.append(cur)
        continue
    if in_refs:
        if not t.startswith('©'):        # the manuscript's closing rights line
            refs.append(t)
    elif cur is not None:
        cur['inhalt'].append({'t': 'p', 's': t})

doc = {'titel': titel, 'untertitel': untertitel, 'autor': autor,
       'datum': datum, 'copyright': copyright_,
       'sections': sections, 'references': refs}
json.dump(doc, io.open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', out, '-', len(sections), 'sections,',
      sum(len(s["inhalt"]) for s in sections), 'blocks,', len(refs), 'references')
for s in sections:
    print(' ', '  ' * (s['level'] - 1) + s['titel'][:70], f'({len(s["inhalt"])})')
