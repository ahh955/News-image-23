#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page, version 2.

Dense one-page newspaper, 1024x1024 PNG. Panel art is realistic
photographic-style imagery (generated for this entry, stored in panels/);
the world map and every label are drawn with PIL vector text.
Deterministic: the same input files always produce the same bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

PAGE_W, PAGE_H = 1024, 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (178, 24, 24)
NAVY = (27, 42, 74)
TEAL = (15, 118, 110)
GREY = (102, 102, 102)
SEA = (205, 225, 240)
LAND = (232, 214, 170)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def _font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def serif_bold(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _font("DejaVuSerif.ttf", size)


def sans_bold(size):
    return _font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap by measured pixel width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_para(draw, x, y, text, font, max_width, leading, fill=INK,
              limit=None):
    """Draw wrapped text; return the y below the last line."""
    lines = wrap_text(draw, text, font, max_width)
    if limit is not None:
        lines = lines[:limit]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def tag_chip(draw, x, y, text, fill):
    """Small filled tag chip."""
    font = sans_bold(11)
    width = int(draw.textlength(text, font=font)) + 12
    draw.rectangle([x, y, x + width, y + 16], fill=fill)
    draw.text((x + 6, y + 2), text, font=font, fill=(255, 255, 255))


def story_dot(draw, x, y, number, fill=RED):
    """Red circle with a white story number."""
    draw.ellipse([x, y, x + 19, y + 19], fill=fill)
    font = sans_bold(12)
    label = str(number)
    tw = draw.textlength(label, font=font)
    draw.text((x + (19 - tw) / 2, y + 2), label, font=font,
              fill=(255, 255, 255))


def place_photo(page, path, x, y, width, height):
    """Center-crop a panel photo into its tile (no distortion, no gaps)."""
    here = os.path.dirname(os.path.abspath(__file__))
    photo = Image.open(os.path.join(here, path)).convert("RGB")
    tile = ImageOps.fit(photo, (width, height), Image.LANCZOS,
                        centering=(0.5, 0.5))
    page.paste(tile, (x, y))


# ------------------------------------------------------------------ world map
# Rough continent outlines in a 0..100 (x) by 0..50 (y) space.

CONTINENTS = [
    [(4, 9), (13, 4), (30, 4), (35, 10), (28, 14), (31, 20), (22, 23),
     (19, 29), (12, 26), (6, 18)],                       # North America
    [(31, 2), (38, 2), (36, 8), (30, 8)],                # Greenland
    [(24, 30), (32, 28), (37, 34), (32, 44), (28, 48), (24, 40)],
    [(46, 24), (56, 20), (62, 26), (60, 34), (54, 42), (48, 36)],  # Africa
    [(44, 8), (60, 4), (86, 2), (96, 8), (92, 16), (84, 14), (78, 22),
     (70, 26), (62, 22), (56, 24), (48, 18)],            # Eurasia
    [(64, 24), (70, 24), (67, 33)],                      # India
    [(74, 26), (80, 28), (78, 34), (74, 32)],            # SE Asia
    [(82, 36), (92, 34), (94, 42), (86, 46), (80, 42)],  # Australia
    [(92, 14), (95, 18), (93, 23)],                      # Japan
]

# Story number -> (map x, map y). No pin for 12: Mercury is in space.
PINS = {1: (11, 17), 2: (48, 11), 3: (68, 21), 4: (56, 8), 5: (87, 45),
        6: (52, 4), 7: (52, 23), 8: (85, 15), 9: (44, 7), 10: (63, 26),
        11: (79, 33), 13: (18, 21)}


def world_map(draw, x, y, width, height):
    draw.rectangle([x, y, x + width, y + height], fill=SEA)
    draw.rectangle([x, y, x + width, y + height], outline=INK, width=1)
    for i in range(1, 5):
        gx = x + i * width // 5
        draw.line([gx, y, gx, y + height], fill=(185, 210, 230), width=1)
    for j in range(1, 3):
        gy = y + j * height // 3
        draw.line([x, gy, x + width, gy], fill=(185, 210, 230), width=1)
    for poly in CONTINENTS:
        pts = [(x + px * width / 100.0, y + py * height / 50.0)
               for px, py in poly]
        draw.polygon(pts, fill=LAND, outline=(180, 160, 120))
    for number, (px, py) in PINS.items():
        cx, cy = x + px * width / 100.0, y + py * height / 50.0
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED,
                     outline=(255, 255, 255), width=1)
        font = sans_bold(7)
        label = str(number)
        tw = draw.textlength(label, font=font)
        draw.text((cx - tw / 2, cy - 4), label, font=font,
                  fill=(255, 255, 255))


