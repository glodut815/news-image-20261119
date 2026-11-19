#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Runs only on the builder's machine (Pillow is available here). The
grader never runs this file: main.py just copies the bundled entry.png.
Deterministic: fixed palette, fixed geometry, no network, no random
(except a fixed-seed skyline), no time — re-running this script
reproduces the same entry.png bytes.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(BASE, "fonts")
OUT = os.path.join(BASE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (178, 34, 34)
SKY = (135, 206, 235)
SEA = (46, 110, 160)
GREY = (90, 90, 90)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 58)
F_DATE = font("DejaVuSans.ttf", 24)
F_HERO_HEAD = font("DejaVuSans-Bold.ttf", 40)
F_HERO_CAP = font("DejaVuSans.ttf", 21)
F_HEAD = font("DejaVuSans-Bold.ttf", 21)
F_CAP = font("DejaVuSans.ttf", 15)


def fit_font(draw, text, max_w, start_size, name="DejaVuSans.ttf"):
    """Largest font size (down to 12) that fits text on one line."""
    size = start_size
    while size > 12:
        f = font(name, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(name, 12)


def wrap(draw, text, f, max_w):
    """Wrap text to lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def person(d, x, y, s, suit, skin=(232, 190, 150), hair=(40, 40, 40)):
    """A simple suited figure, s = height in px, feet at (x, y)."""
    # head
    d.ellipse([x - s * 0.11, y - s, x + s * 0.11, y - s * 0.78], fill=skin)
    # hair
    d.pieslice([x - s * 0.11, y - s, x + s * 0.11, y - s * 0.86], 180, 360, fill=hair)
    # torso (suit)
    d.rectangle([x - s * 0.16, y - s * 0.76, x + s * 0.16, y - s * 0.28], fill=suit)
    # tie
    d.polygon([(x, y - s * 0.74), (x - s * 0.03, y - s * 0.62),
               (x, y - s * 0.52), (x + s * 0.03, y - s * 0.62)], fill=RED)
    # legs
    d.rectangle([x - s * 0.15, y - s * 0.28, x - s * 0.02, y], fill=(30, 30, 30))
    d.rectangle([x + s * 0.02, y - s * 0.28, x + s * 0.15, y], fill=(30, 30, 30))


def star(d, cx, cy, r, fill):
    """A proper 5-pointed star centred at (cx, cy)."""
    import math
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.4
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag_cn(d, x, y, w, h):
    """Small Chinese flag."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(d, x + w * 0.22, y + h * 0.30, h * 0.22, (255, 222, 0))
    star(d, x + w * 0.62, y + h * 0.22, h * 0.09, (255, 222, 0))
    star(d, x + w * 0.72, y + h * 0.42, h * 0.09, (255, 222, 0))
    star(d, x + w * 0.62, y + h * 0.62, h * 0.09, (255, 222, 0))
    # pole
    d.rectangle([x - 3, y - 6, x, y + h + 4], fill=(120, 90, 40))


def skyline(d, x0, y0, x1, y1, color=(70, 80, 110)):
    """Simple city towers along the bottom of a box."""
    import random
    rng = random.Random(19)
    x = x0
    while x < x1:
        w = rng.randint(28, 52)
        h = rng.randint(30, int((y1 - y0) * 0.75))
        d.rectangle([x, y1 - h, x + w, y1], fill=color)
        for wy in range(y1 - h + 6, y1 - 6, 12):
            for wx in range(x + 5, x + w - 5, 10):
                if rng.random() < 0.5:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 220, 120))
        x += w + 4


