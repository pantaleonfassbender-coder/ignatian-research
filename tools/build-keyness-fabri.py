# -*- coding: utf-8 -*-
# Add the Memoriale's keyness profile to data/keyness.json.
#
# The six original profiles were computed with a spaCy pipeline over the
# core texts; that pipeline is not part of this repository, and the
# Memoriale joined the corpus after it had run. This script computes the
# missing profile with the repository's own means, against the SAME
# reference counts the other profiles used: the per-work lemma matrix in
# data/terms.json (900 content lemmas over the six other works) and the
# corpus totals in data/corpus.json. Log-likelihood is Dunning's G2, the
# same statistic as the rest of the page. The tokenizer is deliberately
# simple (lowercase alpha tokens, a function-word stoplist, light suffix
# folding onto the lemma inventory of terms.json); the difference of
# pipeline, and the fact that the Memoriale's English is this site's
# working translation, are disclosed on the method page.
#
# Usage: python tools/build-keyness-fabri.py
import io, json, math, os, re
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def J(name):
    return json.load(io.open(os.path.join(REPO, 'data', name), encoding='utf-8'))

mem = J('memoriale.json')
terms = J('terms.json')
corpus = J('corpus.json')
keyness = J('keyness.json')

# ---- the Memoriale's English, tokenized -------------------------------
texts = []
for sec in mem['sections'] if 'sections' in mem else mem.get('sektionen', []):
    for u in sec['units']:
        if u.get('en'):
            texts.append(u['en'])
raw = ' '.join(texts).lower()
tokens = re.findall(r"[a-z][a-z'’\-]*[a-z]|[a-z]", raw)

STOP = set('''a an the and or but nor so yet for of in on at by to from with
without into unto onto upon about above below under over between among through
during before after since until while as if then than that this these those
there here it its itself he him his himself she her hers herself they them
their theirs themselves we us our ours ourselves you your yours yourself i me
my mine myself who whom whose which what when where why how not no nor never
none nothing all any both each few more most other some such only own same
very can cannot could may might must shall should will would do does did done
doing have has had having be am is are was were been being become becomes
became again further once out up down off away also because against says said
say let lets us one two three first second third et etc do not don came come
go goes going went get gets got give gives gave given take takes took taken
make makes made seem seemed like well even much many still too now day days
today yesterday tomorrow thing things way ways man men whether ever every
towards toward within therefore thus hence yes o oh ye thou thee thy thine'''.split())

# light folding onto the lemma inventory the other profiles used
inventory = set(terms.keys())
def lemma(w):
    w = w.strip("'’-")
    if w in inventory or len(w) < 3:
        return w
    for a, b in (("'s", ''), ('ies', 'y'), ('ses', 's'), ('es', ''), ('s', ''),
                 ('ing', ''), ('ing', 'e'), ('ed', ''), ('ed', 'e')):
        if w.endswith(a):
            c = w[:len(w) - len(a)] + b
            if c in inventory:
                return c
    return w

cnt = Counter()
for w in tokens:
    if w in STOP or len(w) < 3 or "'" in w or '’' in w:
        continue
    cnt[lemma(w)] += 1

# ---- reference: the six other works, from the existing matrix ----------
ids6 = [i for i in corpus['ids'] if i != 'fabri']
ref = {w: sum(v['dist']) for w, v in terms.items()}
# both corpus sizes over the same word universe: the stored inventory
N1 = sum(f for w, f in cnt.items() if w in inventory)
# reference size over the same universe: the inventory totals
N2 = sum(ref.values())

def g2(o1, o2, n1, n2):
    e1 = n1 * (o1 + o2) / (n1 + n2)
    e2 = n2 * (o1 + o2) / (n1 + n2)
    ll = 0.0
    if o1: ll += o1 * math.log(o1 / e1)
    if o2: ll += o2 * math.log(o2 / e2)
    return 2 * ll

rows = []
for w, f in cnt.items():
    if f < 5:
        continue
    # compare like with like: only the lemma inventory the original
    # pipeline stored (terms.json) — words outside it have no reference
    # counts and would only profile the pipelines' difference
    if w not in inventory:
        continue
    o2 = ref.get(w, 0)
    ll = g2(f, o2, N1, N2)
    if f / N1 > (o2 / N2 if N2 else 0):          # keyness, not anti-keyness
        rows.append({'w': w, 'f': f, 'll': round(ll, 1)})
rows.sort(key=lambda r: -r['ll'])
keyness['fabri'] = rows[:45]

json.dump(keyness, io.open(os.path.join(REPO, 'data', 'keyness.json'), 'w',
          encoding='utf-8'), ensure_ascii=False, indent=1)
print('fabri: N1 =', N1, '| N2 =', N2, '| profile:', len(keyness['fabri']))
for r in keyness['fabri'][:18]:
    print('  ', r['w'], r['f'], r['ll'])
