"""Denkmuster 001 – Hauptteil (Kapitel 1–8 + Schluss). Wortgenaue Zeiten aus vo/k*.json."""
import json, math, re, subprocess
from wb import *
from icons import *

CARD, GAP = 5.0, 0.7
TITLES = ["Schüchtern ist nicht dasselbe", "Das Zitronen-Experiment", "Das Belohnungssystem", "Der soziale Kater",
          "Was Alleinsein im Kopf macht", "Der Grund entscheidet", "Das Gegenteil von Einsamkeit", "Was du daraus machen kannst", None]
WORDS = [json.load(open(f"vo/k{i}.json")) for i in range(9)]
CT = []; t = 0.0
for i, d in enumerate(WORDS):
    CT.append(t); t += (CARD if TITLES[i] else 0.8) + d["dur"] + GAP
TOTAL = t + 1.5
VSTART = [CT[i] + (CARD if TITLES[i] else 0.8) for i in range(9)]

MISSING = []
norm = lambda w: re.sub(r"[^\wäöüß]", "", w.lower())
def at(k, phrase, nth=0, end=False):
    ws = WORDS[k]["words"]; ph = [norm(x) for x in phrase.split()]
    hits = [i for i in range(len(ws) - len(ph) + 1) if all(norm(ws[i + j]["w"]).startswith(ph[j]) for j in range(len(ph)))]
    if len(hits) <= nth:
        MISSING.append(f"K{k}: {phrase}"); return VSTART[k] + 1.0
    w = ws[hits[nth] + len(ph) - 1] if end else ws[hits[nth]]
    return VSTART[k] + (w["e"] if end else w["s"])

b = Board()
MK = ["marker_strich.wav", "marker_kurz.wav"]; _m = [0]
def mk(t, v=0.55): b.snd(MK[_m[0] % 2], t, v); _m[0] += 1
def pop(t, v=0.45): b.snd("pop.wav", t, v)
def P(k, p): return (p * 2000 + 960, k * 1700 + 540)
cam = [P(0, -1)[0], P(0, -1)[1], 1.0]
b.key(0, *cam)
def go(t, x, y, z=1.0, d=0.6, sound=True):
    b.key(t, *cam); b.key(t + d, x, y, z); cam[:] = [x, y, z]
    if sound: b.snd("schwenk.wav", t, 0.3)
def gop(t, k, p, z=1.0, dx=0, dy=0): x, y = P(k, p); go(t, x + dx, y + dy, z)

def chapter_card(k):
    x, y = P(k, -1)
    t0 = CT[k]
    if k > 0: go(t0, x, y, 1.0, d=0.7)
    t1 = t0 + 0.5
    b.s(t1, 0.5, circle(x - 560, y, 95), BLUE, 10); b.txt(t1 + 0.4, 0.3, str(k + 1), x - 560, y + 42, 130, BLUE)
    b.txt(t1 + 0.6, 1.1, TITLES[k], x + 120, y + 40, 100, INK)
    b.s(t1 + 1.7, 0.3, line(x - 400, y + 85, x + 640, y + 92), RED, 8)
    b.snd("klang.wav", t1 + 0.4, 0.35); mk(t1 + 0.6)

def fig(t, x, y, s=1.0, dur=0.7, **kw): return stick(b, t, x, y, s, dur=dur, **kw)

