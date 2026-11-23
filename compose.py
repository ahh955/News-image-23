#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page (1024x1024 PNG).

Dense one-page newspaper. Panel art is realistic photographic-style
imagery (generated for this entry, stored in panels/); the world map and
all labels are drawn with PIL vector text. Deterministic: same bytes on
every run. (The art_* functions below are the original procedural art,
kept for reference but no longer used.)
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
RED = (178, 24, 24)
NAVY = (27, 42, 74)
TEAL = (15, 118, 110)
GREY = (102, 102, 102)
LIGHT = (226, 220, 203)

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)


def wrap(d, text, font, max_w):
    """Greedy word wrap by measured pixel width."""
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, max_w, lh, fill=INK, max_lines=None):
    """Draw wrapped text; return y below the last line."""
    lines = wrap(d, text, font, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(d, x, y, text, fill, fg=(255, 255, 255)):
    """Small filled tag chip; returns width used."""
    f = SANS_B(11)
    w = int(d.textlength(text, font=f)) + 12
    d.rectangle([x, y, x + w, y + 16], fill=fill)
    d.text((x + 6, y + 2), text, font=f, fill=fg)
    return w


def num_badge(d, x, y, n, fill=RED):
    """Red circle with a white story number."""
    d.ellipse([x, y, x + 19, y + 19], fill=fill)
    f = SANS_B(12)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x + (19 - tw) / 2, y + 2), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- art panels
# Each draws a flat illustration inside (x, y, w, h). No text inside the art.

def art_airport(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 222, 240))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 120, 120))
    d.rectangle([x, y + h - 30, x + w, y + h - 26], fill=(255, 255, 255))
    # terminal
    d.rectangle([x + 14, y + 52, x + w - 14, y + h - 34], fill=(240, 238, 228))
    d.rectangle([x + 14, y + 52, x + w - 14, y + 62], fill=NAVY)
    for i in range(6):
        d.rectangle([x + 26 + i * 44, y + 72, x + 56 + i * 44, y + 96],
                    fill=(140, 190, 220))
    # control tower
    d.rectangle([x + w - 52, y + 18, x + w - 40, y + 52], fill=(200, 200, 200))
    d.rectangle([x + w - 58, y + 8, x + w - 34, y + 20], fill=NAVY)
    # grounded plane, nose down on the tarmac
    px, py = x + 60, y + h - 52
    d.polygon([(px, py), (px + 150, py), (px + 168, py + 8), (px + 150, py + 12),
               (px, py + 12)], fill=(255, 255, 255))
    d.polygon([(px + 150, py), (px + 168, py + 8), (px + 150, py + 12)],
              fill=RED)
    d.polygon([(px + 60, py + 2), (px + 84, py - 16), (px + 92, py - 16),
               (px + 78, py + 2)], fill=(200, 200, 200))
    d.polygon([(px + 132, py + 2), (px + 150, py - 12), (px + 156, py - 12),
               (px + 146, py + 2)], fill=(200, 200, 200))
    # big red X over the sky
    d.line([x + w - 96, y + 14, x + w - 66, y + 44], fill=RED, width=6)
    d.line([x + w - 66, y + 14, x + w - 96, y + 44], fill=RED, width=6)


def art_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 48, 80))
    d.ellipse([x + w - 70, y + 12, x + w - 30, y + 52], fill=(240, 220, 160))
    # sea
    d.rectangle([x, y + h - 42, x + w, y + h], fill=(30, 90, 130))
    for i in range(5):
        d.arc([x + 10 + i * 58, y + h - 30, x + 52 + i * 58, y + h - 8],
              200, 340, fill=(160, 210, 240), width=2)
    # tanker
    d.rectangle([x + 18, y + h - 58, x + 150, y + h - 40], fill=(90, 40, 40))
    d.rectangle([x + 30, y + h - 72, x + 52, y + h - 58], fill=(200, 200, 200))
    # Reaper-style drone, big in the sky
    cx, cy = x + w // 2 + 20, y + 52
    d.polygon([(cx - 70, cy - 4), (cx + 70, cy - 4), (cx + 78, cy + 2),
               (cx + 70, cy + 8), (cx - 70, cy + 8), (cx - 78, cy + 2)],
              fill=(210, 210, 210))
    d.polygon([(cx - 10, cy - 26), (cx + 10, cy - 26), (cx + 14, cy + 26),
               (cx - 14, cy + 26)], fill=(180, 180, 180))
    d.polygon([(cx - 6, cy - 26), (cx + 6, cy - 26), (cx, cy - 38)],
              fill=(210, 210, 210))
    # explosion star where a second drone is hit
    ex, ey = x + 52, y + 34
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 22, 9
        a = math.radians(ang)
        d.line([ex, ey, ex + int(r1 * math.cos(a)),
                ey + int(r1 * math.sin(a))], fill=(255, 180, 40), width=4)
    d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=(255, 220, 90))
    # count badge
    d.rectangle([x + w - 66, y + h - 36, x + w - 8, y + h - 8], fill=RED)
    d.text((x + w - 58, y + h - 33), "78", font=SANS_B(20),
           fill=(255, 255, 255))


