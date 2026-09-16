# -*- coding: utf-8 -*-
# Build data/ratio.json — the Ratio Studiorum of 1599, in selections: the
# rules for the professor of scholastic theology and the professor of
# philosophy, bilingual.
#
# Latin: the definitive Ratio atque Institutio Studiorum of 1599 as printed
# in the Institutum Societatis Iesu, vol. III (Florence: ex typographia a
# SS. Conceptione, 1893; Internet Archive Institutum3) — a pure text of the
# 1599 rules, collated where the OCR is doubtful with G. M. Pachtler's
# edition (Ratio studiorum et institutiones scholasticae Societatis Jesu,
# vol. II = Monumenta Germaniae Paedagogica V, Berlin 1887; Internet
# Archive ratiostudiorumetinstitutiones2, which prints the 1599 and 1832
# texts in parallel columns). Both printings are in the United States
# public domain. The 1893 printing's marginal captions and source
# references are not carried; the English is an unofficial working
# translation made for this site directly from the Latin (CC0).
#
# These two series are the hinge between the Constitutions and the school's
# doctrine of the soul: rule 2 of the theology professor binds the schools
# to St. Thomas — with the Society's own liberty stated in the same breath
# — and rule 2 of the philosophy professor binds them to Aristotle, with
# the De anima course laid out in the rules that follow.
#
# Usage: python tools/build-ratio.py institutum3.txt
import io, json, os, re, sys
from ratio_en import EN_THEOL, EN_PHIL

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = io.open(sys.argv[1], encoding='utf-8').read().splitlines()

def find_line(rx, start=0):
    r = re.compile(rx)
    return next(i for i in range(start, len(lines)) if r.match(lines[i]))

i_th = find_line(r'^\s*PROFESSORIS\s+SCHOLASTICAE\s+THEOLOGIAE\.\s*$')
i_ca = find_line(r'^\s*CATALOGUS\s+ALIQUOT', i_th)
i_ph = find_line(r'^\s*REGULAE\s+PROFESSORIS\s+PHILOSOPHIAE\.\s*$', i_ca)
i_mo = find_line(r'.*PROFESSORIS\s+PHILOSOPHIAE\s+MORALIS', i_ph)

NOISE = [
    re.compile(r'^\s*(Digitized|Google)\b'),
    re.compile(r"^\s*\d{0,4}\s*[A-Z][A-Z .,'’\-]{5,}\s*\d{0,4}\s*$"),   # running heads
    re.compile(r"^\s*[ivxlcIVXLC0-9 .,*^~•£_'\-]{1,10}\s*$"),
]

WORD_FIXES = {
    'maguo': 'magno', 'Avemus': 'Averroes',
    # the 1893 printing's long-s and ligatures, misread by the OCR
    'Mabiae': 'Mariae', 'Bequantur': 'sequantur', 'quaestioneB': 'quaestiones',
    'quascuraque': 'quascumque', 'Bit scientia': 'sit scientia',
    'Becundum': 'secundum', 'MetaphyBicis': 'Metaphysicis',
    'Bententia': 'sententia', 'BubBtantia': 'substantia',
    'practicnm': 'practicum', 'subaltematio': 'subalternatio',
    'ca dunt': 'cadunt', 'inter pretum': 'interpretum',
    'eo reficiantur': 'eo reiiciantur', 'feBto': 'festo',
    'na- \\ turales': 'naturales', 'inci dat': 'incidat',
}

def clean(t):
    t = re.sub(r'¬\s*', '', t)                     # the printing's soft hyphens
    t = re.sub(r'(\w)-\s+(\w)', r'\1\2', t)
    t = re.sub(r'\s+', ' ', t).strip()
    for a, b in WORD_FIXES.items():
        t = t.replace(a, b)
    t = re.sub(r'\S*[<>{}^]\S*[<>{}^]\S*', ' ', t)
    for ch in '■♦•«»^~*°_·<>|':
        t = t.replace(ch, '')
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def blocks_of(seg):
    out, cur = [], []
    for raw in seg:
        s = raw.rstrip()
        if any(rx.match(s) for rx in NOISE):
            continue
        if not s.strip():
            if cur:
                out.append(cur); cur = []
            continue
        cur.append(s.strip())
    if cur:
        out.append(cur)
    kept = []
    for b in out:
        # the marginal captions and their source references form narrow
        # blocks of short lines: drop the column whole
        if max(len(l) for l in b) < 24:
            continue
        kept.append(b)
    return kept

