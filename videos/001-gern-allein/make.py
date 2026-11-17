import math, random
import cairo
from PIL import Image
import numpy as np

TW, TH = 1280, 720
_keep = []
def load(p):
    im = Image.open(p).convert("RGBA").resize((TW, TH), Image.LANCZOS)
    a = np.array(im)[:, :, [2, 1, 0, 3]].copy(); _keep.append(a)
    return cairo.ImageSurface.create_for_data(memoryview(a), cairo.FORMAT_ARGB32, TW, TH)

YEL = (1.0, 0.82, 0.18); WHITE = (1, 1, 1)

def shadow_text(ctx, s, x, y, size, col, font="Inter Black", align="left", skew=0.0):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s)
    x0 = x - e.x_bearing if align == "left" else x - e.width / 2 - e.x_bearing
    for dx, dy, a in ((0, 10, 0.55), (0, 5, 0.5)):
        ctx.move_to(x0 + dx, y + dy); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, a); ctx.fill()
    ctx.move_to(x0, y); ctx.text_path(s); ctx.set_source_rgba(0, 0, 0, 0.9); ctx.set_line_width(size * 0.06); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.fill()
    return e

def darken(ctx, x0, y0, x1, y1, a=0.75, horizontal=True):
    g = cairo.LinearGradient(x0, y0, x1, y0) if horizontal else cairo.LinearGradient(x0, y0, x0, y1)
    g.add_color_stop_rgba(0, 0, 0, 0, a); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g); ctx.rectangle(0, 0, TW, TH); ctx.fill()

r = random.Random(4)
def marker(ctx, pts, col, w):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0]); [ctx.line_to(x + r.uniform(-1.2, 1.2), y + r.uniform(-1.2, 1.2)) for x, y in pts[1:]]
    ctx.set_source_rgba(0, 0, 0, 0.5); ctx.set_line_width(w + 6); ctx.stroke_preserve()
    ctx.set_source_rgb(*col); ctx.set_line_width(w); ctx.stroke()

def bez(p0, p1, p2, p3, n=40):
    return [tuple((1-u)**3*p0[k] + 3*(1-u)**2*u*p1[k] + 3*(1-u)*u*u*p2[k] + u**3*p3[k] for k in (0, 1)) for u in [i / n for i in range(n + 1)]]

def save(surf, name):
    surf.write_to_png(name)

# V1: Party vs Ruhe
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, TW, TH); c = cairo.Context(s)
c.set_source_surface(load("m0.png"), 0, 0); c.paint()
darken(c, 0, 0, 0, 330, 0.85, horizontal=False)
shadow_text(c, "LIEBER ALLEIN?", 40, 125, 112, YEL)
shadow_text(c, "Das ist kein Fehler.", 44, 215, 62, WHITE, font="Inter ExtraBold")
marker(c, bez((560, 250), (640, 300), (700, 320), (800, 330)), YEL, 9)
marker(c, [(778, 305), (805, 331), (774, 352)], YEL, 9)
save(s, "Thumb_1_Party_vs_Ruhe.png")

# V2: leuchtendes Gedankenmuster
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, TW, TH); c = cairo.Context(s)
c.set_source_surface(load("m1.png"), 0, 0); c.paint()
darken(c, 0, 0, 700, 0, 0.6)
shadow_text(c, "GERN ALLEIN?", 40, 290, 100, YEL)
shadow_text(c, "Dein Gehirn", 44, 395, 80, WHITE, font="Inter ExtraBold")
shadow_text(c, "tickt anders.", 44, 485, 80, WHITE, font="Inter ExtraBold")
save(s, "Thumb_2_Gehirn_tickt_anders.png")

# V3: Allein in der Menge
s = cairo.ImageSurface(cairo.FORMAT_ARGB32, TW, TH); c = cairo.Context(s)
c.set_source_surface(load("m2.png"), 0, 0); c.paint()
darken(c, 0, 0, 0, 300, 0.8, horizontal=False)
e1 = shadow_text(c, "ALLEIN", 90, 140, 128, WHITE)
shadow_text(c, "≠", 90 + e1.x_advance + 25, 140, 128, YEL)
shadow_text(c, "EINSAM", 90 + e1.x_advance + 135, 140, 128, WHITE)
pts = [(865 + 200 * math.cos(a), 500 + 235 * math.sin(a)) for a in [-0.3 + i * 2.15 * math.pi / 80 for i in range(81)]]
marker(c, pts, YEL, 8)
save(s, "Thumb_3_Allein_ungleich_einsam.png")
print("ok")
