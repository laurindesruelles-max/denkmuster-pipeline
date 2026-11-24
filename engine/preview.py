"""Kontaktabzug ohne Rendern: je Szene das fertige Bild kurz vor der nächsten Kamerafahrt.
python3 engine/preview.py videos/NNN-slug [Kapitel ...]  -> /tmp/claude-0/sheet_*.png (4 Bilder pro Zeile)"""
import sys, os, math, importlib
vd = os.path.abspath(sys.argv[1]); sys.argv = [sys.argv[0]] + sys.argv[2:]
os.chdir(vd); sys.path.insert(0, vd)
S = importlib.import_module("scenes")
from wb import *
import wb, cairo
from PIL import Image
b=S.b
S.v.build_cam()
def frame(t):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf); board_bg(ctx)
    cx, cy, z = b.camera(t)
    ctx.save(); ctx.translate(W/2, H/2); ctx.scale(z, z); ctx.translate(-cx, -cy)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for t0, dur, kind, d, tend, bb in b.items:
        if t < t0 or t > tend + 0.35: continue
        f = prog(t, t0, t0 + dur)
        if kind == "s":
            pts, col, w = d; ctx.set_source_rgba(*col); ctx.set_line_width(w); draw_partial(ctx, pts, f)
        else:
            s, x, y, size, col, font, align, rot = d
            ctx.save(); ctx.translate(x, y); ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
            e = ctx.text_extents(s); x0 = -e.width/2 - e.x_bearing
            ctx.rectangle(x0 + e.x_bearing - 0.12*size, -size*1.3, (e.width + 0.24*size)*f, size*1.9); ctx.clip(); ctx.move_to(x0, 0); ctx.set_source_rgba(*col); ctx.show_text(s); ctx.restore()
    for fn in b.dyn: fn(ctx, t)
    ctx.restore(); surf.flush()
    return Image.frombuffer("RGBA", (W, H), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB")
# times: just before each pan (end of each scene) -> collect camera key times
keys = sorted(set(round(k[0], 2) for k in b.cam))
ts = [k - 0.05 for k in keys if k > 1 and b.camera(k-0.05)==b.camera(k-0.3)] + [S.v.TOTAL - 0.5]
ks = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
sel = []
for t in ts:
    kk = max(i for i in range(len(S.v.CT)) if S.v.CT[i] <= t)
    if ks is None or kk in ks: sel.append(t)
ims = [frame(t).resize((480, 270)) for t in sel]
cols = 4; rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 484, rows * 274), "white")
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 484, (i // cols) * 274))
os.makedirs("/tmp/claude-0", exist_ok=True); out = "/tmp/claude-0/sheet_" + "_".join(map(str, ks or ["all"])) + ".png"; sheet.save(out); print(out, len(ims))
