"""Denkmuster icon library: hand-drawn marker icons built from wb primitives."""
import math
import cairo
from wb import *

def label(b, t, s, x, y, size=70, col=INK, dur=None, rot=0.0):
    dur = dur or max(0.35, 0.045 * len(s))
    return b.txt(t, dur, s, x, y, size, col, rot=rot)

def eye(b, t, x, y, s=1.0, col=INK):
    b.many(t, 0.35, [arc(x, y, 50 * s, math.pi * 1.1, math.pi * 1.9, ry=28 * s), arc(x, y, 50 * s, math.pi * 0.1, math.pi * 0.9, ry=28 * s),
                     circle(x, y, 13 * s, n=16)], col, 6)

def book(b, t, x, y, title, col=BLUE):
    b.many(t, 0.6, [poly((x - 150, y - 200), (x + 150, y - 200), (x + 150, y + 200), (x - 150, y + 200), closed=True),
                    line(x - 120, y - 200, x - 120, y + 200)], INK, 8)
    b.txt(t + 0.6, 0.4, title, x + 15, y - 30, 90, col)
    b.s(t + 0.9, 0.2, line(x - 80, y + 20, x + 110, y + 20), col, 5)

def door(b, t, x, y, txt=None):
    b.many(t, 0.5, [poly((x - 110, y), (x - 110, y - 330), (x + 110, y - 330), (x + 110, y)), circle(x + 75, y - 160, 9, n=12)], INK, 8)
    if txt: b.txt(t + 0.5, 0.35, txt, x, y - 360, 56, BLUE)

def notes(b, t, x, y, n=3, col=INK):
    for i in range(n):
        nx, ny = x + i * 70, y + (i % 2) * 40
        b.s(t + i * 0.1, 0.1, circle(nx, ny, 12, n=14), col, 7)
        b.s(t + i * 0.1 + 0.08, 0.08, line(nx + 12, ny, nx + 12, ny - 55, n=3), col, 7)

def heart(b, t, x, y, s=1.0, col=RED):
    pts = [(x + 16 * s * math.sin(a) ** 3, y - s * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))) for a in [i * 2 * math.pi / 50 for i in range(51)]]
    b.s(t, 0.4, wob(pts, 0.6), col, 7)

def check(b, t, x, y, s=1.0, col=GREEN):
    b.s(t, 0.3, poly((x - 40 * s, y), (x - 10 * s, y + 35 * s), (x + 50 * s, y - 45 * s)), col, 12)

def cross(b, t, x, y, s=1.0, col=RED):
    b.s(t, 0.15, line(x - 40 * s, y - 40 * s, x + 40 * s, y + 40 * s, n=4), col, 12)
    b.s(t + 0.15, 0.15, line(x + 40 * s, y - 40 * s, x - 40 * s, y + 40 * s, n=4), col, 12)

def bubble(b, t, x, y, w, h, txt=None, size=56, col=INK, tail=(-1, 1)):
    b.s(t, 0.45, circle(x, y, w / 2, ry=h / 2), col, 7)
    b.s(t + 0.4, 0.15, poly((x + tail[0] * w * 0.2, y + h * 0.42), (x + tail[0] * w * 0.35, y + h * 0.75), (x + tail[0] * w * 0.05, y + h * 0.48)), col, 7)
    if txt: b.txt(t + 0.5, max(0.35, 0.04 * len(txt)), txt, x, y + size * 0.3, size, col)

def couch(b, t, x, y, col=INK):
    b.many(t, 0.6, [poly((x - 200, y), (x - 200, y - 150), (x - 160, y - 190), (x + 160, y - 190), (x + 200, y - 150), (x + 200, y)),
                    poly((x - 230, y - 60), (x + 230, y - 60))], col, 8)

def lemon(b, t, x, y, s=1.0):
    b.s(t, 0.4, circle(x, y, 90 * s, ry=62 * s), YEL, 10)
    b.s(t + 0.35, 0.1, poly((x + 88 * s, y - 6 * s), (x + 108 * s, y), (x + 88 * s, y + 6 * s)), YEL, 9)
    b.s(t + 0.45, 0.15, line(x - 30 * s, y - 20 * s, x + 20 * s, y + 15 * s, n=4), ORANGE, 5)

def drop(b, t, x, y, s=1.0, col=BLUE):
    b.s(t, 0.25, bez((x, y - 40 * s), (x + 40 * s, y + 10 * s), (x + 20 * s, y + 35 * s), (x, y + 35 * s)) + bez((x, y + 35 * s), (x - 20 * s, y + 35 * s), (x - 40 * s, y + 10 * s), (x, y - 40 * s))[1:], col, 6)

