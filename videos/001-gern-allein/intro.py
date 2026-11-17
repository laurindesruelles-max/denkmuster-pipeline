import math
import cairo
from wb import *

b = Board()
O = 0.5  # voice offset
_A, _B, _L10, _L11 = 33.4, 40.85, 3.946916, 5.776689
DELTA = 3.4236
def V(t):
    """Zeit in der Original-Sprachaufnahme -> Zeit im Video (Satz 10/11 nach Faktencheck neu eingesprochen)."""
    if t < _A: r = t
    elif t < 36.3: r = _A + (t - _A) * (_L10 + 0.6) / (36.3 - _A)
    elif t < _B: r = _A + _L10 + 0.6 + (t - 36.3) * (_L11 + 0.55) / (_B - 36.3)
    else: r = t + DELTA
    return r + O
MK = ["marker_strich.wav", "marker_kurz.wav"]
_mk = [0]
def mk(t, v=0.6):
    b.snd(MK[_mk[0] % 2], t, v); _mk[0] += 1

# ===== Room (A–H) centred around (1000, 600) =====
RX, RY = 1000, 600
# A "Fünfzehn Minuten." — clock close-up
CLX, CLY = 1000, 300
b.key(0, CLX, CLY, 2.6)
b.s(V(0.0), 0.5, circle(CLX, CLY, 75), INK, 8); mk(V(0.0))
for k in range(12):
    a = k * math.pi / 6
    b.s(V(0.45 + k * 0.02), 0.03, line(CLX + math.cos(a) * 60, CLY + math.sin(a) * 60, CLX + math.cos(a) * 68, CLY + math.sin(a) * 68, n=2), INK, 5)
b.txt(V(0.2), 0.6, "15 Min.", CLX, CLY + 135, 46, RED); mk(V(0.2), 0.4)
def clock_hands(ctx, t):
    if t < V(0.7): return
    ctx.set_source_rgba(*INK); ctx.set_line_width(6)
    a = -math.pi / 2 + (t - V(0.7)) * 1.4
    ctx.move_to(CLX, CLY); ctx.line_to(CLX + math.cos(a) * 52, CLY + math.sin(a) * 52); ctx.stroke()
    ctx.set_line_width(8); ctx.move_to(CLX, CLY); ctx.line_to(CLX + 30, CLY - 18); ctx.stroke()
b.dyn.append(clock_hands)
b.snd("uhr_ticken.wav", V(0.7), 0.25)
# B "Allein in einem leeren Raum." — zoom out, draw room + hero on chair
b.key(V(1.6), CLX, CLY, 2.6); b.key(V(2.5), RX, RY + 20, 1.0)
room = [poly((300, 120), (300, 1000)), poly((1700, 120), (1700, 1000)), poly((300, 860), (1700, 860)),
        poly((300, 860), (180, 1000)), poly((1700, 860), (1820, 1000))]
b.many(V(1.85), 1.0, room, INK, 8); mk(V(1.85))
b.s(V(2.8), 0.4, poly((930, 860), (930, 720), (1060, 720), (1060, 860)), INK, 8)   # chair
b.s(V(3.15), 0.2, poly((930, 720), (930, 600)), INK, 8)
stick(b, V(2.9), 960, 860, 1.0, dur=1.1, pose="sit", face="neutral", hero=True)
M_C = b.mark()
# C "Kein Handy, kein Buch – nur du und deine Gedanken."
b.key(V(4.0), RX, RY + 20, 1.0)
b.many(V(4.1), 0.5, [rect(470, 620, 90, 160), circle(515, 760, 8, n=10), line(490, 640, 540, 640, n=3)], INK, 7); mk(V(4.1))
b.many(V(4.7), 0.55, [poly((1360, 650), (1460, 630), (1560, 650), (1560, 760), (1460, 740), (1360, 760), closed=True), line(1460, 630, 1460, 740)], INK, 7)
b.s(V(5.15), 0.2, line(450, 600, 580, 800), RED, 10); b.s(V(5.35), 0.2, line(580, 600, 450, 800), RED, 10); mk(V(5.15), 0.7)
b.s(V(5.5), 0.2, line(1340, 610, 1580, 790), RED, 10); b.s(V(5.7), 0.2, line(1580, 610, 1340, 790), RED, 10)
# thought bubble
for (bx, by, r) in ((1030, 560, 9), (1060, 515, 15)):
    b.s(V(6.1), 0.12, circle(bx, by, r, n=20), INK, 6)