def art_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 190))
    # flags: India and Nepal
    d.rectangle([x + 20, y + 16, x + 100, y + 30], fill=(255, 153, 51))
    d.rectangle([x + 20, y + 30, x + 100, y + 44], fill=(255, 255, 255))
    d.rectangle([x + 20, y + 44, x + 100, y + 58], fill=(19, 136, 8))
    d.ellipse([x + 52, y + 31, x + 68, y + 43], outline=(0, 0, 128), width=2)
    d.polygon([(x + w - 100, y + 16), (x + w - 20, y + 16),
               (x + w - 20, y + 58), (x + w - 100, y + 58)], fill=(220, 20, 60))
    d.polygon([(x + w - 100, y + 16), (x + w - 44, y + 30),
               (x + w - 100, y + 44)], fill=(220, 20, 60))
    d.ellipse([x + w - 88, y + 24, x + w - 76, y + 36], fill=(255, 255, 255))
    # two leaders shaking hands over a table
    d.rectangle([x + 30, y + 96, x + w - 30, y + 104], fill=(120, 80, 40))
    for sx, col in ((x + 70, (60, 90, 140)), (x + w - 110, (140, 60, 60))):
        d.ellipse([sx, y + 56, sx + 34, y + 90], fill=(230, 190, 150))
        d.rectangle([sx - 8, y + 88, sx + 42, y + 130], fill=col)
    # arms reaching to the handshake
    cxm = x + w // 2
    d.line([x + 104, y + 102, cxm - 8, y + 86], fill=(230, 190, 150),
           width=6)
    d.line([x + w - 104, y + 102, cxm + 8, y + 86], fill=(230, 190, 150),
           width=6)
    d.ellipse([cxm - 12, y + 74, cxm + 12, y + 98],
              fill=(230, 190, 150))
    # train along the bottom
    d.rectangle([x + 10, y + h - 34, x + w - 10, y + h - 10], fill=(30, 100, 160))
    for i in range(7):
        d.rectangle([x + 22 + i * 42, y + h - 30, x + 52 + i * 42, y + h - 16],
                    fill=(200, 230, 250))
    d.rectangle([x + 10, y + h - 10, x + w - 10, y + h - 6], fill=(80, 80, 80))


def art_rubble(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 200, 195))
    # damaged block
    d.rectangle([x + 20, y + 8, x + 110, y + h - 6], fill=(170, 160, 145))
    d.polygon([(x + 110, y + 8), (x + 150, y + 8), (x + 150, y + 30),
               (x + 128, y + 22), (x + 110, y + 34)], fill=(170, 160, 145))
    for r in range(3):
        for c in range(3):
            d.rectangle([x + 28 + c * 26, y + 16 + r * 20,
                         x + 44 + c * 26, y + 30 + r * 20], fill=(60, 60, 60))
    # smoke
    for cx, cy, r in ((x + 130, y + 14, 12), (x + 148, y + 6, 9),
                      (x + 118, y + 4, 7)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 150, 150))
    # excavator arm
    d.line([x + w - 60, y + h - 10, x + w - 20, y + h - 44], fill=(230, 150, 30),
           width=7)
    d.rectangle([x + w - 72, y + h - 22, x + w - 44, y + h - 6],
                fill=(230, 150, 30))
    d.ellipse([x + w - 26, y + h - 50, x + w - 12, y + h - 36],
              fill=(230, 150, 30))
    # rubble pile
    d.polygon([(x + 110, y + h - 6), (x + 150, y + h - 30),
               (x + 190, y + h - 6)], fill=(140, 130, 115))


