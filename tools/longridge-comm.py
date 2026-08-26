# Longridge 1919: commentary layer on the Exercises.
# The body (translation + numbered notes) is cut into blocks at verified
# anchor offsets; each block is keyed to an Exx unit range [von]-[bis].
import io, re, json

t = io.open('C:/Users/leofa/AppData/Local/Temp/longridge_djvu.txt', encoding='utf-8', errors='replace').read()
body = t[58020:512113]

# XIV anchor: paragraph start before "olation and much fervour"
i = body.find('olation and much fervour')
xiv = body.rfind('\n\n', 0, i-60)
# humility anchor: paragraph containing "following three Modes of Humility"
j = body.find('following three Modes of Humility')
hum = body.rfind('\n\n', 0, j-200)
# obtaining-love heading anchor
k = body.find('CONTEMPLATION FOR OBTAINING LOVE (1)')
love = body.rfind('\n\n', 0, k)
# fuller-discernment anchor
m2 = body.find('Rules to the same effect, with a fuller')
full = body.rfind('\n\n', 0, m2)
# food rules anchor
f2 = body.find('for ordering oneself for the future in the matter of food')
food = body.rfind('\n\n', 0, f2-20)
# FOURTH WEEK heading anchor
w4 = body.find('FOURTH WEEK', 330000)

