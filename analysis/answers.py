"""Answered ghazals in Ganjoor.

A ghazal answers an earlier one when both share metre and rhyme, the earlier poet died at least
GAP lunar years before the later one, and the opening couplets share 2+ words outside the rhyme
(or the later poem's title says so: استقبال، تتبع، ...). Pairs closer in time are kept as
'contemporaries' (direction unknown); openings that are the same (a half-line repeated word for
word, or 80%+ of words) are kept as 'same' (quotation or a poem carried in two divans).
Chance: the same pipeline run on rhymes shuffled within each metre.
Poets dead under 50 years (Iran's copyright term) are left out."""
import json, collections, re, random
GAP = 30
P = {p['id']: p for p in json.load(open('data/poets.json'))}
R = [json.loads(l) for l in open('data/sections.jsonl')]
year = lambda pid: P[pid]['deathYearInLHijri'] or None
G = [r for r in R if r['format'] == 1 and r['metre'] and r['rhyme'] and year(r['poet'])
     and year(r['poet']) <= 1395 and len(r['first']) == 2]
STOP = set("که و از به در با بر را این آن هر چه چو تا ما من تو او یک بی نه هم اگر ای دل جان".split())
def norm(s): return ' '.join(re.sub(r'[ً-ْٰ‌]', '', s).replace('ي','ی').replace('ك','ک').replace('آ','ا').split())
def words(first):
    out = set()
    for h in first: out |= {x for x in norm(h).split()[:-2] if len(x) > 2 and x not in STOP}
    return out
MARK = re.compile('استقبال|تتبع|اقتفا|نظیره')
for i, r in enumerate(G):
    r['i'] = i; r['y'] = year(r['poet']); r['w'] = words(r['first']); r['h'] = {norm(h) for h in r['first']}

def link(rows):
    grp = collections.defaultdict(list)
    for r in rows: grp[(r['metre'], r['rhyme'])].append(r)
    out = []
    for r in rows:
        best = None
        for o in grp[(r['metre'], r['rhyme'])]:
            if o['poet'] == r['poet'] or o['y'] > r['y']: continue
            s = len(r['w'] & o['w'])
            key = (s, -o['y'])
            if best is None or key > best[0]: best = (key, o)
        if not best: continue
        s, o = best[0][0], best[1]
        titled = bool(MARK.search(r['title']))
        if s < 2 and not titled: continue
        same = bool(r['h'] & o['h']) or (s >= 0.8 * max(1, min(len(r['w']), len(o['w']))) and s >= 3)
        tier = 'same' if same else ('answer' if r['y'] - o['y'] >= GAP else 'contemporary')
        out.append(dict(a=r['i'], to=o['i'], shared=s, titled=titled, tier=tier))
    return out

A = link(G)
random.seed(7)
rh = collections.defaultdict(list)
for r in G: rh[r['metre']].append(r['rhyme'])
for v in rh.values(): random.shuffle(v)
it = {m: iter(v) for m, v in rh.items()}
S = [dict(r, rhyme=next(it[r['metre']])) for r in G]
B = link(S)

ce = lambda ah: round(ah * 0.970229 + 621.5693)
print('tiers', collections.Counter(a['tier'] for a in A), 'chance', collections.Counter(a['tier'] for a in B))
n = collections.Counter(ce(r['y']) // 100 for r in G)
obs = collections.Counter(ce(G[a['a']]['y']) // 100 for a in A if a['tier'] == 'answer')
chn = collections.Counter(ce(G[a['a']]['y']) // 100 for a in B if a['tier'] == 'answer')
cent = []
for k in sorted(n):
    if n[k] < 50: continue
    cent.append(dict(c=k * 100, n=n[k], answers=obs[k], chance=chn[k]))
    print(f"{k}00s  n={n[k]:6d}  answers={obs[k]:4d} {obs[k]/n[k]:.3f}  chance={chn[k]:3d} {chn[k]/n[k]:.3f}")
ans = [a for a in A if a['tier'] == 'answer']
out_n = collections.Counter(r['poet'] for r in G)
got = collections.Counter(G[a['to']]['poet'] for a in ans)
gave = collections.Counter(G[a['a']]['poet'] for a in ans)
print('most answered, raw and per ghazal (poets with 100+ ghazals):')
for pid, c in got.most_common(15): print(f"  {P[pid]['name']}: {c} of {out_n[pid]} ({c/out_n[pid]:.2f})")
print('per ghazal:', [(P[p]['name'], round(got[p]/out_n[p], 2)) for p in sorted(got, key=lambda p: -got[p]/out_n[p]) if out_n[p] >= 100][:12])
print('most answering:', [(P[p]['name'], c) for p, c in gave.most_common(10)])
indeg = collections.Counter(a['to'] for a in ans)
for i, c in indeg.most_common(8): print(c, P[G[i]['poet']]['name'], G[i]['first'][0])
json.dump(dict(
    poets={pid: dict(name=P[pid]['name'], born=P[pid]['birthYearInLHijri'], died=P[pid]['deathYearInLHijri'], n=out_n[pid]) for pid in out_n},
    ghazals=[dict(poet=r['poet'], url=r['url'], metre=r['metre'], rhythm=r['rhythm'], rhyme=r['rhyme'], first=r['first'], title=r['title']) for r in G],
    links=A, centuries=cent), open('data/answers.json', 'w'), ensure_ascii=False)