def art_microphone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 30, 60))
    # stage lights
    for lx in (x + 30, x + w - 30):
        d.polygon([(lx - 14, y + 4), (lx + 14, y + 4), (lx + 30, y + h - 6),
                   (lx - 30, y + h - 6)], fill=(120, 110, 60))
    # cowboy hat
    cx = x + w // 2
    d.ellipse([cx - 52, y + 8, cx + 52, y + 26], fill=(210, 180, 120))
    d.pieslice([cx - 28, y - 12, cx + 28, y + 20], 180, 360,
               fill=(210, 180, 120))
    d.rectangle([cx - 28, y + 12, cx + 28, y + 18], fill=(120, 80, 40))
    # microphone
    d.ellipse([cx - 13, y + 30, cx + 13, y + 52], fill=(200, 200, 200))
    d.rectangle([cx - 4, y + 50, cx + 4, y + h - 4], fill=(150, 150, 150))
    # music notes
    for nx, ny in ((x + 16, y + 40), (x + w - 30, y + 36)):
        d.ellipse([nx, ny, nx + 9, ny + 7], fill=(255, 220, 90))
        d.line([nx + 8, ny, nx + 8, ny - 14], fill=(255, 220, 90), width=2)


def art_shipfire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(160, 200, 225))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(40, 100, 150))
    # cargo ship
    d.rectangle([x + 16, y + h - 44, x + w - 30, y + h - 26], fill=(150, 50, 50))
    d.rectangle([x + 30, y + h - 60, x + 60, y + h - 44], fill=(220, 220, 220))
    d.rectangle([x + 70, y + h - 58, x + 110, y + h - 44], fill=(60, 120, 180))
    d.rectangle([x + 120, y + h - 58, x + 150, y + h - 44], fill=(220, 160, 60))
    # flames mid-ship
    fx, fy = x + w // 2, y + h - 58
    d.polygon([(fx - 16, fy), (fx - 6, fy - 26), (fx + 2, fy - 10),
               (fx + 10, fy - 30), (fx + 18, fy)], fill=(255, 140, 20))
    d.polygon([(fx - 8, fy), (fx - 2, fy - 16), (fx + 6, fy - 8), (fx + 10, fy)],
              fill=(255, 220, 60))
    # smoke column
    for cx, cy, r in ((fx + 6, fy - 34, 10), (fx + 14, fy - 48, 8),
                      (fx + 22, fy - 60, 6)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 110, 110))
    # small drone above
    d.line([x + 30, y + 12, x + 70, y + 12], fill=(60, 60, 60), width=3)
    d.ellipse([x + 46, y + 8, x + 54, y + 16], fill=(60, 60, 60))


def art_corvette(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 60, 90))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(25, 80, 120))
    for i in range(4):
        d.arc([x + 12 + i * 48, y + h - 22, x + 48 + i * 48, y + h - 4],
              200, 340, fill=(140, 200, 230), width=2)
    # corvette
    d.polygon([(x + 30, y + h - 30), (x + w - 30, y + h - 30),
               (x + w - 44, y + h - 48), (x + 44, y + h - 48)],
              fill=(120, 130, 140))
    d.rectangle([x + 70, y + h - 62, x + 110, y + h - 48], fill=(100, 110, 120))
    d.line([x + 90, y + h - 76, x + 90, y + h - 62], fill=(180, 180, 180),
           width=3)
    # sea drone speeding in, with wake
    d.polygon([(x + w - 66, y + h - 22), (x + w - 30, y + h - 22),
               (x + w - 24, y + h - 14), (x + w - 60, y + h - 14)],
              fill=(220, 220, 220))
    d.line([x + w - 100, y + h - 18, x + w - 66, y + h - 18],
           fill=(255, 255, 255), width=2)
    # blast at the stern
    ex, ey = x + 40, y + h - 44
    d.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=(255, 180, 40))
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 230, 120))


