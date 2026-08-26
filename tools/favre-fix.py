# Post-processing: drop junk, repair leaked headings, split composite
# appendix item, global fixes, then renumber 1..N.
import io, json, re

d = json.load(io.open('C:/Users/leofa/AppData/Local/Temp/longridge/favre-draft.json', encoding='utf-8'))

def unit(secs, n):
    for s in secs:
        for u in s['units']:
            if u['n'] == n:
                return s, u
    return None, None

S, A = d['sections'], d['appendix']

# 1. drop junk fragment units (no real letters)
for s in S:
    s['units'] = [u for u in s['units']
                  if sum(1 for c in u['la'] if c.isalpha()) > 8]

# 2. epilog argument leak
epi = [x for x in S if x['id'] == 'epilog'][0]
leak = [u for u in epi['units'] if u['la'].startswith('inter tot')]
if leak:
    epi['arg'] = epi['arg'].rstrip('.') + ' ' + leak[0]['la']
    epi['units'].remove(leak[0])

# 3./4. strip leading (Anno NNNN) from first units of a2, a3
for sid in ('a2', 'a3'):
    it = [x for x in A if x['id'] == sid][0]
    it['units'][0]['la'] = re.sub(r'^\(Anno \d{4}\)\s*', '', it['units'][0]['la'])

# 5. a5: subheading leaked into unit; retitle
it = [x for x in A if x['id'] == 'a5'][0]
u0 = it['units'][0]
u0['la'] = re.sub(r'^DE AGENDI RATIONE CUM HAeRETICIS\s*', '', u0['la'])
it['titel'] = 'Ad Iacobum Laynium: de agendi ratione cum haereticis'
it['arg'] += ' De agendi ratione cum haereticis.'

# 6. split a7 at the two internal headings (units 405, 407)
it = [x for x in A if x['id'] == 'a7'][0]
us = it['units']
i405 = next(i for i, u in enumerate(us) if u['la'].startswith('Beati Petri Fabri epistola ad Gerardum'))
i407 = next(i for i, u in enumerate(us) if u['la'].startswith('Beati Petri Fabri adhortatio'))
a7_units = us[:i405]
a8_arg = us[i405]['la']
a8_units = us[i405+1:i407]
a9_arg = us[i407]['la']
a9_units = us[i407+1:]
it['units'] = a7_units
A.append({'id': 'a8', 'titel': 'Ad Gerardum Hammontanum, priorem Carthusiae Coloniensis',
          'arg': a8_arg, 'units': a8_units})
A.append({'id': 'a9', 'titel': 'Adhortatio ad doctum quemdam ad Societatem accedentem',
          'arg': a9_arg, 'units': a9_units})
# strip a leading (Anno 1544) inside a8 if present
if a8_units and re.match(r'^\(Anno \d{4}\)', a8_units[0]['la']):
    a8_units[0]['la'] = re.sub(r'^\(Anno \d{4}\)\s*', '', a8_units[0]['la'])

# 7. global text fixes
def gfix(x):
    x = x.replace('Perrus FABER', 'Petrus Faber').replace('paxChristi', 'pax Christi')
    x = re.sub(r'[„“”‘’]\s*', '', x)
    x = re.sub(r'\s{2,}', ' ', x)
    return x.strip()
for s in S + A:
    s['arg'] = gfix(s.get('arg', ''))
    for u in s['units']:
        u['la'] = gfix(u['la'])
    s['units'] = [u for u in s['units'] if len(u['la']) > 3]

# 8. renumber sequentially
n = 0
for s in S + A:
    for u in s['units']:
        n += 1
        u['n'] = n

json.dump(d, io.open('C:/Users/leofa/AppData/Local/Temp/longridge/favre-fixed.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('total units now:', n)
for s in A:
    print(s['id'], len(s['units']), '|', s['titel'][:60], '|', s['arg'][:60])
