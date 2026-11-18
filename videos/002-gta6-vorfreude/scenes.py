"""Denkmuster 002 – GTA 6 & die Psychologie der Vorfreude. Szenen mit engine/kit.py (ein Satz = ein Bild, Wortzeiten aus vo/k*.json)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "engine"))
from kit import *
import random
_r = random.Random(11)

TITLES = [None, "Vorfreude ist echte Freude", "Der Kuss vom Filmstar", "Das Molekül des Wollens", "Warum Gerüchte fesseln",
          "Erlebnisse schlagen Dinge", "Hype ist ansteckend", "Die Enttäuschungsfalle", "Mehr aus Vorfreude holen", None]
v = Video(__file__, titles=TITLES, music_plan=[1, 2, 2, 3, 3, 4, 2, 4, 2, 5])
b = v.b
A = v.at
def pop(t, vol=0.4): b.snd("pop.wav", t, vol)
def popk(t, vol=0.4): b.snd("pop_klein.wav", t, vol)
def aha(t, vol=0.35): b.snd("aha_funkeln.wav", t, vol)
def pan(k, p, t, z=1.0):
    v.gop(t - 0.4, k, p, z); return v.P(k, p)
def fig(t, x, y, s=1.0, **kw): return v.fig(t, x, y, s, **kw)

# ---------------- eigene Icons ----------------
def dtext(ctx, s, x, y, size, col, font="Caveat"):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); ctx.move_to(x - e.width / 2 - e.x_bearing, y); ctx.set_source_rgba(*col); ctx.show_text(s)

def fmt_de(n): return f"{int(n):,}".replace(",", ".")

def counter(x, y, t0, t1, v0, v1, size=120, col=BLUE, pre="", post="", hide=1e9):
    def fn(ctx, t):
        if t < t0 or t > hide: return
        val = v0 + (v1 - v0) * ease_out(prog(t, t0, t1))
        dtext(ctx, pre + fmt_de(val) + post, x, y, size, col)
    b.dyn.append(fn)
    b.snd("pop_klein.wav", t1, 0.35)

def bars(X, Y, items, h=480, bw=150, gap=60, axis_t=None, lab=48):
    """items: (keys[(t,val)], col, label). keys: Wert 0..1 ab Zeit t (animiert)."""
    n = len(items); W_ = n * bw + (n - 1) * gap; x0 = X - W_ / 2
    t_ax = axis_t if axis_t is not None else min(k[0][0] for k, _, _ in items) - 0.5
    b.many(t_ax, 0.4, [poly((x0 - 40, Y - h - 40), (x0 - 40, Y), (x0 + W_ + 40, Y))], INK, 8)
    for i, (keys, col, lb) in enumerate(items):
        x = x0 + i * (bw + gap)
        if lb: label(b, keys[0][0], lb, x + bw / 2, Y + 70, lab, col)
        def fn(ctx, t, keys=keys, col=col, x=x):
            if t < keys[0][0]: return
            val = 0.0; prev_t, prev_v = keys[0][0], 0.0
            for (tk, vk) in keys:
                if t >= tk: val_target = vk; prev = (tk, vk)
            # Interpolation zwischen den Stufen
            cur = 0.0; last_v = 0.0
            for (tk, vk) in keys:
                if t < tk: break
                f = ease_out(prog(t, tk, tk + 1.0)); cur = last_v + (vk - last_v) * f; last_v = vk
            hh = h * cur
            ctx.save(); ctx.rectangle(x, Y - hh, bw, hh); ctx.clip(); ctx.set_source_rgba(*col); ctx.set_line_width(6)
            for kk in range(-30, 40): ctx.move_to(x + kk * 18, Y); ctx.line_to(x + kk * 18 + 60, Y - 700)
            ctx.stroke(); ctx.restore(); ctx.set_source_rgba(*col); ctx.set_line_width(7); ctx.rectangle(x, Y - hh, bw, hh); ctx.stroke()
        b.dyn.append(fn)
    return x0, W_

def screen(t, x, y, w=420, h=250, col=INK, play=True):
    b.many(t, 0.5, [rect(x - w / 2, y - h / 2, w, h), line(x - 60, y + h / 2 + 50, x + 60, y + h / 2 + 50, n=4), line(x, y + h / 2, x, y + h / 2 + 50, n=3)], col, 8)
    if play: b.s(t + 0.5, 0.25, poly((x - 30, y - 45), (x + 45, y), (x - 30, y + 45), closed=True, n=4), RED, 9)

def controller(t, x, y, s=1.0, col=INK):
    P_ = lambda a, c: (x + a * s, y + c * s)
    body = bez(P_(-150, -40), P_(-60, -90), P_(60, -90), P_(150, -40)) + bez(P_(150, -40), P_(220, 90), P_(130, 130), P_(70, 40))[1:] + \
        poly(P_(70, 40), P_(-70, 40), n=6)[1:] + bez(P_(-70, 40), P_(-130, 130), P_(-220, 90), P_(-150, -40))[1:]
    b.s(t, 0.5, body, col, 8)
    b.many(t + 0.5, 0.3, [line(x - 105 * s, y - 20 * s, x - 55 * s, y - 20 * s, n=3), line(x - 80 * s, y - 45 * s, x - 80 * s, y + 5 * s, n=3),
                          circle(x + 70 * s, y - 35 * s, 10 * s, n=10), circle(x + 100 * s, y - 10 * s, 10 * s, n=10)], col, 7)

def hourglass(t, x, y, s=1.0, col=INK, sand_t=None, sand_d=8.0):
    b.many(t, 0.5, [line(x - 90 * s, y - 160 * s, x + 90 * s, y - 160 * s, n=4), line(x - 90 * s, y + 160 * s, x + 90 * s, y + 160 * s, n=4),
                    poly((x - 70 * s, y - 160 * s), (x - 10 * s, y), (x - 70 * s, y + 160 * s)), poly((x + 70 * s, y - 160 * s), (x + 10 * s, y), (x + 70 * s, y + 160 * s))], col, 8)
    st = sand_t if sand_t is not None else t + 0.5
    def fn(ctx, tt):
        if tt < st: return
        f = prog(tt, st, st + sand_d)
        ctx.set_source_rgba(*ORANGE)
        top = 1 - f; ctx.move_to(x - 60 * s * top, y - 140 * s * top + 0 * s); ctx.line_to(x + 60 * s * top, y - 140 * s * top); ctx.line_to(x, y - 8 * s); ctx.close_path(); ctx.fill()
        hb = 130 * s * math.sqrt(f); ctx.move_to(x - 62 * s, y + 152 * s); ctx.line_to(x + 62 * s, y + 152 * s); ctx.line_to(x + 62 * s * (1 - hb / (150 * s)) , y + 152 * s - hb); ctx.line_to(x - 62 * s * (1 - hb / (150 * s)), y + 152 * s - hb); ctx.close_path(); ctx.fill()
        if f < 1: ctx.set_line_width(4); ctx.move_to(x, y); ctx.line_to(x, y + 150 * s - hb); ctx.set_source_rgba(*ORANGE); ctx.stroke()
    b.dyn.append(fn)

def calendar(t, x, y, top, big, col=RED, s=1.0):
    w, h = 260 * s, 280 * s
    b.many(t, 0.5, [rect(x - w / 2, y - h / 2, w, h), line(x - w / 2, y - h / 2 + 70 * s, x + w / 2, y - h / 2 + 70 * s, n=6),
                    line(x - 60 * s, y - h / 2 - 25 * s, x - 60 * s, y - h / 2 + 25 * s, n=2), line(x + 60 * s, y - h / 2 - 25 * s, x + 60 * s, y - h / 2 + 25 * s, n=2)], INK, 8)
    b.txt(t + 0.4, 0.3, top, x, y - h / 2 + 52 * s, 46 * s, col)
    b.txt(t + 0.6, 0.4, big, x, y + 85 * s, 130 * s, INK)

def star(t, x, y, r=60, col=ORANGE, w=8):
    pts = [(x + (r if i % 2 == 0 else r * 0.45) * math.cos(-math.pi / 2 + i * math.pi / 5), y + (r if i % 2 == 0 else r * 0.45) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(11)]
    b.s(t, 0.35, wob(pts, 0.6), col, w)

def suitcase(t, x, y, col=BLUE):
    b.many(t, 0.5, [rect(x - 110, y - 70, 220, 150), poly((x - 40, y - 70), (x - 40, y - 110), (x + 40, y - 110), (x + 40, y - 70)),
                    line(x - 60, y - 70, x - 60, y + 80, n=5), line(x + 60, y - 70, x + 60, y + 80, n=5)], col, 8)

def sun(t, x, y, r=50):
    b.s(t, 0.3, circle(x, y, r), ORANGE, 8)
    for k in range(8):
        a = k * math.pi / 4
        b.s(t + 0.3 + k * 0.03, 0.05, line(x + math.cos(a) * (r + 15), y + math.sin(a) * (r + 15), x + math.cos(a) * (r + 45), y + math.sin(a) * (r + 45), n=2), ORANGE, 6)

def bolt(t, x, y, s=1.0, col=YEL):
    b.s(t, 0.25, poly((x + 20 * s, y - 120 * s), (x - 40 * s, y + 10 * s), (x + 10 * s, y + 10 * s), (x - 20 * s, y + 120 * s), (x + 50 * s, y - 20 * s), (x, y - 20 * s), (x + 20 * s, y - 120 * s), n=3), col, 9)

def phone(t, x, y, s=1.0, col=INK):
    b.many(t, 0.4, [rect(x - 80 * s, y - 150 * s, 160 * s, 300 * s), line(x - 20 * s, y + 125 * s, x + 20 * s, y + 125 * s, n=2)], col, 8)

def glass(t, x, y, col=ORANGE):
    b.many(t, 0.4, [poly((x - 60, y - 90), (x - 45, y + 90), (x + 45, y + 90), (x + 60, y - 90)), line(x - 50, y - 30, x + 50, y - 30, n=4), line(x + 20, y - 90, x + 50, y - 160, n=3)], col, 8)

def mountain(t, x, y):
    b.many(t, 0.6, [poly((x - 260, y + 120), (x - 80, y - 150), (x + 20, y - 20), (x + 110, y - 110), (x + 260, y + 120)), poly((x - 135, y - 70), (x - 80, y - 150), (x - 30, y - 75))], INK, 8)

def newspaper(t, x, y):
    b.many(t, 0.6, [rect(x - 170, y - 210, 340, 420), line(x - 130, y - 150, x + 130, y - 150, n=5)] + [line(x - 130, y - 80 + i * 50, x + (130 if i % 3 else 40), y - 80 + i * 50, n=5) for i in range(6)], INK, 7)
    b.txt(t + 0.3, 0.3, "NEWS", x, y - 165, 56, RED)

def bike(t, x, y, col=INK):
    b.many(t, 0.7, [circle(x - 110, y, 70), circle(x + 110, y, 70), poly((x - 110, y), (x - 20, y - 110), (x + 70, y - 110), (x + 110, y)), poly((x - 20, y - 110), (x, y), (x + 70, y - 110)), line(x - 40, y - 140, x, y - 140, n=2)], col, 7)

def plane(t, x, y, col=BLUE):
    b.many(t, 0.5, [poly((x - 150, y), (x + 150, y), (x + 170, y - 15), (x + 150, y - 30), (x - 120, y - 30), (x - 150, y - 80), (x - 170, y - 80), (x - 150, y)),
                    poly((x - 20, y - 15), (x + 40, y + 80), (x + 70, y + 80), (x + 50, y - 15))], col, 7)

def trophy(t, x, y, col=ORANGE):
    b.many(t, 0.6, [poly((x - 80, y - 120), (x + 80, y - 120), (x + 60, y), (x - 60, y), closed=True), arc(x - 85, y - 80, 40, math.pi * 0.5, math.pi * 1.5),
                    arc(x + 85, y - 80, 40, -math.pi * 0.5, math.pi * 0.5), line(x, y, x, y + 60, n=3), line(x - 60, y + 60, x + 60, y + 60, n=4)], col, 8)

def dice(t, x, y, col=INK):
    b.s(t, 0.35, rect(x - 70, y - 70, 140, 140), col, 8)
    for i, (dx, dy) in enumerate(((-35, -35), (0, 0), (35, 35))): b.s(t + 0.35 + i * 0.05, 0.05, circle(x + dx, y + dy, 9, n=8), col, 8)

def slot(t, x, y):
    b.many(t, 0.6, [rect(x - 200, y - 150, 400, 300)] + [rect(x - 170 + i * 120, y - 80, 100, 130) for i in range(3)] + [line(x + 200, y - 60, x + 250, y - 140, n=3), circle(x + 255, y - 155, 18, n=10)], INK, 7)
    for i in range(3): b.txt(t + 0.6 + i * 0.15, 0.15, "?", x - 120 + i * 120, y + 30, 90, RED)

def glasses(t, x, y, col=RED):
    b.many(t, 0.5, [circle(x - 90, y, 70), circle(x + 90, y, 70), arc(x, y + 5, 25, math.pi * 1.15, math.pi * 1.85), line(x - 160, y - 10, x - 230, y - 30, n=3), line(x + 160, y - 10, x + 230, y - 30, n=3)], col, 9)

def crowd(t, X, Y, rows, cols, s=0.55, dx=200, dy=330, hero_i=None):
    i = 0
    for r in range(rows):
        for c in range(cols):
            fig(t + i * 0.06, X - (cols - 1) * dx / 2 + c * dx, Y + r * dy, s, dur=0.3, face="happy", hero=(i == hero_i), w=6); i += 1

def neuron(t, x0, y0, w, events, dur=1.2, col=INK):
    """Aktivitätsspur: events=[(pos 0..1, +1 Spitze / -1 Delle)]."""
    pts = []
    for i in range(201):
        u = i / 200; yy = 0.0
        for pos, sg in events:
            d = (u - pos) / 0.012
            yy += (-150 if sg > 0 else 45) * math.exp(-d * d) if sg > 0 else 0
            if sg < 0: yy += 55 * math.exp(-((u - pos) / 0.04) ** 2)
        pts.append((x0 + w * u, y0 + yy + _r.uniform(-4, 4)))
    b.s(t, dur, pts, col, 6)

# ===================== K0 Hook =====================
k = 0
X, Y = v.P(0, 0)
t = A(k, "Am neunzehnten"); calendar(t, X - 450, Y - 20, "November", "19", RED, 1.3); pop(t + 0.6)
label(b, A(k, "zweitausendsechsundzwanzig"), "2026", X - 450, Y + 300, 90, INK)
t = A(k, "GTA sechs erscheint"); b.txt(t, 0.7, "GTA 6", X + 380, Y - 40, 230, BLUE); pop(t + 0.5, 0.5)
b.s(t + 0.8, 0.35, line(X + 120, Y + 30, X + 650, Y + 40), ORANGE, 10)
t = A(k, "Millionen Menschen"); X, Y = pan(k, 1, t)
crowd(t, X, Y - 120, 2, 8, 0.55, 210, 360, hero_i=11)
label(b, t + 0.8, "Millionen warten", X, Y - 380, 100, RED)
t = A(k, "Fast drei Jahre"); X, Y = pan(k, 2, t)
b.s(t, 0.8, line(X - 800, Y, X + 800, Y, n=30), INK, 9)
for i, (px, top, col) in enumerate(((-650, "Dez. 2023", BLUE), (-220, "2025", GREY), (220, "Mai 2026", GREY), (650, "19.11.2026", GREEN))):
    b.s(t + 0.3 + i * 0.15, 0.15, line(X + px, Y - 30, X + px, Y + 30, n=2), INK, 9)
    b.txt(t + 0.4 + i * 0.15, 0.35, top, X + px, Y + 110, 60, col)
label(b, t + 0.6, "1. Trailer", X - 650, Y - 70, 56, BLUE)
t = A(k, "Zwei Verschiebungen"); cross(b, t, X - 220, Y - 90, 0.9); cross(b, t + 0.4, X + 220, Y - 90, 0.9); pop(t); pop(t + 0.4)
t = A(k, "Unzählige Gerüchte")
for i, (bx, by, s_) in enumerate(((-500, -330, "Leak?"), (0, -360, "bald?"), (500, -330, "verschoben?"), (-250, 320, "Trailer 3?"), (300, 330, "Gerücht!"))):
    bubble(b, t + i * 0.2, X + bx, Y + by, 290, 120, s_, 50, RED if i % 2 else INK);
popk(t); popk(t + 0.4); popk(t + 0.8)
t = A(k, "Und jetzt eine Frage"); X, Y = pan(k, 3, t)
fig(t, X - 500, Y + 420, 1.3, hero=True, face="neutral"); b.txt(t + 0.6, 0.4, "?", X - 330, Y - 160, 200, BLUE)
t = A(k, "schönste Teil"); heart(b, t, X + 350, Y - 250, 4.0); label(b, t + 0.3, "der schönste Teil", X + 350, Y - 20, 80, RED)
t = A(k, "Nicht das Spielen"); controller(t, X + 100, Y + 240, 0.9); cross(b, t + 0.6, X + 100, Y + 240, 1.6)
t = A(k, "Sondern das Warten"); hourglass(t, X + 620, Y + 220, 0.9); check(b, t + 0.6, X + 760, Y + 60, 1.3); pop(t + 0.6)
t = A(k, "Forscher in den Niederlanden"); X, Y = pan(k, 4, t)
label(b, t, "Niederlande", X - 450, Y - 380, 90, ORANGE)
t = A(k, "über fünfzehnhundert"); counter(X - 450, Y - 180, t, t + 1.4, 0, 1500, 130, BLUE, pre="über "); label(b, t + 0.8, "Erwachsene", X - 450, Y - 70, 64, INK)
t = A(k, "fuhr in den Urlaub"); suitcase(t, X - 520, Y + 220); sun(t + 0.4, X - 330, Y + 120)
t = A(k, "Vor der Reise", 0)
t2 = A(k, "Nach der Reise")
bars(X + 380, Y + 330, [([(t, 0.85), (t2, 0.55)], ORANGE, "Urlauber"), ([(t + 0.6, 0.55)], GREY, "Daheim")], h=560, bw=170, gap=90)
label(b, t + 0.2, "vorher", X + 380, Y - 380, 80, ORANGE)
_m = b.mark(); b.txt(t2, 0.4, "nachher: gleich", X + 380, Y - 300, 64, INK); popk(t2 + 0.8)
t = A(k, "Der Glücksschub"); X, Y = pan(k, 5, t)
b.s(t, 0.6, bez((X - 700, Y + 300), (X - 300, Y + 280), (X - 150, Y - 250), (X + 50, Y - 260)), ORANGE, 12)
b.s(t + 0.6, 0.6, bez((X + 50, Y - 260), (X + 250, Y - 260), (X + 350, Y + 280), (X + 700, Y + 300)), GREY, 9)
label(b, t + 0.3, "vorher", X - 300, Y + 380, 70, ORANGE); label(b, t + 0.9, "nachher", X + 400, Y + 380, 70, GREY)
t = A(k, "Vermutlich aus der Vorfreude"); b.txt(t, 0.7, "Vorfreude?", X, Y - 360, 130, RED); aha(t + 0.4)
t = A(k, "In diesem Video"); X, Y = pan(k, 6, t)
head_profile(b, t, X - 550, Y + 40, 260, INK, 10, 0.9); brain(b, t + 0.9, X - 560, Y - 40, 0.8, RED, 0.6)
t = A(k, "schon bei einem Trailer"); screen(t, X + 50, Y - 230, 340, 200); bolt(t + 0.7, X + 300, Y - 260, 0.7); b.snd("stromschlag.wav", t + 0.7, 0.25)
t = A(k, "Warum Gerüchte"); bubble(b, t, X + 620, Y - 250, 320, 140, "Gerüchte", 60, BLUE, tail=(-1, 1))
t = A(k, "Falle sein"); b.many(t - 0.4, 0.6, [poly((X - 50, Y + 380), (X + 650, Y + 380)), poly((X + 100, Y + 380), (X + 300, Y + 150), (X + 500, Y + 380))], INK, 8)
label(b, t, "Hype-Falle", X + 300, Y + 110, 70, RED); pop(t)
t = A(k, "Kein Spieletest"); X, Y = pan(k, 7, t)
controller(t, X - 550, Y - 80, 0.8); cross(b, t + 0.5, X - 550, Y - 80, 1.3); label(b, t + 0.4, "kein Spieletest", X - 550, Y + 160, 64, RED)
t = A(k, "Keine Bilder"); screen(t, X, Y - 90, 300, 190, play=False); cross(b, t + 0.5, X, Y - 90, 1.2); label(b, t + 0.4, "keine Spielbilder", X, Y + 160, 64, RED)
t = A(k, "Nur Psychologie"); brain(b, t, X + 560, Y - 90, 0.9, BLUE, 0.6); check(b, t + 0.6, X + 680, Y - 200, 1.2); label(b, t + 0.4, "nur Psychologie", X + 560, Y + 160, 70, GREEN); aha(t + 0.6)

# ===================== K1 Vorfreude ist echte Freude =====================
k = 1
t = A(k, "Schauen wir"); X, Y = pan(k, 0, t)
book(b, t, X - 550, Y, "Studie"); label(b, t + 0.6, "Nawijn u. a., 2010", X - 550, Y + 290, 64, INK)
t = A(k, "fünfzehnhundertdreißig"); counter(X + 300, Y - 180, t, t + 1.5, 0, 1530, 150, BLUE); label(b, t + 0.6, "Niederländer", X + 300, Y - 60, 70, INK)
t = A(k, "Neunhundertvierundsiebzig"); suitcase(t, X + 100, Y + 260, ORANGE); counter(X + 450, Y + 300, t, t + 1.2, 0, 974, 110, ORANGE)
label(b, t + 0.8, "im Urlaub", X + 450, Y + 400, 56, ORANGE)
t = A(k, "Vor der Reise"); X, Y = pan(k, 1, t)
t2 = A(k, "Nach der Rückkehr")
bars(X - 380, Y + 330, [([(t, 0.85), (t2, 0.56)], ORANGE, "Urlauber"), ([(t + 0.5, 0.55)], GREY, "andere")], h=560, bw=170, gap=90)
label(b, t, "vor der Reise", X - 380, Y - 380, 74, ORANGE)
t = A(k, "Die Forscher vermuten"); bubble(b, t, X + 450, Y - 230, 420, 160, "Vorfreude?", 70, RED, tail=(-1, 1)); fig(t + 0.3, X + 450, Y + 330, 1.0, face="happy")
label(b, t2 + 0.3, "nachher: meist gleich", X - 380, Y - 300, 56, INK)
t = A(k, "sehr entspannten"); X, Y = pan(k, 2, t)
couch(b, t, X - 450, Y + 250); fig(t + 0.4, X - 490, Y + 230, 1.0, pose="sit", face="happy", hero=True); label(b, t + 0.4, "sehr entspannt", X - 450, Y - 220, 80, GREEN)
t = A(k, "acht Wochen")
for i in range(8):
    x_ = X + 120 + (i % 4) * 160; y_ = Y - 120 + (i // 4) * 170
    b.s(t + i * 0.08, 0.1, rect(x_, y_, 130, 130), INK, 6)
    def fill(ctx, tt, x_=x_, y_=y_, i=i, t0=t):
        if tt < t0 + 0.8: return
        a = 1 - prog(tt, t0 + 0.8 + i * 0.25, t0 + 1.2 + i * 0.25)
        ctx.set_source_rgba(*GREEN[:3], 0.65 * a); ctx.rectangle(x_ + 10, y_ + 10, 110, 110); ctx.fill()
    b.dyn.append(fill)
label(b, t + 0.5, "nach 8 Wochen vorbei", X + 360, Y - 260, 70, RED)
t = A(k, "Eine zweite Studie"); X, Y = pan(k, 3, t)
label(b, t, "Van Boven & Ashworth, 2007", X, Y - 400, 74, INK)
head_profile(b, t + 0.3, X, Y + 20, 220, INK, 10, 0.8)
t = A(k, "das bald kommt"); b.s(t, 0.5, line(X + 250, Y, X + 750, Y, n=10), BLUE, 10); b.s(t + 0.5, 0.2, poly((X + 700, Y - 40), (X + 750, Y), (X + 700, Y + 40)), BLUE, 10)
label(b, t + 0.3, "bald", X + 500, Y - 50, 80, BLUE)
t = A(k, "schon vorbei"); b.s(t, 0.5, line(X - 250, Y, X - 750, Y, n=10), GREY, 10); b.s(t + 0.5, 0.2, poly((X - 700, Y - 40), (X - 750, Y), (X - 700, Y + 40)), GREY, 10)
label(b, t + 0.3, "vorbei", X - 500, Y - 50, 80, GREY)
t = A(k, "ausgedachten Skiurlaub"); mountain(t, X + 500, Y + 300); label(b, t + 0.5, "Skiurlaub (ausgedacht)", X + 500, Y + 480, 52, BLUE)
t = A(k, "Das Ergebnis"); X, Y = pan(k, 4, t)
t2 = A(k, "stärkere Gefühle")
wave(b, t2, X + 420, Y - 80, 600, 110, 3, RED, 0.9); wave(b, t2 + 0.7, X - 420, Y - 80, 600, 30, 3, GREY, 0.9)
label(b, t, "Zukunft", X + 420, Y - 320, 90, RED); label(b, t + 0.3, "Vergangenheit", X - 420, Y - 320, 80, GREY); pop(t2)
t = A(k, "Der Grund"); label(b, t, "mehr Nachdenken", X, Y + 180, 80, INK)
t = A(k, "Wir spielen sie"); head_profile(b, t, X, Y + 380, 130, INK, 8, 0.5)
b.s(t + 0.5, 0.5, arc(X + 10, Y + 330, 70, 0, math.pi * 1.7), BLUE, 7); b.s(t + 1.0, 0.15, poly((X + 50, Y + 255), (X + 70, Y + 280), (X + 40, Y + 300)), BLUE, 7)
label(b, t + 0.8, "Kopfkino", X + 300, Y + 400, 70, BLUE); aha(t + 0.8)
t = A(k, "Genau das passiert"); X, Y = pan(k, 5, t)
fig(t, X - 600, Y + 430, 1.2, hero=True, face="happy")
t = A(k, "Jeder Trailer"); screen(t, X - 50, Y - 200, 360, 210)
t = A(k, "jedes Gerücht"); bubble(b, t, X + 550, Y - 250, 330, 140, "Gerücht", 60, RED, tail=(-1, 1))
t = A(k, "jede Diskussion"); bubble(b, t, X + 400, Y + 120, 360, 140, "Diskussion", 56, BLUE, tail=(-1, 1))
t = A(k, "neuer Durchlauf"); counter(X, Y + 320, t, t + 2.0, 1, 999, 90, ORANGE, pre="Durchlauf Nr. ")

# ===================== K2 Der Kuss vom Filmstar =====================
k = 2
t = A(k, "Neunzehnhundertsiebenundachtzig"); X, Y = pan(k, 0, t)
label(b, t, "1987", X - 500, Y - 300, 140, GREY)
t = A(k, "George Loewenstein"); book(b, t, X - 500, Y + 120, "Studie", BLUE)
t = A(k, "dreißig Studierenden")
for i in range(6): fig(t + i * 0.1, X + 50 + i * 150, Y + 380, 0.6, dur=0.35, face="neutral", w=6)
label(b, t + 0.5, "30 Studierende", X + 420, Y - 30, 80, INK)
t = A(k, "ungewöhnliche Frage"); b.txt(t, 0.4, "?", X + 420, Y - 200, 200, RED); pop(t + 0.3)
t = A(k, "Stell dir vor"); X, Y = pan(k, 1, t)
fig(t, X - 500, Y + 430, 1.3, hero=True, face="happy")
t = A(k, "Kuss von einem"); star(t, X + 150, Y - 180, 140, ORANGE, 10); heart(b, t + 0.4, X + 150, Y - 160, 2.4); label(b, t + 0.5, "Kuss vom Filmstar", X + 150, Y + 60, 84, RED); aha(t + 0.4)
t = A(k, "Wie viel"); coin(b, t, X + 600, Y + 260); coin(b, t + 0.2, X + 720, Y + 300); label(b, t + 0.3, "wie viel wert?", X + 400, Y + 420, 64, ORANGE)
# Zeitleiste
t = A(k, "Sofort?"); X, Y = pan(k, 2, t)
b.s(t - 0.3, 0.6, line(X - 800, Y + 100, X + 800, Y + 100, n=30), INK, 9)
for i, (w_, ph) in enumerate((("sofort", "Sofort?"), ("3 Std.", "drei Stunden"), ("morgen", "Morgen?"), ("3 Tage", "In drei Tagen"), ("1 Jahr", "In einem Jahr"))):
    tt = A(k, ph); px = X - 700 + i * 350
    b.s(tt, 0.12, line(px, Y + 70, px, Y + 130, n=2), INK, 9); label(b, tt, w_, px, Y + 220, 70, BLUE); popk(tt)
heart(b, A(k, "In drei Tagen"), X + 350, Y - 50, 2.4)
t = A(k, "Normalerweise gilt"); X, Y = pan(k, 3, t)
t2 = A(k, "Geld heute")
for i in range(5): coin(b, t2 + i * 0.1, X - 400, Y + 250 - i * 70)
for i in range(3): coin(b, t2 + 0.6 + i * 0.1, X + 400, Y + 250 - i * 70)
label(b, t2, "heute", X - 400, Y + 400, 80, GREEN); label(b, t2 + 0.6, "morgen", X + 400, Y + 400, 80, GREY)
label(b, t, "sofort = mehr wert", X, Y - 350, 90, INK)
# Kuss-Diagramm (Loewenstein 1987, Tabelle: relativer Wert)
t = A(k, "Aber beim Kuss"); X, Y = pan(k, 4, t)
t3 = A(k, "erst in drei Tagen")
vals = [(1.00, "sofort"), (1.30, "3 Std."), (1.59, "1 Tag"), (1.78, "3 Tage"), (1.31, "1 Jahr"), (0.64, "10 Jahre")]
tz = A(k, "In zehn Jahren")
items = []
for i, (val, lb) in enumerate(vals):
    tt = (t + 0.3 + i * 0.35) if i < 4 else (t3 + 1.5 if i == 4 else tz)
    items.append(([(tt, val / 1.9)], RED if i == 3 else (GREY if i == 5 else BLUE), lb))
bars(X, Y + 330, items, h=600, bw=150, gap=70, lab=46)
label(b, t, "Wert des Kusses", X, Y - 400, 80, INK)
label(b, t3, "am meisten!", X + 120, Y - 300, 70, RED); pop(t3)
t = A(k, "Deutlich mehr"); star(t, X + 120, Y - 200, 40, ORANGE, 7)
t = A(k, "Warum? Drei Tage"); X, Y = pan(k, 5, t)
for i in range(3):
    calendar(t + i * 0.4, X - 500 + i * 500, Y - 80, "Tag", str(i + 1), BLUE, 0.9); heart(b, t + 1.4 + i * 0.4, X - 500 + i * 500, Y + 200, 1.2 + i * 0.8)
label(b, A(k, "drei Tage Vorfreude"), "3 Tage Vorfreude", X, Y - 380, 100, RED)
t = A(k, "ausmalen"); bubble(b, t, X + 620, Y + 330, 300, 120, "Kopfkino", 52, BLUE)
t = A(k, "Zu lange"); X, Y = pan(k, 4, t, 1.0)
b.s(A(k, "weniger wert"), 0.4, circle(X + 550, Y + 330 - 101, 120, ry=160), RED, 7)
t = A(k, "Kommt dir das"); X, Y = pan(k, 6, t)
label(b, t, "GTA 6: zweimal verschoben", X, Y - 380, 90, BLUE)
t = A(k, "Ein bisschen Warten"); hourglass(t, X - 450, Y + 100, 0.8, sand_d=3); check(b, t + 0.6, X - 450, Y + 330, 1.2); label(b, t + 0.5, "macht Lust", X - 450, Y - 180, 70, GREEN)
t = A(k, "Zu viel Warten"); hourglass(t, X + 450, Y + 100, 0.8, sand_d=1.5); zzz(b, t + 0.6, X + 580, Y - 50); label(b, t + 0.5, "macht müde", X + 450, Y - 180, 70, GREY)
t = A(k, "Bei etwas Unangenehmem"); X, Y = pan(k, 7, t)
fig(t, X - 600, Y + 430, 1.2, face="worried")
t = A(k, "nicht tödlichen Stromschlag"); bolt(t, X - 600, Y - 220, 1.2); b.snd("stromschlag.wav", t + 0.1, 0.35); label(b, t + 0.3, "Stromschlag", X - 600, Y - 420, 64, ORANGE)
t2 = A(k, "teurer vermeiden")
bars(X + 300, Y + 330, [([(A(k, "einen sofort", end=True) - 0.2, 1.0 / 1.9)], GREY, "sofort"), ([(t2, 1.84 / 1.9)], RED, "in 10 Jahren")], h=600, bw=180, gap=120)
label(b, t2 + 0.5, "vermeiden: teurer", X + 300, Y - 380, 70, RED)
t = A(k, "fürchtet sich"); label(b, t, "lange Angst", X - 330, Y - 40, 60, RED)
t = A(k, "Loewenstein zeigte"); X, Y = pan(k, 8, t)
t2 = A(k, "Wir genießen nicht")
label(b, t2, "Wir genießen nicht nur Dinge –", X, Y - 250, 90, INK)
t3 = A(k, "auch das Warten"); b.txt(t3, 0.8, "auch das Warten.", X, Y - 100, 130, RED); aha(t3 + 0.5)
hourglass(t3 + 0.4, X - 300, Y + 250, 0.7, sand_d=4); heart(b, t3 + 0.8, X + 300, Y + 250, 3.0)

# ===================== K3 Das Molekül des Wollens =====================
k = 3
t = A(k, "Was passiert dabei"); X, Y = pan(k, 0, t)
brain(b, t, X - 450, Y, 1.5, RED)
t = A(k, "Dopamin.", 0); molecule(b, t, X + 300, Y - 200, 2.5); label(b, t + 0.3, "Dopamin", X + 450, Y - 30, 110, BLUE); pop(t + 0.3)
t = A(k, "Glückshormon"); _g = b.mark(); label(b, t, "„Glückshormon“", X + 400, Y + 220, 80, ORANGE)
t = A(k, "so einfach"); cross(b, t, X + 400, Y + 200, 1.6); pop(t)
t = A(k, "Wolfram Schultz"); X, Y = pan(k, 1, t)
label(b, t, "Wolfram Schultz", X, Y - 400, 90, INK)
t = A(k, "Nervenzellen von Affen"); b.many(t, 0.7, [circle(X - 500, Y + 50, 90), circle(X - 610, Y + 10, 35), circle(X - 390, Y + 10, 35), circle(X - 500, Y + 90, 45, ry=30)], INK, 8)
b.many(t + 0.7, 0.2, [circle(X - 530, Y + 30, 5, n=6), circle(X - 470, Y + 30, 5, n=6)], INK, 8); label(b, t + 0.6, "Affe", X - 500, Y + 230, 60, GREY)
t = A(k, "Schluck Saft"); glass(t, X + 400, Y + 50); label(b, t + 0.4, "Saft", X + 400, Y + 220, 70, ORANGE)
t = A(k, "Zuerst feuerten"); X, Y = pan(k, 2, t)
label(b, t - 0.2, "1. vorher", X - 820, Y - 300, 56, INK)
neuron(t, X - 650, Y - 300, 1300, [(0.7, 1)], 1.4)
glass(t + 1.0, X + 430, Y - 420, ORANGE); b.snd("pop_klein.wav", t + 1.0, 0.4)
t = A(k, "Ein Lichtsignal"); bulb(b, t, X - 460, Y - 110, YEL); label(b, t + 0.4, "Licht kündigt an", X - 580, Y + 70, 50, ORANGE)
t = A(k, "Die Zellen feuerten schon"); label(b, t - 0.2, "2. gelernt", X - 820, Y + 160, 56, INK)
neuron(t, X - 650, Y + 160, 1300, [(0.27, 1)], 1.4); pop(t + 0.5)
label(b, A(k, "Nicht mehr beim Saft"), "beim Licht!", X - 300, Y + 260, 60, RED)
t = A(k, "ausblieb"); X, Y = pan(k, 3, t)
label(b, t - 0.3, "3. Saft bleibt aus", X - 650, Y - 300, 60, INK)
neuron(t, X - 650, Y - 100, 1300, [(0.27, 1), (0.7, -1)], 1.6)
bulb(b, t, X - 300, Y - 370, YEL); glass(t + 0.6, X + 260, Y - 330, GREY); cross(b, t + 1.0, X + 260, Y - 330, 1.0)
t = A(k, "unter den normalen"); b.s(t, 0.4, circle(X + 260, Y - 50, 110, ry=70), RED, 7); label(b, t + 0.3, "Enttäuschung", X + 260, Y + 120, 70, RED); pop(t)
t = A(k, "hätte kommen sollen"); clock(b, t - 0.6, X + 650, Y + 300, 80)
t = A(k, "Kent Berridge"); X, Y = pan(k, 4, t)
label(b, t, "Berridge & Robinson, 1998", X, Y - 400, 74, INK)
t = A(k, "Versuche mit Ratten")
b.many(t, 0.8, [circle(X - 450, Y + 50, 150, ry=80), poly((X - 300, Y + 30), (X - 220, Y + 60), (X - 300, Y + 90)), circle(X - 330, Y - 30, 30), bez((X - 600, Y + 60), (X - 720, Y + 40), (X - 720, Y + 160), (X - 820, Y + 120))], GREY, 8)
b.s(t + 0.8, 0.05, circle(X - 280, Y + 40, 5, n=6), INK, 8); label(b, t + 0.6, "Ratte", X - 450, Y + 210, 60, GREY)
t = A(k, "fast alles Dopamin"); molecule(b, t, X - 450, Y - 220, 1.5, GREY); cross(b, t + 0.3, X - 450, Y - 220, 0.8)
t = A(k, "mochten Zucker"); b.s(t, 0.3, rect(X + 150, Y - 60, 110, 110), INK, 8); label(b, t + 0.2, "Zucker", X + 205, Y + 120, 60, INK); heart(b, t + 0.5, X + 380, Y - 30, 2.0); label(b, t + 0.6, "mögen: ja", X + 600, Y - 20, 64, GREEN)
t = A(k, "strengten sich kaum"); cross(b, t, X + 380, Y + 230, 0.9); label(b, t + 0.2, "wollen: kaum", X + 600, Y + 240, 64, RED); pop(t)
t = A(k, "Ihre Erklärung"); X, Y = pan(k, 5, t)
t2 = A(k, "das Wollen"); b.txt(t2, 0.6, "WOLLEN", X - 350, Y - 50, 170, RED); pop(t2)
t3 = A(k, "das Genießen"); b.txt(t3, 0.5, "genießen", X + 450, Y - 30, 90, GREY)
label(b, t, "Dopamin steuert vor allem …", X, Y - 330, 80, BLUE)
t = A(k, "Vereinfacht gesagt"); X, Y = pan(k, 6, t)
t2 = A(k, "wie das Lichtsignal"); screen(t2, X - 550, Y - 60, 380, 220); b.txt(t2 + 0.7, 0.3, "=", X - 200, Y - 30, 160, INK); bulb(b, t2 + 0.9, X + 50, Y - 100, YEL)
t = A(k, "Da kommt etwas Gutes"); bubble(b, t, X + 550, Y - 250, 420, 150, "Da kommt was!", 60, ORANGE, tail=(-1, 1))
t = A(k, "reagiert schon jetzt"); brain(b, t, X + 400, Y + 250, 0.9, RED, 0.6); aha(t + 0.5)
for i in range(6):
    a = i * math.pi / 3; b.s(t + 0.7 + i * 0.05, 0.08, line(X + 400 + math.cos(a) * 160, Y + 250 + math.sin(a) * 120, X + 400 + math.cos(a) * 210, Y + 250 + math.sin(a) * 160, n=2), ORANGE, 7)

# ===================== K4 Warum Gerüchte fesseln =====================
k = 4
t = A(k, "Bei GTA sechs"); X, Y = pan(k, 0, t)
fig(t, X - 600, Y + 430, 1.2, hero=True, face="worried"); phone(t + 0.6, X - 420, Y + 120, 0.6)
t = A(k, "Gerüchte.", 0); label(b, t, "Gerüchte", X - 600, Y - 380, 100, RED)
t = A(k, "Kommt ein neuer Trailer"); bubble(b, t, X + 200, Y - 280, 420, 140, "neuer Trailer?", 58, BLUE, tail=(-1, 1)); popk(t)
t = A(k, "Wird es verschoben"); bubble(b, t, X + 550, Y + 20, 380, 140, "verschoben?", 58, RED, tail=(-1, 1)); popk(t)
t = A(k, "hinter dem Leak"); bubble(b, t, X + 150, Y + 300, 360, 140, "Leak echt?", 58, INK, tail=(-1, 1)); popk(t)
t = A(k, "Christopher Fiorillo"); X, Y = pan(k, 1, t)
label(b, t, "Fiorillo, Tobler & Schultz, 2003", X, Y - 400, 70, INK)
t = A(k, "Jedes Bild stand")
for i, (pct, ph) in enumerate((("0 %", "Null Prozent"), ("25 %", "Fünfundzwanzig"), ("50 %", "Fünfzig."), ("75 %", "Fünfundsiebzig"), ("100 %", "hundert Prozent"))):
    tt = A(k, ph); x_ = X - 720 + i * 360
    b.s(tt - 0.1, 0.3, rect(x_ - 130, Y - 150, 260, 230), BLUE if i != 2 else RED, 8); label(b, tt, pct, x_, Y - 10, 90, BLUE if i != 2 else RED); popk(tt)
label(b, t, "Chance auf Belohnung", X, Y - 250, 70, GREY)
t = A(k, "zwei Sekunden Warten"); clock(b, t, X, Y + 300, 90); label(b, t + 0.4, "2 Sekunden", X + 260, Y + 320, 64, INK); b.snd("uhr_ticken.wav", t + 0.3, 0.3)
t = A(k, "Bei sicherer Belohnung"); X, Y = pan(k, 2, t)
tb = [A(k, "Bei gar keiner"), A(k, "Aber bei fünfzig"), A(k, "langsam an"), t]
bars(X, Y + 330, [([(tb[0], 0.03)], GREY, "0 %"), ([(tb[2], 0.55)], BLUE, "25 %"), ([(tb[1] + 0.5, 1.0)], RED, "50 %"), ([(tb[2], 0.55)], BLUE, "75 %"), ([(t + 0.3, 0.03)], GREY, "100 %")],
     h=560, bw=170, gap=70, axis_t=t, lab=52)
label(b, t, "Dopamin beim Warten (vereinfacht)", X, Y - 410, 66, INK)
label(b, A(k, "sicherer"), "ruhig", X + 480, Y + 230, 56, GREY)
label(b, A(k, "Am stärksten"), "am stärksten!", X, Y - 300, 80, RED); pop(A(k, "Am stärksten"))
t = A(k, "Unsicherheit hält"); X, Y = pan(k, 3, t)
brain(b, t, X - 550, Y - 150, 1.0, RED); eye(b, t + 0.7, X - 550, Y - 150, 1.3, BLUE); label(b, t + 0.5, "hellwach", X - 550, Y + 30, 70, BLUE)
t = A(k, "Glücksspiel"); slot(t, X + 300, Y - 180)
t = A(k, "immer wieder nachschauen"); phone(t, X - 500, Y + 330, 0.7); label(b, t + 0.3, "neu laden … neu laden …", X + 100, Y + 300, 60, INK)
t = A(k, "Vielleicht kommt heute"); bubble(b, t, X + 600, Y + 220, 260, 110, "heute?", 54, GREEN)
t = A(k, "Vielleicht auch nicht"); cross(b, t, X + 600, Y + 380, 0.7)
t = A(k, "Wichtig"); X, Y = pan(k, 4, t)
label(b, t, "Wichtig:", X, Y - 380, 100, RED)
t = A(k, "Tierversuch"); label(b, t, "Tierversuch", X - 450, Y - 180, 80, ORANGE); clock(b, t + 0.3, X - 450, Y + 80, 90, "Sekunden")
t = A(k, "Jahren Warten"); calendar(t, X + 450, Y + 40, "Jahre?", "?", RED, 1.0)
t = A(k, "Muster passt"); check(b, t, X, Y + 300, 1.5); label(b, t + 0.3, "Muster passt", X, Y + 450, 70, GREEN); pop(t)

# ===================== K5 Erlebnisse schlagen Dinge =====================
k = 5
t = A(k, "Ist die Vorfreude"); X, Y = pan(k, 0, t)
b.txt(t, 0.4, "?", X - 650, Y + 50, 260, BLUE)
t = A(k, "Amit Kumar"); label(b, t, "Kumar, Killingsworth & Gilovich, 2014", X + 100, Y - 380, 64, INK)
t = A(k, "Smartphone-App"); phone(t, X - 250, Y + 120, 1.0)
t = A(k, "mehr als zweitausend"); counter(X + 400, Y - 150, t, t + 1.3, 0, 2000, 130, BLUE, pre="über "); label(b, t + 0.6, "Menschen", X + 400, Y - 40, 64, INK)
t = A(k, "Denkst du gerade"); bubble(b, t, X + 400, Y + 200, 520, 160, "Was willst du kaufen?", 50, BLUE, tail=(-1, 1))
t = A(k, "wie fühlst du dich"); bubble(b, t, X - 250, Y - 210, 380, 120, "Wie fühlst du dich?", 44, ORANGE, tail=(1, 1))
t = A(k, "Wer sich auf ein Erlebnis"); X, Y = pan(k, 1, t)
plane(A(k, "Reise"), X - 600, Y - 330); notes(b, A(k, "Konzert"), X - 380, Y - 330, 3, BLUE); b.many(A(k, "Essen"), 0.4, [circle(X - 600, Y - 120, 80, ry=30), line(X - 720, Y - 160, X - 720, Y - 60, n=3)], ORANGE, 7)
label(b, t + 0.4, "Erlebnis", X - 480, Y + 20, 80, GREEN)
t2 = A(k, "Wer sich auf einen Gegenstand"); t3 = A(k, "keinen Kauf")
bars(X + 350, Y + 330, [([(t + 1.0, 0.85)], GREEN, "Erlebnis"), ([(t3, 0.55)], GREY, "kein Kauf"), ([(A(k, "diesen Vorteil"), 0.56)], ORANGE, "Ding")], h=560, bw=150, gap=60)
label(b, t3 + 0.5, "im Schnitt glücklicher", X + 350, Y - 380, 66, GREEN)
t = A(k, "Jacke"); b.s(t, 0.5, poly((X - 650, Y + 200), (X - 600, Y + 150), (X - 520, Y + 160), (X - 440, Y + 150), (X - 390, Y + 200), (X - 430, Y + 240), (X - 460, Y + 220), (X - 460, Y + 400), (X - 580, Y + 400), (X - 580, Y + 220), (X - 610, Y + 240), closed=True, n=3), ORANGE, 7)
phone(A(k, "neues Handy"), X - 250, Y + 280, 0.6, ORANGE)
t = A(k, "Zeitungsberichte"); X, Y = pan(k, 2, t)
newspaper(t, X - 650, Y)
t = A(k, "Warteschlangen")
for i in range(5): fig(t + i * 0.12, X - 300 + i * 150, Y - 30, 0.55, dur=0.3, face="neutral", w=6)
t = A(k, "für ein Erlebnis anstanden")
for i in range(4): fig(t + i * 0.1, X - 250 + i * 150, Y + 450, 0.55, dur=0.3, face="happy", w=6)
label(b, t + 0.4, "Erlebnis: gut gelaunt", X - 30, Y + 140, 56, GREEN)
t = A(k, "Sie sangen"); notes(b, t, X - 250, Y + 220, 4, GREEN); b.snd("pop_klein.wav", t, 0.3)
t = A(k, "Streit und Randale")
for i in range(4): fig(t + i * 0.1, X + 450 + (i % 2) * 150, Y + 450 - (i // 2) * 360 + 0, 0.55, dur=0.3, face="worried", w=6, col=RED)
label(b, t + 0.4, "Dinge: eher Streit", X + 520, Y - 380, 60, RED); bolt(t + 0.6, X + 750, Y - 200, 0.6, RED)
t = A(k, "Und ein Videospiel"); X, Y = pan(k, 3, t)
controller(t, X - 550, Y - 80, 1.0)
t = A(k, "Du kaufst ein Ding"); label(b, t, "ein Ding …", X - 550, Y + 150, 80, ORANGE)
t = A(k, "Erlebnis:", 0); b.txt(t, 0.3, "=", X - 100, Y - 40, 160, INK); label(b, t, "… ein Erlebnis", X + 450, Y + 150, 80, GREEN)
t = A(k, "eine Welt"); b.many(t, 0.8, [circle(X + 450, Y - 100, 150), arc(X + 450, Y - 100, 150, -0.2, math.pi + 0.2, ry=50), line(X + 450, Y - 250, X + 450, Y + 50, n=6),
                                  bez((X + 350, Y - 180), (X + 420, Y - 150), (X + 380, Y - 80), (X + 460, Y - 40))], BLUE, 7); aha(t + 0.6)
t = A(k, "genau deshalb"); label(b, t, "doppelte Vorfreude?", X, Y - 380, 90, RED)

# ===================== K6 Hype ist ansteckend =====================
k = 6
t = A(k, "Aber warum warten"); X, Y = pan(k, 0, t)
crowd(t, X - 200, Y - 100, 2, 6, 0.5, 190, 340)
t = A(k, "ein Hype"); b.txt(t, 0.6, "HYPE", X + 620, Y - 50, 200, RED); pop(t + 0.4, 0.5)
t = A(k, "eigenen Regeln"); label(b, t, "eigene Regeln", X + 620, Y + 120, 70, INK)
t = A(k, "Der erste Trailer"); X, Y = pan(k, 1, t)
screen(t, X - 500, Y - 80, 500, 300)
t = A(k, "vierundzwanzig Stunden"); clock(b, t, X - 500, Y + 330, 70); label(b, t + 0.3, "24 Std.", X - 300, Y + 350, 64, INK)
t = A(k, "dreiundneunzig Millionen"); counter(X + 400, Y - 120, t - 0.3, t + 1.6, 0, 93000000, 120, RED, pre="über "); label(b, t + 1.0, "Aufrufe", X + 400, Y, 70, INK)
t = A(k, "meistgesehene"); trophy(t, X + 400, Y + 250); label(b, t + 0.5, "Rekord laut YouTube", X + 400, Y + 420, 56, ORANGE); aha(t + 0.5)
t = A(k, "Je mehr Menschen"); X, Y = pan(k, 2, t)
for i in range(9):
    bubble(b, t + i * 0.18, X - 700 + (i % 5) * 350, Y - 250 + (i // 5) * 260, 200 + i * 10, 90, "…", 50, BLUE if i % 2 else INK)
t = A(k, "wichtiger wirkt"); label(b, t, "wirkt wichtiger", X, Y + 360, 90, RED); pop(t)
t = A(k, "Matthew Salganik"); X, Y = pan(k, 3, t)
label(b, t, "Salganik, Dodds & Watts, 2006", X, Y - 410, 70, INK)
t = A(k, "Über vierzehntausend"); counter(X - 500, Y - 220, t, t + 1.4, 0, 14000, 110, BLUE, pre="über "); label(b, t + 0.6, "Menschen", X - 500, Y - 120, 60, INK)
t = A(k, "achtundvierzig Songs")
for i in range(12):
    x_ = X + 150 + (i % 6) * 110; y_ = Y - 260 + (i // 6) * 140
    b.s(t + i * 0.05, 0.08, circle(x_, y_, 13, n=10), BLUE, 7); b.s(t + i * 0.05 + 0.05, 0.05, line(x_ + 13, y_, x_ + 13, y_ - 55, n=2), BLUE, 7)
label(b, t + 0.6, "48 Songs", X + 820, Y - 190, 64, BLUE)
t = A(k, "Ein Teil sah"); fig(t, X - 450, Y + 450, 0.9, face="neutral"); bubble(b, t + 0.4, X - 450, Y + 70, 340, 120, "512 Downloads", 46, RED, tail=(-1, 1))
t = A(k, "Ein anderer Teil"); fig(t, X + 400, Y + 450, 0.9, face="neutral"); bubble(b, t + 0.4, X + 400, Y + 70, 220, 120, "?", 60, GREY, tail=(-1, 1))
t = A(k, "Mit dieser Info"); X, Y = pan(k, 4, t)
t2 = A(k, "schwerer vorherzusagen")
bars(X - 300, Y + 330, [([(t, 0.3), (t + 1.2, 0.95)], RED, "Song A"), ([(t + 0.2, 0.25)], GREY, "Song B"), ([(t + 0.4, 0.2)], GREY, "Song C"), ([(t + 0.6, 0.15)], GREY, "Song D")], h=560, bw=130, gap=50, lab=44)
label(b, t + 1.0, "Beliebte werden beliebter", X - 300, Y - 380, 70, RED)
dice(t2, X + 550, Y - 100); dice(t2 + 0.3, X + 700, Y + 50); label(b, t2 + 0.3, "schwer vorherzusagen", X + 600, Y + 240, 56, INK)
t = A(k, "zufällig"); label(b, t, "Zufall!", X + 600, Y - 280, 80, ORANGE); pop(t)
t = A(k, "die Angst, etwas"); X, Y = pan(k, 5, t)
door(b, t, X + 300, Y + 430, "Party"); notes(b, t + 0.5, X + 450, Y - 20, 3, BLUE)
fig(t + 0.4, X - 450, Y + 430, 1.2, hero=True, face="sad")
t = A(k, "Fear of Missing Out"); b.txt(t, 0.6, "FOMO", X - 450, Y - 300, 150, RED); pop(t + 0.4)
t = A(k, "Andrew Przybylski"); label(b, t, "Przybylski u. a., 2013", X + 300, Y - 400, 60, INK)
t = A(k, "ohne dich"); bubble(b, t - 0.5, X + 650, Y - 200, 300, 120, "ohne dich", 54, RED)
t = A(k, "am ersten Tag"); calendar(t, X - 50, Y - 200, "Tag", "1", BLUE, 0.75)
t = A(k, "treibt den Hype"); label(b, t, "treibt den Hype", X - 450, Y - 140, 64, RED)

# ===================== K7 Die Enttäuschungsfalle =====================
k = 7
t = A(k, "Jetzt kommt die Schattenseite"); X, Y = pan(k, 0, t)
cloud(b, t, X - 500, Y - 250, 1.6, GREY); label(b, t + 0.4, "Schattenseite", X - 500, Y - 50, 80, GREY)
t = A(k, "desto höher die Erwartungen"); dial(b, t, X + 350, Y + 150, "Erwartung")
dial_needle(b, X + 350, Y + 150, [(t + 0.8, 0.2), (t + 2.5, 0.92)], t + 0.8)
t = A(k, "gefährlich"); label(b, t, "gefährlich", X + 350, Y - 200, 80, RED); pop(t)
t = A(k, "Terence Mitchell"); X, Y = pan(k, 1, t)
label(b, t, "Mitchell u. a., 1997", X, Y - 400, 74, INK)
t = A(k, "einer Europatour"); plane(t, X - 600, Y - 50); label(b, t + 0.3, "Europatour", X - 600, Y + 120, 66, BLUE)
t = A(k, "Thanksgiving-Ferien"); calendar(t, X, Y - 40, "Ferien", "TG", ORANGE, 0.8); label(b, t + 0.4, "Thanksgiving", X, Y + 180, 66, ORANGE)
t = A(k, "Fahrradtour"); bike(t, X + 600, Y); label(b, t + 0.5, "3 Wochen Rad", X + 600, Y + 160, 66, GREEN)
t = A(k, "Vorher waren"); X, Y = pan(k, 2, t)
b.many(t - 0.3, 0.4, [poly((X - 750, Y - 300), (X - 750, Y + 250), (X + 750, Y + 250))], INK, 8)
t2 = A(k, "Während der Reise"); t3 = A(k, "Und hinterher")
b.s(t, 0.5, bez((X - 650, Y + 150), (X - 600, Y - 150), (X - 450, Y - 200), (X - 400, Y - 200)), GREEN, 10); label(b, t + 0.3, "vorher", X - 450, Y + 330, 66, GREEN)
b.s(t2, 0.7, bez((X - 400, Y - 200), (X - 200, Y - 190), (X - 150, Y + 120), (X, Y + 120)), RED, 10); label(b, t2 + 0.3, "während", X, Y + 330, 66, RED)
t4 = A(k, "Ablenkung"); label(b, t4, "Stress", X - 150, Y + 30, 52, RED); cloud(b, t4 + 0.3, X + 120, Y - 20, 0.6, GREY)
b.s(t3, 0.7, bez((X, Y + 120), (X + 200, Y + 120), (X + 300, Y - 230), (X + 600, Y - 230)), GREEN, 10); label(b, t3 + 0.3, "hinterher", X + 500, Y + 330, 66, GREEN)
t = A(k, "rosarote Sicht"); glasses(t, X + 450, Y - 380, RED); label(b, t + 0.4, "rosarote Sicht", X - 250, Y - 380, 80, RED); aha(t + 0.4)
t = A(k, "Robb Rutledge"); X, Y = pan(k, 3, t)
label(b, t, "Rutledge u. a., 2014", X, Y - 410, 74, INK)
t = A(k, "bei einem Glücksspiel"); coin(b, t, X - 650, Y - 180); coin(b, t + 0.2, X - 520, Y - 180); bubble(b, t + 0.6, X - 230, Y - 220, 300, 120, "Wie glücklich?", 44, ORANGE, tail=(-1, 1))
t = A(k, "Über achtzehntausend"); phone(t, X - 600, Y + 200, 0.8); counter(X - 250, Y + 220, t, t + 1.3, 0, 18000, 100, BLUE, pre="über ")
t = A(k, "insgesamt gewonnen"); [coin(b, t + i * 0.08, X + 350, Y - 20 - i * 60) for i in range(5)]; cross(b, t + 0.6, X + 350, Y - 120, 1.2)
t = A(k, "was er erwartet"); bubble(b, t, X + 650, Y - 250, 280, 120, "erwartet", 52, BLUE, tail=(-1, 1)); check(b, t + 0.4, X + 650, Y - 90, 1.0)
t = A(k, "besser als erwartet"); label(b, t, "besser: Stimmung steigt", X + 300, Y + 170, 60, GREEN); pop(t)
t = A(k, "Lief es schlechter"); label(b, t, "schlechter: Stimmung sinkt", X + 300, Y + 280, 60, RED)
t = A(k, "schon die Erwartung"); heart(b, t, X + 300, Y + 420, 1.8); label(b, t + 0.3, "Erwartung allein: hebt die Stimmung", X - 300, Y + 430, 54, ORANGE)
t = A(k, "Übertragen auf"); X, Y = pan(k, 4, t)
t2 = A(k, "Latte extrem hoch")
b.many(t2, 0.6, [line(X - 400, Y + 430, X - 400, Y - 380, n=10), line(X + 400, Y + 430, X + 400, Y - 380, n=10), line(X - 420, Y - 360, X + 420, Y - 360, n=10)], INK, 9)
label(b, t2 + 0.5, "die Latte", X + 600, Y - 360, 70, RED)
fig(t + 0.2, X, Y + 430, 1.0, hero=True, face="worried")
t = A(k, "sehr gutes Spiel")
for i in range(5): star(t + i * 0.15, X - 220 + i * 110, Y - 150, 42, ORANGE, 7)
popk(t + 0.6)
t = A(k, "kurz enttäuschend"); label(b, t, "kurz enttäuscht?", X, Y - 20, 70, RED)
t = A(k, "Nicht, weil es schlecht"); cross(b, t, X - 600, Y + 150, 0.8); label(b, t + 0.2, "schlecht", X - 600, Y + 260, 56, GREY)
t = A(k, "Erwartung so groß"); check(b, t, X + 600, Y + 150, 0.9); label(b, t + 0.2, "Erwartung zu groß", X + 620, Y + 260, 56, RED)

# ===================== K8 Mehr aus Vorfreude holen =====================
k = 8
t = A(k, "Was kannst du"); X, Y = pan(k, 0, t)
bulb(b, t, X - 550, Y - 60)
t = A(k, "Spiel, einen Urlaub"); controller(t, X + 50, Y - 230, 0.6); suitcase(t + 0.3, X + 400, Y - 230, ORANGE); notes(b, A(k, "Konzert"), X + 600, Y - 270, 3, BLUE)
t = A(k, "vier Ideen"); b.txt(t, 0.6, "4 Ideen", X + 300, Y + 150, 150, RED); pop(t + 0.4)
t = A(k, "Erstens"); X, Y = pan(k, 1, t)
v_ = b.mark(); b.txt(t, 0.6, "1  Vorfreude einplanen", X, Y - 380, 90, BLUE); b.s(t + 0.6, 0.3, line(X - 450, Y - 330, X + 450, Y - 325), ORANGE, 8)
t = A(k, "etwas früher"); calendar(t, X - 450, Y + 50, "früh", "!", GREEN, 1.0); b.many(t + 0.5, 0.5, [rect(X - 140, Y - 20, 280, 140), line(X + 60, Y - 20, X + 60, Y + 120, n=4)], ORANGE, 7)
label(b, t + 0.8, "Ticket", X - 40, Y + 70, 56, ORANGE)
t = A(k, "länger etwas"); hourglass(t, X + 450, Y + 80, 0.9, sand_d=6)
t = A(k, "Kuss vom Filmstar"); star(t, X - 100, Y + 340, 60); heart(b, t + 0.3, X + 30, Y + 350, 1.5); label(b, t + 0.4, "3 Tage warten", X + 250, Y + 370, 52, RED)
t = A(k, "Zweitens"); X, Y = pan(k, 2, t)
b.txt(t, 0.6, "2  Erlebnisse statt Dinge", X, Y - 380, 90, BLUE); b.s(t + 0.6, 0.3, line(X - 470, Y - 330, X + 470, Y - 325), ORANGE, 8)
t = A(k, "lieber auf Erlebnisse"); plane(t, X - 450, Y); notes(b, t + 0.4, X - 600, Y + 150, 3, GREEN); check(b, t + 0.8, X - 450, Y + 280, 1.3)
t = A(k, "doch ein Ding"); controller(t, X + 450, Y, 0.8)
t = A(k, "damit erleben"); bubble(b, t, X + 450, Y + 270, 360, 120, "Was erlebe ich?", 48, GREEN); aha(t)
t = A(k, "Drittens"); X, Y = pan(k, 3, t)
b.txt(t, 0.6, "3  Lücken lassen", X, Y - 380, 90, BLUE); b.s(t + 0.6, 0.3, line(X - 330, Y - 330, X + 330, Y - 325), ORANGE, 8)
t = A(k, "jedes Detail")
for i in range(12):
    if i in (2, 7, 9): continue
    b.s(t + i * 0.06, 0.1, rect(X - 750 + (i % 4) * 150, Y - 200 + (i // 4) * 150, 130, 130), INK, 6)
for i in (2, 7, 9): b.txt(t + 1.0, 0.2, "?", X - 685 + (i % 4) * 150, Y - 110 + (i // 4) * 150, 90, RED)
label(b, A(k, "weniger zu entdecken"), "weniger zu entdecken", X - 450, Y + 330, 60, GREY)
t = A(k, "eher eine Vermutung"); label(b, t, "Vermutung,", X + 400, Y - 100, 80, ORANGE); label(b, t + 0.6, "kein Beweis", X + 400, Y + 20, 80, ORANGE)
t = A(k, "Studien über Unsicherheit"); label(b, t, "passt zu: Unsicherheit", X + 400, Y + 200, 56, BLUE)
t = A(k, "Viertens"); X, Y = pan(k, 4, t)
b.txt(t, 0.6, "4  Erwartung realistisch", X, Y - 380, 90, BLUE); b.s(t + 0.6, 0.3, line(X - 450, Y - 330, X + 450, Y - 325), ORANGE, 8)
t = A(k, "realistisch."); dial(b, t, X - 400, Y + 150, "Erwartung"); dial_needle(b, X - 400, Y + 150, [(t + 0.6, 0.95), (t + 2.0, 0.55)], t + 0.6)
t = A(k, "riesig freuen"); heart(b, t, X + 400, Y - 150, 3.0); label(b, t + 0.3, "Freude: ja!", X + 400, Y + 20, 70, GREEN)
t = A(k, "ganz Leben verändert") if False else A(k, "ganzes Leben"); cross(b, t, X + 400, Y + 200, 0.8); label(b, t + 0.2, "Lebenswende: nein", X + 400, Y + 320, 60, RED)
t = A(k, "positiv überraschen"); star(t, X - 400, Y - 160, 70, ORANGE); aha(t)
t = A(k, "große Tag"); X, Y = pan(k, 5, t)
for i in range(3):
    calendar(t + i * 0.5, X - 550 + i * 550, Y - 30, "bald", ["GTA", "Urlaub", "Konzert"][i] if False else "!", [BLUE, GREEN, ORANGE][i], 0.8)
label(b, t + 0.3, "GTA 6", X - 550, Y + 230, 60, BLUE); label(b, t + 0.8, "Urlaub", X, Y + 230, 60, GREEN); label(b, t + 1.3, "Konzert", X + 550, Y + 230, 60, ORANGE)
for i in range(2): b.s(t + 0.4 + i * 0.5, 0.25, line(X - 380 + i * 550, Y - 30, X - 170 + i * 550, Y - 30, n=5), INK, 8)
t = A(k, "keine Einbahnstraße"); label(b, t, "Vorfreude: immer wieder neu", X, Y - 360, 90, RED); aha(t + 0.4)

# ===================== K9 Schluss =====================
k = 9
X, Y = v.P(k, 0); v.go(v.CT[k], X, Y, 1.0, d=0.7)
t = A(k, "keine verlorene Zeit"); hourglass(v.VSTART[k], X - 650, Y + 100, 0.8, sand_d=4); check(b, t, X - 650, Y + 340, 1.2)
t = A(k, "eigene Form von Glück"); label(b, t, "Vorfreude = Glück", X, Y - 380, 110, RED); heart(b, t + 0.5, X + 550, Y - 380, 1.6); pop(t)
t = A(k, "beim Trailer"); screen(t, X - 150, Y - 60, 300, 180); bolt(t + 0.5, X + 40, Y - 110, 0.5)
t = A(k, "Unsicherheit macht"); b.txt(t, 0.4, "50 %", X + 300, Y - 30, 100, BLUE)
t = A(k, "andere Menschen"); [fig(t + i * 0.12, X + 50 + i * 170, Y + 450, 0.6, dur=0.3, face="happy", w=6) for i in range(4)]
t = A(k, "Nur eines"); X, Y = pan(k, 1, t)
dial(b, t, X - 300, Y + 150, "Erwartung"); dial_needle(b, X - 300, Y + 150, [(t + 0.6, 0.3), (A(k, "Je höher"), 0.95)], t + 0.6)
t = A(k, "der Maßstab"); label(b, t, "Erwartung = Maßstab", X + 400, Y - 250, 90, INK); pop(t)
t = A(k, "Wirklichkeit"); label(b, t, "schwer für die Wirklichkeit", X + 400, Y + 100, 64, RED)
t = A(k, "Jetzt bin ich neugierig"); X, Y = pan(k, 2, t)
comment_box(b, t, X, Y - 80)
label(b, A(k, "Worauf freust"), "Worauf freust du dich?", X - 20, Y - 115, 66, BLUE)
label(b, A(k, "Ist es GTA"), "GTA 6 – oder etwas anderes?", X, Y - 40, 50, RED)
t = A(k, "Kommentare"); label(b, t, "Schreib's in die Kommentare!", X, Y + 300, 80, INK); pop(t)
t = A(k, "Abonniere"); X, Y = pan(k, 3, t)
head_profile(b, t - 0.6, X - 520, Y - 30, 230, INK, 10, 0.8)
def endpat(ctx, tt, X=X, Y=Y, t0=t):
    if tt < t0: return
    for i, (r, col) in enumerate(zip((25, 50, 75, 100), (BLUE, RED, GREEN, ORANGE))):
        f = ease_out(prog(tt, t0 + i * 0.2, t0 + 0.7 + i * 0.2))
        if f <= 0: continue
        ctx.set_source_rgba(*col); ctx.set_line_width(9); ctx.new_path()
        for kk in range(int(60 * f) + 1):
            a = -math.pi * 0.95 + 1.75 * math.pi * kk / 60; rr = r * (1 + 0.07 * math.sin(5 * a + i))
            ctx.line_to(X - 532 + math.cos(a) * rr * 1.12, Y - 85 + math.sin(a) * rr)
        ctx.stroke()
b.dyn.append(endpat)
b.txt(t, 0.8, "Denkmuster", X + 200, Y - 30, 150, INK); b.txt(t + 0.5, 0.3, "abonnieren", X + 200, Y + 90, 70, BLUE)
tt = A(k, "Glocke"); bell(b, tt, X + 620, Y + 260); b.snd("pop.wav", tt, 0.5)
t = A(k, "Bis zum nächsten"); fig(t, X - 150, Y + 450, 0.6, hero=True, face="happy", pose="arms_up")

if __name__ == "__main__":
    if "--check" in sys.argv:
        print("FEHLEND:", v.missing, "TOTAL", round(v.TOTAL, 1)); sys.exit(0)
    v.render()
