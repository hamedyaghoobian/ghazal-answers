"""Crawl Ganjoor: every poet, every category, every poem's main sections
(metre, rhyme letters, format, first couplet). One request per category.
Writes data/poets.json and data/sections.jsonl; resumable (skips cats done)."""
import json, os, sys, time, requests
from concurrent.futures import ThreadPoolExecutor

B = "https://api.ganjoor.net/api/ganjoor/"
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
S = requests.Session()
S.headers["User-Agent"] = "ghazal-answers research crawler"

def get(path, **params):
    for i in range(6):
        try:
            r = S.get(B + path, params=params, timeout=60)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        time.sleep(2 ** i)
    raise RuntimeError(path)

def main():
    poets = get("poets")
    json.dump(poets, open(f"{OUT}/poets.json", "w"), ensure_ascii=False)
    done_path = f"{OUT}/cats_done.txt"
    done = set(open(done_path).read().split()) if os.path.exists(done_path) else set()
    out = open(f"{OUT}/sections.jsonl", "a")
    dlog = open(done_path, "a")

    def crawl_cat(poet, cid):
        c = get(f"cat/{cid}", poems="true", mainSections="true")["cat"]
        rows = []
        for p in c.get("poems") or []:
            for s in p.get("mainSections") or []:
                lines = (s.get("plainText") or "").replace("\r", "").split("\n")
                m = s.get("ganjoorMetre") or {}
                rows.append(dict(poet=poet["id"], cat=cid, cat_title=c["title"], poem=p["id"],
                    title=p["title"], url=c["fullUrl"] + "/" + p["urlSlug"], index=s["index"],
                    format=s.get("poemFormat"), verseType=s.get("verseType"),
                    metre=s.get("ganjoorMetreId"), rhythm=m.get("rhythm"),
                    rhyme=s.get("rhymeLetters"), couplets=s.get("coupletsCount"),
                    first=lines[:2]))
        return c, rows

    for n, poet in enumerate(poets):
        stack = [poet["rootCatId"]]
        while stack:
            batch, stack = stack[:8], stack[8:]
            with ThreadPoolExecutor(4) as ex:
                res = list(ex.map(lambda cid: crawl_cat(poet, cid), batch))
            for c, rows in res:
                stack += [ch["id"] for ch in c.get("children") or []]
                if str(c["id"]) in done:
                    continue
                for r in rows:
                    out.write(json.dumps(r, ensure_ascii=False) + "\n")
                dlog.write(f"{c['id']}\n"); done.add(str(c["id"]))
            out.flush(); dlog.flush()
        print(f"{n+1}/{len(poets)} {poet['name']}", flush=True)

main()
