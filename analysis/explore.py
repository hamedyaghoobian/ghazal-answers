import json, collections, random, re
P = {p['id']: p for p in json.load(open('data/poets.json'))}
R = [json.loads(l) for l in open('data/sections.jsonl')]
G = [r for r in R if r['format'] == 1 and r['metre'] and r['rhyme']]
def year(pid): return P[pid]['deathYearInLHijri'] or None
G = [r for r in G if year(r['poet'])]
print('dated ghazals', len(G), 'poets', len({r['poet'] for r in G}))
def ce(ah): return round(ah * 0.970229 + 621.5693)

def joined(rows, key):
    first = {}  # pattern -> earliest year
    for r in rows:
        k = key(r); y = year(r['poet'])
        first.setdefault(k, {}); first[k].setdefault(r['poet'], y)
    out = []
    for r in rows:
        y = year(r['poet']); k = key(r)
        out.append(any(p != r['poet'] and yy < y for p, yy in first[k].items()))
    return out

j = joined(G, lambda r: (r['metre'], r['rhyme']))
# baseline: shuffle rhyme within metre
rh = collections.defaultdict(list)
for r in G: rh[r['metre']].append(r['rhyme'])
for v in rh.values(): random.shuffle(v)
it = {m: iter(v) for m, v in rh.items()}
S = [dict(r, rhyme=next(it[r['metre']])) for r in G]
b = joined(S, lambda r: (r['metre'], r['rhyme']))
cent = collections.defaultdict(lambda: [0, 0, 0])
for r, a, c in zip(G, j, b):
    k = ce(year(r['poet'])) // 100
    cent[k][0] += 1; cent[k][1] += a; cent[k][2] += c
for k in sorted(cent):
    n, a, c = cent[k]; print(f"{k}00s CE  n={n:6d}  joined={a/n:.2f}  chance={c/n:.2f}")
mark = re.compile('استقبال|تتبع|جواب|اقتفا|به طرز|نظیره|در زمین')
M = [r for r in G if mark.search(r['title'])]
print('titled answers', len(M)); print(collections.Counter(re.sub(r'^.*?-\s*','',r['title']) for r in M).most_common(25))
