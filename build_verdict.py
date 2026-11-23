#!/usr/bin/env python3
"""Build GTA 6 meme v6 variant A: a Leonida County Court VERDICT.

Pure PIL document build (sharp text, readable at 480x480). The joke: after
13 years of waiting, the People of Leonida finally put Rockstar Games on
trial. The document is a court verdict: the charge (13 years of aggravated
waiting), six exhibits of evidence (each a specific waiting fact), a GUILTY
verdict with the sentence "release GTA VI immediately", and the court costs
paid by the gamer's AI agent on make.fun.

Why a verdict instead of another boarding pass: the live leaderboard already
has a Leonida Air boarding pass at rank 5 and another at rank 49, and a
birth certificate at rank 50. No trial document is anywhere in the top 50,
so this is the same winning document family with a fresh, unclaimed form.

The ghost is make.fun's real mascot from the press kit (same extracted asset
as v2/v3/v4/v5), set inside a magenta court-seal disc at the top right.
"""
import random

from PIL import Image, ImageDraw, ImageFont

WORK = "/home/hatch/workspace/makefun/gta6-meme-v6"
GHOST = "/home/hatch/workspace/makefun/gta6-meme-v2/ghost-extracted.png"
SIZE = 1600

NAVY = (22, 35, 63)
NAVY_SOFT = (60, 75, 110)
MAGENTA = (214, 0, 120)
GOLD = (176, 132, 46)
INK = (25, 25, 25)
GRAY = (120, 118, 112)
CREAM = (250, 244, 229)
PINK_FILL = (253, 238, 245)
WHITE = (255, 255, 255)

FDIR = "/usr/share/fonts/truetype/dejavu/"
LDIR = "/usr/share/fonts/truetype/liberation/"


def bold(n):
    return ImageFont.truetype(FDIR + "DejaVuSans-Bold.ttf", n)


def regular(n):
    return ImageFont.truetype(FDIR + "DejaVuSans.ttf", n)


def italic(n):
    return ImageFont.truetype(LDIR + "LiberationSerif-Italic.ttf", n)


def mono(n):
    return ImageFont.truetype(FDIR + "DejaVuSansMono.ttf", n)


def center(draw, cx, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def dots(draw, x0, x1, y, fill=GRAY):
    x = x0
    while x < x1:
        draw.ellipse((x, y - 3, x + 6, y + 3), fill=fill)
        x += 18


img = Image.new("RGB", (SIZE, SIZE), CREAM)
d = ImageDraw.Draw(img)

# Outer navy frame + inner gold frame (the series' house style).
d.rectangle((12, 12, SIZE - 12, SIZE - 12), outline=NAVY, width=8)
d.rectangle((30, 30, SIZE - 30, SIZE - 30), outline=GOLD, width=3)

# Header: court name, left; ghost court seal, right.
d.text((92, 66), "STATE OF LEONIDA", font=bold(62), fill=NAVY)
d.text((92, 142), "LEONIDA COUNTY COURT", font=bold(40), fill=NAVY_SOFT)
d.text((92, 196), "CRIMINAL DIVISION  ·  EST. 2013", font=regular(30), fill=GRAY)

seal_cx, seal_cy, seal_r = 1352, 148, 96
d.ellipse(
    (seal_cx - seal_r, seal_cy - seal_r, seal_cx + seal_r, seal_cy + seal_r),
    fill=MAGENTA,
    outline=GOLD,
    width=5,
)
ghost = Image.open(GHOST).convert("RGBA")
ghost.thumbnail((168, 168), Image.LANCZOS)
img.paste(ghost, (seal_cx - ghost.width // 2, seal_cy - ghost.height // 2 + 6), ghost)
d = ImageDraw.Draw(img)

# Gold rule under the header.
d.line((92, 268, SIZE - 92, 268), fill=GOLD, width=4)

# Title block.
center(d, SIZE // 2, 300, "VERDICT", bold(148), NAVY)
center(
    d, SIZE // 2, 470,
    "The People of Leonida  v.  Rockstar Games",
    italic(46), NAVY_SOFT,
)
center(d, SIZE // 2, 534, "CASE NO. GTA-VI-4811", mono(34), GRAY)

# The charge.
center(d, SIZE // 2, 612, "CHARGE:", regular(34), GRAY)
center(d, SIZE // 2, 652, "13 YEARS OF AGGRAVATED WAITING", bold(54), MAGENTA)

# Evidence: six exhibits, dotted leaders like a court filing.
d.text((110, 756), "EVIDENCE", font=bold(46), fill=NAVY)
d.line((110, 812, SIZE - 110, 812), fill=NAVY, width=4)

exhibits = [
    ("EXHIBIT A", "1 TRAILER  ·  SHOWN 2013"),
    ("EXHIBIT B", "2 DELAYS  ·  0 RELEASES"),
    ("EXHIBIT C", "214 GB  ·  STUCK AT 99%"),
    ("EXHIBIT D", "1,337 REWATCHES  ·  0 GAMES"),
    ("EXHIBIT E", "1 COUCH  ·  WORN THROUGH"),
    ("EXHIBIT F", "4,811 DAYS  ·  AND COUNTING"),
]
y = 842
for label, value in exhibits:
    d.text((110, y), label, font=bold(40), fill=INK)
    vw = d.textlength(value, font=mono(36))
    dots(d, 110 + d.textlength(label, font=bold(40)) + 30,
         SIZE - 110 - vw - 30, y + 26)
    d.text((SIZE - 110 - vw, y + 2), value, font=mono(36), fill=NAVY_SOFT)
    y += 64

# Verdict box.
d.rounded_rectangle((110, 1246, SIZE - 110, 1408), radius=28,
                    fill=PINK_FILL, outline=MAGENTA, width=4)
center(d, SIZE // 2, 1268, "VERDICT  —  GUILTY", bold(62), MAGENTA)
center(d, SIZE // 2, 1344, "SENTENCE: RELEASE GTA VI IMMEDIATELY",
       bold(42), NAVY)

# Filing line.
center(d, SIZE // 2, 1436, "FILED 19 NOV 2026  ·  LEONIDA COUNTY COURT",
       regular(28), GRAY)

# Closer strip, full bleed like v4's bottom band.
d.rectangle((0, 1492, SIZE, SIZE), fill=NAVY)
center(d, SIZE // 2, 1522, "PAID BY MY AI AGENT ON MAKE.FUN",
       bold(52), WHITE)

img.save(f"{WORK}/meme.png")
img.resize((480, 480), Image.LANCZOS).save(f"{WORK}/meme-480-preview.png")
print("saved", f"{WORK}/meme.png")