# ===================== K1 Schüchtern ist nicht dasselbe =====================
k = 0; chapter_card(k)
X, Y = P(k, 0); gop(VSTART[k] - 0.6, k, 0)
t = at(k, "Fangen wir"); label(b, t, "Das größte Missverständnis", X, Y - 330, 100, RED); mk(t)
t = at(k, "Wer gern allein ist"); fig(t, X - 420, Y + 420, 1.25, face="worried"); mk(t)
label(b, t + 0.6, "schüchtern", X - 420, Y - 130, 80, RED)
t = at(k, "Aber das sind"); fig(t, X + 420, Y + 420, 1.25, hero=True, face="neutral"); mk(t)
label(b, t + 0.6, "introvertiert", X + 420, Y - 130, 80, BLUE)
b.s(t + 1.0, 0.2, line(X - 70, Y + 60, X + 70, Y + 60, n=4), INK, 12); b.s(t + 1.2, 0.2, line(X - 70, Y + 130, X + 70, Y + 130, n=4), INK, 12)
b.s(t + 1.4, 0.2, line(X + 50, Y + 10, X - 50, Y + 180, n=4), RED, 12); pop(t + 1.4)
X, Y = P(k, 1); t = at(k, "Die Autorin"); gop(t - 0.3, k, 1)
book(b, t + 0.2, X - 420, Y + 40, "Still"); mk(t + 0.2)
label(b, at(k, "Susan Cain"), "Susan Cain", X - 420, Y + 330, 70, INK)
label(b, at(k, "erklärt den Unterschied"), "Der Unterschied:", X + 380, Y - 250, 90, INK)
t = at(k, "Schüchternheit ist die Angst"); X, Y = P(k, 2); gop(t - 0.3, k, 2)
fig(t, X - 450, Y + 430, 1.2, face="worried"); mk(t)
for i, (ex, ey) in enumerate(((X - 700, Y - 40), (X - 450, Y - 160), (X - 200, Y - 40))): eye(b, t + 0.8 + i * 0.25, ex, ey, 0.9)
label(b, at(k, "bewertet"), "Angst vor Bewertung", X - 450, Y - 330, 70, RED); pop(at(k, "bewertet"))
t = at(k, "Introversion dagegen"); couch(b, t, X + 450, Y + 430); fig(t + 0.5, X + 400, Y + 410, 1.0, pose="sit", face="happy", hero=True); mk(t)
label(b, at(k, "ruhigere"), "mag es ruhig", X + 450, Y - 330, 70, BLUE); pop(at(k, "ruhigere"))
t = at(k, "Schüchternheit tut weh")
for i in range(3): b.s(t + i * 0.12, 0.12, poly((X - 650 + i * 30, Y + 60), (X - 620 + i * 30, Y + 20), (X - 600 + i * 30, Y + 70), (X - 570 + i * 30, Y + 25), n=2), RED, 6)
label(b, t + 0.2, "tut weh", X - 220, Y + 180, 64, RED)
t = at(k, "Introversion nicht"); check(b, t, X + 650, Y + 120, 1.2); label(b, t + 0.2, "tut nicht weh", X + 450, Y + 560 - 380, 56, GREEN)
# party door
t = at(k, "Ein schüchterner Mensch"); X, Y = P(k, 3); gop(t - 0.3, k, 3)
door(b, t, X + 300, Y + 420, "Party"); notes(b, t + 0.6, X + 470, Y - 30, 3, BLUE); mk(t)
fig(t + 0.6, X - 420, Y + 420, 1.1, face="worried")
heart(b, at(k, "würde gern"), X - 420, Y - 60, 2.2)
t = at(k, "traut sich nicht"); b.s(t, 0.4, poly((X - 300, Y + 300), (X + 120, Y + 300)), INK, 8); cross(b, t + 0.4, X - 90, Y + 300, 0.9); pop(t + 0.4)
t = at(k, "Ein introvertierter Mensch"); fig(t, X + 700, Y + 420, 1.1, hero=True, face="neutral"); mk(t)
b.txt(at(k, "problemlos"), 0.4, "kann hingehen", X + 700, Y - 140, 54, GREEN)
t = at(k, "keine Lust"); bubble(b, t - 0.3, X + 700, Y - 300, 330, 140, "keine Lust", 56, BLUE, tail=(1, 1))
# shy extroverts
t = at(k, "Und es gibt sogar"); X, Y = P(k, 4); gop(t - 0.3, k, 4)
for i, px in enumerate((X - 650, X - 380, X + 380, X + 650)): fig(t + i * 0.15, px, Y + 430, 0.85, dur=0.45, face="happy")
fig(t + 0.6, X, Y + 430, 1.15, face="happy", col=BLUE); mk(t)
label(b, at(k, "extrovertiert sind"), "schüchtern + extrovertiert", X, Y - 380, 74, BLUE)
heart(b, at(k, "lieben Gesellschaft"), X, Y - 110, 2.0)
bubble(b, at(k, "Angst vor dem"), X + 330, Y - 140, 300, 120, "H-hallo …", 52, INK, tail=(-1, 1)); pop(at(k, "Angst vor dem"))
# population
t = at(k, "keine kleine Minderheit"); X, Y = P(k, 5); gop(t - 0.3, k, 5)
for r in range(2):
    for c in range(6):
        hi = (r * 6 + c) % 3 == 0 or (r * 6 + c) == 7
        fig(t + (r * 6 + c) * 0.12, X - 700 + c * 280, Y + 80 + r * 420, 0.75, dur=0.35, face="neutral", hero=hi, w=7)
mk(t); mk(t + 0.8)
t = at(k, "ein Drittel"); label(b, t, "1/3 bis 1/2", X, Y - 380, 120, BLUE); pop(t, 0.5)
label(b, at(k, "jeder zweite"), "jeder 2. oder 3.", X + 520, Y - 250, 60, INK)

# ===================== K2 Das Zitronen-Experiment =====================
k = 1; chapter_card(k)
X, Y = P(k, 0); gop(VSTART[k] - 0.6, k, 0)
t = at(k, "Aber warum");
for i, px in enumerate((X - 600, X - 350, X - 100)): fig(t + i * 0.15, px, Y + 430, 0.8, dur=0.4, face="happy")
notes(b, t + 0.4, X - 600, Y - 40, 4, INK); b.txt(t + 0.8, 0.5, "Trubel", X - 350, Y - 230, 80, RED); mk(t)
b.txt(t + 1.3, 0.3, "?", X + 300, Y + 100, 260, BLUE)
t = at(k, "Sechzigerjahren"); label(b, t, "1960er", X + 500, Y - 330, 90, GREY)
t = at(k, "Hans und Sybil"); label(b, t, "Hans & Sybil Eysenck", X + 500, Y - 200, 64, INK); bulb(b, at(k, "eine Idee"), X + 750, Y + 220); b.snd("aha_funkeln.wav", at(k, "eine Idee"), 0.4)
t = at(k, "Introvertierte Gehirne"); X, Y = P(k, 1); gop(t - 0.4, k, 1)
brain(b, t, X - 450, Y - 40, 1.4, RED); mk(t)
for i in range(4):
    b.s(t + 0.8 + i * 0.15, 0.15, poly((X + 150 + i * 150, Y + 380 - i * 110), (X + 300 + i * 150, Y + 380 - i * 110)), INK, 8)
    b.s(t + 0.95 + i * 0.15, 0.1, line(X + 300 + i * 150, Y + 380 - i * 110, X + 300 + i * 150, Y + 270 - i * 110, n=3), INK, 8)
