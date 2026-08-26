# Longridge 1919: the seventeen Additional Notes (A-Q), as essays,
# each keyed editorially to a section and unit range of the Exercises.
import io, re, json

t = io.open('C:/Users/leofa/AppData/Local/Temp/longridge_djvu.txt', encoding='utf-8', errors='replace').read()
an = t[512113:676029]
end_all = an.find('PART I')

NOTES = [
 ('A', 17,     'On the Adaptation of the Exercises to Various Classes of Retreatants', 'ann', 18, 20),
 ('B', 9514,   'On the Principle and Foundation', 'tit', 23, 23),
 ('C', 19029,  'On the Exercise of the Three Powers of the Soul', 'exx', 45, 54),
 ('D', 27026,  'On the First Exercise', 'exx', 45, 54),
 ('E', 34876,  'On the Second Exercise', 'exx', 55, 61),
 ('F', 39322,  'On the Third and Fourth Exercises', 'exx', 62, 64),
 ('G', 42424,  'On the Fifth Exercise', 'exx', 65, 71),
 ('H', 49365,  'On the Matter of the Meditations of the First Week', 'exx', 45, 72),
 ('I', 61606,  'On the Form of the Meditations of the First Week', 'exx', 45, 72),
 ('J', 70893,  'On the Kingdom of Christ', 'king', 91, 100),
 ('K', 79290,  'On the Purpose and Order of the Exercises of the Second Week', 'incnat', 101, 117),
 ('L', 88062,  'On Two Standards', 'states', 136, 148),
 ('M', 101812, 'On Three Classes', 'states', 149, 157),
 ('N', 110317, 'On Three Modes of Humility', 'states', 165, 168),
 ('O', 117483, 'On the Form of the Exercises of the Second and Following Weeks', 'rep', 118, 131),
 ('P', 136349, "On 'Contemplation' as used in the Exercises, and its Relation to Contemplation as understood in Mystical Theology", 'incnat', 101, 117),
 ('Q', 149966, 'On the Rules for the Discernment of Spirits', 'disc', 313, 336),
]

def clean_paras(chunk):
    paras, cur, in_fn = [], [], False
    def flushp():
        nonlocal cur
        if cur:
            s = ' '.join(cur)
            s = re.sub(r'(\w)[-\u00ad]\s+(\w)', r'\1\2', s)
            s = re.sub(r'\s+', ' ', s).strip()
            if len(s) > 2:
                paras.append(s)
        cur = []
    for ln in chunk.split('\n'):
        s = ln.strip()
        if not s:
            flushp(); continue
        letters = [c for c in s if c.isalpha()]
        upr = sum(1 for c in letters if c.isupper())
        if re.fullmatch(r'\d{1,3}', s):
            in_fn = False; continue
        if letters and upr/len(letters) > 0.7 and re.search(r'\d', s):
            in_fn = False; continue          # running head
        if s.startswith('NOTE') or s.startswith('NOTH'):
            continue
        if letters and upr/len(letters) > 0.6 and len(s) >= 10 and not re.search(r'[a-z]{4,}', s):
            continue                          # caps/smallcaps heading line
        if in_fn:
            continue
        if re.match(r'^[\d*]{1,2}\s+\S', s) and not re.match(r'^\d{1,2}\s+\d', s) and re.match(r'^[\d*]', s):
            in_fn = True; continue
        cur.append(s)
    flushp()
    return paras

def fix(s):
    s = re.sub(r'\b8\.\s+(?=[A-Z])', 'S. ', s)
    s = s.replace('Hxercises', 'Exercises').replace('Fxercises', 'Exercises')
    s = re.sub(r'(?<=[a-z] )1s(?= [a-z])', 'is', s)
    s = re.sub(r'(?<=[a-z] )ws(?= [a-z])', 'is', s)
    s = re.sub(r'\s*[|©®™]+\s*', ' ', s)
    s = re.sub(r'\s{2,}', ' ', s)
    s = re.sub(r'\s+([,.;:!?])', r'\1', s)
    return s.strip()

out = []
for i, (nid, pos, titel, sec, von, bis) in enumerate(NOTES):
    end = NOTES[i+1][1] if i+1 < len(NOTES) else end_all
    paras = [fix(p) for p in clean_paras(an[pos:end])]
    # drop title residue at the start (OCR'd small-caps headings)
    while paras and (len(paras[0]) < 60 or
                     re.match(r"^(On T|NOTE|‘NOTE|NOTH|WEEK\b|THEOLOGY\b|Sal\b)", paras[0])):
        paras.pop(0)
    out.append({'id': nid, 'titel': titel, 'section': sec, 'von': von, 'bis': bis, 'paras': paras})
    print(f"{nid}: {len(paras):3d} paras, {sum(len(p) for p in paras):6d} chars | first: {paras[0][:80] if paras else '—'}")

json.dump(out, io.open('C:/Users/leofa/AppData/Local/Temp/longridge/notes-final.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
