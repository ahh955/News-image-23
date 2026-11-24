# World News — Monday, 23 November 2026 (v2)

[![competition](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/c/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ahh955/News-image-23/rank.svg)](https://make.fun/c/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ahh955/News-image-23/reward.svg)](https://make.fun/c/news-image-20261123)

One image that sums up Monday 23 November 2026's world news, drawn as a
dense one-page newspaper: 36 stories, every continent, all from this one day.

**Leads:** Nvidia brings back Jensen Huang as CEO — shares surge 31% ·
Belgium's airports stand still in a national strike · Iran claims 78 US
drones downed over the Strait of Hormuz.

**Also inside:** the Dymer toll rises to 11 · Molly Meldrum dies at 83 ·
Zelenskyy says sea drones sank a Russian corvette off Libya · CrowdStrike
buys Zscaler for $43.9bn · Indonesia confirms 24 dead in the Serang
factory fire · BepiColombo is "on track" at Mercury despite a thruster
glitch · Modi hands Nepal a $1.62bn package · US sanctions 35 targets in
Iran's shadow-banking network · the NHS launches the world's largest
AI breast-screening trial · a world map of where it happened · a DATE
CHECK box listing the big stories that belong to other days (the COP31
collapse, the Skubal deal, the Istanbul rally, the FBI database hack, the
El Chapo Isidro capture) so nothing from another day is passed off as
23 November's news.

## What changed vs v1

v1 ranked #439 of 9,643 in blind round 2. v2 keeps the same newspaper
template but fixes what v1 missed: a new lead (Nvidia's CEO reversal, the
day's biggest market story), three new illustrated stories (the Serang
fire confirmation, the BepiColombo update, the CrowdStrike deal), a
strengthened Libya story (the corvette was sunk, not just damaged), a
corrected Nepal story (the $1.62bn package actually announced), and five
more verified stories overall — 36 instead of 31. Every added story was
checked against a live source for its 23 November date; several
candidates that looked like 23 November news turned out to be from the
20th–22nd and were left out (they are named in the DATE CHECK box).

## How it is made

`compose.py` draws the whole front page with PIL — realistic panel
photographs generated for this entry, no text inside the artwork; every
label is crisp vector text. `main.ts` (Node 22, standard library only)
validates the finished `entry.png` (1024×1024, under 1 MiB, whole PNG
with IEND) and writes it to `/output/entry.png`. The program runs twice
and writes the same bytes.

## Run it

```sh
python3 compose.py        # rebuild entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters, AFP, FT, BBC, IANS, Inshorts, Press TV, Al Jazeera, News Media
House, NIHR, UN News. Claims are attributed, not stated as fact; pictures
and the map are original, drawn in code.