t2 = at(k, "höheren Stufe"); b.s(t2, 0.3, circle(X + 600, Y + 50, 70, n=30), BLUE, 7); label(b, t2 + 0.2, "Introvertierte", X + 600, Y - 70, 52, BLUE)
label(b, at(k, "Grund-Erregungsniveau") if False else at(k, "Ihr Grund"), "Grund-Erregung: höher", X, Y - 380, 80, RED); pop(at(k, "Ihr Grund"))
t = at(k, "ungewöhnlichen Werkzeug"); X, Y = P(k, 2); gop(t - 0.4, k, 2)
_mq = b.mark(); b.txt(t, 0.4, "?", X - 450, Y + 40, 240, GREY); b.clear(_mq, b.mark(), at(k, "Zitronensaft", 0) - 0.3)
t = at(k, "Zitronensaft", 0); lemon(b, t, X - 450, Y + 20, 2.0); b.snd("aha_funkeln.wav", t, 0.35); mk(t)
label(b, t + 0.3, "Zitronensaft", X - 450, Y + 260, 80, ORANGE)
t = at(k, "Hundert Versuchspersonen"); label(b, t, "100 Personen", X + 420, Y - 360, 80, INK)
for i in range(4): drop(b, at(k, "vier Tropfen") + i * 0.18, X + 270 + i * 100, Y - 170, 1.0, ORANGE)
b.txt(at(k, "vier Tropfen") + 0.8, 0.3, "4 Tropfen", X + 420, Y - 50, 64, ORANGE); pop(at(k, "vier Tropfen"))
t = at(k, "Speichel sie"); b.many(t - 0.6, 0.6, [poly((X + 260, Y + 120), (X + 300, Y + 420), (X + 540, Y + 420), (X + 580, Y + 120))], INK, 8)
for i in range(4): b.s(t + i * 0.1, 0.1, line(X + 520, Y + 380 - i * 60, X + 560, Y + 380 - i * 60, n=2), INK, 5)
label(b, t, "Speichel?", X + 420, Y + 520 - 30, 60, BLUE); mk(t - 0.6)
t = at(k, "Das Ergebnis"); X, Y = P(k, 3); gop(t - 0.3, k, 3)
b.many(t, 0.5, [poly((X - 450, Y - 300), (X - 450, Y + 350), (X + 450, Y + 350))], INK, 8); mk(t)
def lemonbars(ctx, tt, X=X, Y=Y, t0=at(k, "Introvertierte produzierten")):
    for i, (val, col, x) in enumerate(((0.85, BLUE, X - 230), (0.45, RED, X + 200))):
        if tt < t0 + i * 0.8: continue
        f = ease_out(prog(tt, t0 + i * 0.8, t0 + i * 0.8 + 1.2)); h = 560 * val * f
        ctx.save(); ctx.rectangle(x - 110, Y + 350 - h, 220, h); ctx.clip(); ctx.set_source_rgba(*col); ctx.set_line_width(7)
        for kk in range(-20, 40): ctx.move_to(x - 110 + kk * 20, Y + 350); ctx.line_to(x - 110 + kk * 20 + 60, Y + 350 - 600)
        ctx.stroke(); ctx.restore(); ctx.set_source_rgba(*col); ctx.set_line_width(8); ctx.rectangle(x - 110, Y + 350 - h, 220, h); ctx.stroke()
b.dyn.append(lemonbars); b.snd("marker_strich.wav", at(k, "Introvertierte produzierten"), 0.5)
label(b, at(k, "Introvertierte produzierten") + 0.4, "Intro", X - 230, Y + 430, 64, BLUE)
label(b, at(k, "als Extrovertierte"), "Extro", X + 200, Y + 430, 64, RED)
label(b, at(k, "stärker auf"), "stärkere Reaktion", X, Y - 380, 80, INK); pop(at(k, "stärker auf"))
# volume knobs
t = at(k, "Lautstärkeregler"); X, Y = P(k, 4); gop(t - 0.5, k, 4)
dial(b, t, X - 450, Y + 120, "Introvertiert"); dial(b, t + 0.3, X + 450, Y + 120, "Extrovertiert"); mk(t); mk(t + 0.4)
dial_needle(b, X - 450, Y + 120, [(t + 1.0, 0.1), (at(k, "etwas höher"), 0.1), (at(k, "etwas höher") + 0.8, 0.55), (at(k, "roten Bereich") - 0.6, 0.55), (at(k, "roten Bereich"), 0.97)], t + 1.0)
notes(b, at(k, "laute Party"), X - 600, Y - 330, 4, RED); b.snd("pop_klein.wav", at(k, "roten Bereich"), 0.5)
dial_needle(b, X + 450, Y + 120, [(t + 1.3, 0.1), (at(k, "starten leiser"), 0.1), (at(k, "starten leiser") + 0.6, 0.2), (at(k, "mehr Lärm"), 0.2), (at(k, "mehr Lärm") + 1.0, 0.68)], t + 1.3)
notes(b, at(k, "mehr Lärm"), X + 300, Y - 330, 4, BLUE)
label(b, at(k, "wohlzufühlen"), "wohlfühlen :)", X + 450, Y + 330, 56, GREEN)
t = at(k, "Der Zitronentest ist alt"); X, Y = P(k, 5); gop(t - 0.3, k, 5)
lemon(b, t, X - 450, Y, 1.4); label(b, t + 0.3, "1967", X - 450, Y + 200, 70, GREY)
label(b, at(k, "kein Beweis"), "kein Beweis", X + 300, Y - 200, 90, RED); pop(at(k, "kein Beweis"))
t = at(k, "Aber er hat"); b.txt(t, 0.4, "?", X + 300, Y + 200, 220, BLUE); label(b, t + 0.6, "aber: eine neue Frage", X + 300, Y + 380, 64, BLUE); mk(t)