b.s(V(6.3), 0.5, circle(1150, 420, 110, ry=70), INK, 7); mk(V(6.1))
b.s(V(6.8), 0.7, spiral(1150, 420, 55, turns=2.4), BLUE, 6)
# D "Klingt harmlos, oder?"
b.txt(V(8.45), 0.8, "harmlos?", 620, 330, 110, INK, rot=-0.06); mk(V(8.45), 0.6)
M_D = b.mark()
# E "Genau das haben Forscher in den USA getestet." — pan to study area
SX = 3100
b.key(V(9.7), RX, RY + 20, 1.0); b.key(V(10.4), SX, 600, 1.0); b.snd("schwenk.wav", V(9.7), 0.35)
b.snd("stift_klick.wav", V(10.2), 0.5)
b.many(V(10.3), 0.9, [rect(2600, 330, 380, 520), rect(2720, 300, 140, 60)] + [line(2650, 440 + i * 70, 2930, 440 + i * 70, n=6) for i in range(5)], INK, 8); mk(V(10.3))
b.txt(V(11.1), 0.7, "Studie", 3420, 470, 120, BLUE); mk(V(11.1), 0.5)
b.txt(V(11.8), 0.5, "USA · 2014", 3420, 600, 80, INK)
b.txt(V(12.3), 0.4, "Wilson et al., Science", 3420, 700, 46, GREY)
b.clear(M_C, M_D, V(12.2))
# F "Und neben jede Versuchsperson legten sie einen Knopf." — back to room, draw table + button
b.key(V(12.8), SX, 600, 1.0); b.key(V(13.6), 1150, 680, 1.35); b.snd("schwenk.wav", V(12.8), 0.35)
b.many(V(13.9), 0.6, [poly((1180, 860), (1180, 760)), poly((1380, 860), (1380, 760)), poly((1150, 760), (1410, 760))], INK, 8); mk(V(13.9))
b.s(V(14.6), 0.5, circle(1280, 735, 42, ry=18), INK, 8)
b.s(V(15.1), 0.4, arc(1280, 728, 32, math.pi, 2 * math.pi, ry=22), RED, 12)
M_K = b.mark()
b.txt(V(15.6), 0.5, "Knopf", 1280, 950, 64, RED)
# G "Wer ihn drückt, bekommt einen Stromschlag."
b.s(V(17.2), 0.35, poly((965, 690), (1120, 700), (1250, 728)), INK, 9); mk(V(17.2))   # arm reaches
bolt = poly((1290, 690), (1240, 600), (1300, 590), (1230, 470), (1330, 600), (1270, 610), (1320, 690))
b.s(V(17.6), 0.3, bolt, YEL, 16); b.s(V(17.6), 0.3, bolt, INK, 5)
b.txt(V(17.9), 0.4, "Autsch!", 1420, 520, 80, RED, rot=0.1)
b.snd("stromschlag.wav", V(17.6), 0.45)
b.clear(M_K, b.mark(), V(20.0))
# H "...sie würden sogar Geld zahlen, um ihn zu vermeiden."
b.key(V(19.6), 1150, 680, 1.35); b.key(V(20.3), RX, 560, 1.0)
b.many(V(20.4), 0.6, [bez((820, 520), (640, 520), (520, 470), (560, 360)), bez((560, 360), (600, 250), (900, 250), (930, 360)), bez((930, 360), (950, 440), (900, 500), (860, 520)), poly((860, 520), (900, 590), (820, 520))], INK, 7); mk(V(20.4))
b.txt(V(21.0), 0.7, "Nein danke!", 745, 400, 64, INK)
for k in range(3):
    b.s(V(22.2 + k * 0.25), 0.25, circle(1450 + k * 40, 380 - k * 12, 48, ry=22), ORANGE, 8)