def art_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    # grid
    for gy in range(y + 12, y + h - 10, 14):
        d.line([x + 10, gy, x + w - 10, gy], fill=(220, 220, 220), width=1)
    # falling line
    pts = [(x + 14, y + 14), (x + 48, y + 20), (x + 82, y + 16),
           (x + 116, y + 34), (x + 150, y + 30), (x + w - 14, y + h - 16)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(x + w - 14, y + h - 16), (x + w - 26, y + h - 22),
               (x + w - 22, y + h - 8)], fill=RED)
    # chip
    d.rectangle([x + 16, y + h - 34, x + 52, y + h - 6], fill=(30, 30, 30))
    d.rectangle([x + 24, y + h - 28, x + 44, y + h - 12], fill=(80, 160, 220))
    for px in (x + 24, x + 34, x + 44):
        d.line([px, y + h - 6, px, y + h - 1], fill=(150, 150, 150), width=2)


def art_parliament(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 225, 240))
    # Big Ben-ish tower
    d.rectangle([x + 20, y + 10, x + 46, y + h - 8], fill=(190, 180, 150))
    d.polygon([(x + 16, y + 10), (x + 33, y - 6), (x + 50, y + 10)],
              fill=(120, 110, 90))
    d.ellipse([x + 26, y + 18, x + 40, y + 32], fill=(255, 255, 255))
    d.line([x + 33, y + 25, x + 33, y + 20], fill=INK, width=1)
    d.line([x + 33, y + 25, x + 37, y + 25], fill=INK, width=1)
    # EU stars circle
    import math
    cx, cy = x + w - 62, y + 30
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(0, 51, 153))
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx, sy = cx + int(18 * math.cos(a)), cy + int(18 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    # green benches
    d.rectangle([x + 56, y + h - 26, x + w - 10, y + h - 8], fill=(40, 120, 70))
    for i in range(4):
        d.rectangle([x + 64 + i * 30, y + h - 40, x + 86 + i * 30, y + h - 26],
                    fill=(60, 150, 90))


def art_podium(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
    # podium steps 1-2-3
    cx = x + w // 2
    d.rectangle([cx - 24, y + 14, cx + 24, y + h - 6], fill=(200, 170, 60))
    d.rectangle([cx - 72, y + 26, cx - 24, y + h - 6], fill=(170, 170, 170))
    d.rectangle([cx + 24, y + 38, cx + 72, y + h - 6], fill=(190, 120, 70))
    f = SANS_B(16)
    d.text((cx - 6, y + 18), "1", font=f, fill=(255, 255, 255))
    d.text((cx - 54, y + 30), "2", font=f, fill=(255, 255, 255))
    d.text((cx + 42, y + 42), "3", font=f, fill=(255, 255, 255))
    # small Indian flag, top-left corner
    d.rectangle([x + 8, y + 6, x + 38, y + 10], fill=(255, 153, 51))
    d.rectangle([x + 8, y + 10, x + 38, y + 14], fill=(255, 255, 255))
    d.rectangle([x + 8, y + 14, x + 38, y + 18], fill=(19, 136, 8))


def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 90, 80))
    # globe
    d.ellipse([x + 10, y + 6, x + 66, y + 58], fill=(60, 140, 200))
    d.ellipse([x + 22, y + 16, x + 38, y + 30], fill=(80, 180, 90))
    d.ellipse([x + 38, y + 38, x + 56, y + 52], fill=(80, 180, 90))
    # draft text with fossil fuels crossed out
    d.rectangle([x + 78, y + 8, x + w - 10, y + h - 8], fill=(255, 255, 255))
    for i in range(4):
        d.rectangle([x + 84, y + 14 + i * 9, x + w - 16, y + 17 + i * 9],
                    fill=(200, 200, 200))
    d.line([x + 84, y + 24, x + w - 16, y + 24], fill=RED, width=2)
    d.rectangle([x + 84, y + h - 20, x + 128, y + h - 10], fill=RED)
    d.text((x + 88, y + h - 19), "NO DEAL", font=SANS_B(8),
           fill=(255, 255, 255))


