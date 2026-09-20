# -*- coding: utf-8 -*-
"""ogp.png（1200×630）を作り直す。Pillow と Noto Serif CJK が必要です。"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = (240, 241, 241)
INK   = (20, 24, 26)
MUTED = (91, 100, 107)
FAINT = (138, 146, 153)
RULE  = (208, 212, 211)
HI    = (138, 98, 51)    # 昼
YO    = (59, 86, 116)    # 夜

SERIF   = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
SERIF_M = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Medium.ttc'

def font(path, size):
    return ImageFont.truetype(path, size, index=0)

def vertical(d, text, f, x, step, fill, yoff=0):
    y = (H - step * len(text)) // 2 + yoff
    for ch in text:
        bb = d.textbbox((0, 0), ch, font=f)
        d.text((x - (bb[2] - bb[0]) / 2 - bb[0], y), ch, font=f, fill=fill)
        y += step

img = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([36, 36, W - 37, H - 37], outline=RULE, width=1)

vertical(d, '短い休日', font(SERIF_M, 64), 950, 84, INK, -8)
vertical(d, '中編小説', font(SERIF, 21), 850, 30, MUTED, 8)

f_en = font(SERIF, 16)
x = 97
for ch in 'A SHORT HOLIDAY':
    d.text((x, 190), ch, font=f_en, fill=FAINT)
    x += d.textlength(ch, font=f_en) + 3.4

f_l = font(SERIF, 27)
d.text((96, 258), '長い一週間が過ぎ、短い休日が訪れる。', font=f_l, fill=MUTED)
d.text((96, 302), 'その一週間の記憶が、彼にはない。', font=f_l, fill=MUTED)

# 昼と夜を表す点
d.line([(96, 372), (152, 372)], fill=RULE, width=1)
d.ellipse([96, 398, 108, 410], fill=HI)
d.ellipse([120, 398, 132, 410], fill=YO)

d.text((96, 432), '全10章＋エピローグ ／ 約23,000字', font=font(SERIF, 18), fill=FAINT)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img.save(os.path.join(ROOT, 'ogp.png'), optimize=True)
print('ogp.png', img.size)