b.txt(V(22.8), 0.4, "€", 1490, 370, 56, ORANGE); mk(V(22.2))
b.txt(V(23.3), 0.6, "lieber zahlen", 1490, 470, 54, ORANGE)
# I "Das Ergebnis?" — pan to chart
CX = 5200
b.key(V(24.9), RX, 560, 1.0); b.key(V(25.6), CX, 560, 1.0); b.snd("schwenk.wav", V(24.9), 0.35)
b.txt(V(25.6), 0.7, "Ergebnis", CX, 220, 120, INK); mk(V(25.6))
b.s(V(26.3), 0.3, line(CX - 260, 245, CX + 260, 250), RED, 8)
# J chart: 2/3 men, 1/4 women
BASE = 900; HMAX = 520
b.many(V(26.9), 0.6, [poly((CX - 450, 330), (CX - 450, BASE), (CX + 450, BASE))], INK, 8); mk(V(26.9))
def bars(ctx, t):
    for i, (val, col, x) in enumerate(((2 / 3, BLUE, CX - 220), (1 / 4, RED, CX + 200))):
        t0 = V(27.6 + i * 2.0)
        if t < t0: continue
        f = ease_out(prog(t, t0, t0 + 1.4)); h = HMAX * val * f
        ctx.save(); ctx.rectangle(x - 110, BASE - h, 220, h); ctx.clip()
        ctx.set_source_rgba(*col); ctx.set_line_width(7)
        for k in range(-20, 40): ctx.move_to(x - 110 + k * 20, BASE); ctx.line_to(x - 110 + k * 20 + 60, BASE - 60 * 10)
        ctx.stroke(); ctx.restore()
        ctx.set_source_rgba(*col); ctx.set_line_width(8); ctx.rectangle(x - 110, BASE - h, 220, h); ctx.stroke()
        if f > 0.98:
            ctx.select_font_face("Caveat", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(80)
            s = ("2 von 3", "1 von 4")[i]; e = ctx.text_extents(s)
            ctx.move_to(x - e.width / 2, BASE - h - 30); ctx.set_source_rgba(*col); ctx.show_text(s)
b.dyn.append(bars)
b.snd("marker_strich.wav", V(27.6), 0.5); b.snd("marker_strich.wav", V(29.6), 0.5); b.snd("pop_klein.wav", V(29.0), 0.6); b.snd("pop_klein.wav", V(31.0), 0.6)
b.txt(V(28.0), 0.5, "Männer", CX - 220, BASE + 80, 70, INK)
b.txt(V(30.0), 0.5, "Frauen", CX + 200, BASE + 80, 70, INK)
b.txt(V(31.2), 0.8, "drückten lieber", CX + 520, 420, 60, GREY, rot=-0.05)
# K "Ein Mann drückte hundertneunzig Mal." — pan to counter
KX = 7300
b.key(V(32.9), CX, 560, 1.0); b.key(V(33.6), KX, 600, 1.0); b.snd("schwenk.wav", V(32.9), 0.35)
stick(b, V(33.4), KX - 450, 900, 1.15, dur=0.8, pose="stand", face="worried"); mk(V(33.4))
b.s(V(34.0), 0.4, circle(KX - 180, 830, 50, ry=22), INK, 8)
b.s(V(34.3), 0.3, arc(KX - 180, 822, 38, math.pi, 2 * math.pi, ry=26), RED, 12)
b.s(V(34.0), 0.4, poly((KX - 280, 860), (KX - 120, 860), (KX - 100, 900), (KX - 300, 900), closed=True), INK, 7)
def presser(ctx, t):
    if t < V(34.5): return
    ph = abs(math.sin((t - V(34.5)) * 14))
    ctx.set_source_rgba(*INK); ctx.set_line_width(10)
    sx, sy = KX - 450 + 55 * 1.15, 900 - 150 * 1.15
    ctx.move_to(KX - 450, 900 - 170 * 1.15); ctx.line_to(sx + 40, sy + 20); ctx.line_to(KX - 190, 790 + 25 * ph); ctx.stroke()
    n = int(190 * ease_out(prog(t, V(34.5), V(36.3))))
    ctx.select_font_face("Caveat", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(300)
    s = f"{n}×"; e = ctx.text_extents(s)
    ctx.move_to(KX + 330 - e.width / 2, 700); ctx.set_source_rgba(*RED); ctx.show_text(s)
    if t > V(34.5) and int((t - V(34.5)) * 7) % 2 == 0 and t < V(36.3):
        bx = KX - 180
        ctx.set_source_rgba(*YEL); ctx.set_line_width(8)
        ctx.move_to(bx - 60, 760); ctx.line_to(bx - 90, 720); ctx.move_to(bx + 60, 760); ctx.line_to(bx + 90, 720); ctx.stroke()
b.dyn.append(presser)
for k in range(9): b.snd("pop_klein.wav", V(34.5 + k * 0.2), 0.4)
b.txt(V(36.3), 0.4, "in 15 Minuten", KX + 330, 820, 70, INK)
# L "Für die meisten Menschen ist Alleinsein also kaum auszuhalten." — grid of rooms
GX, GY = 9600, 600
b.key(V(36.3), KX, 600, 1.0); b.key(V(37.1), GX, GY, 1.0); b.snd("schwenk.wav", V(36.3), 0.35)
cells = [(GX - 600 + c * 600, GY - 230 + r * 470) for r in range(2) for c in range(3)]
for i, (x, y) in enumerate(cells):
    t0 = V(37.0 + i * 0.45)
    b.s(t0, 0.25, rect(x - 250, y - 200, 500, 400), INK, 6)
    if i != 5:
        stick(b, t0 + 0.2, x - 40, y + 170, 0.6, dur=0.3, pose="sit", face="worried", w=6)
        b.s(t0 + 0.5, 0.1, bez((x + 30, y - 60), (x + 20, y - 40), (x + 40, y - 30), (x + 30, y - 20), n=5), BLUE, 5)  # sweat drop
mk(V(37.0)); mk(V(38.4))
b.txt(V(38.3), 0.9, "viele", GX, GY - 470, 100, RED)
# M "Aber es gibt Menschen, für die genau diese fünfzehn Minuten das Schönste ... sind." — hero cell
HX, HY = cells[5]
b.key(V(40.9), GX, GY, 1.0); b.key(V(41.8), HX, HY, 2.2)
stick(b, V(41.6), HX - 40, HY + 170, 0.6, dur=0.9, pose="sit", face="happy", hero=True, w=6); mk(V(41.6))
for k in range(7):
    a = -math.pi / 2 + (k - 3) * 0.4
    b.s(V(42.7 + k * 0.08), 0.1, line(HX + 140 + math.cos(a) * 45, HY - 110 + math.sin(a) * 45, HX + 140 + math.cos(a) * 75, HY - 110 + math.sin(a) * 75, n=3), ORANGE, 5)
b.s(V(42.6), 0.2, circle(HX + 140, HY - 110, 30, n=24), ORANGE, 6)
b.txt(V(43.6), 1.0, "das Schönste am Tag", HX, HY - 160, 44, GREEN); mk(V(43.6))
# N three quick panels
NX = 12200
b.key(V(46.9), HX, HY, 2.2); b.key(V(47.6), NX - 650, 600, 1.6); b.snd("schwenk.wav", V(46.9), 0.35)
# party invite crossed out
b.s(V(47.6), 0.4, rect(NX - 850, 420, 400, 300), INK, 7); mk(V(47.6))
b.txt(V(47.9), 0.4, "Party!", NX - 650, 540, 80, BLUE)
b.txt(V(48.2), 0.3, "Sa · 20 Uhr", NX - 650, 640, 50, INK)
b.s(V(48.6), 0.2, line(NX - 870, 400, NX - 430, 740), RED, 12); b.s(V(48.75), 0.2, line(NX - 430, 400, NX - 870, 740), RED, 12)
# walking alone
b.key(V(48.9), NX - 650, 600, 1.6); b.key(V(49.4), NX, 600, 1.6)
tree = [poly((NX - 300, 760), (NX + 300, 760)), line(NX + 170, 760, NX + 170, 560), line(NX + 160, 640, NX + 120, 600, n=3),
        arc(NX + 130, 530, 45, 1.6, 4.4), arc(NX + 175, 480, 50, 3.4, 6.0), arc(NX + 220, 535, 45, 4.9, 7.9), arc(NX + 175, 580, 40, 0.1, 3.1)]
b.many(V(49.2), 0.6, tree, GREEN, 7); mk(V(49.2))
stick(b, V(49.5), NX - 80, 760, 0.8, dur=0.6, pose="walk", face="happy", hero=True, w=7)
b.snd("schritte_weg.wav", V(49.6), 0.35); b.snd("vogel.wav", V(49.9), 0.25)
# calendar meeting cancelled
b.key(V(50.6), NX, 600, 1.6); b.key(V(51.2), NX + 650, 600, 1.6)
b.many(V(51.2), 0.5, [rect(NX + 470, 420, 360, 330), line(NX + 470, 500, NX + 830, 500), line(NX + 550, 400, NX + 550, 440), line(NX + 750, 400, NX + 750, 440)], INK, 7); mk(V(51.2))
b.txt(V(51.7), 0.4, "Treffen", NX + 650, 600, 64, INK)
b.s(V(52.1), 0.25, line(NX + 540, 585, NX + 760, 585), RED, 9)
b.txt(V(52.4), 0.5, "abgesagt", NX + 650, 700, 56, RED)
b.txt(V(53.0), 0.4, ":)", NX + 870, 380, 90, GREEN, rot=1.4)
# O labels around hero
OX = 14700
b.key(V(53.8), NX + 650, 600, 1.6); b.key(V(54.5), OX, 600, 1.0); b.snd("schwenk.wav", V(53.8), 0.35)
stick(b, V(54.3), OX, 900, 1.5, dur=1.0, face="neutral", hero=True, w=10); mk(V(54.3))
labels = [("schüchtern?", OX - 560, 380, V(55.2), -0.08), ("einsam?", OX + 560, 330, V(56.6), 0.07), ("seltsam?", OX + 520, 760, V(57.7), -0.05)]
for s_, x, y, t0, r in labels:
    b.txt(t0, 0.6, s_, x, y, 96, RED, rot=r); b.snd("pop.wav", t0, 0.45)
b.s(V(55.8), 0.3, poly((OX - 400, 420), (OX - 120, 520)), RED, 7)
b.s(V(57.2), 0.3, poly((OX + 420, 370), (OX + 110, 500)), RED, 7)
b.s(V(58.3), 0.3, poly((OX + 360, 740), (OX + 110, 690)), RED, 7)
# P cross out labels, zoom into head
b.s(V(60.0), 0.25, line(OX - 790, 365, OX - 330, 355), INK, 10); mk(V(60.0))
b.s(V(60.3), 0.2, line(OX + 410, 315, OX + 710, 310), INK, 10)
b.s(V(60.55), 0.2, line(OX + 350, 745, OX + 690, 740), INK, 10)
PX = 17300
b.key(V(61.2), OX, 600, 1.0); b.key(V(62.2), PX, 560, 1.0); b.snd("schwenk.wav", V(61.2), 0.35)
def head_path(cx, cy, s_):
    P = lambda x, y: (cx + x * s_, cy + y * s_)
    pts = bez(P(-0.55, 1.0), P(-0.75, 0.35), P(-0.85, -0.55), P(-0.2, -0.85))
    pts += bez(P(-0.2, -0.85), P(0.35, -1.05), P(0.72, -0.6), P(0.62, -0.1))[1:]
    pts += poly(P(0.62, -0.1), P(0.8, 0.12), P(0.66, 0.2), P(0.68, 0.38), P(0.6, 0.46), P(0.64, 0.58), P(0.52, 0.66), P(0.3, 0.66), P(0.28, 1.0), n=5)[1:]
    return pts
HC = (PX - 330, 600)
b.s(V(61.9), 1.0, head_path(HC[0], HC[1], 380), INK, 14); mk(V(61.9))
def headpattern(ctx, t):
    if t < V(62.9): return
    cols = [BLUE, RED, GREEN, ORANGE]
    for i, r in enumerate((45, 85, 125, 165)):
        f = ease_out(prog(t, V(62.9 + i * 0.3), V(63.8 + i * 0.3)))
        if f <= 0: continue
        ctx.set_source_rgba(*cols[i]); ctx.set_line_width(14)
        n = 80; ctx.new_path()
        wob_ = 0.07 + 0.02 * math.sin(t * 2 + i)
        for k in range(int(n * f) + 1):
            a = -math.pi * 0.95 + 1.75 * math.pi * k / n
            rr = r * (1 + wob_ * math.sin(5 * a + i + t * 0.8))
            ctx.line_to(HC[0] - 20 + math.cos(a) * rr * 1.12, HC[1] - 90 + math.sin(a) * rr)
        ctx.stroke()
b.dyn.append(headpattern)
for k in range(4): mk(V(62.9 + k * 0.3), 0.35)
b.snd("aha_funkeln.wav", V(63.6), 0.5)
# Q "Heute schauen wir uns an, was im Gehirn ... passiert ... – und warum das oft eine Stärke ist, keine Schwäche."
b.txt(V(65.0), 1.4, "Was passiert im Kopf?", PX + 420, 330, 100, BLUE); mk(V(65.0))
b.s(V(66.4), 0.3, line(PX + 30, 360, PX + 810, 365), BLUE, 7)
b.txt(V(69.6), 0.6, "Stärke", PX + 420, 600, 130, GREEN, rot=-0.04); mk(V(69.6))
b.txt(V(70.5), 0.4, "statt", PX + 420, 700, 64, GREY)
b.txt(V(71.2), 0.6, "Schwäche", PX + 420, 820, 100, RED, rot=0.03)
b.s(V(71.9), 0.25, line(PX + 210, 790, PX + 630, 800), INK, 10)
# end title card
TX = 19800
b.key(V(72.9), PX, 560, 1.0); b.key(V(73.7), TX, 560, 1.0); b.snd("schwenk.wav", V(72.9), 0.35)
b.txt(V(73.6), 1.3, "Die Psychologie von Menschen,", TX, 470, 110, INK); mk(V(73.6))
b.snd("klang.wav", V(75.9), 0.45)
b.txt(V(74.9), 1.0, "die gern allein sind", TX, 620, 130, BLUE); mk(V(74.9))
b.s(V(75.9), 0.4, bez((TX - 520, 670), (TX - 200, 700), (TX + 200, 640), (TX + 520, 680)), RED, 9)

if __name__ == "__main__":
    import sys
    dur = float(sys.argv[1]) if len(sys.argv) > 1 else round(78.0 + DELTA, 2)
    render(b, "/home/claude/pilot/denkmuster_pilot_intro.mp4", dur, "/home/claude/pilot/intro_vo2.wav", O)
    print("ok")
