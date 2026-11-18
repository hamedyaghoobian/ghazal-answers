"""Write the web data: data/web/field.json (every ghazal as a firefly, the links, the counts)
and data/web/text/<poet>.json (each poet's opening couplets, fetched when one is read)."""
import json, os, collections, re
D = json.load(open('data/answers.json'))
G, L, POETS = D['ghazals'], D['links'], D['poets']
out = 'data/web'; os.makedirs(f'{out}/text', exist_ok=True)
pids = sorted(POETS, key=lambda p: (POETS[p]['died'], POETS[p]['name']))
pidx = {p: i for i, p in enumerate(pids)}
metres = sorted({g['rhythm'] for g in G}, key=lambda m: -sum(1 for g in G if g['rhythm'] == m))
midx = {m: i for i, m in enumerate(metres)}
order = sorted(range(len(G)), key=lambda i: (pidx[str(G[i]['poet'])], i))
new = {old: n for n, old in enumerate(order)}
local = collections.Counter()
gp, gm, gl = [], [], []
texts = collections.defaultdict(list)
for old in order:
    g = G[old]; p = pidx[str(g['poet'])]
    gp.append(p); gm.append(midx[g['rhythm']]); gl.append(local[p]); local[p] += 1
    texts[p].append([g['first'][0].strip(), g['first'][1].strip(), g['title'], g['url'], g['rhyme']])
for p, t in texts.items():
    json.dump(t, open(f'{out}/text/{p}.json', 'w'), ensure_ascii=False, separators=(',', ':'))
TIER = {'answer': 0, 'contemporary': 1, 'same': 2}
links = []
for a in L:
    links += [new[a['a']], new[a['to']], TIER[a['tier']], a['shared'], int(a['titled'])]
ce = lambda ah: round(ah * 0.970229 + 621.5693)
poets = [[POETS[p]['name'], ce(POETS[p]['born']) if POETS[p]['born'] else None, ce(POETS[p]['died']), POETS[p]['born'], POETS[p]['died']] for p in pids]
json.dump(dict(poets=poets, metres=metres, poet=gp, metre=gm, local=gl, links=links, centuries=D['centuries']),
          open(f'{out}/field.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(gp), 'ghazals', len(links) // 5, 'links', len(poets), 'poets')
os.system(f'du -sh {out}/field.json {out}/text; gzip -c {out}/field.json | wc -c')
