"""Denkmuster whiteboard engine: timed marker strokes on an endless board, camera, pen, text."""
import math, random, subprocess, os
import cairo

W, H, FPS = 1920, 1080, 30
SFX = os.environ.get("DM_SFX", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sfx"))  # Denkmuster-eigene Effekte

def hexc(h, a=1.0):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (a,)

INK = hexc("#1D1D1F"); RED = hexc("#D7263D"); BLUE = hexc("#1F5FBF"); GREEN = hexc("#1E9E5A")
ORANGE = hexc("#E39B17"); GREY = hexc("#8A8A90"); YEL = hexc("#F2C14E")

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, t0, t1): return clamp((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t0)
def ease(x): return 3 * x * x - 2 * x ** 3
def ease_out(x): return 1 - (1 - x) ** 3

_r = random.Random(7)
def wob(pts, a=1.2): return [(x + _r.uniform(-a, a), y + _r.uniform(-a, a)) for x, y in pts]

# ---------- shape builders (return point lists) ----------
def circle(cx, cy, r, a0=-1.7, turns=1.03, n=60, ry=None):
    ry = ry or r
    return wob([(cx + r * math.cos(a0 + 2 * math.pi * turns * i / n), cy + ry * math.sin(a0 + 2 * math.pi * turns * i / n)) for i in range(n + 1)], 1.0)

def line(x0, y0, x1, y1, n=12): return wob([(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)], 0.9)

def poly(*pts, n=8, closed=False):
    pts = list(pts) + ([pts[0]] if closed else [])
    out = []
    for (a, b), (c, d) in zip(pts, pts[1:]): out += [(a + (c - a) * i / n, b + (d - b) * i / n) for i in range(n)]
    out.append(pts[-1]); return wob(out, 0.9)

def rect(x, y, w, h): return poly((x, y), (x + w, y), (x + w, y + h), (x, y + h), closed=True)

def bez(p0, p1, p2, p3, n=30):
    return wob([tuple((1-u)**3*p0[k] + 3*(1-u)**2*u*p1[k] + 3*(1-u)*u*u*p2[k] + u**3*p3[k] for k in (0, 1)) for u in [i / n for i in range(n + 1)]], 0.9)

def spiral(cx, cy, r, turns=2.2, n=70):
    return wob([(cx + r * (i / n) * math.cos(6.28 * turns * i / n), cy + r * (i / n) * math.sin(6.28 * turns * i / n)) for i in range(n + 1)], 0.6)

def arc(cx, cy, r, a0, a1, n=30, ry=None):
    ry = ry or r
    return wob([(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)], 0.8)

class Board:
    def __init__(self):
        self.items = []   # (t0, dur, kind, data, layer)
        self.cam = []     # (t, cx, cy, zoom)
        self.sfx = []
        self.dyn = []     # callables(ctx, t) drawn in world space after strokes
        self.overlay = [] # callables(ctx, t) in screen space

    def s(self, t0, dur, pts, col=INK, w=9, sound=None):
        xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
        self.items.append([t0, dur, "s", (pts, col, w), 1e9, (min(xs)-w, min(ys)-w, max(xs)+w, max(ys)+w)])
        if sound: self.sfx.append((sound, t0, 0.7))
        return t0 + dur

    def many(self, t0, dur, strokes, col=INK, w=9):
        """draw several point-lists sequentially within dur (split by length)."""
        L = [max(1, sum(math.dist(a, b) for a, b in zip(p, p[1:]))) for p in strokes]
        tot = sum(L); t = t0
        for p, l in zip(strokes, L):
            d = dur * l / tot; self.s(t, d, p, col, w); t += d
        return t

    def txt(self, t0, dur, s, x, y, size, col=INK, font="Caveat", align="center", rot=0.0):
        L=len(s)*size*0.6+40
        self.items.append([t0, dur, "t", (s, x, y, size, col, font, align, rot), 1e9, (x-L, y-size*1.5, x+L, y+size)])
        return t0 + dur

    def mark(self): return len(self.items)

    def clear(self, i0, i1, t):
        for it in self.items[i0:i1]: it[4] = min(it[4], t)

    def key(self, t, cx, cy, z=1.0): self.cam.append((t, cx, cy, z))

    def snd(self, f, t, v=0.7): self.sfx.append((f, t, v))

    def camera(self, t):
        k = sorted(self.cam)
        if t <= k[0][0]: return k[0][1:]
        for a, b in zip(k, k[1:]):
            if a[0] <= t <= b[0]:
                u = ease(prog(t, a[0], b[0]))
                z = math.exp(math.log(a[3]) + (math.log(b[3]) - math.log(a[3])) * u)
                return (a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, z)
        return k[-1][1:]

def plen(p): return sum(math.dist(a, b) for a, b in zip(p, p[1:]))

def draw_partial(ctx, pts, f):
    tot = plen(pts); target = tot * f; acc = 0
    ctx.move_to(*pts[0]); tip = pts[0]
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        if acc + d >= target:
            r = (target - acc) / d if d else 0
            tip = (a[0] + (b[0] - a[0]) * r, a[1] + (b[1] - a[1]) * r); ctx.line_to(*tip); break
        ctx.line_to(*b); acc += d; tip = b
    ctx.stroke(); return tip

def board_bg(ctx):
    ctx.set_source_rgba(*hexc("#FBFAF6")); ctx.paint()
    g = cairo.RadialGradient(W / 2, H / 2, 350, W / 2, H / 2, 1300)
    g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, 0.72, 0.71, 0.66, 0.32)
    ctx.set_source(g); ctx.paint()