def brain(b, t, x, y, s=1.0, col=RED, dur=0.9):
    pts = [(x + 150 * s * math.cos(a) * (1 + 0.1 * math.sin(7 * a)), y + 105 * s * math.sin(a) * (1 + 0.1 * math.sin(7 * a))) for a in [i * 2 * math.pi / 90 for i in range(91)]]
    b.s(t, dur * 0.6, wob(pts, 1.2), col, 8)
    b.s(t + dur * 0.6, dur * 0.2, bez((x - 100 * s, y), (x - 40 * s, y - 60 * s), (x + 20 * s, y + 50 * s), (x + 90 * s, y - 20 * s)), col, 6)
    b.s(t + dur * 0.8, dur * 0.2, line(x, y - 100 * s, x - 10 * s, y + 100 * s, n=8), col, 5)

def head_profile(b, t, cx, cy, s, col=INK, w=12, dur=0.9):
    P = lambda x, y: (cx + x * s, cy + y * s)
    pts = bez(P(-0.55, 1.0), P(-0.75, 0.35), P(-0.85, -0.55), P(-0.2, -0.85))
    pts += bez(P(-0.2, -0.85), P(0.35, -1.05), P(0.72, -0.6), P(0.62, -0.1))[1:]
    pts += poly(P(0.62, -0.1), P(0.8, 0.12), P(0.66, 0.2), P(0.68, 0.38), P(0.6, 0.46), P(0.64, 0.58), P(0.52, 0.66), P(0.3, 0.66), P(0.28, 1.0), n=5)[1:]
    b.s(t, dur, pts, col, w)

def battery(b, t, x, y, col=INK):
    b.s(t, 0.45, poly((x - 90, y - 45), (x + 90, y - 45), (x + 90, y + 45), (x - 90, y + 45), closed=True), col, 8)
    b.s(t + 0.45, 0.12, poly((x + 90, y - 18), (x + 110, y - 18), (x + 110, y + 18), (x + 90, y + 18)), col, 8)

def battery_fill(b, x, y, t0, t1, l0, l1):
    def fn(ctx, t):
        if t < t0: return
        lv = l0 + (l1 - l0) * ease(prog(t, t0, t1))
        col = RED if lv < 0.3 else (ORANGE if lv < 0.6 else GREEN)
        ctx.save(); ctx.rectangle(x - 80, y - 36, 160 * lv, 72); ctx.clip()
        ctx.set_source_rgba(*col); ctx.set_line_width(7)
        for k in range(-10, 30): ctx.move_to(x - 80 + k * 15, y + 40); ctx.line_to(x - 80 + k * 15 + 40, y - 40)
        ctx.stroke(); ctx.restore()
    b.dyn.append(fn)

def dial(b, t, x, y, label_txt=None):
    """volume knob; needle drawn dynamically via dial_needle."""
    b.s(t, 0.5, arc(x, y, 160, math.pi, 2 * math.pi), INK, 8)
    for k in range(7):
        a = math.pi + k * math.pi / 6
        b.s(t + 0.5 + k * 0.03, 0.05, line(x + math.cos(a) * 160, y + math.sin(a) * 160, x + math.cos(a) * 185, y + math.sin(a) * 185, n=2), INK, 6)
    b.s(t + 0.75, 0.3, arc(x, y, 175, math.pi * 1.72, math.pi * 1.98), RED, 14)
    if label_txt: b.txt(t + 0.9, 0.4, label_txt, x, y + 80, 56, INK)

def dial_needle(b, x, y, keys, t_show):
    """keys: list of (t, value 0..1)."""
    def fn(ctx, t):
        if t < t_show: return
        v = keys[0][1]
        for (ta, va), (tb, vb) in zip(keys, keys[1:]):
            if ta <= t <= tb: v = va + (vb - va) * ease(prog(t, ta, tb)); break
            if t > tb: v = vb
        a = math.pi + v * math.pi
        ctx.set_source_rgba(*(RED if v > 0.82 else INK)); ctx.set_line_width(10); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(x, y); ctx.line_to(x + math.cos(a) * 140, y + math.sin(a) * 140); ctx.stroke()
        ctx.arc(x, y, 14, 0, 2 * math.pi); ctx.set_source_rgba(*INK); ctx.fill()
    b.dyn.append(fn)

def scanner(b, t, x, y):
    b.many(t, 0.8, [circle(x, y, 210), circle(x, y, 130), poly((x - 420, y + 60), (x + 60, y + 60)), poly((x - 420, y + 110), (x + 60, y + 110))], INK, 8)

def coin(b, t, x, y, col=ORANGE):
    b.s(t, 0.3, circle(x, y, 55, ry=55), col, 9)
    b.txt(t + 0.3, 0.2, "€", x, y + 22, 64, col)

def molecule(b, t, x, y, s=1.0, col=BLUE):
    pts = [(x + 30 * s * math.cos(a), y + 30 * s * math.sin(a)) for a in [math.pi / 6 + i * math.pi / 3 for i in range(7)]]
    b.s(t, 0.2, wob(pts, 0.5), col, 6)
    b.s(t + 0.2, 0.1, line(x + 26 * s, y - 15 * s, x + 60 * s, y - 35 * s, n=3), col, 6)

