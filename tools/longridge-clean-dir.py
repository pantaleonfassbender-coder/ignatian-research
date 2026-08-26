# Cleanup pass: structural repairs (c4, c28), footnote-tail trimming,
# systematic OCR normalisation, title fixes.
import io, json, re

DIR = 'C:/Users/leofa/AppData/Local/Temp/longridge/'
f = json.load(io.open(DIR+'dir-final.json', encoding='utf-8'))
C = f['chapters']

def para(c, n):
    return [p for p in C[c]['paras'] if p['n'] == n][0]

# ---- structural repair c4:
# [2] = footnote + continuation of para 1; [3] = real paras 2+3 fused
p2 = para('c4', 2)['en']
p3 = para('c4', 3)['en']
i = p2.find('especially of friends')
j = p3.find('Besides a director')
assert i > -1 and j > 0
para('c4', 1)['en'] += ' ' + p2[i:].strip()
para('c4', 2)['en'] = p3[:j].strip()
para('c4', 3)['en'] = p3[j:].strip()

# ---- structural repair c28: fn + para1-tail + real para2 fused into [2]
p2 = para('c28', 2)['en']
i = p2.find('first, we must go on')
j = p2.find('For these two methods')
assert i > -1 and j > i
tail = p2[i:j].strip()
tail = re.sub(r'\s*2\.\s*$', '', tail)
para('c28', 1)['en'] += ' ' + tail
para('c28', 2)['en'] = p2[j:].strip()

# ---- trailing footnote-junk trimming (hand-verified cut points)
CUTS = [
    ('c21', 3, '1 See Observation'),
    ('c13', 8, '1 Cassian'),
    ('c38', 1, 'fe .Cor'),
]
for c, n, marker in CUTS:
    p = para(c, n)
    i = p['en'].find(marker)
    if i > -1:
        p['en'] = p['en'][:i].strip()

# c9[9]: two-page footnote (Du Cange/Rashdall) fused mid-paragraph
p = para('c9', 9)
i = p['en'].find('1 Baccalaurei')
j = p['en'].find('deal directly with such matters')
if i > -1 and j > i:
    p['en'] = (p['en'][:i] + p['en'][j:]).strip()

# ---- global OCR normalisation, applied to every English text
def fix(s):
    s = re.sub(r'\b8\.\s+(Ignatius|Paul|Peter|John|Francis|Augustine|Thomas|Gregory|Bernard|Basil|Chrysostom|Ambrose|Jerome|P\b)', r'S. \1', s)
    s = re.sub(r'(?<=[a-z] )1s(?= [a-z])', 'is', s)
    s = re.sub(r'(?<=[a-z] )rs(?= [a-z])', 'is', s)
    s = re.sub(r'(?<=[a-z] )ws(?= [a-z])', 'is', s)
    s = re.sub(r'(?<=[a-z] )1t(?= [a-z])', 'it', s)
    s = s.replace('Hxercises', 'Exercises').replace('Hlection', 'Election')
    s = s.replace('Furst', 'First').replace('Fxercises', 'Exercises')
    s = s.replace('Exereises', 'Exercises').replace('Exercitia >', 'Exercitia')
    s = re.sub(r'\s+[—_]\s+', ' ', s)          # stray dash/underscore line-end artifacts
    s = re.sub(r'\s*[|©®™]+\s*', ' ', s)        # stray pipes/copyright marks
    s = re.sub(r'\s*\'\'\s*', ' ', s)
    s = re.sub(r'\s{2,}', ' ', s)
    s = re.sub(r'\s+([,.;:!?])', r'\1', s)
    s = re.sub(r'\.\s*\.\s*(?=[A-Z])', '. ', s) # doubled periods
    return s.strip()

for c in C.values():
    c['titel'] = fix(c['titel'])
    for p in c['paras']:
        p['en'] = fix(p['en'])
f['praef']['text'] = fix(f['praef']['text'])
f['prooem']['titel'] = fix(f['prooem']['titel'])
for p in f['prooem']['paras']:
    p['en'] = fix(p['en'])
f['translator_note'] = fix(f['translator_note'])

# ---- hand-corrected chapter titles (OCR of italic type is poor)
TITLES = {
 'c1': 'How men are to be induced to make the Exercises',
 'c2': 'What ought to be the dispositions of those who come to make the Exercises',
 'c3': 'Of the instructions to be given to one entering upon the Exercises',
 'c4': 'Of a suitable place for the Exercises, and of certain particulars concerning them',
 'c5': 'What manner of person he who gives the Exercises ought to be, and what he ought to do',
 'c6': 'Of visiting the exercitant',
 'c7': 'Of requiring an account of the meditation',
 'c8': 'Of giving the meditations',
 'c9': 'Of various kinds of persons to whom the Exercises may be given, and of the First Week and its Exercises',
 'c10': 'Of the manner of giving the Exercises to Ours',
 'c11': 'Of the First Week in general',
 'c12': 'Of the Foundation',
 'c13': 'Of the twofold Examination',
 'c14': 'Of the first Exercise of the First Week',
 'c15': 'Of the other Exercises of the First Week',
 'c16': 'Of general Confession',
 'c17': 'Of the close of the First Week',
 'c18': 'Of the Second Week, and first of the end set before us in it',
 'c19': 'Of the first four Exercises of the Second Week',
 'c20': 'Of the fifth Exercise of the Second Week, which is the application of the senses',
 'c21': 'Of the hours for meditation, for spiritual reading, and for visiting the exercitant',
 'c22': 'Of the Election, its importance, and the method to be observed in it',
 'c23': 'What sort of persons those who are admitted to the Election ought to be',
 'c24': 'What sort of person the director of him who is about to make his Election ought to be',
 'c25': 'What are the matters with which the Election is concerned',
 'c26': 'Of the three Times in which a good Election may be made',
 'c27': 'A comparison of the second Time of making an Election with the third',
 'c28': 'Of the first and second methods of making a good Election',
 'c29': 'Concerning the procedure and order of the Election',
 'c30': 'Of the actual Election according to the method of the second Time',
 'c31': 'Of making an Election according to the first and second methods of the third Time',
 'c32': 'Of prayer after the Election has been made',
 'c33': 'What the director should do when he perceives that he who is making the Election is under the influence of some inordinate desire',
 'c34': 'Of those whose state of life is already fixed',
 'c35': 'Of the Third Week',
 'c36': 'Of the Fourth Week',
 'c37': 'Of three methods of prayer',
 'c38': 'Of imparting the Rules',
 'c39': 'A brief explanation of some things concerning the three Ways, viz. the Purgative, the Illuminative, and the Unitive',
 'c40': 'What instructions should be given to the exercitant at the close of the Exercises',
}
for k, v in TITLES.items():
    C[k]['titel'] = v

json.dump(f, io.open(DIR+'dir-clean.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)

# report remaining suspects
for cname in [f'c{n}' for n in range(1,41)]:
    for p in C[cname]['paras']:
        for pat in [r'\bp\.\s?\d{2,3}', r'See (Observation|Note)', r'\bCf[.,]', r'\bT\.?e\.', r'\d{3}\s+THE', r'\bLe\.\s']:
            if re.search(pat, p['en']):
                print(f"{cname}[{p['n']}] {pat} :: …{p['en'][max(0,re.search(pat,p['en']).start()-60):re.search(pat,p['en']).start()+80]}…")
print('praef:', f['praef']['text'][:200])
print('prooem[1]:', f['prooem']['paras'][0]['en'][:150])
PY_DONE = True