def pen(ctx, x, y, col):
    ctx.save(); ctx.translate(x, y); ctx.rotate(-0.55)
    ctx.set_source_rgba(0, 0, 0, 0.16); ctx.move_to(14, 10); ctx.rel_line_to(0, 260); ctx.set_line_width(40); ctx.stroke()
    ctx.set_source_rgba(*col); ctx.move_to(0, 0); ctx.line_to(-11, 38); ctx.line_to(11, 38); ctx.close_path(); ctx.fill()
    ctx.rectangle(-19, 38, 38, 230); ctx.set_source_rgba(*hexc("#2F2F35")); ctx.fill()
    ctx.rectangle(-19, 38, 38, 36); ctx.set_source_rgba(*hexc("#E8E6DF")); ctx.fill()
    ctx.rectangle(-19, 228, 38, 40); ctx.set_source_rgba(*col); ctx.fill()
    ctx.restore()

def render(board, path, duration, voice, voice_start=0.5, music=None):
    silent = path.replace(".mp4", "_v.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for i in range(int(duration * FPS)):
        t = i / FPS
        ctx = cairo.Context(surf)
        board_bg(ctx)
        cx, cy, z = board.camera(t)
        ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-cx, -cy)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        tip = None; tipcol = INK
        vx0, vx1 = cx - W / 2 / z - 50, cx + W / 2 / z + 50
        vy0, vy1 = cy - H / 2 / z - 50, cy + H / 2 / z + 50
        for t0, dur, kind, d, tend, bb in board.items:
            if t < t0 or t > tend + 0.35: continue
            if bb[2] < vx0 or bb[0] > vx1 or bb[3] < vy0 or bb[1] > vy1: continue
            fading = t > tend
            if fading: ctx.push_group()
            f = prog(t, t0, t0 + dur)
            if kind == "s":
                pts, col, w = d
                ctx.set_source_rgba(*col); ctx.set_line_width(w)
                tp = draw_partial(ctx, pts, f)
                if f < 1: tip, tipcol = tp, col
            else:
                s, x, y, size, col, font, align, rot = d
                ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
                ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
                e = ctx.text_extents(s)
                x0 = -e.width / 2 - e.x_bearing if align == "center" else (-e.width - e.x_bearing if align == "right" else 0)
                ctx.save(); ctx.rectangle(x0 + e.x_bearing - 0.12 * size, -size * 1.3, (e.width + 0.24 * size) * f, size * 1.9); ctx.clip()  # Fix 24.11.2026: Clip begann bei x0 statt x0+x_bearing -> letzter Buchstabe rechts abgeschnitten
                ctx.move_to(x0, 0); ctx.set_source_rgba(*col); ctx.show_text(s); ctx.restore()
                ctx.restore()
                if f < 1:
                    tip, tipcol = (x + math.cos(rot) * (x0 + e.width * f), y + math.sin(rot) * (x0 + e.width * f) - size * 0.3), col
            if fading:
                ctx.pop_group_to_source(); ctx.paint_with_alpha(1 - prog(t, tend, tend + 0.35))
        for fn in board.dyn: fn(ctx, t)
        if tip: pen(ctx, tip[0], tip[1], tipcol)
        ctx.restore()
        for fn in board.overlay: fn(ctx, t)
        surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close(); p.wait()
    inputs = ["-i", silent, "-i", voice]
    vs = int(voice_start * 1000)
    filt = [f"[1:a]aformat=channel_layouts=stereo,adelay={vs}|{vs}[vo]"]; labels = ["[vo]"]
    k = 2
    if music:
        mf, mvol = music
        inputs += ["-i", mf]; filt.append(f"[{k}:a]aformat=channel_layouts=stereo,volume={mvol}[mu]"); labels.append("[mu]"); k += 1
    for f, t, v in board.sfx:
        inputs += ["-i", os.path.join(SFX, f)]
        ms = int(t * 1000)
        filt.append(f"[{k}:a]aformat=channel_layouts=stereo,adelay={ms}|{ms},volume={v}[s{k}]"); labels.append(f"[s{k}]"); k += 1
    filt.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,atrim=0:{duration},alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(duration), path], check=True)
    os.remove(silent)