def clock(b, t, x, y, r=80, hours=None):
    b.s(t, 0.4, circle(x, y, r), INK, 8)
    b.s(t + 0.4, 0.15, line(x, y, x, y - r * 0.7, n=3), INK, 7)
    b.s(t + 0.55, 0.15, line(x, y, x + r * 0.5, y + r * 0.1, n=3), INK, 7)
    if hours: b.txt(t + 0.7, 0.4, hours, x, y + r + 70, 56, RED)

def zzz(b, t, x, y, col=BLUE):
    for i, sz in enumerate((40, 55, 70)):
        b.txt(t + i * 0.2, 0.2, "z", x + i * 45, y - i * 50, sz, col)

def building(b, t, x, y, txt=None):
    b.many(t, 0.8, [poly((x - 220, y), (x - 220, y - 260), (x + 220, y - 260), (x + 220, y)), poly((x - 250, y - 260), (x, y - 400), (x + 250, y - 260))] +
           [line(x - 160 + i * 80, y - 230, x - 160 + i * 80, y - 20, n=6) for i in range(5)], INK, 7)
    if txt: b.txt(t + 0.8, 0.4, txt, x, y + 70, 56, BLUE)

def bulb(b, t, x, y, col=ORANGE):
    b.many(t, 0.5, [arc(x, y, 70, math.pi * 0.75, math.pi * 2.25), poly((x - 40, y + 50), (x - 35, y + 100), (x + 35, y + 100), (x + 40, y + 50)), line(x - 30, y + 125, x + 30, y + 125, n=3)], col, 8)
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.5
        b.s(t + 0.5 + k * 0.05, 0.06, line(x + math.cos(a) * 95, y + math.sin(a) * 95, x + math.cos(a) * 130, y + math.sin(a) * 130, n=2), col, 6)

def cloud(b, t, x, y, s=1.0, col=GREY):
    b.many(t, 0.5, [arc(x - 60 * s, y, 50 * s, math.pi * 0.5, math.pi * 1.5), arc(x, y - 30 * s, 60 * s, math.pi, 2 * math.pi), arc(x + 60 * s, y, 50 * s, -math.pi * 0.5, math.pi * 0.5), line(x - 60 * s, y + 50 * s, x + 60 * s, y + 50 * s, n=6)], col, 7)

def dimmer(b, t, x, y):
    b.many(t, 0.5, [poly((x - 60, y - 220), (x + 60, y - 220), (x + 60, y + 220), (x - 60, y + 220), closed=True), line(x, y - 180, x, y + 180)], INK, 8)

def dimmer_knob(b, x, y, t0, t1, v0, v1, t_show):
    def fn(ctx, t):
        if t < t_show: return
        v = v0 + (v1 - v0) * ease(prog(t, t0, t1))
        ky = y + 180 - 360 * v
        ctx.rectangle(x - 45, ky - 22, 90, 44); ctx.set_source_rgba(*ORANGE); ctx.fill_preserve()
        ctx.set_source_rgba(*INK); ctx.set_line_width(6); ctx.stroke()
    b.dyn.append(fn)

def wave(b, t, x, y, w, amp, n_waves, col, dur=0.8):
    pts = [(x - w / 2 + w * i / 120, y + amp * math.sin(i / 120 * n_waves * 2 * math.pi)) for i in range(121)]
    b.s(t, dur, wob(pts, 0.5), col, 8)

def plug(b, t, x, y, col=GREEN):
    b.many(t, 0.6, [poly((x - 60, y - 70), (x + 60, y - 70), (x + 60, y + 30), (x - 60, y + 30), closed=True), line(x - 25, y - 70, x - 25, y - 130, n=3), line(x + 25, y - 70, x + 25, y - 130, n=3), bez((x, y + 30), (x, y + 120), (x + 120, y + 80), (x + 160, y + 160))], col, 8)
    b.s(t + 0.6, 0.25, poly((x - 15, y - 40), (x - 30, y - 5), (x - 5, y - 5), (x - 20, y + 20)), YEL, 7)

def bell(b, t, x, y, col=ORANGE):
    b.many(t, 0.5, [bez((x - 70, y + 50), (x - 60, y - 90), (x + 60, y - 90), (x + 70, y + 50)), line(x - 85, y + 50, x + 85, y + 50, n=4), circle(x, y + 70, 14, n=12), line(x, y - 70, x, y - 95, n=2)], col, 8)

def comment_box(b, t, x, y):
    b.many(t, 0.6, [poly((x - 330, y - 110), (x + 330, y - 110), (x + 330, y + 70), (x - 200, y + 70), (x - 260, y + 130), (x - 250, y + 70), (x - 330, y + 70), closed=True)], INK, 8)
