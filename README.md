# ghazal-answers

The data and analysis behind *What the Poets Answered* (Readings, Otherwise No. 7).

- `crawl/crawl.py` pulls every poem on Ganjoor (api.ganjoor.net), one request per category, keeping
  each poem's metre, rhyme letters, format and opening couplet → `data/sections.jsonl`.
- `analysis/explore.py` shows that sharing a metre and rhyme happens about as often as chance
  (rhymes shuffled within each metre).
- `analysis/echo.py` shows that opening couplets sharing words outside the rhyme does not.
- `analysis/answers.py` finds the answers: same metre and rhyme, 2+ shared opening words (or a title
  that says استقبال، تتبع، …), the answered poet dead 30+ lunar years earlier; closer pairs are
  'contemporary', identical openings 'same'. The same pipeline on shuffled rhymes gives chance.
- `analysis/export.py` writes the web data the piece reads.

`data/answers.json` (every ghazal kept, every answer, and the chance counts per century), `data/poets.json`,
`data/chance_mean.json` and `data/web/` (what the piece reads) are committed. The raw crawl,
`data/sections.jsonl` (65 MB), is not; run `crawl/crawl.py` to rebuild it. Poets who died less than fifty
years ago are left out of everything committed here.

## Licence and how to cite

- **Code**: MIT (`LICENSE`).
- **The piece** (its words, drawings, data and design, as published at https://hamedyaghoobian.com/readings-otherwise/what-the-poets-answered/): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it, change it, teach with it; say where it came from.
- **What comes from elsewhere keeps its own terms:**
  - The ghazals are in the public domain; their typed texts, metres and rhymes are [Ganjoor](https://ganjoor.net)'s, and the opening couplets in `data/` are quoted from it.

To cite it:

> Yaghoobian, Hamed. 2026. "What the Poets Answered." *Readings, Otherwise*, no. 7. Interactive work, 18 November 2026. https://hamedyaghoobian.com/readings-otherwise/what-the-poets-answered/

`CITATION.cff` has the same, and GitHub's "Cite this repository" reads it. It was made with Claude, a language model, as its colophon says.