# ===================== K3 Das Belohnungssystem =====================
k = 2; chapter_card(k)
X, Y = P(k, 0); gop(VSTART[k] - 0.6, k, 0)
t = at(k, "Moderne Hirnscans"); scanner(b, t, X + 150, Y + 30); mk(t)
fig(t + 0.6, X - 140, Y + 90, 0.45, dur=0.4, pose="sit", face="neutral", w=6)
label(b, at(k, "zweiten Teil"), "Teil 2 der Antwort", X, Y - 380, 80, BLUE)
t = at(k, "Belohnungssystem", 0); X, Y = P(k, 1); gop(t - 0.4, k, 1)
brain(b, t, X - 400, Y, 1.5, RED); label(b, t + 0.6, "Belohnungssystem", X - 400, Y - 300, 72, INK); mk(t)
t = at(k, "Dopamin")
for i, (mx, my) in enumerate(((X + 100, Y - 80), (X + 260, Y + 40), (X + 160, Y + 180), (X + 380, Y - 160))): molecule(b, t + i * 0.2, mx, my, 1.4, BLUE)
label(b, t + 0.2, "Dopamin", X + 300, Y + 360, 80, BLUE); pop(t)
bubble(b, at(k, "Mehr davon"), X + 550, Y - 300, 360, 150, "Mehr davon!", 60, GREEN, tail=(-1, 1)); b.snd("aha_funkeln.wav", at(k, "Mehr davon"), 0.35)
t = at(k, "Glücksspiel"); X, Y = P(k, 2); gop(t - 0.6, k, 2)
coin(b, t, X - 650, Y - 250); coin(b, t + 0.2, X - 530, Y - 300); coin(b, t + 0.4, X - 600, Y - 360); mk(t)
label(b, t + 0.2, "Glücksspiel im Scanner", X + 200, Y - 380, 70, INK)
t = at(k, "gewannen"); head_profile(b, t, X - 300, Y + 200, 230, INK, 9, 0.7); head_profile(b, t + 0.3, X + 450, Y + 200, 230, INK, 9, 0.7)
label(b, t + 0.6, "Intro", X - 300, Y + 520 - 20, 56, BLUE); label(b, t + 0.8, "Extro", X + 450, Y + 520 - 20, 56, RED)
t2 = at(k, "extrovertierten Teilnehmern")
wave(b, t2, X - 300, Y + 120, 220, 18, 3, BLUE, 0.6); wave(b, t2 + 0.3, X + 450, Y + 120, 220, 70, 3, RED, 0.6)
label(b, at(k, "stärker"), "stärker!", X + 450, Y - 150, 72, RED); pop(at(k, "stärker"))
t = at(k, "Für extrovertierte Menschen"); X, Y = P(k, 3); gop(t - 0.4, k, 3)
for i, px in enumerate((X - 700, X - 470, X - 240)): fig(t + i * 0.15, px, Y + 430, 0.8, dur=0.4, face="happy")
fig(t + 0.5, X + 50, Y + 430, 1.0, face="happy", col=RED); mk(t)
for i, w_ in enumerate(("voller Raum", "neues Gesicht", "lautes Lachen")):
    tt = at(k, w_.split()[1]); coin(b, tt, X + 380 + i * 160, Y - 200 + (i % 2) * 90); b.snd("pop_klein.wav", tt, 0.5)
label(b, at(k, "kleiner Gewinn"), "= kleiner Gewinn", X + 520, Y + 60, 70, ORANGE)
t = at(k, "Bei introvertierten Menschen"); X, Y = P(k, 4); gop(t - 0.4, k, 4)
fig(t, X - 450, Y + 430, 1.1, hero=True, face="neutral"); mk(t)
wave(b, at(k, "Kick"), X - 450, Y - 270, 260, 15, 3, BLUE, 0.6); label(b, at(k, "schwächer"), "Kick: schwächer", X - 450, Y - 390, 66, BLUE)
check(b, at(k, "nicht schlimm"), X + 200, Y - 230, 1.2); label(b, at(k, "nicht schlimm") + 0.2, "nicht schlimm", X + 450, Y - 230, 60, GREEN)
coin(b, at(k, "nur weniger"), X + 330, Y + 30); label(b, at(k, "nur weniger") + 0.2, "nur weniger", X + 560, Y + 50, 60, ORANGE)
t = at(k, "Und genau deshalb"); X, Y = P(k, 5); gop(t - 0.4, k, 5)
b.many(t, 0.8, [line(X - 500, Y + 380, X + 500, Y + 380), line(X, Y + 380, X, Y - 100), poly((X - 450, Y + 60), (X + 450, Y - 120))], INK, 8); mk(t)
tt = at(k, "Arbeit"); b.s(tt, 0.4, rect(X - 560, Y + 60, 220, 160), INK, 8); label(b, tt + 0.2, "Arbeit", X - 450, Y + 160, 60, RED); pop(tt)
tt = at(k, "Belohnung"); coin(b, tt, X + 450, Y - 180); label(b, tt + 0.3, "Belohnung", X + 450, Y - 290, 60, ORANGE)

# ===================== K4 Der soziale Kater =====================
k = 3; chapter_card(k)
X, Y = P(k, 0); gop(VSTART[k] - 0.6, k, 0)
t = at(k, "Kennst du")
for i, px in enumerate((X - 700, X - 470, X - 240, X + 0)): fig(t + i * 0.15, px, Y + 430, 0.75, dur=0.4, face="happy")
fig(t + 0.6, X - 350, Y + 430, 1.0, hero=True, face="happy"); mk(t)
label(b, at(k, "gut gelaunt"), "gut gelaunt", X - 350, Y - 360, 70, GREEN)
label(b, at(k, "hat gelacht"), "haha!", X - 50, Y - 230, 70, ORANGE, rot=0.1); pop(at(k, "hat gelacht"))
t = at(k, "ein paar Stunden"); clock(b, t, X + 450, Y - 180, 90, "+ ein paar Stunden"); b.snd("uhr_ticken.wav", t, 0.2)
battery(b, t + 0.8, X + 450, Y + 250); battery_fill(b, X + 450, Y + 250, t + 1.2, at(k, "völlig leer") + 0.6, 0.9, 0.05)
label(b, at(k, "völlig leer"), "leer", X + 450, Y + 380, 66, RED)
t = at(k, "Universität Helsinki"); X, Y = P(k, 1); gop(t - 0.6, k, 1)
building(b, t, X - 450, Y + 250, "Uni Helsinki"); mk(t)
t = at(k, "mehrmals am Tag")
b.s(t, 0.5, poly((X + 50, Y + 200), (X + 850, Y + 200)), INK, 8)
for i in range(5):
    tt = t + 0.5 + i * 0.3; b.s(tt, 0.15, circle(X + 130 + i * 170, Y + 200, 20, n=14), BLUE, 7); b.snd("pop_klein.wav", tt, 0.35)