def art_school(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 215, 235))
    # school building
    d.rectangle([x + 18, y + 22, x + 120, y + h - 6], fill=(235, 220, 180))
    d.polygon([(x + 12, y + 22), (x + 69, y + 4), (x + 126, y + 22)],
              fill=(160, 60, 60))
    for i in range(3):
        d.rectangle([x + 28 + i * 30, y + 30, x + 46 + i * 30, y + 42],
                    fill=(140, 190, 220))
    d.rectangle([x + 58, y + h - 20, x + 80, y + h - 6], fill=(120, 80, 40))
    # flag pole
    d.line([x + 140, y + 6, x + 140, y + h - 6], fill=(100, 100, 100), width=2)
    d.rectangle([x + 140, y + 6, x + 168, y + 15], fill=(0, 91, 187))
    d.rectangle([x + 140, y + 15, x + 168, y + 24], fill=(255, 213, 0))
    # falling debris
    d.polygon([(x + 150, y + 34), (x + 168, y + 44), (x + 146, y + 52)],
              fill=(80, 80, 80))
    d.line([x + 158, y + 30, x + 152, y + 52], fill=(120, 120, 120), width=2)
    d.ellipse([x + w - 34, y + h - 22, x + w - 18, y + h - 6],
              fill=(255, 180, 40))


def art_trench(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 40, 80))
    # depth gradient bands
    for i, col in enumerate(((20, 70, 120), (15, 55, 100), (10, 40, 80))):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=col)
    # seafloor with a deep V trench
    d.polygon([(x, y + h - 18), (x + w // 2 - 30, y + h - 18),
               (x + w // 2, y + h - 2), (x + w // 2 + 30, y + h - 18),
               (x + w, y + h - 18), (x + w, y + h), (x, y + h)],
              fill=(120, 100, 70))
    # volcano eruption at the trench lip
    vx, vy = x + w // 2 - 52, y + h - 26
    d.polygon([(vx - 18, vy + 8), (vx, vy - 18), (vx + 18, vy + 8)],
              fill=(140, 60, 40))
    d.ellipse([vx - 6, vy - 28, vx + 6, vy - 16], fill=(255, 140, 40))
    d.ellipse([vx - 3, vy - 36, vx + 9, vy - 24], fill=(255, 200, 80))
    # tiny submersible with a light cone
    sx, sy = x + w - 58, y + 30
    d.ellipse([sx, sy, sx + 34, sy + 14], fill=(255, 220, 60))
    d.polygon([(sx + 34, sy + 3), (sx + 62, sy - 6), (sx + 62, sy + 16)],
              fill=(255, 240, 160))
    # depth label
    d.text((x + 10, y + 8), "10,935 m", font=SANS_B(11), fill=(180, 220, 255))


# ---------------------------------------------------------------- world map
# Rough continent outlines in a 0..100 (x) by 0..50 (y) space.

CONTINENTS = [
    # North America
    [(4, 9), (13, 4), (30, 4), (35, 10), (28, 14), (31, 20), (22, 23),
     (19, 29), (12, 26), (6, 18)],
    # Greenland
    [(31, 2), (38, 2), (36, 8), (30, 8)],
    # South America
    [(24, 30), (32, 28), (37, 34), (32, 44), (28, 48), (24, 40)],
    # Africa
    [(46, 24), (56, 20), (62, 26), (60, 34), (54, 42), (48, 36)],
    # Eurasia
    [(44, 8), (60, 4), (86, 2), (96, 8), (92, 16), (84, 14), (78, 22),
     (70, 26), (62, 22), (56, 24), (48, 18)],
    # India
    [(64, 24), (70, 24), (67, 33)],
    # SE Asia
    [(74, 26), (80, 28), (78, 34), (74, 32)],
    # Australia
    [(82, 36), (92, 34), (94, 42), (86, 46), (80, 42)],
    # Japan
    [(92, 14), (95, 18), (93, 23)],
]

# Story number -> (map x, map y) — spread so no two pins touch.
PINS = {1: (48, 11), 2: (66, 22), 3: (70, 19), 4: (56, 8), 5: (87, 45),
        6: (52, 4), 7: (52, 23), 8: (85, 15), 9: (44, 7), 10: (62, 28),
        11: (93, 41), 12: (60, 12), 13: (89, 27)}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 225, 240))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    for i in range(1, 5):
        gx = x + i * w // 5
        d.line([gx, y, gx, y + h], fill=(185, 210, 230), width=1)
    for j in range(1, 3):
        gy = y + j * h // 3
        d.line([x, gy, x + w, gy], fill=(185, 210, 230), width=1)
    for poly in CONTINENTS:
        pts = [(x + px * w / 100.0, y + py * h / 50.0) for px, py in poly]
        d.polygon(pts, fill=(232, 214, 170), outline=(180, 160, 120))
    for n, (px, py) in PINS.items():
        cx, cy = x + px * w / 100.0, y + py * h / 50.0
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = SANS_B(7)
        t = str(n)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 4), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- story data