def rules_of(seg, expect):
    """paragraph blocks folded into numbered rules, strictly sequential"""
    rules, cur = {}, 0
    for b in blocks_of(seg):
        p = clean(' '.join(b))
        if len(p) < 3:
            continue
        m = re.match(r'^(\d{1,2})\s*\.\s+(.*)$', p)
        if m and int(m.group(1)) == cur + 1:
            cur = int(m.group(1))
            rules[cur] = m.group(2)
        elif cur:
            rules[cur] = clean(rules[cur] + ' ' + p)
    assert sorted(rules) == list(range(1, expect + 1)), \
        f'expected rules 1..{expect}, got {sorted(rules)}'
    return rules

# drop-cap letters the printing sets apart at each series' first rule
OPEN_FIX = [('I I coniam artes', 'Quoniam artes'),
            ('I I coniam', 'Quoniam'),
            ('Quoniam artes vel scientiae na- \\ turales', 'Quoniam artes vel scientiae naturales'),
            ('muneris esse intelligat', 'Sui muneris esse intelligat')]

def open_fix(t):
    for a, b in OPEN_FIX:
        if t.startswith(a):
            t = b + t[len(a):]
    return t

theol = rules_of(lines[i_th + 1:i_ca], 14)
phil = rules_of(lines[i_ph + 1:i_mo], 20)
theol[1] = open_fix(theol[1]); phil[1] = open_fix(phil[1])

def units_of(rules, en):
    out = []
    for n in sorted(rules):
        out.append({'n': n, 'k': n, 'en': en[n], 'orig': rules[n]})
    return out

sections = [
 {'id': 'theol', 'zk': 'Ratio, Prof. theol.',
  'titel': 'Regulae Professoris Scholasticae Theologiae — Rules of the '
           'Professor of Scholastic Theology',
  'units': units_of(theol, EN_THEOL)},
 {'id': 'phil', 'zk': 'Ratio, Prof. phil.',
  'titel': 'Regulae Professoris Philosophiae — Rules of the Professor of '
           'Philosophy',
  'units': units_of(phil, EN_PHIL)},
]

out = {
 'id': 'ratio',
 'autor': 'Society of Jesus',
 'titel': 'Ratio Studiorum (1599, selections)',
 'jahr': '1599',
 'lang': 'la',
 'zitierweise': 'Ratio, Prof. X, reg. N',
 'quelle': ("Latin: the definitive Ratio atque Institutio Studiorum Societatis Iesu of "
            "1599, as printed in the Institutum Societatis Iesu, vol. III (Florence, "
            "1893; Internet Archive Institutum3) — collated, where the OCR is doubtful, "
            "with Pachtler's edition of 1887 (Monumenta Germaniae Paedagogica V), which "
            "prints the 1599 text beside that of 1832. Both printings are in the United "
            "States public domain. Carried: the rules for the professor of scholastic "
            "theology (14) and the professor of philosophy (20), complete; the 1893 "
            "printing's marginal captions and source references are not carried. The "
            "English is an unofficial machine-generated working translation made for "
            "this site directly from the Latin (CC0); it carries no authority — cite "
            "the Latin."),
 'hinweis': ("The pedagogical constitution of the order, and the hinge between the "
             "Constitutions and the school's doctrine of the soul: rule 2 binds the "
             "theologians to St. Thomas — with the Society's liberty stated in the "
             "same breath — and rule 2 of the philosophers binds them to Aristotle, "
             "the De anima course following in the rules on the curriculum. This is "
             "the document under which the Coimbra commentaries and Suárez's De anima "
             "were taught, and the programme of the doctrine-of-the-soul modules that "
             "follow it here. Cited by office and rule number, the print's own grid. "
             "Part of the concordance and the citation-bound dialogue; not part of "
             "the linguistic statistics, which describe the core corpus only."),
 'sections': sections,
}

path = os.path.join(REPO, 'data', 'ratio.json')
json.dump(out, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', path, '-', sum(len(s['units']) for s in sections), 'units in',
      len(sections), 'sections')
for s in sections:
    print(' ', s['zk'], '|', len(s['units']), 'rules')