label(b, t + 0.4, "5× am Tag gefragt", X + 450, Y + 60, 64, BLUE)
label(b, at(k, "wie gesellig"), "Wie gesellig? Wie fühlst du dich?", X + 450, Y - 230, 52, INK)
t = at(k, "In dem Moment"); X, Y = P(k, 2); gop(t - 0.4, k, 2)
b.many(t, 0.5, [poly((X - 650, Y - 300), (X - 650, Y + 350), (X + 650, Y + 350))], INK, 8); mk(t)
b.s(t + 0.5, 1.0, bez((X - 620, Y + 250), (X - 400, Y + 200), (X - 300, Y - 200), (X - 150, Y - 150)), GREEN, 9)
label(b, at(k, "gute Laune"), "Laune", X - 300, Y - 260, 60, GREEN)
t = at(k, "drei Stunden"); clock(b, t, X + 120, Y - 100, 60); label(b, t + 0.4, "+3 Std.", X + 120, Y + 30, 60, RED); b.snd("uhr_ticken.wav", t, 0.2)
t = at(k, "müder"); b.s(t, 1.0, bez((X - 620, Y + 300), (X - 100, Y + 300), (X + 250, Y + 250), (X + 600, Y - 230)), RED, 9)
label(b, t + 0.6, "Müdigkeit", X + 470, Y - 280, 60, RED); zzz(b, t + 0.9, X + 520, Y - 380)
t = at(k, "überraschende Teil"); X, Y = P(k, 3); gop(t - 0.4, k, 3)
b.txt(t, 0.4, "!", X, Y - 250, 240, RED); pop(t, 0.5)
t = at(k, "nicht nur für Introvertierte"); fig(t, X - 450, Y + 430, 1.1, hero=True, face="sad"); zzz(b, t + 0.8, X - 380, Y - 160)
label(b, t + 0.5, "Intro", X - 450, Y - 300, 64, BLUE); mk(t)
t = at(k, "Auch extrovertierte"); fig(t, X + 450, Y + 430, 1.1, face="sad", col=RED); zzz(b, t + 0.8, X + 520, Y - 160)
label(b, t + 0.5, "Extro", X + 450, Y - 300, 64, RED)
t = at(k, "Eine wichtige Rolle"); X, Y = P(k, 4); gop(t - 0.4, k, 4)
label(b, t, "Wichtig:", X, Y - 380, 80, INK)
t = at(k, "wie vielen Menschen")
for i in range(10): fig(t + i * 0.12, X - 760 + i * 170, Y + 230, 0.55, dur=0.25, face="neutral", w=6)
b.snd("pop_klein.wav", t, 0.4); label(b, t + 1.2, "wie viele Menschen", X, Y + 380, 74, BLUE)
t = at(k, "Die Studie war klein"); X, Y = P(k, 5); gop(t - 0.4, k, 5)
b.many(t, 0.6, [circle(X - 450, Y - 60, 130), line(X - 360, Y + 30, X - 230, Y + 170)], INK, 10); label(b, t + 0.5, "kleine Studie", X - 450, Y + 330, 66, GREY); mk(t)
label(b, at(k, "bestätigt"), "muss noch bestätigt werden", X - 300, Y - 340, 56, GREY)
t = at(k, "keine Einbildung"); label(b, t, "keine Einbildung!", X + 430, Y - 120, 74, RED); pop(t)
t = at(k, "Ruhe"); couch(b, t - 0.6, X + 430, Y + 420); fig(t - 0.2, X + 390, Y + 400, 0.95, pose="sit", face="happy", hero=True)
label(b, t + 0.2, "Ruhe", X + 430, Y + 60, 80, GREEN)