def panel_frame(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_panel(d, x, y, w, h, headline, caption, scene):
    panel_frame(d, x, y, w, h)
    scene(d, x + 2, y + 2, x + w - 2, y + 118)
    # headline, up to 2 lines
    lines = wrap(d, headline, F_HEAD, w - 16)
    ty = y + 126
    for ln in lines[:2]:
        d.text((x + 8, ty), ln, font=F_HEAD, fill=INK)
        ty += 24
    # caption, one line, shrink-to-fit
    fcap = fit_font(d, caption, w - 16, 15)
    d.text((x + 8, y + h - 26), caption, font=fcap, fill=(40, 40, 40))


# ---------------------------------------------------------------- scenes
def scene_hero(d, x0, y0, x1, y1):
    # sky + skyline + ground
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.rectangle([x0, y1 - 130, x1, y1], fill=(200, 210, 220))
    skyline(d, x0, y0 + 60, x1, y1 - 130, color=(96, 110, 140))
    # flags flanking the leaders
    flag_cn(d, x0 + 60, y0 + 30, 90, 60)
    flag_cn(d, x1 - 150, y0 + 30, 90, 60)
    ground = y1 - 8
    # three leaders shaking hands: outer two reach to the centre clasp
    person(d, x0 + 330, ground, 150, (25, 35, 80))
    person(d, x0 + 488, ground, 150, (40, 40, 40))
    person(d, x0 + 646, ground, 150, (60, 30, 30))
    d.line([x0 + 352, ground - 100, x0 + 478, ground - 90], fill=(232, 190, 150), width=10)
    d.line([x0 + 624, ground - 100, x0 + 498, ground - 90], fill=(210, 170, 130), width=10)
    # clasped hands at the centre
    d.ellipse([x0 + 470, ground - 104, x0 + 506, ground - 78], fill=(232, 190, 150))


def scene_icj(d, x0, y0, x1, y1):
    """UN court in The Hague: Peace Palace + scales of justice."""
    d.rectangle([x0, y0, x1, y1], fill=(180, 205, 225))
    # court building
    bx0, bx1 = x0 + 40, x1 - 40
    d.rectangle([bx0, y1 - 40, bx1, y1 - 24], fill=(230, 225, 210))
    for cx in range(bx0 + 18, bx1 - 14, 30):
        d.rectangle([cx, y1 - 66, cx + 10, y1 - 40], fill=(245, 242, 235))
    d.polygon([(bx0 - 6, y1 - 66), ((bx0 + bx1) // 2, y1 - 96), (bx1 + 6, y1 - 66)], fill=(200, 60, 40))
    d.rectangle([bx0 + 60, y1 - 104, bx0 + 78, y1 - 86], fill=(160, 150, 130))
    d.polygon([(bx0 + 56, y1 - 104), (bx0 + 82, y1 - 104), (bx0 + 69, y1 - 112)], fill=(120, 40, 30))
    # scales of justice, foreground
    sx, sy = (x0 + x1) // 2, y1 - 6
    d.line([sx, sy - 44, sx, sy], fill=(180, 150, 60), width=4)
    d.line([sx - 26, sy - 44, sx + 26, sy - 44], fill=(180, 150, 60), width=4)
    d.line([sx - 26, sy - 44, sx - 26, sy - 26], fill=(180, 150, 60), width=2)
    d.line([sx + 26, sy - 44, sx + 26, sy - 26], fill=(180, 150, 60), width=2)
    d.pieslice([sx - 38, sy - 28, sx - 14, sy - 12], 0, 180, fill=(220, 180, 80))
    d.pieslice([sx + 14, sy - 28, sx + 38, sy - 12], 0, 180, fill=(220, 180, 80))
    d.ellipse([sx - 4, sy - 50, sx + 4, sy - 42], fill=(220, 180, 80))
    d.text((x0 + 10, y0 + 6), "THE HAGUE", font=font("DejaVuSans-Bold.ttf", 13), fill=(255, 255, 255))


def scene_bridge(d, x0, y0, x1, y1):
    """Long sea bridge, explosion, collapsed span — all inside the box."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(176, 216, 240))
    # sea (bottom third)
    sea_y = y0 + int(h * 0.62)
    d.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for i, wy in enumerate((sea_y + 14, sea_y + 32)):
        for wx in range(x0 + 8 + (i * 20), x1 - 10, 44):
            d.line([wx, wy, wx + 24, wy], fill=(255, 255, 255), width=3)
    # bridge deck across the middle
    mid = y0 + int(h * 0.42)
    d.rectangle([x0, mid, x1, mid + 10], fill=(120, 120, 120))
    # pylons + cables on the standing left part
    for fx in (0.12, 0.32):
        px = x0 + int(w * fx)
        d.rectangle([px, y0 + 8, px + 8, mid], fill=(90, 90, 90))
        d.line([px + 4, y0 + 8, px - 26, mid], fill=(150, 150, 150), width=2)
        d.line([px + 4, y0 + 8, px + 34, mid], fill=(150, 150, 150), width=2)
    # break point: deck ends, span tilts down into the sea
    bx = x0 + int(w * 0.56)
    d.polygon([(bx, mid), (bx + int(w * 0.22), mid + 12),
               (bx + int(w * 0.22), mid + 20), (bx, mid + 10)], fill=(80, 80, 80))
    d.polygon([(bx + int(w * 0.22), mid + 12), (bx + int(w * 0.30), sea_y + 12),
               (bx + int(w * 0.26), sea_y + 14), (bx + int(w * 0.22), mid + 20)],
              fill=(100, 100, 100))
    # explosion fireball just above the break
    ex, ey = bx + 18, mid - 22
    d.ellipse([ex - 26, ey - 26, ex + 26, ey + 26], fill=(255, 140, 0))
    d.ellipse([ex - 17, ey - 17, ex + 17, ey + 17], fill=(255, 210, 0))
    d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=(255, 255, 200))
    # small smoke puffs, kept inside the box
    for sx, sy, sr in ((ex - 30, ey - 20, 10), (ex - 12, ey - 30, 11),
                       (ex + 16, ey - 28, 10), (ex + 32, ey - 16, 9)):
        if sy - sr >= y0:
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 90))
    # splash where the span hits the water
    sx0 = bx + int(w * 0.24)
    d.ellipse([sx0, sea_y + 2, sx0 + 34, sea_y + 16], fill=(255, 255, 255))


def scene_anthropic(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(245, 240, 225))
    # stock board rising line
    pts = [(x0 + 8, y1 - 30), (x0 + 60, y1 - 52), (x0 + 110, y1 - 44),
           (x0 + 160, y1 - 78), (x0 + 205, y1 - 96)]
    d.line(pts, fill=(200, 60, 40), width=5)
    d.polygon([(x0 + 195, y1 - 104), (x0 + 208, y1 - 94), (x0 + 192, y1 - 88)], fill=(200, 60, 40))
    d.text((x0 + 10, y0 + 6), "$81.3bn", font=font("DejaVuSans-Bold.ttf", 22), fill=INK)
    # robot figure, right
    rx, ry = x0 + 240, y1 - 8
    d.rectangle([rx - 26, ry - 78, rx + 26, ry - 30], fill=(200, 90, 40))  # body
    d.rectangle([rx - 20, ry - 104, rx + 20, ry - 76], fill=(220, 110, 60))  # head
    d.ellipse([rx - 12, ry - 96, rx - 2, ry - 86], fill=(255, 255, 255))
    d.ellipse([rx + 2, ry - 96, rx + 12, ry - 86], fill=(255, 255, 255))
    d.ellipse([rx - 9, ry - 93, rx - 5, ry - 89], fill=(0, 0, 0))
    d.ellipse([rx + 5, ry - 93, rx + 9, ry - 89], fill=(0, 0, 0))
    d.line([rx, ry - 104, rx, ry - 112], fill=(120, 120, 120), width=3)
    d.ellipse([rx - 4, ry - 116, rx + 4, ry - 108], fill=(255, 200, 0))
    d.rectangle([rx - 40, ry - 74, rx - 26, ry - 44], fill=(200, 90, 40))
    d.rectangle([rx + 26, ry - 74, rx + 40, ry - 44], fill=(200, 90, 40))
    d.rectangle([rx - 20, ry - 30, rx - 6, ry], fill=(80, 80, 80))
    d.rectangle([rx + 6, ry - 30, rx + 20, ry], fill=(80, 80, 80))


def scene_gulf(d, x0, y0, x1, y1):
    """Gulf night sky: drones over an air base, interceptors rising."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(38, 48, 70))
    # stars
    for sx, sy in ((0.08, 0.12), (0.22, 0.08), (0.35, 0.18), (0.55, 0.08),
                   (0.72, 0.14), (0.88, 0.09), (0.95, 0.22), (0.45, 0.06)):
        d.ellipse([x0 + int(w * sx) - 2, y0 + int(h * sy) - 2,
                   x0 + int(w * sx) + 2, y0 + int(h * sy) + 2], fill=(255, 255, 255))
    # moon
    d.ellipse([x1 - 52, y0 + 10, x1 - 22, y0 + 40], fill=(240, 235, 200))
    # ground + air base
    gy = y1 - 30
    d.rectangle([x0, gy, x1, y1], fill=(60, 55, 45))
    # control tower
    d.rectangle([x0 + 24, gy - 34, x0 + 40, gy], fill=(120, 115, 100))
    d.rectangle([x0 + 18, gy - 46, x0 + 46, gy - 34], fill=(140, 135, 120))
    # radar dish
    d.pieslice([x0 + 250, gy - 34, x0 + 280, gy - 4], 270, 360, fill=(200, 200, 200))
    d.rectangle([x0 + 263, gy - 8, x0 + 267, gy], fill=(150, 150, 150))
    # interceptor streaks rising
    for ix, iy in ((0.45, 0.62), (0.62, 0.55), (0.80, 0.60)):
        px, py = x0 + int(w * ix), y0 + int(h * iy)
        d.line([px, py, px + 26, py - 30], fill=(255, 220, 120), width=3)
        d.ellipse([px + 22, py - 34, px + 30, py - 26], fill=(255, 240, 180))
    # drones: small dark diamonds with motion trails
    for dx, dy in ((0.18, 0.28), (0.38, 0.20), (0.70, 0.30)):
        px, py = x0 + int(w * dx), y0 + int(h * dy)
        d.line([px - 22, py, px - 6, py], fill=(150, 150, 150), width=2)
        d.polygon([(px, py - 5), (px + 9, py), (px, py + 5), (px - 9, py)], fill=(20, 20, 20))
    # explosion puff near the base
    ex, ey = x0 + int(w * 0.55), gy - 14
    d.ellipse([ex - 14, ey - 14, ex + 14, ey + 14], fill=(255, 140, 0))
    d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=(255, 210, 0))
    d.text((x0 + 10, y0 + 6), "GULF", font=font("DejaVuSans-Bold.ttf", 13), fill=(255, 255, 255))


def scene_cop31(d, x0, y0, x1, y1):
    """COP31 climate summit: globe, rising sun, green leaves."""
    d.rectangle([x0, y0, x1, y1], fill=(200, 230, 215))
    # sun with rays, top right
    sx, sy = x1 - 34, y0 + 26
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 16, 26
        a = math.radians(ang)
        d.line([sx + r1 * math.cos(a), sy + r1 * math.sin(a),
                sx + r2 * math.cos(a), sy + r2 * math.sin(a)], fill=(255, 190, 0), width=3)
    d.ellipse([sx - 14, sy - 14, sx + 14, sy + 14], fill=(255, 200, 0))
    # globe, centre left
    cx, cy, r = x0 + 78, y0 + 62, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 160))
    d.ellipse([cx - 26, cy - 30, cx + 4, cy - 6], fill=(80, 170, 90))
    d.ellipse([cx - 6, cy + 8, cx + 30, cy + 30], fill=(80, 170, 90))
    d.ellipse([cx + 12, cy - 26, cx + 32, cy - 2], fill=(80, 170, 90))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(20, 60, 90), width=2)
    # leaves sprouting at the base
    for lx, tilt in ((x0 + 170, -1), (x0 + 205, 1), (x0 + 240, -1), (x0 + 272, 1)):
        d.pieslice([lx - 14, y1 - 34, lx + 14, y1 - 6], 180 + tilt * 30, 360 + tilt * 30, fill=(60, 150, 70))
        d.line([lx, y1 - 34, lx, y1 - 6], fill=(40, 110, 50), width=2)
    # banner
    d.rectangle([x0 + 150, y0 + 8, x1 - 8, y0 + 34], fill=(30, 90, 60))
    d.text((x0 + 158, y0 + 11), "COP31", font=font("DejaVuSans-Bold.ttf", 18), fill=(255, 255, 255))
    d.text((x0 + 10, y1 - 22), "ANTALYA", font=font("DejaVuSans-Bold.ttf", 13), fill=(30, 90, 60))