# (start, sectionId, von, bis, label)
BLOCKS = [
 (122,    'ann', 1, 20,  'Annotations: title and purpose'),
 (2860,   'ann', 1, 3,   'Annotations I–III'),
 (16076,  'ann', 4, 4,   'Annotation IV'),
 (19832,  'ann', 5, 5,   'Annotation V'),
 (21347,  'ann', 6, 6,   'Annotation VI'),
 (22139,  'ann', 7, 7,   'Annotation VII'),
 (24557,  'ann', 8, 8,   'Annotation VIII'),
 (25204,  'ann', 9, 9,   'Annotation IX'),
 (25879,  'ann', 10, 10, 'Annotation X'),
 (27682,  'ann', 11, 11, 'Annotation XI'),
 (28008,  'ann', 12, 12, 'Annotation XII'),
 (28524,  'ann', 13, 13, 'Annotation XIII'),
 (xiv,    'ann', 14, 15, 'Annotations XIV–XV'),
 (32063,  'ann', 16, 17, 'Annotations XVI–XVII'),
 (34938,  'ann', 18, 18, 'Annotation XVIII'),
 (42858,  'ann', 19, 19, 'Annotation XIX'),
 (43945,  'ann', 20, 20, 'Annotation XX'),
 (47508,  'ann', 1, 20,  'Synopsis of the Annotations'),
 (49617,  'tit', 21, 22, 'Title and Presupposition'),
 (52273,  'tit', 23, 23, 'Principle and Foundation'),
 (65292,  'tit', 23, 23, 'Explanation of the Foundation'),
 (67031,  'tit', 23, 23, 'The End of Man'),
 (82536,  'tit', 23, 23, 'The End of Creatures'),
 (88232,  'tit', 23, 23, 'The Right Use of Creatures'),
 (91431,  'tit', 23, 23, 'Indifference'),
 (96444,  'exam', 24, 31, 'The Particular Examination'),
 (102250, 'exam', 32, 43, 'General Examination of Conscience'),
 (111359, 'exam', 44, 44, 'General Confession and Communion'),
 (113747, 'exx', 45, 54, 'The First Exercise'),
 (134128, 'exx', 55, 61, 'The Second Exercise'),
 (144118, 'exx', 62, 63, 'The Third Exercise'),
 (148441, 'exx', 64, 64, 'The Fourth Exercise'),
 (149205, 'exx', 65, 72, 'The Fifth Exercise'),
 (156242, 'add', 73, 90, 'The Additions'),
 (170747, 'king', 91, 100, 'Second Week: the Kingdom of Christ'),
 (190477, 'incnat', 101, 109, 'The First Day: first Contemplation (Incarnation)'),
 (207758, 'incnat', 110, 117, 'The Second Contemplation (Nativity)'),
 (212321, 'rep', 118, 119, 'The Third Contemplation'),
 (213459, 'rep', 120, 120, 'The Fourth Contemplation'),
 (213593, 'rep', 121, 131, 'The Fifth Contemplation: Application of the Senses'),
 (220185, 'rep', 132, 135, 'The Second and Third Days; Preamble on States'),
 (228051, 'states', 136, 148, 'The Fourth Day: Two Standards'),
 (249559, 'states', 149, 157, 'Three Classes of Men'),
 (265694, 'states', 158, 158, 'The Fifth Day'),
 (270280, 'states', 159, 159, 'The Sixth Day'),
 (270923, 'states', 160, 161, 'The Seventh to Twelfth Days'),
 (271320, 'states', 162, 164, 'Three Observations'),
 (hum,    'states', 165, 168, 'Three Modes of Humility'),
 (289586, 'elec', 169, 189, 'The Election'),
 (313584, 'w3', 190, 199, 'Third Week: first Contemplation'),
 (327315, 'w3', 200, 207, 'The Second Contemplation'),
 (332033, 'w3', 208, 209, 'The Second to Seventh Days'),
 (food,   'w3', 210, 217, 'Rules respecting Food'),
 (w4,     'w4', 218, 229, 'Fourth Week: first Contemplation'),
 (love,   'w4', 230, 237, 'Contemplation for obtaining Love'),
 (368394, 'modos', 238, 248, 'The First Method of Prayer'),
 (376502, 'modos', 249, 257, 'The Second Method of Prayer'),
 (379846, 'modos', 258, 260, 'The Third Method of Prayer'),
 (381812, 'myst1', 261, 261, 'The Mysteries of the Life of Christ: introduction'),
]
MYST = [
 (384094,262,'The Annunciation'),(384778,263,'The Visitation'),(385394,264,'The Nativity'),
 (385992,265,'The Shepherds'),(386393,266,'The Circumcision'),(386671,267,'The Three Magi Kings'),
 (387157,268,'The Purification and Presentation'),(387741,269,'The Flight into Egypt'),
 (388152,270,'The Return from Egypt'),(388542,271,'The Life from Twelve to Thirty Years'),
 (389283,272,'The Coming to the Temple at Twelve'),(390192,273,'The Baptism'),
 (390802,274,'The Temptations'),(391303,275,'The Call of the Apostles'),
 (392336,276,'The First Miracle, at Cana'),(392837,277,'The Sellers cast out of the Temple'),
 (393487,278,'The Sermon on the Mount'),(394492,279,'The Tempest calmed'),
 (395076,280,'The Walking on the Sea'),(395745,281,'The Apostles sent to preach'),
 (396405,282,'The Conversion of Magdalen'),(397003,283,'The Feeding of the Five Thousand'),
 (397581,284,'The Transfiguration'),(398339,285,'The Resurrection of Lazarus'),
 (398909,286,'The Supper at Bethany'),(399352,287,'Palm Sunday'),
 (399960,288,'The Preaching in the Temple'),(400181,289,'The Last Supper'),
 (401072,290,'From the Supper to the Garden'),(401962,291,'From the Garden to the House of Annas'),
 (402916,292,'From the House of Annas to the House of Caiphas'),
 (403503,293,'From the House of Caiphas to Pilate'),(404097,294,'From Pilate to Herod'),
 (404476,295,'From Herod back to Pilate'),(405240,296,'From the House of Pilate to the Cross'),
 (405862,297,'The Mysteries on the Cross'),(406648,298,'From the Cross to the Sepulchre'),
 (407007,299,'The Resurrection; first Apparition'),(407375,300,'The Second Apparition'),
 (407923,301,'The Third Apparition'),(408378,302,'The Fourth Apparition'),
 (408824,None,None),  # fifth + sixth apparition (sixth heading lost in OCR)
 (409918,305,'The Seventh Apparition'),(410447,306,'The Eighth Apparition'),
 (411170,307,'The Ninth Apparition'),(411591,308,'The Tenth Apparition'),
 (411789,309,'The Eleventh Apparition'),(411874,310,'The Twelfth Apparition'),
 (412014,311,'The Thirteenth Apparition'),(412184,312,'The Ascension'),
]
for pos, n, lab in MYST:
    if n is None:
        BLOCKS.append((pos, 'myst2', 303, 304, 'The Fifth and Sixth Apparitions'))
    else:
        sec = 'myst1' if n <= 287 else 'myst2'
        BLOCKS.append((pos, sec, n, n, lab))