# ===================== K5 Was Alleinsein im Kopf macht =====================
k = 4; chapter_card(k)
X, Y = P(k, 0); gop(VSTART[k] - 0.6, k, 0)
t = at(k, "Und was passiert"); b.s(t, 0.8, rect(X - 700, Y - 300, 700, 650), INK, 8); fig(t + 0.6, X - 380, Y + 330, 0.95, pose="sit", face="neutral", hero=True); mk(t)
t = at(k, "Universität Rochester"); building(b, t, X + 400, Y + 250, "Uni Rochester"); mk(t)
t = at(k, "eine Weile allein"); X, Y = P(k, 1); gop(t - 0.4, k, 1)
fig(t, X - 300, Y + 420, 1.2, pose="sit", face="neutral", hero=True); mk(t)
b.many(t + 0.6, 0.4, [rect(X + 150, Y - 120, 110, 200), circle(X + 205, Y + 55, 8, n=10)], INK, 7); cross(b, t + 1.1, X + 205, Y - 20, 1.3)
t = at(k, "ohne Gespräch"); bubble(b, t, X + 520, Y - 150, 230, 120, "…", 60, INK); cross(b, t + 0.6, X + 520, Y - 150, 1.0)
t = at(k, "Abschalteffekt"); X, Y = P(k, 2); gop(t - 0.5, k, 2)
label(b, t, "„Abschalteffekt“", X, Y - 390, 100, BLUE); b.snd("aha_funkeln.wav", t, 0.4)
t = at(k, "Starke Gefühle wurden ruhiger")
wave(b, t, X - 300, Y - 50, 900, 120, 5, RED, 1.0); mk(t)
b.s(t + 1.2, 0.5, poly((X + 200, Y - 50), (X + 300, Y - 50)), INK, 8); b.s(t + 1.6, 0.2, poly((X + 270, Y - 80), (X + 305, Y - 50), (X + 270, Y - 20)), INK, 8)
wave(b, t + 1.8, X + 600, Y - 50, 350, 20, 3, GREEN, 0.8)
label(b, at(k, "Stress"), "Stress, Ärger", X - 300, Y + 230, 64, RED)
label(b, at(k, "Begeisterung"), "auch Begeisterung", X - 300, Y + 340, 64, ORANGE)
t = at(k, "Dimmer"); X, Y = P(k, 3); gop(t - 0.5, k, 3)
dimmer(b, t, X - 300, Y + 40); dimmer_knob(b, X - 300, Y + 40, t + 0.8, t + 2.5, 0.92, 0.25, t + 0.5); mk(t)
label(b, t + 0.3, "Dimmer für Gefühle", X - 300, Y - 330, 70, INK)
t = at(k, "am stärksten entspannten"); fig(t, X + 450, Y + 430, 1.1, face="happy", hero=True); mk(t)
label(b, at(k, "selbst entschieden"), "selbst gewählt", X + 450, Y - 330, 70, GREEN); check(b, at(k, "selbst entschieden") + 0.4, X + 700, Y - 200, 1.0)
t = at(k, "Stromschlag-Studie") if True else 0
X, Y = P(k, 4); gop(t - 0.5, k, 4)
b.s(t, 0.4, circle(X - 450, Y + 230, 46, ry=20), INK, 8); b.s(t + 0.3, 0.3, arc(X - 450, Y + 222, 36, math.pi, 2 * math.pi, ry=24), RED, 12)
bolt = poly((X - 440, Y + 180), (X - 490, Y + 80), (X - 430, Y + 70), (X - 500, Y - 60), (X - 400, Y + 80), (X - 460, Y + 90), (X - 410, Y + 180))
b.s(t + 0.4, 0.3, bolt, YEL, 16); b.s(t + 0.4, 0.3, bolt, INK, 5); b.snd("stromschlag.wav", t + 0.4, 0.3)
label(b, at(k, "nicht freiwillig"), "nicht freiwillig", X - 450, Y - 230, 74, RED); pop(at(k, "nicht freiwillig"))
label(b, at(k, "mussten es"), "musste", X - 450, Y - 120, 60, RED)
t = at(k, "Genau da liegt"); label(b, t, "freiwillig = Erholung", X + 380, Y + 20, 80, GREEN); b.snd("aha_funkeln.wav", t, 0.35)

# ===================== K6 Der Grund entscheidet =====================
k = 5; chapter_card(k)
X, Y = P(k, 0); gop(VSTART[k] - 0.6, k, 0)
t = at(k, "Warum bist du allein"); label(b, t, "Warum bist du allein?", X, Y - 250, 110, BLUE); mk(t)
fig(t + 0.7, X, Y + 430, 1.0, hero=True, face="neutral")
t = at(k, "ersten Jahr"); X, Y = P(k, 1); gop(t - 0.6, k, 1)
building(b, t - 0.4, X - 500, Y + 250, "1. Jahr an der Uni"); mk(t)
t = at(k, "weil er sie genoss"); fig(t, X + 250, Y + 430, 1.0, hero=True, face="happy"); book(b, t + 0.6, X + 600, Y - 100, ""); mk(t)
label(b, at(k, "besseres Selbstwertgefühl"), "Selbstwert höher", X + 400, Y - 380, 74, GREEN)
label(b, at(k, "weniger einsam"), "weniger einsam", X - 300, Y - 380, 66, GREEN); pop(at(k, "weniger einsam"))
t = at(k, "Wer dagegen allein war"); X, Y = P(k, 2); gop(t - 0.4, k, 2)
fig(t, X - 300, Y + 430, 1.1, face="sad"); cloud(b, t + 0.6, X - 300, Y - 230, 1.4); mk(t)
label(b, at(k, "abgelehnt"), "unwohl / abgelehnt", X + 330, Y - 180, 70, RED)
label(b, at(k, "schlechter"), "geht es schlechter", X + 330, Y - 60, 60, RED)
t = at(k, "Buffalo"); X, Y = P(k, 3); gop(t - 0.5, k, 3)
building(b, t, X - 500, Y + 250, "Uni Buffalo"); mk(t)
label(b, at(k, "fast dreihundert"), "≈ 300 Befragte", X + 350, Y - 360, 74, INK)
t = at(k, "aus Angst"); X, Y = P(k, 4); gop(t - 0.4, k, 4)
fig(t, X - 450, Y + 430, 1.1, face="worried"); label(b, t + 0.4, "aus Angst", X - 450, Y - 330, 70, RED); mk(t)
bulb(b, t + 0.8, X - 450, Y - 120, GREY)
t = at(k, "ohne Angst"); fig(t, X + 450, Y + 430, 1.1, face="happy", hero=True); label(b, t + 0.4, "einfach gern allein", X + 450, Y - 330, 64, GREEN); mk(t)
bulb(b, at(k, "kreativer"), X + 450, Y - 140, ORANGE); b.snd("aha_funkeln.wav", at(k, "kreativer"), 0.4)
label(b, at(k, "kreativer") + 0.4, "kreativer", X + 700, Y - 40, 56, ORANGE)
t = at(k, "Die Motivation zählt"); X, Y = P(k, 5); gop(t - 0.8, k, 5)
label(b, t, "Die Motivation zählt.", X, Y + 20, 130, BLUE); b.s(t + 1.0, 0.4, bez((X - 600, Y + 80), (X - 200, Y + 120), (X + 200, Y + 50), (X + 600, Y + 90)), RED, 9); mk(t)