def scene_bangladesh(d, x0, y0, x1, y1):
    """Dusk street: a house on fire, smoke, crowd silhouettes."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(240, 170, 110))
    d.rectangle([x0, y1 - 26, x1, y1], fill=(90, 70, 60))
    # house
    hx0, hx1 = x0 + 60, x0 + 180
    d.rectangle([hx0, y1 - 58, hx1, y1 - 26], fill=(150, 110, 80))
    d.polygon([(hx0 - 8, y1 - 58), ((hx0 + hx1) // 2, y1 - 76), (hx1 + 8, y1 - 58)], fill=(120, 60, 40))
    d.rectangle([hx0 + 46, y1 - 44, hx0 + 74, y1 - 26], fill=(60, 40, 30))
    # flames on the roof, kept inside the scene box
    fx, fy = (hx0 + hx1) // 2, y1 - 76
    d.polygon([(fx - 22, fy + 6), (fx - 12, fy - 14), (fx - 4, fy - 4),
               (fx + 4, fy - 20), (fx + 12, fy - 6), (fx + 22, fy + 6)],
              fill=(255, 120, 0))
    d.polygon([(fx - 12, fy + 6), (fx - 6, fy - 8), (fx + 2, fy - 2),
               (fx + 6, fy - 12), (fx + 12, fy + 6)], fill=(255, 210, 0))
    # smoke rising, kept inside the scene box
    for sx, sy, sr in ((fx + 26, fy - 8, 8), (fx + 38, fy - 18, 9), (fx + 50, fy - 26, 8)):
        if sy - sr >= y0 + 2:
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 110, 105))
    # crowd silhouettes, right side
    for cx in (x0 + 215, x0 + 245, x0 + 275):
        person(d, cx, y1 - 8, 46, (50, 50, 50), skin=(120, 90, 70), hair=(20, 20, 20))
    d.text((x0 + 10, y0 + 6), "DHAKA", font=font("DejaVuSans-Bold.ttf", 13), fill=(255, 255, 255))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.text((W // 2, 6), "THE WORLD TODAY", font=F_TITLE, fill=INK, anchor="ma")
    d.line([24, 78, W - 24, 78], fill=INK, width=3)
    d.text((W // 2, 84), "Thursday 19 November 2026", font=F_DATE, fill=RED, anchor="ma")
    d.line([24, 118, W - 24, 118], fill=INK, width=2)

    # hero panel
    hx, hy, hw, hh = 24, 126, 976, 416
    panel_frame(d, hx, hy, hw, hh)
    scene_hero(d, hx + 2, hy + 2, hx + hw - 2, hy + 268)
    hero_head = "TRUMP, XI AND PUTIN MEET IN SHENZHEN"
    lines = wrap(d, hero_head, F_HERO_HEAD, hw - 32)
    ty = hy + 278
    for ln in lines[:2]:
        d.text((hx + 16, ty), ln, font=F_HERO_HEAD, fill=INK)
        ty += 46
    fcap = fit_font(d, "First three-way summit ends with a pledge on nuclear arms.", hw - 32, 21)
    d.text((hx + 16, hy + hh - 34), "First three-way summit ends with a pledge on nuclear arms.",
           font=fcap, fill=(40, 40, 40))

    # six small panels: 3 columns x 2 rows
    pw, ph, gap = 317, 220, 12
    panels = [
        ("UN COURT: MYANMAR GUILTY OF GENOCIDE",
         "First state ever convicted; 10,000 killed in 2017.",
         scene_icj),
        ("CRIMEAN BRIDGE HIT A THIRD TIME",
         "Ukraine hits the span again; road traffic halted.",
         scene_bridge),
        ("ANTHROPIC DEBUTS AT $1.5 TRILLION",
         "Record $81.3bn IPO starts trading as ANT.",
         scene_anthropic),
        ("IRAN HITS GULF BASES AFTER US STRIKE",
         "Drones strike Kuwait and Bahrain bases.",
         scene_gulf),
        ("COP31 ENTERS FINAL PHASE",
         "Ministers in Antalya race for a climate deal.",
         scene_cop31),
        ("BANGLADESH BURNS AS VIOLENCE SPREADS",
         "Yunus home set on fire; unrest hits 28 districts.",
         scene_bangladesh),
    ]
    for i, (head, cap, scene) in enumerate(panels):
        col, row = i % 3, i // 3
        x = 24 + col * (pw + gap)
        y = 554 + row * (ph + gap)
        draw_panel(d, x, y, pw, ph, head, cap, scene)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