LEADS = [
    dict(art="panels/airport.png", tag="BRUSSELS · STRIKE", tagfill=NAVY, n=1,
         head="Belgium's airports stand still",
         body="Air traffic control walks out 7am–9pm in a national strike; "
              "429 flights and 59,500 passengers hit at Brussels, Charleroi "
              "shut. — AFP"),
    dict(art="panels/drone.png", tag="HORMUZ · WAR", tagfill=RED, n=2,
         head="Iran claims 78 US drones downed",
         body="An IRGC infographic counts 58 MQ-9 Reapers and 20 MQ-1 "
              "Predators, plus a fourth drone in 24 hours. Unconfirmed by "
              "the US. — Press TV"),
    dict(art="panels/summit.png", tag="DELHI · DIPLOMACY", tagfill=TEAL, n=3,
         head="Modi and Balen Shah talk for 100 minutes",
         body="On his first visit as PM, Nepal's Balen Shah flags off a new "
              "Ayodhya–Janakpur train and seeks $2bn for flood rebuilding. "
              "— IANS"),
]

SMALL = [
    dict(art="panels/rubble.png", tag="DYMER · WAR", n=4,
         head="Toll in Dymer rises to 11",
         body="Another body pulled from the rubble; a boy of 7 and a woman "
              "found alive. — Reuters"),
    dict(art="panels/microphone.png", tag="MELBOURNE · OBITUARY", n=5,
         head="Molly Meldrum dies at 83",
         body="Countdown host who championed AC/DC and Kylie; a state "
              "funeral is planned. — Reuters"),
    dict(art="panels/shipfire.png", tag="MOSCOW · WAR", n=6,
         head="Kremlin cries 'terrorism' over ship fire",
         body="Moscow blames Kyiv for the drone strike that set the Sparta II "
              "ablaze. — Reuters"),
    dict(art="panels/corvette.png", tag="LIBYA · WAR", n=7,
         head="Zelenskyy: we hit a Russian corvette",
         body="Kyiv says a sea drone severely damaged the Merkury off Libya. "
              "— Inshorts"),
    dict(art="panels/markets.png", tag="ASIA · MARKETS", n=8,
         head="Asian shares slide on AI doubts",
         body="Korean chipmakers shed about 3% as regulators move to steady "
              "sagging markets. — FT"),
    dict(art="panels/parliament.png", tag="LONDON · POLITICS", n=9,
         head="Burnham sells EU deal to MPs",
         body="A 'broken status quo or change'; May is 'aghast' at talk of "
              "rejoining. — BBC"),
    dict(art="panels/podium.png", tag="NEW DELHI · POWER", n=10,
         head="India holds No. 3 in Asia power rank",
         body="The Lowy Index scores India 40.5 points for 2026, still "
              "third in the region. — Inshorts"),
    dict(art="panels/cop.png", tag="CANBERRA · CLIMATE", n=11,
         head="Albanese defends Bowen on COP31",
         body="The PM backs his minister after the Antalya talks end with "
              "no deal. — N.M. House"),
    dict(art="panels/school.png", tag="KYIV · WAR", n=12,
         head="Drone debris falls on Kyiv schools",
         body="Air defences down drones over the capital in an early-morning "
              "attack. — N.M. House"),
    dict(art="panels/trench.png", tag="PACIFIC · SCIENCE", n=13,
         head="How the deepest place was made",
         body="Volcanic remnants explain how the Challenger Deep formed, "
              "scientists find. — Digest"),
]