# ===================== K7 Das Gegenteil von Einsamkeit =====================
k = 6; chapter_card(k)
X, Y = P(k, 0); gop(VSTART[k] - 0.6, k, 0)
t = at(k, "kaum jemand kennt"); b.txt(t, 0.4, "?", X + 500, Y, 260, BLUE); mk(t)
t = at(k, "Einsamkeit"); fig(t, X - 400, Y + 430, 1.1, face="sad"); label(b, t + 0.3, "Einsamkeit", X - 400, Y - 330, 80, INK); mk(t)
label(b, at(k, "zu wenig Kontakt"), "zu wenig Kontakt", X - 400, Y - 210, 56, GREY)
t = at(k, "Robert Coplan"); X, Y = P(k, 1); gop(t - 0.6, k, 1)
label(b, t, "Robert Coplan", X - 400, Y - 350, 80, INK); label(b, t + 0.6, "Kanada", X - 400, Y - 240, 56, GREY)
t = at(k, "zu wenig Zeit für sich")
for i, px in enumerate((X + 250, X + 450, X + 650, X + 350, X + 550)): fig(t + i * 0.12, px, Y + 300 + (i // 3) * 150, 0.7, dur=0.35, face="neutral", w=7)
fig(t + 0.6, X - 400, Y + 430, 1.1, face="worried", hero=True); mk(t)
t = at(k, "eigenen Namen"); X, Y = P(k, 2); gop(t - 0.4, k, 2)
label(b, at(k, "aloneliness"), "„Aloneliness“", X, Y - 120, 150, BLUE); b.snd("aha_funkeln.wav", at(k, "aloneliness"), 0.45)
label(b, at(k, "aloneliness") + 1.2, "= zu wenig Zeit allein", X, Y + 60, 70, GREY)
t = at(k, "Wer das Gefühl"); X, Y = P(k, 3); gop(t - 0.4, k, 3)
fig(t, X - 450, Y + 430, 1.1, face="sad", hero=True); mk(t)
label(b, at(k, "gestresster"), "mehr Stress", X + 300, Y - 250, 90, RED); pop(at(k, "gestresster"))
label(b, at(k, "unzufriedener"), "weniger zufrieden", X + 300, Y - 80, 90, RED); pop(at(k, "unzufriedener"))
t = at(k, "kein Luxus"); X, Y = P(k, 4); gop(t - 0.5, k, 4)
label(b, t, "Ruhe ist kein Luxus –", X, Y - 120, 100, INK); mk(t)
label(b, at(k, "echtes Bedürfnis"), "sondern ein Bedürfnis.", X, Y + 50, 100, GREEN); b.s(at(k, "echtes Bedürfnis") + 0.9, 0.4, bez((X - 520, Y + 100), (X - 200, Y + 130), (X + 200, Y + 70), (X + 520, Y + 110)), RED, 9)

# ===================== K8 Was du daraus machen kannst =====================
k = 7; chapter_card(k)
X, Y = P(k, 0); gop(VSTART[k] - 0.6, k, 0)
t = at(k, "Was heißt das"); fig(t, X, Y + 430, 1.1, hero=True, face="happy"); mk(t)
t = at(k, "Erstens"); X, Y = P(k, 1); gop(t - 0.4, k, 1)
b.s(t, 0.3, circle(X - 760, Y - 300, 55), BLUE, 8); b.txt(t + 0.2, 0.2, "1", X - 760, Y - 270, 80, BLUE)
label(b, t + 0.3, "Ruhe einplanen", X - 320, Y - 270, 90, INK); mk(t)
tt = at(k, "blocke dir"); b.many(tt, 0.6, [rect(X - 300, Y - 100, 600, 450), line(X - 300, Y - 20, X + 300, Y - 20)], INK, 8)
for i in range(3): b.s(tt + 0.6 + i * 0.1, 0.1, line(X - 280, Y + 40 + i * 90, X + 280, Y + 40 + i * 90, n=6), GREY, 4)
b.s(tt + 0.9, 0.4, rect(X - 260, Y + 220, 520, 90), GREEN, 8); label(b, tt + 1.2, "Zeit für mich", X, Y + 285, 56, GREEN)
t = at(k, "Zweitens"); X, Y = P(k, 2); gop(t - 0.4, k, 2)
b.s(t, 0.3, circle(X - 760, Y - 300, 55), BLUE, 8); b.txt(t + 0.2, 0.2, "2", X - 760, Y - 270, 80, BLUE)
label(b, t + 0.3, "Aktiv entscheiden", X - 300, Y - 270, 90, INK); mk(t)
tt = at(k, "Ich kann leider"); bubble(b, tt, X - 350, Y + 50, 520, 170, "Ich kann leider nicht …", 50, GREY); cross(b, tt + 1.5, X - 350, Y + 50, 1.2)
tt = at(k, "Ich nehme mir"); bubble(b, tt, X + 380, Y + 250, 560, 190, "Ich nehme mir Zeit für mich.", 48, GREEN, tail=(1, 1)); check(b, tt + 1.8, X + 690, Y + 100, 1.0)
t = at(k, "Drittens"); X, Y = P(k, 3); gop(t - 0.4, k, 3)
b.s(t, 0.3, circle(X - 760, Y - 300, 55), BLUE, 8); b.txt(t + 0.2, 0.2, "3", X - 760, Y - 270, 80, BLUE)
label(b, t + 0.3, "Auf die Anzahl achten", X - 230, Y - 270, 90, INK); mk(t)
tt = at(k, "Ein langes Gespräch"); fig(tt, X - 600, Y + 430, 0.9, face="happy", hero=True); fig(tt + 0.3, X - 380, Y + 430, 0.9, face="happy")
battery(b, tt + 0.6, X - 490, Y - 60); battery_fill(b, X - 490, Y - 60, tt + 1.0, tt + 2.0, 0.9, 0.7)
tt = at(k, "zehn kurze")
for i in range(8): fig(tt + i * 0.1, X + 120 + (i % 4) * 160, Y + 230 + (i // 4) * 220, 0.5, dur=0.25, face="neutral", w=6)
battery(b, tt + 0.6, X + 380, Y - 160); battery_fill(b, X + 380, Y - 160, tt + 1.0, tt + 2.2, 0.9, 0.15); b.snd("pop_klein.wav", tt, 0.4)
t = at(k, "viertens"); X, Y = P(k, 4); gop(t - 0.4, k, 4)
b.s(t, 0.3, circle(X - 760, Y - 300, 55), BLUE, 8); b.txt(t + 0.2, 0.2, "4", X - 760, Y - 270, 80, BLUE)
label(b, t + 0.3, "Erklär es", X - 450, Y - 270, 90, INK); mk(t)
tt = at(k, "Wer weiß"); fig(tt, X - 300, Y + 430, 1.0, hero=True, face="happy"); fig(tt + 0.3, X + 300, Y + 430, 1.0, face="happy")
heart(b, at(k, "nicht persönlich"), X, Y + 30, 2.5); label(b, at(k, "nicht persönlich") + 0.3, "nicht persönlich", X, Y - 120, 64, RED)
t = at(k, "Und falls du merkst"); X, Y = P(k, 5); gop(t - 0.4, k, 5)
fig(t, X - 450, Y + 430, 1.1, face="worried"); mk(t)
label(b, at(k, "aus Angst"), "aus Angst?", X - 450, Y - 330, 80, RED)
label(b, at(k, "genauer hinzuschauen"), "genauer hinschauen", X + 380, Y - 200, 70, INK)
t = at(k, "Hilfe holen"); heart(b, t, X + 380, Y + 40, 3.0, GREEN); label(b, t + 0.3, "Hilfe ist okay", X + 380, Y + 230, 74, GREEN); b.snd("klang.wav", t, 0.25)

# ===================== Schluss =====================
k = 8
X, Y = P(k, 0); go(CT[k], X, Y, 1.0, d=0.7)
t = at(k, "nicht kaputt"); fig(VSTART[k], X, Y + 430, 1.2, hero=True, face="happy"); mk(VSTART[k])
for i, (w_, x_, y_) in enumerate((("nicht kaputt", X - 550, Y - 280), ("nicht unhöflich", X + 550, Y - 280), ("nicht einsam", X, Y - 380))):
    tt = at(k, w_.split()[1] if i else "kaputt"); label(b, tt, w_, x_, y_, 72, GREEN); b.snd("pop.wav", tt, 0.4)
t = at(k, "Vieles spricht"); X, Y = P(k, 1); gop(t - 0.4, k, 1)
brain(b, t, X - 550, Y - 80, 1.0, RED); label(b, t + 0.6, "reagiert wohl stärker", X - 550, Y + 140, 56, RED); mk(t)
t = at(k, "weniger Kick"); wave(b, t, X, Y - 80, 260, 15, 3, BLUE, 0.6); label(b, t + 0.5, "weniger Kick", X, Y + 140, 56, BLUE)
t = at(k, "Ruhe hilft"); plug(b, t, X + 550, Y - 80); label(b, at(k, "Ladestation"), "Ladestation", X + 550, Y + 140, 56, GREEN); b.snd("aha_funkeln.wav", t, 0.35)
t = at(k, "Wichtig ist nur"); X, Y = P(k, 2); gop(t - 0.4, k, 2)
label(b, at(k, "weil man es will"), "allein, weil man es will", X, Y - 150, 96, GREEN); mk(at(k, "weil man es will"))
label(b, at(k, "nicht, weil"), "– nicht aus Angst", X, Y + 20, 80, RED)
t = at(k, "nächste Mal"); X, Y = P(k, 3); gop(t - 0.4, k, 3)
door(b, t, X - 450, Y + 420, "Party"); cross(b, t + 0.8, X - 450, Y + 250, 1.4); mk(t)
couch(b, t + 1.2, X + 350, Y + 420); fig(t + 1.6, X + 310, Y + 400, 1.0, pose="sit", face="happy", hero=True)
label(b, at(k, "nicht rechtfertigen"), "Du musst dich nicht rechtfertigen.", X, Y - 360, 70, BLUE)
t = at(k, "Jetzt bin ich neugierig"); X, Y = P(k, 4); gop(t - 0.4, k, 4)
comment_box(b, t, X, Y - 80); b.snd("schwenk.wav", t, 0.3)
label(b, at(k, "Ruhe braucht"), "Ruhe tanken?", X - 60, Y - 70, 70, BLUE)
label(b, at(k, "lädst du"), "oder bei anderen?", X + 60, Y + 20, 56, RED)
label(b, at(k, "Kommentare"), "Schreib's in die Kommentare!", X, Y + 300, 80, INK); mk(at(k, "Kommentare"))
t = at(k, "Abonniere"); X, Y = P(k, 5); gop(t - 0.6, k, 5)
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
b.txt(t, 0.8, "Denkmuster", X + 200, Y - 30, 150, INK); b.txt(t + 0.5, 0.3, "abonnieren", X + 200, Y + 90, 70, BLUE); mk(t)
tt = at(k, "Glocke"); bell(b, tt, X + 620, Y + 260); b.snd("pop.wav", tt, 0.5)

if __name__ == "__main__":
    import sys
    # audio: concatenated chapter voices placed at VSTART
    inputs, filt, lab = [], [], ""
    for i in range(9):
        inputs += ["-i", f"vo/k{i}.mp3"]; ms = int(VSTART[i] * 1000)
        filt.append(f"[{i}:a]aformat=channel_layouts=stereo,aresample=48000,adelay={ms}|{ms}[v{i}]"); lab += f"[v{i}]"
    filt.append(lab + f"amix=inputs=9:normalize=0:duration=longest,apad,atrim=0:{TOTAL}[o]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filt), "-map", "[o]", "vo/main_vo.wav"], check=True)
    if MISSING: print("FEHLEND:", MISSING); sys.exit(1)
    dur = float(sys.argv[1]) if len(sys.argv) > 1 else TOTAL
    print("TOTAL", TOTAL, "items", len(b.items))
    render(b, "/home/claude/pilot/denkmuster_main.mp4", dur, "/home/claude/pilot/vo/main_vo.wav", 0.0)
    print("ok")
