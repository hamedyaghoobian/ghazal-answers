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

`data/` is not committed; run the crawl to rebuild it.