# ------------------------------------------------------------------ stories
# Every story happened, or was first reported, on Monday 23 Nov 2026.

LEADS = [
    dict(photo="panels/nvidia.png", tag="SANTA CLARA · TECH", fill=NAVY,
         n=1, head="Nvidia brings back Jensen Huang",
         body="Reinstated as CEO after Trump called into the board "
              "meeting; shares surge 31% in premarket trading. — Reuters"),
    dict(photo="panels/airport.png", tag="BRUSSELS · STRIKE", fill=NAVY,
         n=2, head="Belgium's airports stand still",
         body="Air traffic control walks out 7am–9pm in a national "
              "strike; 429 flights and 59,500 passengers hit at Brussels, "
              "Charleroi shut. — AFP"),
    dict(photo="panels/drone.png", tag="HORMUZ · WAR", fill=RED,
         n=3, head="Iran claims 78 US drones downed",
         body="An IRGC infographic counts 58 MQ-9 Reapers and 20 MQ-1 "
              "Predators, plus a fourth drone in 24 hours. Unconfirmed by "
              "the US. — Press TV"),
]

SMALL = [
    dict(photo="panels/rubble.png", tag="DYMER · WAR", n=4,
         head="Toll in Dymer rises to 11",
         body="Another body pulled from the rubble; a boy of 7 and a woman "
              "found alive. — Reuters"),
    dict(photo="panels/microphone.png", tag="MELBOURNE · OBITUARY", n=5,
         head="Molly Meldrum dies at 83",
         body="Countdown host who championed AC/DC and Kylie; a state "
              "funeral is planned. — Reuters"),
    dict(photo="panels/shipfire.png", tag="MOSCOW · WAR", n=6,
         head="Kremlin: ship fire was 'terrorism'",
         body="Moscow blames Kyiv for the drone strike that set the "
              "Sparta II ablaze. — Reuters"),
    dict(photo="panels/corvette.png", tag="LIBYA · WAR", n=7,
         head="Zelenskyy: we sank a Russian corvette",
         body="Seven sea drones sank the Merkury, hit the Angara and "
              "destroyed a Ka-27 helicopter. — Reuters"),
    dict(photo="panels/markets.png", tag="ASIA · MARKETS", n=8,
         head="Asian shares slide on AI doubts",
         body="Korean chipmakers shed about 3% as regulators move to "
              "steady sagging markets. — FT"),
    dict(photo="panels/parliament.png", tag="LONDON · POLITICS", n=9,
         head="Burnham sells EU deal to MPs",
         body="A 'broken status quo or change'; May is 'aghast' at talk "
              "of rejoining. — BBC"),
    dict(photo="panels/summit.png", tag="DELHI · DIPLOMACY", n=10,
         head="Modi hands Nepal $1.62bn package",
         body="After 100 minutes of talks, India pledges $1.62bn for "
              "Nepal's flood rebuilding. — Reuters"),
    dict(photo="panels/factoryfire.png", tag="SERANG · DISASTER", n=11,
         head="24 confirmed dead in factory fire",
         body="Monday confirms 24 dead from Saturday's candy-factory "
              "blaze; about 30 still missing. — Reuters"),
    dict(photo="panels/mercury.png", tag="SPACE · SCIENCE", n=12,
         head="BepiColombo 'on track' despite glitch",
         body="ESA says the Mercury probe is safe in stable orbit after "
              "Saturday's burn cut short. — Reuters"),
    dict(photo="panels/crowdstrike.png", tag="AUSTIN · BUSINESS", n=13,
         head="CrowdStrike buys Zscaler for $43.9bn",
         body="The biggest cybersecurity deal ever, all stock, as cyber "
              "threats mount. — Reuters"),
]

