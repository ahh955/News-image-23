# World News — Monday, 23 November 2026

[![competition](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ahh955/News-image-23/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ahh955/News-image-23/reward.svg)](https://make.fun/c/news-image-20261123)

One image that sums up Monday 23 November 2026's world news, drawn as a
dense one-page newspaper: 31 stories, every continent, all from this one day.

**Leads:** Belgium's airports stand still in a national strike · Iran claims
78 US drones downed over the Strait of Hormuz · Modi and Nepal's Balen Shah
talk for 100 minutes in Delhi.

**Also inside:** the Dymer toll rises to 11 · Molly Meldrum dies at 83 ·
the Kremlin blames Kyiv for the Sparta II fire · Asian shares slide on AI
doubts · a world map of where it happened · a DATE CHECK box listing the
big stories that belong to other days (COP31's collapse, the Democrats'
258 House seats, the Alcaraz title, the Delta outage) so nothing from
another day is passed off as 23 November's news.

## How it is made

`compose.py` draws the whole front page with PIL — flat vector art, no
photographs, no text inside the artwork; every label is crisp vector text.
`main.ts` (Node 22, standard library only) validates the finished
`entry.png` (1024×1024, under 1 MiB, whole PNG with IEND) and writes it to
`/output/entry.png`. The program runs twice and writes the same bytes.

## Run it

```sh
python3 compose.py        # rebuild entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters, AFP, FT, BBC, IANS, Inshorts, Press TV, Al Jazeera, News Media
House. Claims are attributed, not stated as fact; pictures and the map are
original, drawn in code.