ALSO = [
    (14, "Washington — Trump: Iran attacks hit a year high.", "Digest"),
    (15, "California — Extreme tides, rain after mudslides.", "GEORGE"),
    (16, "Memphis — FedEx pilot Sanders dies at 82.", "GEORGE"),
    (17, "London — PIP overhaul urged; NHS cuts feared.", "D. Brief"),
    (18, "London — CBI presses case for private cash.", "D. Brief"),
    (19, "London — IAG: Heathrow runway 'doomed'.", "D. Brief"),
    (20, "Space — Star seen spiralling into a giant.", "Digest"),
    (21, "Damascus — Syria and EU seek normalisation.", "N.M. House"),
    (22, "Gaza — Report calls it a 'toxic wasteland'.", "N.M. House"),
    (23, "Hormuz — Maritime attacks hit record high.", "N.M. House"),
    (24, "New York — Thanksgiving storm forecast.", "GEORGE"),
    (25, "Zawtar — Israeli demolitions shown Monday.", "Al Jazeera"),
    (26, "Vienna — Austrian Air cancels Brussels runs.", "V. Vienna"),
    (27, "Brussels — Trains run; buses, trams hit.", "B. Times"),
    (28, "New York — Wall St set to rebound after rout.", "FT"),
    (29, "New York — FT: Nvidia financing in focus.", "FT"),
    (30, "Brussels — Airlines: notice 'exceptionally difficult'.",
     "T. Tomorrow"),
    (31, "Brussels — 60% of controllers joined walkout.", "QNC"),
]

STATS = [
    ("429", "flights cancelled at Brussels"),
    ("59,500", "passengers hit at Brussels"),
    ("78", "US drones Iran claims downed"),
    ("11", "dead after the Dymer strike"),
    ("100", "minutes of Modi–Shah talks"),
    ("83", "Molly Meldrum dies aged 83"),
]

DATECHECK = ("Every story here happened, or was first reported, on Monday "
             "23 November 2026. LEFT OUT — 22 NOV: COP31 collapse · "
             "Democrats' 258 seats · Alcaraz title · Delta outage · Alice "
             "Huang report. 21 NOV: 58th MQ-9 claim · Riemann verified. "
             "20 NOV: Penny law · Denmark–Russia row · Indonesia seizure · "
             "Riemann announced. 25 NOV: Iowa blast (Wed).")


def fit_font(d, text, sizes, max_w):
    """Largest sans font from sizes that fits text in max_w."""
    for s in sizes:
        f = SANS(s)
        if d.textlength(text, font=f) <= max_w:
            return f
    return SANS(sizes[-1])


def paste_art(img, art, x, y, w, h):
    """Place art in a tile at (x, y, w, h). art is either a drawing
    function (drawn on an offscreen tile, clips overflow) or a photo file
    path relative to this file's directory (center-cropped to fit with
    ImageOps.fit: no distortion, no gaps). Both paths are deterministic."""
    if isinstance(art, str):
        here = os.path.dirname(os.path.abspath(__file__))
        photo = Image.open(os.path.join(here, art)).convert("RGB")
        tile = ImageOps.fit(photo, (w, h), Image.LANCZOS,
                            centering=(0.5, 0.5))
        img.paste(tile, (x, y))
        return
    tmp = Image.new("RGB", (w, h), PAPER)
    td = ImageDraw.Draw(tmp)
    art(td, 0, 0, w, h)
    img.paste(tmp, (x, y))


