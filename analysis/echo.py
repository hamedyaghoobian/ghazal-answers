import json, collections, random, re
random.seed(1)
P = {p['id']: p for p in json.load(open('data/poets.json'))}
R = [json.loads(l) for l in open('data/sections.jsonl')]
year = lambda pid: P[pid]['deathYearInLHijri'] or None
G = [r for r in R if r['format'] == 1 and r['metre'] and r['rhyme'] and year(r['poet']) and len(r['first']) == 2]
STOP = set("که و از به در با بر را این آن هر چه چو تا ما من تو او یک بی نه هم اگر ای دل جان".split())
def norm(s): return re.sub(r'[ً-ْٰ‌]', '', s).replace('ي','ی').replace('ك','ک').replace('آ','ا')
def words(r):
    out = set()
    for h in r['first']:
        w = norm(h).split()[:-2]          # drop the rhyme and radif end of each half-line
        out |= {x for x in w if len(x) > 2 and x not in STOP}
    return out
W = {id(r): words(r) for r in G}
grp = collections.defaultdict(list); bym = collections.defaultdict(list)
for r in G: grp[(r['metre'], r['rhyme'])].append(r); bym[r['metre']].append(r)
def best(r, pool):
    y = year(r['poet']); b = (0, None)
    for o in pool:
        if o['poet'] != r['poet'] and year(o['poet']) < y:
            s = len(W[id(r)] & W[id(o)])
            if s > b[0]: b = (s, o)
    return b
same = collections.Counter(); ctrl = collections.Counter(); ex = []
sample = random.sample(G, 8000)
for r in sample:
    g = grp[(r['metre'], r['rhyme'])]
    s, o = best(r, g); same[min(s, 4)] += 1
    pool = random.sample(bym[r['metre']], min(len(g) * 3 + 20, len(bym[r['metre']])))
    pool = [x for x in pool if x['rhyme'] != r['rhyme']][:len(g)]
    c, _ = best(r, pool); ctrl[min(c, 4)] += 1
    if s >= 3: ex.append((s, P[r['poet']]['name'], r['first'][0], P[o['poet']]['name'], o['first'][0]))
print('shared words  same-pattern  control (same metre, other rhyme, same pool size)')
for k in range(5): print(k, same[k], ctrl[k])
for e in ex[:12]: print(e)
