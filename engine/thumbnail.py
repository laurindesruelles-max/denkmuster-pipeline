"""Denkmuster-Thumbnail (Standard seit Video 001, von Laurin gewählt):
EIN großes, professionell illustriertes Motiv (Higgsfield gpt_image_2_6, 16:9, ~0,25 Credits, Motiv rechts, links dunkler Freiraum)
+ Text links: Zeile 1 gelb (Frage/Hook, 2–3 Wörter, Großbuchstaben), Zeilen 2–3 weiß (Auflösung/Neugier), Inter Black/ExtraBold, Schatten.
Keine Strichmännchen im Thumbnail (Laurin: „muss professioneller aussehen“), keine Logos, keine echten Personen.

python3 engine/thumbnail.py motiv.png "GERN ALLEIN?" "Dein Gehirn" "tickt anders." out.png [--right]
--right: Text rechts statt links (wenn das Motiv links steht).
Motiv-Prompt-Muster: "Cinematic semi-realistic digital illustration for a psychology YouTube thumbnail. <ein starkes Motiv>,
dramatic rim light, very high contrast, large empty dark space on the left for text, no text, no logos."
"""
import sys
import cairo
import numpy as np
from PIL import Image

TW, TH = 1280, 720
YEL = (1.0, 0.82, 0.18); WHITE = (1, 1, 1)

def load(p, keep):
    im = Image.open(p).convert("RGBA").resize((TW, TH), Image.LANCZOS)
    a = np.array(im)[:, :, [2, 1, 0, 3]].copy(); keep.append(a)
    return cairo.ImageSurface.create_for_data(memoryview(a), cairo.FORMAT_ARGB32, TW, TH)

def text(ctx, s, x, y, size, col, font, right=False):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s)
    while e.width > 640 and size > 40:
        size -= 4; ctx.set_font_size(size); e = ctx.text_extents(s)
    x0 = (x - e.width - e.x_bearing) if right else (x - e.x_bearing)
    for dy, a in ((10, 0.55), (5, 0.5)):
        ctx.move_to(x0, y + dy); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, a); ctx.fill()
    ctx.move_to(x0, y); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, 0.9); ctx.set_line_width(size * 0.06); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill()

def make(motif, l1, l2, l3, out, right=False):
    keep = []
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, TW, TH); c = cairo.Context(s)
    c.set_source_surface(load(motif, keep), 0, 0); c.paint()
    g = cairo.LinearGradient(TW, 0, TW - 700, 0) if right else cairo.LinearGradient(0, 0, 700, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.6); g.add_color_stop_rgba(1, 0, 0, 0, 0); c.set_source(g); c.paint()
    x = TW - 44 if right else 44
    text(c, l1, x, 290, 100, YEL, "Inter Black", right)
    if l2: text(c, l2, x, 395, 80, WHITE, "Inter ExtraBold", right)
    if l3: text(c, l3, x, 485, 80, WHITE, "Inter ExtraBold", right)
    s.write_to_png(out)

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--right"]
    make(a[0], a[1], a[2], a[3], a[4], right="--right" in sys.argv)
    print("ok", a[4])