ALSO = [
    (14, "Washington — US sanctions 35 in Iran shadow banking. Reuters"),
    (15, "London — NHS starts biggest AI breast-screening trial. NIHR"),
    (16, "Pennsylvania — Measles deaths rise to 9; 1,638 cases. Reuters"),
    (17, "Washington — Nvidia partner Megaspeed blacklisted. Reuters"),
    (18, "Washington — Meta pauses Class C shares amid lawsuit. Reuters"),
    (19, "Washington — US seeks extradition of 'El Chapo Isidro'. Reuters"),
    (20, "Barbados — Guterres urges global AI rules at summit. UN News"),
    (21, "Melbourne — Prespakis wins AFLW best and fairest. ABC"),
    (22, "Kyiv — Drone debris falls on schools. N.M. House"),
    (23, "Pacific — How the deepest place was made. Digest"),
    (24, "New Delhi — India holds No. 3 in Asia power rank. Inshorts"),
    (25, "Canberra — Albanese defends Bowen on COP31. N.M. House"),
    (26, "Washington — Trump: Iran attacks hit a year high. Digest"),
    (27, "Damascus — Syria and EU seek normalisation. N.M. House"),
    (28, "Gaza — Report calls it a 'toxic wasteland'. N.M. House"),
    (29, "Hormuz — Maritime attacks hit record high. N.M. House"),
    (30, "New York — Thanksgiving storm forecast. GEORGE"),
    (31, "Zawtar — Israeli demolitions shown Monday. Al Jazeera"),
    (32, "Brussels — 60% of controllers joined walkout. QNC"),
    (33, "California — Extreme tides, rain after mudslides. GEORGE"),
    (34, "Memphis — FedEx pilot Sanders dies at 82. GEORGE"),
    (35, "Space — Star seen spiralling into a giant. Digest"),
    (36, "London — PIP overhaul urged; NHS cuts feared. D. Brief"),
]

STATS = [
    ("+31%", "Nvidia shares surge"),
    ("429", "flights cancelled at Brussels"),
    ("59,500", "passengers hit at Brussels"),
    ("78", "US drones Iran claims downed"),
    ("$43.9bn", "CrowdStrike buys Zscaler"),
    ("24", "confirmed dead in factory fire"),
]

DATECHECK = ("Every story here happened, or was first reported, on Monday "
             "23 November 2026. LEFT OUT — 22 NOV: COP31 collapse · "
             "Democrats' 258 seats · Alcaraz title · Delta outage · Alice "
             "Huang report · Skubal deal · Istanbul rally · Khartoum "
             "strikes. 21 NOV: 58th MQ-9 claim · Riemann verified · Serang "
             "fire starts · BepiColombo arrival. 20 NOV: Penny law · "
             "Denmark–Russia row · Indonesia seizure · Riemann announced · "
             "FBI hack · El Chapo Isidro held · Tom Jackson dies. 24 NOV: "
             "Korean airspace alert · Hormuz tankers · Nikkei +2.6%. "
             "25 NOV: Iowa blast.")


def fit_sans(draw, text, sizes, max_width):
    """Largest sans font from sizes that fits text in max_width."""
    for size in sizes:
        font = sans(size)
        if draw.textlength(text, font=font) <= max_width:
            return font
    return sans(sizes[-1])


def draw_stat_strip(canvas, figures):
    """Six headline numbers across the page: red figures over labels."""
    slot = (PAGE_W - 16) / 6.0
    for slot_index, (figure, caption) in enumerate(figures):
        left = 8 + int(slot_index * slot)
        if slot_index:
            divider = left - 4
            canvas.line([divider, 114, divider, 140],
                        fill=(190, 180, 160), width=1)
        canvas.text((left + 4, 112), figure, font=serif_bold(24),
                    fill=RED)
        canvas.text((left + 4, 140), caption, font=sans(10), fill=INK)
    canvas.line([8, 156, PAGE_W - 8, 156], fill=INK, width=1)


def draw_date_check(canvas, top):
    """Red DATE CHECK box: what counts as 23 Nov, what was left out."""
    box_bottom = top + 58
    canvas.rectangle([8, top, PAGE_W - 8, box_bottom], outline=RED,
                     width=2)
    heading_font = sans_bold(12)
    canvas.text((14, top + 5), "DATE CHECK", font=heading_font, fill=RED)
    body_left = 110
    body_width = PAGE_W - 8 - body_left - 8
    draw_para(canvas, body_left, top + 5, DATECHECK, sans(10),
              body_width, 13, limit=4)


# ------------------------------------------------------------------ compose