BLOCKS += [
 (413404, 'disc', 313, 327, 'Rules for the Discernment of Spirits (First Week)'),
 (full,   'disc', 328, 336, 'Rules for the fuller Discernment of Spirits (Second Week)'),
 (437396, 'rules', 337, 344, 'Rules for the Distribution of Alms'),
 (441585, 'rules', 345, 351, 'Concerning Scruples'),
 (446496, 'rules', 352, 370, 'Rules for Thinking with the Church'),
]
BLOCKS.sort()
starts = [b[0] for b in BLOCKS]
assert starts == sorted(set(starts)), 'duplicate/misordered anchors'

CAPS_HEAD = re.compile(r'^[^a-z]*$')
def clean_paras(chunk):
    """lines -> paragraphs [{t:'text'|'note', s}], dropping running heads,
    page numbers and footnote suffixes."""
    paras, cur, in_fn = [], [], False
    def flushp():
        nonlocal cur
        if cur:
            s = ' '.join(cur)
            s = re.sub(r'(\w)[-\u00ad]\s+(\w)', r'\1\2', s)
            s = re.sub(r'\s+', ' ', s).strip()
            if len(s) > 2:
                t_ = 'note' if re.match(r'^\(\d{1,3}\)', s) else 'text'
                paras.append({'t': t_, 's': s})
        cur = []
    for ln in chunk.split('\n'):
        s = ln.strip()
        if not s:
            flushp()
            continue
        letters = [c for c in s if c.isalpha()]
        upr = sum(1 for c in letters if c.isupper())
        if re.fullmatch(r'\d{1,3}', s):          # bare page number = page break
            in_fn = False
            continue
        if letters and upr/len(letters) > 0.7 and re.search(r'\d', s):
            in_fn = False                         # running head with page no.
            continue
        if letters and upr/len(letters) > 0.85 and len(s) >= 6:
            continue                              # caps heading line
        if in_fn:
            continue
        if re.match(r'^\d{1,2}\s+\S', s) and not re.match(r'^\d{1,2}\s+\d', s):
            in_fn = True                          # footnote suffix begins
            continue
        cur.append(s)
    flushp()
    return paras

def fix(s):
    s = re.sub(r'\b8\.\s+(?=[A-Z])', 'S. ', s)
    s = s.replace('Hxercises', 'Exercises').replace('Fxercises', 'Exercises')
    s = s.replace('Exereises', 'Exercises').replace('Hlection', 'Election')
    s = re.sub(r'(?<=[a-z] )1s(?= [a-z])', 'is', s)
    s = re.sub(r'(?<=[a-z] )rs(?= [a-z])', 'is', s)
    s = re.sub(r'(?<=[a-z] )ws(?= [a-z])', 'is', s)
    s = re.sub(r'(?<=[a-z] )1t(?= [a-z])', 'it', s)
    s = re.sub(r'\s*[|©®™]+\s*', ' ', s)
    s = re.sub(r'\s+[—_]\s+', ' — ', s)
    s = re.sub(r'\s{2,}', ' ', s)
    s = re.sub(r'\s+([,.;:!?])', r'\1', s)
    return s.strip()

sections = {}
order = []
for i, (pos, sec, von, bis, label) in enumerate(BLOCKS):
    end = BLOCKS[i+1][0] if i+1 < len(BLOCKS) else len(body)
    paras = clean_paras(body[pos:end])
    for p in paras:
        p['s'] = fix(p['s'])
    if sec not in sections:
        sections[sec] = []
        order.append(sec)
    sections[sec].append({'label': label, 'von': von, 'bis': bis, 'paras': paras})

out = {'sections': [{'id': s, 'blocks': sections[s]} for s in order]}
json.dump(out, io.open('C:/Users/leofa/AppData/Local/Temp/longridge/comm-draft.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)

nb = sum(len(v) for v in sections.values())
np_ = sum(len(b['paras']) for v in sections.values() for b in v)
nn = sum(1 for v in sections.values() for b in v for p in b['paras'] if p['t']=='note')
ch = sum(len(p['s']) for v in sections.values() for b in v for p in b['paras'])
print(f"blocks={nb} paras={np_} notes={nn} chars={ch}")
for s in order:
    print(f"  {s:8s} {len(sections[s])} blocks, {sum(len(b['paras']) for b in sections[s])} paras")