# ---------- reusable figures ----------
def stick(b, t0, x, y, s=1.0, dur=1.0, pose="stand", face="neutral", col=INK, hero=False, w=9):
    """stick figure standing on y (feet). hero=True adds Denkmuster spiral curl + yellow scarf."""
    hy = y - 235 * s; R = 40 * s
    parts = [circle(x, hy, R)]
    if pose == "sit":
        parts += [line(x, hy + R, x, y - 110 * s),
                  poly((x - 55 * s, y - 150 * s), (x, y - 185 * s), (x + 55 * s, y - 150 * s)),
                  poly((x, y - 110 * s), (x + 75 * s, y - 110 * s), (x + 75 * s, y - 20 * s)),
                  poly((x, y - 110 * s), (x + 65 * s, y - 100 * s), (x + 60 * s, y - 20 * s))]
    elif pose == "walk":
        parts += [line(x, hy + R, x, y - 95 * s),
                  poly((x - 45 * s, y - 120 * s), (x, y - 170 * s), (x + 50 * s, y - 135 * s)),
                  line(x, y - 95 * s, x - 45 * s, y), line(x, y - 95 * s, x + 50 * s, y)]
    elif pose == "arms_up":
        parts += [line(x, hy + R, x, y - 95 * s),
                  poly((x - 60 * s, y - 230 * s), (x, y - 165 * s), (x + 60 * s, y - 230 * s)),
                  line(x, y - 95 * s, x - 40 * s, y), line(x, y - 95 * s, x + 40 * s, y)]
    else:
        parts += [line(x, hy + R, x, y - 95 * s),
                  poly((x - 55 * s, y - 120 * s), (x, y - 170 * s), (x + 55 * s, y - 120 * s)),
                  line(x, y - 95 * s, x - 40 * s, y), line(x, y - 95 * s, x + 40 * s, y)]
    # face
    ex = 13 * s
    parts += [circle(x - ex, hy - 5 * s, 3 * s, n=8), circle(x + ex, hy - 5 * s, 3 * s, n=8)]
    if face == "happy": parts.append(arc(x, hy + 8 * s, 16 * s, 0.2, 2.9, n=14))
    elif face == "sad": parts.append(arc(x, hy + 26 * s, 14 * s, 3.5, 5.9, n=14))
    elif face == "worried": parts.append(poly((x - 14 * s, hy + 18 * s), (x - 5 * s, hy + 13 * s), (x + 5 * s, hy + 19 * s), (x + 14 * s, hy + 14 * s), n=3))
    else: parts.append(line(x - 12 * s, hy + 16 * s, x + 12 * s, hy + 16 * s, n=4))
    t = b.many(t0, dur * (0.8 if hero else 1.0), parts, col, w)
    if hero:
        t = b.s(t, dur * 0.1, spiral(x + 6 * s, hy - R - 12 * s, 16 * s, turns=1.6), BLUE, max(5, w - 2))
        b.s(t, dur * 0.1, poly((x - 22 * s, hy + R + 6 * s), (x + 22 * s, hy + R + 6 * s), (x + 30 * s, hy + R + 40 * s), n=6), ORANGE, w + 3)
    return t0 + dur