# ---------------------------------------------------------------- compose

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top strip
    d.text((8, 3), "THE WORLD IN ONE DAY", font=SANS_B(12), fill=RED)
    rt = "31 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
    d.text((W - 8 - d.textlength(rt, font=SANS_B(11)), 4), rt,
           font=SANS_B(11), fill=INK)
    d.line([8, 19, W - 8, 19], fill=INK, width=2)

    # masthead
    title = "Monday 23 November 2026"
    tf = SERIF_B(58)
    d.text(((W - d.textlength(title, font=tf)) / 2, 24), title, font=tf,
           fill=INK)
    sub = ("Belgium's airports stand still · Iran claims 78 US drones "
           "downed · Modi and Balen Shah talk for 100 minutes")
    sf = SERIF(16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 88), sub, font=sf, fill=RED)
    d.line([8, 108, W - 8, 108], fill=INK, width=1)

    # stat strip
    colw = (W - 16) / 6.0
    for i, (num, lab) in enumerate(STATS):
        x0 = 8 + int(i * colw)
        if i:
            d.line([x0 - 4, 114, x0 - 4, 140], fill=(190, 180, 160), width=1)
        d.text((x0 + 4, 112), num, font=SERIF_B(24), fill=RED)
        d.text((x0 + 4, 138 - 14 + 16), lab, font=SANS(10), fill=INK)
    d.line([8, 156, W - 8, 156], fill=INK, width=1)

    # three leads
    lw, lgap, ly, lh = 328, 8, 160, 276
    for i, s in enumerate(LEADS):
        x0 = 8 + i * (lw + lgap)
        d.rectangle([x0, ly, x0 + lw, ly + lh], outline=INK, width=1)
        paste_art(img, s["art"], x0 + 1, ly + 1, lw - 2, 140)
        chip(d, x0 + 8, ly + 8, s["tag"], s["tagfill"])
        num_badge(d, x0 + 8, ly + 148, s["n"])
        para(d, x0 + 32, ly + 150, s["tag"], SANS_B(11), lw - 40, 14,
             fill=RED)
        para(d, x0 + 8, ly + 170, s["head"], SERIF_B(22), lw - 16, 26,
             max_lines=2)
        para(d, x0 + 8, ly + 224, s["body"], SANS(11), lw - 16, 14,
             max_lines=3)

    # ten small panels, two rows of five
    widths = [196, 195, 195, 195, 195]
    sy, sh = 444, 170
    for row in range(2):
        y0 = sy + row * (sh + 8)
        x0 = 8
        for j in range(5):
            s = SMALL[row * 5 + j]
            w = widths[j]
            d.rectangle([x0, y0, x0 + w, y0 + sh], outline=INK, width=1)
            paste_art(img, s["art"], x0 + 1, y0 + 1, w - 2, 62)
            num_badge(d, x0 + 6, y0 + 68, s["n"])
            d.text((x0 + 28, y0 + 70), s["tag"], font=SANS_B(9), fill=RED)
            para(d, x0 + 6, y0 + 88, s["head"], SERIF_B(15), w - 12, 18,
                 max_lines=2)
            para(d, x0 + 6, y0 + 126, s["body"], SANS(10), w - 12, 13,
                 max_lines=3)
            x0 += w + 8

    # bottom: map + ALSO list
    by = 800
    d.text((8, by), "WHERE IT HAPPENED", font=SANS_B(12), fill=RED)
    d.text((180, by + 1), "numbers match the stories", font=SANS(10),
           fill=GREY)
    d.text((344, by), "ALSO ON MONDAY 23 NOVEMBER 2026", font=SANS_B(12),
           fill=RED)
    d.text((344 + 300, by + 1), "place · what happened · source",
           font=SANS(10), fill=GREY)
    draw_map(d, 8, by + 20, 328, 118)
    d.text((8, by + 140), "Pins: stories 1–13 (8 is markets).",
           font=SANS(9), fill=GREY)

    col_w = 332
    for k, (n, txt, src) in enumerate(ALSO):
        cx = 344 + (k // 9) * (col_w + 8)
        cy = by + 20 + (k % 9) * 15
        d.text((cx, cy), str(n), font=SANS_B(11), fill=RED)
        full = txt + " " + src
        f = fit_font(d, full, [11, 10, 9], col_w - 24)
        d.text((cx + 22, cy), full, font=f, fill=INK)

    # DATE CHECK box
    dy = 950
    d.rectangle([8, dy, W - 8, dy + 48], outline=RED, width=2)
    d.text((14, dy + 5), "DATE CHECK", font=SANS_B(12), fill=RED)
    para(d, 14 + 96, dy + 5, DATECHECK, SANS(11), W - 8 - 14 - 96 - 8, 14,
         max_lines=3)

    # footer
    foot = ("Claims are attributed, not stated as fact · Pictures: original "
            "generated images; map: drawn in code · Sources: Reuters, AFP, "
            "FT, BBC, IANS, Inshorts, Press TV, Al Jazeera, N.M. House · "
            "2026-11-23")
    ff = SANS(9)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1006), foot, font=ff,
           fill=GREY)
    return img


if __name__ == "__main__":
    import os
    out = os.environ.get("NEWS_OUT", "entry.png")
    build().save(out, "PNG")
    print("wrote", out)