def build():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(page)

    # top strip
    d.text((8, 3), "THE WORLD IN ONE DAY", font=sans_bold(12), fill=RED)
    right = "36 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
    d.text((PAGE_W - 8 - d.textlength(right, font=sans_bold(11)), 4),
           right, font=sans_bold(11), fill=INK)
    d.line([8, 19, PAGE_W - 8, 19], fill=INK, width=2)

    # masthead
    title = "Monday 23 November 2026"
    title_font = serif_bold(58)
    d.text(((PAGE_W - d.textlength(title, font=title_font)) / 2, 24),
           title, font=title_font, fill=INK)
    sub = ("Nvidia brings back Jensen Huang · Belgium's airports stand "
           "still · Iran claims 78 US drones downed")
    sub_font = serif(16)
    d.text(((PAGE_W - d.textlength(sub, font=sub_font)) / 2, 88), sub,
           font=sub_font, fill=RED)
    d.line([8, 108, PAGE_W - 8, 108], fill=INK, width=1)

    # stat strip
    draw_stat_strip(d, STATS)

    # three leads
    lead_w, lead_gap, lead_y, lead_h = 328, 8, 160, 276
    for i, story in enumerate(LEADS):
        x0 = 8 + i * (lead_w + lead_gap)
        d.rectangle([x0, lead_y, x0 + lead_w, lead_y + lead_h],
                    outline=INK, width=1)
        place_photo(page, story["photo"], x0 + 1, lead_y + 1, lead_w - 2,
                    140)
        tag_chip(d, x0 + 8, lead_y + 8, story["tag"], story["fill"])
        story_dot(d, x0 + 8, lead_y + 148, story["n"])
        d.text((x0 + 32, lead_y + 150), story["tag"], font=sans_bold(11),
               fill=RED)
        draw_para(d, x0 + 8, lead_y + 170, story["head"], serif_bold(22),
                  lead_w - 16, 26, limit=2)
        draw_para(d, x0 + 8, lead_y + 224, story["body"], sans(11),
                  lead_w - 16, 14, limit=3)

    # ten small panels, two rows of five
    widths = [196, 195, 195, 195, 195]
    small_y, small_h = 442, 158
    for row in range(2):
        y0 = small_y + row * (small_h + 6)
        x0 = 8
        for j in range(5):
            story = SMALL[row * 5 + j]
            w = widths[j]
            d.rectangle([x0, y0, x0 + w, y0 + small_h], outline=INK,
                        width=1)
            place_photo(page, story["photo"], x0 + 1, y0 + 1, w - 2, 58)
            story_dot(d, x0 + 6, y0 + 62, story["n"])
            d.text((x0 + 28, y0 + 64), story["tag"], font=sans_bold(9),
                   fill=RED)
            draw_para(d, x0 + 6, y0 + 82, story["head"], serif_bold(15),
                      w - 12, 18, limit=2)
            draw_para(d, x0 + 6, y0 + 120, story["body"], sans(10),
                      w - 12, 12, limit=3)
            x0 += w + 8

    # bottom: map + ALSO list
    bottom_y = 772
    d.text((8, bottom_y), "WHERE IT HAPPENED", font=sans_bold(12),
           fill=RED)
    d.text((180, bottom_y + 1), "numbers match the stories",
           font=sans(10), fill=GREY)
    d.text((344, bottom_y), "ALSO ON MONDAY 23 NOVEMBER 2026",
           font=sans_bold(12), fill=RED)
    d.text((344 + 300, bottom_y + 1), "place · what happened · source",
           font=sans(10), fill=GREY)
    world_map(d, 8, bottom_y + 20, 328, 118)
    d.text((8, bottom_y + 140), "Pins: stories 1–13 (8 is markets, "
           "12 is in space).", font=sans(9), fill=GREY)

    col_w = 328
    for k, (number, text) in enumerate(ALSO):
        cx = 344 + (k // 12) * (col_w + 8)
        cy = bottom_y + 20 + (k % 12) * 12
        d.text((cx, cy), str(number), font=sans_bold(10), fill=RED)
        font = fit_sans(d, text, [10, 9, 8], col_w - 24)
        d.text((cx + 22, cy), text, font=font, fill=INK)

    # DATE CHECK box
    draw_date_check(d, 940)

    # footer
    foot = ("Claims are attributed, not stated as fact · Pictures: "
            "original generated images; map: drawn in code · Sources: "
            "Reuters, AFP, FT, BBC, IANS, Inshorts, Press TV, Al Jazeera, "
            "N.M. House, NIHR, UN News · 2026-11-23")
    foot_font = sans(9)
    d.text(((PAGE_W - d.textlength(foot, font=foot_font)) / 2, 1006),
           foot, font=foot_font, fill=GREY)
    return page


if __name__ == "__main__":
    out = os.environ.get("NEWS_OUT", "entry.png")
    build().save(out, "PNG")
    print("wrote", out)
