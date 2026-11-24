"""Denkmuster 004 – Der Halo-Effekt: Warum schöne Menschen klüger wirken.
Szenen mit engine/kit.py + engine/bausteine.py (ein Satz = ein Bild, Wortzeiten aus vo/k*.json).
Jede Einstellung wird mit S(...) gesetzt – daraus entsteht bilddrehbuch.json (python3 scenes.py --drehbuch).
Sounds: assets/sfx + Laurins Goldsmith-Sounds sub_drop/slap/paper (für alle Kanäle frei, EFFEKTE.md „Sound je Effekt“)
als gs_*.wav; DM_SFX zeigt auf einen Ordner mit beiden (siehe INFO.md)."""
import os, sys, math, json
import cairo
HERE_ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE_, "..", "..", "engine"))
from kit import *
from bausteine import *

TITLES = [None, "Der Heiligenschein", "Schön gleich gut?", "Der Aufsatz", "Eine Sekunde reicht",
          "Im Gerichtssaal", "Du merkst es nicht", "Auch bei Dingen", "So trickst du ihn aus", None]
v = Video(__file__, titles=TITLES, music_plan=[1, 3, 2, 4, 3, 4, 1, 2, 2, 5], hook_music_from=8.0)
b = v.b
A = v.at
SHOTS = []
# Farbregel (EFFEKTE.md): Schwarz auf Weiß, Blau/Orange nur an der Hauptfigur, Rot = Betonung
_check, _bell, _bulb, _building = check, bell, bulb, building
def building(b_, t, x, y, txt=None):
    _building(b_, t, x, y, None)
    if txt: b_.txt(t + 0.8, 0.4, txt, x, y + 70, 56, INK)
def check(b_, t, x, y, s=1.0, col=INK): _check(b_, t, x, y, s, col)
def bell(b_, t, x, y, col=INK): _bell(b_, t, x, y, col)
def bulb(b_, t, x, y, col=INK): _bulb(b_, t, x, y, col)

def S(k, phrase, anim, zeigt, inhalt=("geschehen",), gen="schema", neu="", num="", nth=0):
    t = A(k, phrase, nth)
    SHOTS.append(dict(t=t, k=k, animation=anim, zeigt=zeigt, inhalt=list(inhalt), genauigkeit=gen, neugier=neu, num=num))
    return t

def pan(k, p, t, z=1.0, dx=0, dy=0, sound=False):
    x, y = v.P(k, p); v.go(t - 0.4, x + dx, y + dy, z, d=0.6, sound=sound); return x, y

def fig(t, x, y, s=1.0, **kw): return v.fig(t, x, y, s, **kw)

# ---------- Sound-Plan (EFFEKTE.md, Version 2) ----------
def treffer(t, v_=0.5):
    """Zahl wird eingekreist: tiefer trockener Treffer (sub_drop + leiser slap), kein aha_funkeln."""
    b.snd("gs_sub_drop.wav", t, v_); b.snd("gs_slap.wav", t, v_ * 0.35)

def zahl2(t, x, y, s, size=200, col=RED):
    """Zahl in Handschrift: erscheint, dann rot eingekreist mit tiefem Treffer."""
    zahl(b, t, x, y, s, size, col, kreis=True, sound=False); treffer(t + 0.6)
    return t + 1.0

def streich(t, x, y, s, size=90, t_strike=None):
    """Mythos durchstreichen mit trockenem Papier-Wisch (statt Stift-Klick / Knüllen)."""
    b.txt(t, max(0.4, 0.04 * len(s)), s, x, y, size, INK)
    ts = t_strike if t_strike is not None else t + 1.0
    L = len(s) * size * 0.25
    b.s(ts, 0.3, line(x - L, y - size * 0.2, x + L, y - size * 0.35, n=10), RED, 11)
    b.snd("gs_paper.wav", ts, 0.35)
    return ts + 0.3

# ---------- Zeichnungen dieses Videos ----------
def gesicht(t, x, y, s=1.0, haar=0, mund="neutral", col=INK, dur=0.8, w=7):
    """Gezeichnetes, erfundenes Gesicht (keine echte Person)."""
    R = 110 * s
    parts = [circle(x, y, R * 0.82, ry=R)]
    parts += [circle(x - 30 * s, y - 15 * s, 6 * s, n=8), circle(x + 30 * s, y - 15 * s, 6 * s, n=8)]
    parts += [line(x - 50 * s, y - 42 * s, x - 14 * s, y - 47 * s, n=4), line(x + 14 * s, y - 47 * s, x + 50 * s, y - 42 * s, n=4)]
    parts += [poly((x + 2 * s, y - 5 * s), (x - 9 * s, y + 25 * s), (x + 6 * s, y + 28 * s), n=3)]
    if mund == "happy": parts.append(arc(x, y + 38 * s, 30 * s, 0.35, 2.8, n=14))
    elif mund == "sad": parts.append(arc(x, y + 78 * s, 26 * s, 3.6, 5.8, n=14))
    else: parts.append(line(x - 22 * s, y + 55 * s, x + 22 * s, y + 55 * s, n=4))
    if haar == 0:
        parts.append(arc(x, y - 22 * s, R * 0.86, math.pi * 1.02, math.pi * 1.98, ry=R * 0.98))
    elif haar == 1:
        parts += [bez((x - R * 0.84, y + 30 * s), (x - R * 1.15, y - R * 1.4), (x + R * 1.15, y - R * 1.4), (x + R * 0.84, y + 30 * s)),
                  line(x - R * 0.84, y + 30 * s, x - R * 0.95, y + R * 1.05, n=5), line(x + R * 0.84, y + 30 * s, x + R * 0.95, y + R * 1.05, n=5)]
    else:
        parts += [circle(x - R * 0.6 + i * R * 0.3, y - R * 0.88 + (i % 2) * 10 * s, 26 * s, n=12) for i in range(5)]
    parts += [line(x - 24 * s, y + R * 0.98, x - 30 * s, y + R + 45 * s, n=3), line(x + 24 * s, y + R * 0.98, x + 30 * s, y + R + 45 * s, n=3)]
    b.many(t, dur, parts, col, w)
    return t + dur

def halo(t, x, y, w=140, col=RED):
    """Heiligenschein: Ring über dem Kopf, kurze Strahlen."""
    b.s(t, 0.45, circle(x, y, w, ry=w * 0.24), col, 9)
    for i in range(7):
        a = math.pi * (1.1 + 0.8 * i / 6)
        b.s(t + 0.4 + i * 0.05, 0.08, line(x + math.cos(a) * w * 1.15, y + math.sin(a) * w * 0.4, x + math.cos(a) * w * 1.45, y + math.sin(a) * w * 0.55, n=3), col, 6)
    return t + 0.8

def blatt(t, x, y, w=300, h=400, n=6, foto=None, col=INK):
    """Blatt Papier mit Textzeilen; foto=(haar, mund) setzt ein kleines Passfoto oben rechts."""
    b.s(t, 0.4, rect(x - w / 2, y - h / 2, w, h), col, 7)
    for i in range(n):
        ww = w * (0.7 if foto and i < 2 else 0.8) * (0.75 if i == n - 1 else 1)
        b.s(t + 0.3 + i * 0.06, 0.08, line(x - w * 0.4, y - h * 0.3 + i * h * 0.12, x - w * 0.4 + ww * (0.7 if foto and i < 2 else 1), y - h * 0.3 + i * h * 0.12, n=5), GREY, 5)
    if foto:
        fx, fy = x + w * 0.27, y - h * 0.3
        b.s(t + 0.5, 0.2, rect(fx - 50, fy - 60, 100, 120), col, 5)
        gesicht(t + 0.6, fx, fy, 0.38, foto[0], foto[1], dur=0.4, w=4)

def note(t, x, y, txt, col=RED, size=90):
    b.txt(t, 0.3, txt, x, y + size * 0.3, size, col)
    b.s(t + 0.3, 0.3, circle(x, y, max(size * 0.7, len(txt) * size * 0.32), ry=size * 0.7), col, 6)

def urne(t, x, y, s=1.0):
    b.many(t, 0.5, [rect(x - 120 * s, y - 140 * s, 240 * s, 180 * s), line(x - 50 * s, y - 140 * s, x + 50 * s, y - 140 * s, n=3)], INK, 8)
    b.s(t + 0.5, 0.25, rect(x - 40 * s, y - 230 * s, 80 * s, 100 * s), INK, 6)
    check(b, t + 0.75, x, y - 185 * s, 0.6 * s, RED)

def kapitol(t, x, y, s=1.0):
    """Gezeichnetes Parlamentsgebäude (Kuppel + Säulen), kein echtes Logo."""
    parts = [line(x - 260 * s, y, x + 260 * s, y, n=10), line(x - 240 * s, y - 40 * s, x + 240 * s, y - 40 * s, n=10)]
    parts += [line(x - 200 * s + i * 80 * s, y - 40 * s, x - 200 * s + i * 80 * s, y - 200 * s, n=4) for i in range(6)]
    parts += [line(x - 240 * s, y - 200 * s, x + 240 * s, y - 200 * s, n=10), arc(x, y - 200 * s, 130 * s, math.pi, 2 * math.pi, ry=120 * s),
              line(x, y - 320 * s, x, y - 380 * s, n=3)]
    b.many(t, 0.8, parts, INK, 7)

def boot(t, x, y, s=1.0):
    b.many(t, 0.7, [poly((x - 200 * s, y - 60 * s), (x + 200 * s, y - 60 * s), (x + 140 * s, y + 20 * s), (x - 140 * s, y + 20 * s), closed=True),
                    line(x, y - 60 * s, x, y - 360 * s, n=6), poly((x + 10 * s, y - 350 * s), (x + 170 * s, y - 110 * s), (x + 10 * s, y - 110 * s), closed=True)], INK, 8)

def welle(t, x, y, w=900):
    wave(b, t, x, y, w, 18, 6, GREY, 0.8)

def richter(t, x, y):
    """Richterpult mit Hammer."""
    b.many(t, 0.6, [rect(x - 330, y - 120, 660, 240), line(x - 330, y - 70, x + 330, y - 70, n=8)], INK, 8)
    fig(t + 0.3, x, y - 120, 0.75, face="neutral", w=7)
    b.many(t + 0.9, 0.3, [rect(x + 200, y - 175, 70, 40), line(x + 235, y - 135, x + 250, y - 85, n=3)], INK, 7)

def keks(t, x, y, r=140, bio=False):
    b.s(t, 0.4, circle(x, y, r), INK, 8)
    for i in range(7):
        a = i * 0.9; rr = r * (0.3 + 0.08 * (i % 4))
        b.s(t + 0.3 + i * 0.04, 0.05, circle(x + rr * math.cos(a), y + rr * math.sin(a), 10, n=8), INK, 6)
    if bio: b.txt(t + 0.6, 0.4, "Bio-Mehl & Bio-Zucker", x, y - r - 50, 46, RED)

def hoerner(t, x, y, s=1.0):
    b.s(t, 0.25, poly((x - 60 * s, y), (x - 90 * s, y - 80 * s), (x - 30 * s, y - 20 * s)), RED, 8)
    b.s(t + 0.25, 0.25, poly((x + 60 * s, y), (x + 90 * s, y - 80 * s), (x + 30 * s, y - 20 * s)), RED, 8)

def deckkarte(t, x, y, txt="???", w=640, h=220):
    """Neugier-Lücke: abgedeckte Karte (schraffiert), Auflösung später."""
    b.s(t, 0.4, rect(x - w / 2, y - h / 2, w, h), INK, 7)
    for i in range(int(w / 46)):
        b.s(t + 0.3 + i * 0.02, 0.05, line(x - w / 2 + 20 + i * 44, y + h / 2 - 15, x - w / 2 + 60 + i * 44, y - h / 2 + 15, n=3), GREY, 5)
    b.txt(t + 0.6, 0.3, txt, x, y + 30, 100, RED)

def figuren(t, x, y, n, cols=12, dx=50, dy=95, n_rot=0, t_rot=None):
    """n Mini-Strichmännchen im Raster (wie hundert(), aber mit beliebiger Anzahl)."""
    rows = math.ceil(n / cols); x0 = x - (cols - 1) * dx / 2; y0 = y - (rows - 1) * dy / 2
    tr = t_rot if t_rot is not None else t + 1.6
    def fn(ctx, tt):
        if tt < t: return
        shown = int(n * ease_out(prog(tt, t, t + 1.2))); nr = int(n_rot * ease_out(prog(tt, tr, tr + 1.0)))
        ctx.set_line_width(4); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(shown):
            cx = x0 + (i % cols) * dx; cy = y0 + (i // cols) * dy
            ctx.set_source_rgba(*(RED if i < nr else INK))
            ctx.new_path(); ctx.arc(cx, cy - 26, 9, 0, 6.3); ctx.stroke()
            ctx.move_to(cx, cy - 17); ctx.line_to(cx, cy + 8); ctx.move_to(cx - 12, cy - 6); ctx.line_to(cx + 12, cy - 6)
            ctx.move_to(cx, cy + 8); ctx.line_to(cx - 9, cy + 26); ctx.move_to(cx, cy + 8); ctx.line_to(cx + 9, cy + 26); ctx.stroke()
    b.dyn.append(fn)

STAT = ["Eindruck", "schön = gut", "Noten", "Gesichter", "Gericht", "unbewusst", "Dinge"]
def stationen(n, t, X, Y):
    """Rückkehr zum Hook: Weg mit 7 Stationen, Station n wird erreicht (rot), Mini-Hauptfigur läuft hin."""
    b.txt(t, 0.5, f"Station {n}", X, Y - 340, 110, RED)
    pts = [(X - 720 + i * 240, Y + 40 + 50 * math.sin(i * 1.3)) for i in range(7)]
    b.s(t + 0.1, 0.5, poly(*pts, n=6), GREY, 5)
    for i, (x, y) in enumerate(pts):
        b.s(t + 0.2 + i * 0.05, 0.12, circle(x, y, 42, n=20), RED if i == n - 1 else INK, 7)
        if i < n: label(b, t + 0.4 + i * 0.05, STAT[i], x, y + 120, 40, RED if i == n - 1 else GREY)
        if i < n - 1: check(b, t + 0.35, x, y, 0.55, INK)
    x, y = pts[n - 1]; check(b, t + 0.8, x, y, 0.75, RED); b.snd("pop_klein.wav", t + 0.85, 0.3)
    x0 = pts[n - 2][0] if n > 1 else X - 900
    walker(b, t + 0.2, t + 1.4, x0, x, y - 60, 0.45, hero=True)

# ===================== K0 Hook =====================
X, Y = v.P(0, 0)
t = S(0, "Zwei Gesichter", "Live-Strich", "Zwei erfundene Gesichter entstehen nebeneinander, Mitte ein großes ODER", ("person",), "exakt")
gesicht(t - 0.3, X - 450, Y - 40, 1.6, 1, "happy"); gesicht(t + 0.2, X + 450, Y - 40, 1.6, 0, "neutral")
label(b, t + 0.6, "oder?", X, Y + 20, 90, GREY)
t = S(0, "Du siehst", "Tagesuhr", "Eine Stoppuhr erscheint oben in der Mitte, Zeiger läuft genau eine Runde: 1 SEKUNDE", ("zeit",), "exakt", num="1 Sekunde")
tagesuhr(b, t, X, Y - 380, [(t, 0.0), (t + 0.6, 1.0)], 80, None); label(b, t + 0.6, "1 Sekunde", X, Y - 230, 56, RED)
t = S(0, "Wer von beiden", "Mitmach-Test", "Unter den Gesichtern: WER WIRKT KOMPETENTER? Countdown 3–2–1 läuft", ("geschehen",), "exakt", "frage:wer")
label(b, t, "Wer wirkt kompetenter?", X, Y + 330, 80, INK)
for i, n_ in enumerate("321"):
    _m = b.mark(); b.txt(t + 0.7 + i * 0.45, 0.15, n_, X, Y + 470, 70, RED); b.clear(_m, b.mark(), t + 1.1 + i * 0.45)
t = S(0, "Du hast dich", "Pose wechselt", "Über dem linken Gesicht erscheint ein roter Heiligenschein: die Entscheidung ist gefallen", ("gefuehl",), "schema")
halo(t, X - 450, Y - 270, 150)
t = S(0, "Obwohl du", "Live-Strich", "Unter beiden Gesichtern je ein leeres Namensschild mit ???", ("geschehen",), "schema")
for dx in (-450, 450):
    b.s(t + (0 if dx < 0 else 0.3), 0.3, rect(X + dx - 150, Y + 160, 300, 80), INK, 6); b.txt(t + 0.3 + (0 if dx < 0 else 0.3), 0.2, "???", X + dx, Y + 215, 56, GREY)
t = S(0, "Genau so ein", "Kamerafahrt übers Board", "Kamera fährt weiter: eine Wahlurne, ein Stimmzettel mit rotem Haken fällt hinein", ("geschehen",), "exakt")
X, Y = pan(0, 1, t)
urne(t, X - 450, Y + 250, 1.3); label(b, t + 0.5, "Wahl", X - 450, Y + 380, 70, INK)
t = S(0, "Und zwar erstaunlich", "Zahl in Handschrift", "Neben der Urne: ERSTAUNLICH OFT, ein großes rotes Ausrufezeichen wird eingekreist", ("zahl",), "schema")
label(b, t, "erstaunlich oft", X + 350, Y - 250, 90, INK); zahl2(t + 0.4, X + 350, Y + 50, "!", 220)
t = S(0, "Dein Kopf schließt", "Ursache-Wirkungs-Kette", "Kopfprofil, aus ihm laufen drei Pfeile: KLUG, SYMPATHISCH, STRAFE", ("erklaerung",), "schema")
X, Y = pan(0, 2, t)
head_profile(b, t - 0.3, X - 550, Y + 20, 320, INK, 10, 0.7)
for i, (w_, ph) in enumerate((("klug", "Klugheit"), ("sympathisch", "Sympathie"), ("Strafe", "Strafe"))):
    tt = A(0, ph); arrow(b, tt, X - 250, Y - 60 + i * 40, X + 150, Y - 260 + i * 220, RED); label(b, tt + 0.3, w_, X + 400, Y - 240 + i * 220, 90, INK)
t = S(0, "Aber warum", "Gedankenschleife", "Rote Schleife kreist um das Kopfprofil, großes Fragezeichen", ("gefuehl",), "schema", "frage:warum")
schleife(b, t, t + 5, X - 550, Y - 80, 230, hide=A(0, "In diesem Video") - 0.3)
b.txt(t + 0.2, 0.3, "?", X - 550, Y - 330, 160, RED)
t = S(0, "Und was passiert", "Live-Strich", "Drei kleine Orte entstehen: Schulhaus, Bewerbungstisch, Gerichtssaal mit Hammer", ("ort",), "schema")
X, Y = pan(0, 3, t)
building(b, A(0, "Schule"), X - 600, Y + 200, "Schule")
tb = A(0, "Bewerbungsgespräch"); b.many(tb, 0.5, [line(X - 180, Y + 150, X + 180, Y + 150, n=6), line(X - 150, Y + 150, X - 150, Y + 300, n=3), line(X + 150, Y + 150, X + 150, Y + 300, n=3)], INK, 8)
fig(tb + 0.2, X - 260, Y + 300, 0.6, face="neutral", w=6); fig(tb + 0.4, X + 260, Y + 300, 0.6, face="neutral", w=6); label(b, tb + 0.6, "Bewerbung", X, Y + 400, 56, INK)
tg = A(0, "Gerichtssaal"); b.many(tg, 0.5, [rect(X + 450, Y + 120, 300, 180), rect(X + 640, Y + 60, 60, 35), line(X + 670, Y + 95, X + 690, Y + 130, n=3)], INK, 8)
label(b, tg + 0.5, "Gericht", X + 600, Y + 400, 56, INK)
t = S(0, "In diesem Video", "Mitmach-Test", "Ein Weg mit sieben leeren Stationen wird gezogen, Überschrift 7 STATIONEN", ("zahl",), "exakt", "frage:stationen", num="7 Stationen")
X, Y = pan(0, 4, t)
b.txt(t, 0.5, "7 Stationen", X, Y - 340, 130, RED)
pts = [(X - 720 + i * 240, Y + 40 + 50 * math.sin(i * 1.3)) for i in range(7)]
b.s(t + 0.3, 0.6, poly(*pts, n=6), GREY, 5)
for i, (x, y) in enumerate(pts): b.s(t + 0.5 + i * 0.08, 0.12, circle(x, y, 42, n=20), INK, 7)
t = S(0, "Zähl mit", "Figur bewegt sich", "Die Hauptfigur läuft klein an den Start des Weges: ZÄHL MIT!", ("geschehen",), "schema")
walker(b, t, t + 1.4, X - 1000, X - 820, Y - 20, 0.45, hero=True); label(b, t + 0.3, "Zähl mit!", X, Y + 300, 90, INK)
t = S(0, "Und am Ende", "Schlüsselwort erscheint", "Am Ende des Weges eine abgedeckte Karte DER TRICK: ??? – Auflösung erst am Schluss", ("geschehen",), "schema", "frage:trick")
deckkarte(t + 0.3, X + 560, Y + 400, "Trick: ???", 520, 150)

# ===================== K1 Der Heiligenschein =====================
t = S(1, "Die Geschichte beginnt", "Kamerafahrt übers Board", "Kamera fliegt zu einer Ortsmarke USA, darunter ein gezeichnetes Armee-Zeltlager", ("ort",), "exakt")
X, Y = pan(1, 0, t)
pin(b, t, X - 500, Y - 50, "USA, Armee", RED, 80)
for i in range(4): b.s(t + 0.3 + i * 0.12, 0.25, poly((X - 120 + i * 230, Y + 380), (X - 20 + i * 230, Y + 200), (X + 80 + i * 230, Y + 380), closed=True), INK, 7)
t = S(1, "Neunzehnhundertzwanzig", "Studien-Karteikarte", "Karteikarte wird angeheftet: 1920 · Edward Thorndike · kurzer Aufsatz", ("zeit", "person"), "exakt", num="1920")
karteikarte(b, t, X + 450, Y - 220, "1920", "Edward Thorndike", "kurzer Aufsatz")
t = S(1, "Er hatte sich", "Experiment nachgespielt", "Ein Vorgesetzter mit Klemmbrett steht vor einer Reihe von Soldaten", ("geschehen", "person"), "schema")
X, Y = pan(1, 1, t)
fig(t - 0.2, X - 650, Y + 430, 1.1, face="neutral"); b.s(t + 0.3, 0.3, rect(X - 600, Y + 160, 90, 120), INK, 6)
for i in range(4): fig(t + 0.2 + i * 0.12, X - 150 + i * 230, Y + 430, 0.85, face="neutral", w=7)
t = S(1, "Zum Beispiel", "Zahl in Handschrift", "Große rote 137 wird über der Reihe geschrieben und eingekreist: FLUGSCHÜLER", ("zahl",), "exakt", num="137")
zahl2(t + 0.3, X + 200, Y - 280, "137", 160); label(b, t + 0.9, "Flugschüler", X + 200, Y - 80, 64, INK)
t = S(1, "Körperbau, Intelligenz", "Live-Strich", "Bewertungsbogen mit vier Zeilen: Körperbau, Intelligenz, Führung, Charakter", ("geschehen",), "exakt")
X, Y = pan(1, 2, t)
b.s(t - 0.2, 0.4, rect(X - 520, Y - 380, 1040, 760), INK, 7)
ROWS = [("Körperbau", "Körperbau"), ("Intelligenz", "Intelligenz"), ("Führung", "Führungsstärke"), ("Charakter", "Charakter")]
for i, (w_, ph) in enumerate(ROWS): label(b, A(1, ph), w_, X - 250, Y - 220 + i * 160, 70, INK)
t = S(1, "Jede Eigenschaft", "Live-Strich", "Hinter jeder Zeile erscheint ein leeres Kästchen: EINZELN", ("geschehen",), "schema")
for i in range(4): b.s(t + i * 0.15, 0.15, rect(X + 180, Y - 270 + i * 160, 110, 90), INK, 6)
label(b, t + 0.7, "einzeln!", X + 420, Y + 300, 60, RED)
t = S(1, "Doch Thorndike fiel", "Blick in den Kopf", "Lupe über dem Bogen, Kamera zoomt auf die Kästchen", ("geschehen",), "schema", "frage:seltsam")
b.many(t, 0.5, [circle(X + 235, Y - 50, 170), line(X + 355, Y + 70, X + 470, Y + 190, n=4)], RED, 9)
v.go(t + 0.2, X + 150, Y - 50, 1.3); b.snd("schwenk.wav", t + 0.2, 0.25)
t = S(1, "Die Noten hingen", "Handgezeichnetes Diagramm", "Vier Balken wachsen fast gleich hoch: ZU STARK ZUSAMMEN", ("vergleich",), "schema", "antwort:seltsam")
X, Y = pan(1, 3, t)
bars(b, X - 250, Y + 330, [(t + i * 0.2, 0.86 - 0.03 * i, INK, w_) for i, (w_, _) in enumerate(ROWS)], h=560, bw=140, gap=60, lab=40)
label(b, t + 1.2, "alles gleich hoch?", X + 550, Y - 250, 70, RED)
t = S(1, "Wer körperlich", "Pose wechselt", "Soldat steht aufrecht, lächelt, neben ihm vier rote Haken", ("person",), "schema")
fig(t, X + 550, Y + 430, 1.0, face="happy")
for i in range(4): check(b, t + 0.4 + i * 0.12, X + 750, Y + 30 + i * 90, 0.6, RED)
t = S(1, "Wer einen schlechten", "Pose wechselt", "Zweiter Soldat sackt zusammen, vier rote Kreuze", ("person",), "schema")
X, Y = pan(1, 4, t)
fig(t, X - 500, Y + 430, 1.0, face="sad")
for i in range(4): cross(b, t + 0.4 + i * 0.12, X - 300, Y + 30 + i * 90, 0.45)
t = S(1, "Als hätten", "Ursache-Wirkungs-Kette", "Ein großes Urteil EINDRUCK verzweigt sich mit Pfeilen auf alle vier Eigenschaften", ("erklaerung",), "schema")
label(b, t, "1 Eindruck", X + 250, Y - 300, 90, RED)
for i, (w_, _) in enumerate(ROWS):
    arrow(b, t + 0.6 + i * 0.25, X + 250, Y - 250, X - 50 + i * 200, Y + 20, INK, 6); label(b, t + 0.8 + i * 0.25, w_, X - 50 + i * 200, Y + 110, 44, INK)
t = S(1, "Thorndike nannte", "Schlüsselwort erscheint", "Das Wort HALO wird riesig geschrieben und rot unterstrichen", ("erklaerung",), "exakt")
X, Y = pan(1, 5, t)
schluesselwort(b, t, X, Y - 200, "Halo", 220, INK)
t = S(1, "Daraus wurde", "Schlüsselwort erscheint", "Darunter wird in Rot das ganze Wort HALO-EFFEKT ergänzt", ("erklaerung",), "schema")
label(b, t, "Halo-Effekt", X, Y + 30, 100, RED)
t = S(1, "Halo ist das", "Metapher verwandelt sich", "Das O von HALO wird zu einem Ring, der über den Kopf der Hauptfigur schwebt: HEILIGENSCHEIN", ("erklaerung",), "schema")
X, Y = pan(1, 6, t)
fig(t - 0.2, X - 300, Y + 450, 1.4, hero=True, face="happy"); halo(t + 0.4, X - 290, Y + 450 - 235 * 1.4 - 90, 120)
label(b, t + 0.8, "Heiligenschein", X + 450, Y - 200, 90, INK)
t = S(1, "Eine einzige gute", "Ursache-Wirkungs-Kette", "Strahlen laufen vom Heiligenschein über die ganze Figur: klug, nett, fleißig", ("erklaerung",), "schema")
for i, w_ in enumerate(("klug", "nett", "fleißig")):
    arrow(b, t + i * 0.35, X - 150, Y - 50, X + 250, Y + 30 + i * 140, RED, 6); label(b, t + 0.3 + i * 0.35, w_, X + 450, Y + 60 + i * 140, 64, INK)
t = S(1, "Station Nummer eins", "Mitmach-Test", "Rückkehr zum Hook: Weg mit sieben Stationen, Station 1 EINDRUCK wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(1, 7, t); stationen(1, t, X, Y)
t = S(1, "Er färbt alles", "Metapher verwandelt sich", "Ein roter Farbfleck breitet sich von Station 1 über den weiteren Weg aus", ("erklaerung",), "schema")
b.s(t, 0.8, spiral(X - 720, Y + 40, 120, 2.2), RED, 6)
t = S(1, "Aber welche", "Gedankenschleife", "Fragezeichen über drei Eigenschaften: Stimme? Kleidung? Schönheit?", ("gefuehl",), "schema", "frage:staerkste")
X, Y = pan(1, 8, t)
for i, w_ in enumerate(("Stimme?", "Kleidung?", "Aussehen?")): label(b, t + i * 0.3, w_, X - 550 + i * 550, Y - 100, 80, INK if i < 2 else RED)
fig(t, X, Y + 430, 1.0, hero=True, face="worried"); schleife(b, t + 0.3, t + 5, X, Y + 140, 140)

# ===================== K2 Schön gleich gut? =====================
t = S(2, "Neunzehnhundertzweiundsiebzig", "Studien-Karteikarte", "Karteikarte 1972 · Universität Minnesota · Dion, Berscheid, Walster", ("zeit", "person"), "exakt", num="1972")
X, Y = pan(2, 0, t)
karteikarte(b, t, X - 400, Y - 100, "1972", "Univ. of Minnesota", "Dion, Berscheid, Walster")
t = S(2, "Karen Dion", "100 Figuren", "Sechzig kleine Figuren erscheinen in Reihen: 60 STUDIERENDE", ("zahl",), "exakt", num="60")
figuren(t + 0.4, X + 450, Y + 80, 60, cols=12, dx=56, dy=100)
t = S(2, "sechzig Studierenden", "Zahl in Handschrift", "Über den Figuren wird eine rote 60 geschrieben und eingekreist", ("zahl",), "exakt", num="60")
zahl2(t, X + 450, Y - 330, "60", 120)
t = S(2, "Universität von Minnesota", "Live-Strich", "Unter der Karte erscheint eine kleine Ortsmarke MINNESOTA", ("ort",), "exakt")
label(b, t, "Minnesota, USA", X - 400, Y + 250, 64, RED)
t = S(2, "Manche galten", "Live-Strich", "Drei Passfotos werden an eine Wand geheftet: sehr attraktiv, durchschnittlich, wenig attraktiv", ("person",), "exakt")
X, Y = pan(2, 1, t)
for i, (h, m, w_, ph) in enumerate(((1, "happy", "sehr attraktiv", "sehr"), (0, "neutral", "durchschnittlich", "durchschnittlich"), (2, "sad", "wenig attraktiv", "wenig"))):
    tt = A(2, ph); b.s(tt, 0.3, rect(X - 700 + i * 560, Y - 330, 300, 380), INK, 6); gesicht(tt + 0.2, X - 550 + i * 560, Y - 150, 0.95, h, m, dur=0.6)
    label(b, tt + 0.6, w_, X - 550 + i * 560, Y + 160, 56, INK)
t = S(2, "Die Studierenden sollten", "Experiment nachgespielt", "Eine Studentin mit Stift schaut auf die Fotos, Fragebogen in der Hand", ("geschehen",), "schema")
fig(t, X, Y + 450, 0.8, face="neutral", w=7); b.s(t + 0.3, 0.3, rect(X + 60, Y + 170, 80, 110), INK, 5)
t = S(2, "Freundlich oder", "Innerer Regler", "Regler FREUNDLICH – KÜHL schlägt aus", ("gefuehl",), "schema")
X, Y = pan(2, 2, t)
dial(b, t, X - 450, Y - 80, "kühl  ·  freundlich"); dial_needle(b, X - 450, Y - 80, [(t + 0.3, 0.5), (t + 1.0, 0.2), (t + 1.6, 0.8)], t + 0.3)
t = S(2, "Erfolgreich oder", "Innerer Regler", "Zweiter Regler ERFOLGREICH – NICHT schlägt aus", ("gefuehl",), "schema")
dial(b, t, X + 450, Y - 80, "nein  ·  erfolgreich"); dial_needle(b, X + 450, Y - 80, [(t + 0.3, 0.5), (t + 1.0, 0.85)], t + 0.3)
t = S(2, "Mehr wussten", "Live-Strich", "Zwischen den Reglern nur ein Gesicht, sonst leeres Papier: NUR DAS GESICHT", ("geschehen",), "schema")
gesicht(t, X, Y + 260, 0.9, 1, "happy"); label(b, t + 0.6, "nur das Gesicht", X, Y + 470, 64, RED)
t = S(2, "Das Ergebnis gab", "Schlüsselwort erscheint", "Abgedeckte Karte ERGEBNIS: ??? wird gezeichnet", ("geschehen",), "schema", "frage:ergebnis")
X, Y = pan(2, 3, t)
_md = b.mark(); deckkarte(t, X, Y - 150, "???", 1100, 240)
t = S(2, "Was schön ist", "Schlüsselwort erscheint", "Abdeckung verschwindet, darunter: WAS SCHÖN IST, IST GUT – rot unterstrichen", ("erklaerung",), "exakt", "antwort:staerkste")
b.clear(_md, b.mark(), t - 0.1); schluesselwort(b, t, X, Y - 150, "Was schön ist, ist gut.", 110, INK)
halo(t + 0.9, X, Y + 150, 160)
t = S(2, "Den attraktiven", "Handgezeichnetes Diagramm", "Diagramm PERSÖNLICHKEIT: Balken attraktiv hoch, wenig attraktiv niedrig", ("vergleich",), "schema", "antwort:ergebnis")
X, Y = pan(2, 4, t)
bars(b, X - 550, Y + 330, [(t + 0.2, 0.8, RED, "attraktiv"), (t + 0.6, 0.45, GREY, "wenig")], h=520, bw=150, gap=60, lab=44)
label(b, t, "Persönlichkeit", X - 550, Y - 300, 60, INK)
t = S(2, "Die besseren Berufe", "Live-Strich", "Daneben: Aktentasche mit Krawatte – BERUF, roter Haken", ("vergleich",), "schema")
b.many(t, 0.5, [rect(X - 60, Y - 20, 220, 150), arc(X + 50, Y - 20, 50, math.pi, 2 * math.pi)], INK, 8); label(b, t + 0.4, "Beruf", X + 50, Y + 220, 60, INK); check(b, t + 0.7, X + 50, Y - 180, 0.9, RED)
t = S(2, "Sogar ein", "Live-Strich", "Daneben: lachende Sonne – GLÜCKLICHES LEBEN, roter Haken", ("vergleich",), "schema")
b.many(t, 0.5, [circle(X + 550, Y + 40, 90)] + [line(X + 550 + math.cos(a) * 120, Y + 40 + math.sin(a) * 120, X + 550 + math.cos(a) * 160, Y + 40 + math.sin(a) * 160, n=2) for a in [i * 0.785 for i in range(8)]], INK, 7)
b.s(t + 0.5, 0.2, arc(X + 550, Y + 50, 40, 0.3, 2.8, n=12), INK, 6); label(b, t + 0.5, "glücklich", X + 550, Y + 260, 60, INK); check(b, t + 0.8, X + 550, Y - 180, 0.9, RED)
t = S(2, "Nur in einem", "Mythos durchstreichen", "Kamera schwenkt: ein Kinderwagen erscheint, der Heiligenschein darüber wird rot durchgestrichen", ("vergleich",), "schema")
X, Y = pan(2, 5, t)
b.many(t, 0.6, [arc(X - 300, Y + 100, 170, math.pi, 2 * math.pi), line(X - 470, Y + 100, X - 130, Y + 100, n=6), circle(X - 420, Y + 200, 45), circle(X - 180, Y + 200, 45), line(X - 130, Y + 100, X - 60, Y - 60, n=4)], INK, 8)
streich(t + 0.4, X + 300, Y - 50, "Eltern", 120, A(2, "am wenigsten"))
t = S(2, "Als Eltern", "Zahl in Handschrift", "Unter ELTERN: AM WENIGSTEN zugetraut, rot eingekreist", ("vergleich",), "schema")
label(b, t + 0.6, "am wenigsten", X + 300, Y + 200, 80, RED)
t = S(2, "Spätere Auswertungen", "Studien-Karteikarte", "Ein Stapel aus vielen Karteikarten: AUSWERTUNG VIELER STUDIEN (1991)", ("zeit",), "exakt", num="1991")
X, Y = pan(2, 6, t)
for i in range(4): b.s(t + i * 0.12, 0.2, rect(X - 750 + i * 25, Y - 300 + i * 25, 420, 260), GREY if i < 3 else INK, 6)
karteikarte(b, t + 0.5, X - 450, Y - 80, "1991", "Meta-Analyse", "viele Studien", sound=False)
t = S(2, "Am stärksten strahlt", "Handgezeichnetes Diagramm", "Drei Balken: SOZIAL hoch, KLUGHEIT mittel, EHRLICHKEIT fast null", ("vergleich",), "schema")
bars(b, X + 400, Y + 350, [(A(2, "soziale"), 0.9, RED, "sozial"), (A(2, "Auf Klugheit"), 0.5, INK, "Klugheit"), (A(2, "Auf Ehrlichkeit"), 0.08, GREY, "Ehrlichkeit")], h=560, bw=170, gap=70, axis_t=t, lab=44)
t = S(2, "beliebt, gesellig", "Netz der Menschen", "Über dem SOZIAL-Balken verbinden sich kleine Figuren: beliebt, gesellig", ("erklaerung",), "schema")
netz(b, t, [(X + 60, Y - 330), (X + 180, Y - 400), (X + 300, Y - 330)], [(0, 1), (1, 2), (0, 2)], s=0.35)
t = S(2, "Auf Klugheit", "Pose wechselt", "Über dem mittleren Balken eine kleine Glühbirne", ("vergleich",), "schema")
bulb(b, t + 0.4, X + 400, Y - 150)
t = S(2, "Auf Ehrlichkeit", "Live-Strich", "Über dem leeren dritten Balken: KAUM", ("vergleich",), "schema")
label(b, t + 0.3, "kaum", X + 640, Y + 160, 70, GREY)
t = S(2, "Station Nummer zwei", "Mitmach-Test", "Rückkehr zum Hook: Station 2 SCHÖN = GUT wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(2, 7, t); stationen(2, t, X, Y)
t = S(2, "Schönheit bekommt", "Metapher verwandelt sich", "Eine Münze mit Heiligenschein: VORSCHUSS", ("erklaerung",), "schema")
X, Y = pan(2, 8, t)
b.s(t, 0.4, circle(X - 400, Y, 150), INK, 9); b.txt(t + 0.3, 0.3, "+", X - 400, Y + 50, 160, RED); halo(t + 0.4, X - 400, Y - 200, 110)
label(b, t + 0.6, "Vorschuss", X - 400, Y + 270, 80, INK)
t = S(2, "Und dieser Vorschuss", "Ursache-Wirkungs-Kette", "Pfeil von der Münze zu einem Zeugnis mit roter 1 und Fragezeichen", ("erklaerung",), "schema", "frage:noten")
arrow(b, t, X - 200, Y, X + 150, Y, RED); blatt(t + 0.4, X + 450, Y, 300, 380); note(t + 1.0, X + 520, Y + 100, "1?", RED, 90)

# ===================== K3 Der Aufsatz =====================
t = S(3, "Neunzehnhundertvierundsiebzig", "Studien-Karteikarte", "Karteikarte 1974 · Landy & Sigall · 60 Studenten", ("zeit", "person", "zahl"), "exakt", "antwort:noten", num="1974, 60")
X, Y = pan(3, 0, t)
karteikarte(b, t, X - 450, Y - 120, "1974", "Landy & Sigall", "60 Studenten")
t = S(3, "einen Aufsatz zum", "Experiment nachgespielt", "Ein männlicher Student sitzt am Tisch vor einem Stapel Aufsätze", ("geschehen",), "exakt")
fig(t, X + 350, Y + 430, 1.0, face="neutral", pose="sit"); b.many(t + 0.3, 0.4, [line(X + 480, Y + 320, X + 800, Y + 320, n=6), line(X + 520, Y + 320, X + 520, Y + 440, n=3)], INK, 8)
for i in range(3): b.s(t + 0.5 + i * 0.1, 0.12, rect(X + 560 + i * 8, Y + 240 - i * 12, 160, 70), INK, 5)
t = S(3, "Mal war der Text", "Zwei Wege", "Board teilt sich: links GUTER TEXT, rechts SCHWACHER TEXT", ("vergleich",), "schema")
X, Y = pan(3, 1, t)
zwei_wege(b, t, X, Y + 40, "guter Text", "schwacher Text", 860, 76)
blatt(A(3, "gut geschrieben"), X - 450, Y + 100, 280, 360, 7); blatt(A(3, "gut geschrieben") + 0.7, X + 450, Y + 100, 280, 360, 4)
t = S(3, "Und an jedem", "Live-Strich", "An beide Texte wird ein kleines Passfoto mit Büroklammer geheftet", ("geschehen",), "exakt")
X, Y = pan(3, 2, t)
blatt(t, X - 450, Y + 40, 340, 460, 7, foto=(1, "happy")); b.s(t + 0.8, 0.2, poly((X - 290, Y - 230), (X - 290, Y - 120), (X - 260, Y - 120), (X - 260, Y - 210)), GREY, 5)
t = S(3, "Mal eine attraktive", "Experiment nachgespielt", "Drei Versionen nebeneinander: attraktives Foto, weniger attraktives Foto, kein Foto", ("vergleich",), "exakt")
blatt(A(3, "weniger"), X + 50, Y + 40, 340, 460, 7, foto=(2, "sad")); blatt(A(3, "gar kein"), X + 550, Y + 40, 340, 460, 7)
label(b, A(3, "gar kein") + 0.4, "kein Foto", X + 550, Y - 280, 56, GREY)
t = S(3, "Der Text war", "Ursache-Wirkungs-Kette", "Gleichheitszeichen zwischen den drei Texten: GLEICHER TEXT", ("vergleich",), "schema")
for dx in (-200, 300): b.txt(t + (0 if dx < 0 else 0.3), 0.3, "=", X + dx, Y + 80, 140, RED)
label(b, t + 0.5, "gleicher Text", X + 50, Y + 380, 70, RED)
t = S(3, "Trotzdem bekam", "Pose wechselt", "Rote Noten erscheinen: über dem attraktiven Foto die bessere Note", ("vergleich",), "schema", "frage:groesste")
note(t + 0.2, X - 450, Y - 330, "gut", RED, 70); note(t + 0.6, X + 50, Y - 330, "mäßig", INK, 60)
t = S(3, "Am größten war", "Handgezeichnetes Diagramm", "Diagramm SCHWACHER AUFSATZ: Balken attraktiv deutlich höher als weniger attraktiv", ("vergleich",), "schema", "antwort:groesste")
X, Y = pan(3, 3, t)
bars(b, X - 400, Y + 330, [(t + 0.2, 0.75, RED, "attraktiv"), (t + 0.6, 0.38, GREY, "weniger")], h=560, bw=170, gap=80, lab=46)
label(b, t, "schwacher Aufsatz", X - 400, Y - 330, 64, INK)
t = S(3, "Wenn die Arbeit", "Metapher verwandelt sich", "Eine Waage: links dünnes Blatt, rechts schweres Foto – die Waage kippt zum Foto", ("erklaerung",), "schema")
b.many(t, 0.5, [line(X + 450, Y + 380, X + 450, Y - 50, n=6), line(X + 250, Y + 380, X + 650, Y + 380, n=6)], INK, 8)
def waage(ctx, tt, t0=t, X=X, Y=Y):
    if tt < t0 + 0.5: return
    a = -0.25 * ease_out(prog(tt, t0 + 1.0, t0 + 2.0)); cx, cy = X + 450, Y - 50
    ctx.set_source_rgba(*INK); ctx.set_line_width(8)
    lx, ly = cx - 280 * math.cos(a), cy - 280 * math.sin(a); rx, ry = cx + 280 * math.cos(a), cy + 280 * math.sin(a)
    ctx.move_to(lx, ly); ctx.line_to(rx, ry); ctx.stroke()
    for px, py, lab in ((lx, ly, "Text"), (rx, ry, "Foto")):
        ctx.move_to(px - 90, py + 80); ctx.line_to(px + 90, py + 80); ctx.stroke(); ctx.move_to(px, py); ctx.line_to(px, py + 80); ctx.stroke()
        dtext(ctx, lab, px, py + 150, 52, RED if lab == "Foto" else INK)
b.dyn.append(waage)
t = S(3, "Ähnliches fanden", "Kamerafahrt übers Board", "Kamera fährt zu einem gezeichneten Schulhaus mit Klassenzimmer", ("ort",), "schema")
X, Y = pan(3, 4, t)
building(b, t, X - 500, Y + 250, "Schule"); fig(t + 0.4, X - 100, Y + 430, 0.8, face="neutral", w=7)
t = S(3, "Neunzehnhundertdreiundsiebzig", "Studien-Karteikarte", "Karteikarte 1973 · Lehrkräfte · USA · Clifford & Walster", ("zeit",), "exakt", num="1973")
karteikarte(b, t, X + 400, Y - 180, "1973", "Lehrkräfte, USA", "Clifford & Walster", rot=0.03)
t = S(3, "Zeugnis mit Foto", "Live-Strich", "Ein Zeugnis mit Kinderfoto wird an die Tafel geheftet", ("geschehen",), "exakt")
blatt(t, X + 350, Y + 250, 260, 320, 5, foto=(2, "happy"))
t = S(3, "Das Zeugnis war", "Zwei Wege", "Zwei identische Zeugnisse, nur das Foto unterscheidet sich", ("vergleich",), "schema")
X, Y = pan(3, 5, t)
blatt(t, X - 450, Y - 50, 300, 400, 6, foto=(1, "happy")); blatt(t + 0.4, X + 450, Y - 50, 300, 400, 6, foto=(0, "sad"))
b.txt(t + 0.8, 0.3, "=", X, Y, 160, RED)
t = S(3, "Doch dem attraktiveren", "Pose wechselt", "Über dem attraktiveren Kind erscheinen Glühbirne und ein Pfeil nach oben: KLUG, KOMMT WEITER", ("vergleich",), "schema")
bulb(b, t, X - 450, Y - 380)
t = S(3, "erwarteten, dass", "Ursache-Wirkungs-Kette", "Roter Pfeil nach oben neben dem Zeugnis, Schrift KOMMT WEITER", ("erklaerung",), "schema")
label(b, t, "kommt weiter", X - 450, Y + 280, 60, RED)
arrow(b, A(3, "erwarteten") + 0.3, X - 650, Y + 380, X - 650, Y + 150, RED)
t = S(3, "Station Nummer drei", "Mitmach-Test", "Rückkehr zum Hook: Station 3 NOTEN wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(3, 6, t); stationen(3, t, X, Y)
t = S(3, "Wo die Leistung", "Metapher verwandelt sich", "Ein Puzzle mit Loch: das fehlende Teil ist ein Gesicht und rastet ein", ("erklaerung",), "schema")
X, Y = pan(3, 7, t)
b.s(t, 0.6, rect(X - 600, Y - 250, 700, 500), INK, 8); b.s(t + 0.4, 0.4, rect(X - 350, Y - 100, 200, 200), RED, 6)
label(b, t + 0.6, "Leistung unklar", X - 250, Y - 320, 64, INK)
gesicht(A(3, "füllt"), X - 250, Y, 0.65, 1, "happy", dur=0.5)
t = S(3, "Doch wie schnell", "Tagesuhr", "Rechts eine Stoppuhr, Zeiger rast: WIE SCHNELL?", ("zeit",), "schema", "frage:schnell")
tagesuhr(b, t, X + 500, Y - 40, [(t, 0.0), (t + 1.5, 3.0)], 170, "Wie schnell?")

# ===================== K4 Eine Sekunde reicht =====================
t = S(4, "Zweitausendfünf", "Studien-Karteikarte", "Karteikarte 2005 · Princeton · Todorov u. a.", ("zeit", "ort", "person"), "exakt", "antwort:schnell", num="2005")
X, Y = pan(4, 0, t)
karteikarte(b, t, X - 450, Y - 120, "2005", "Princeton", "Todorov u. a.")
t = S(4, "das viele erschreckt", "Pose wechselt", "Eine Figur liest die Studie und reißt erschrocken die Arme hoch", ("gefuehl",), "schema")
fig(t, X + 400, Y + 430, 1.0, face="worried", pose="arms_up"); b.txt(t + 0.3, 0.3, "!", X + 560, Y + 80, 140, RED)
t = S(4, "Er zeigte Menschen", "Experiment nachgespielt", "Bildschirm mit zwei erfundenen Gesichtern, davor eine Versuchsperson", ("geschehen",), "exakt")
X, Y = pan(4, 1, t)
b.s(t - 0.2, 0.5, rect(X - 600, Y - 380, 1000, 600), INK, 8); b.s(t + 0.2, 0.3, line(X - 100, Y + 220, X - 100, Y + 320, n=3), INK, 8)
gesicht(t + 0.3, X - 350, Y - 90, 1.1, 0, "neutral"); gesicht(t + 0.6, X + 150, Y - 90, 1.1, 2, "neutral")
fig(t + 0.4, X + 650, Y + 450, 1.0, face="neutral")
t = S(4, "Es waren echte", "Kamerafahrt übers Board", "Unter dem Bildschirm entsteht ein gezeichnetes Parlamentsgebäude: US-KONGRESS", ("ort",), "exakt")
X, Y = pan(4, 2, t)
kapitol(t, X - 300, Y + 300, 1.2); label(b, t + 0.8, "US-Kongress", X - 300, Y + 420, 70, INK)
t = S(4, "Die Versuchspersonen", "Blick in den Kopf", "Gedankenblase der Versuchsperson: WER IST DAS? – zwei leere Namensschilder", ("gefuehl",), "schema")
fig(t - 0.2, X + 550, Y + 450, 1.0, face="neutral"); bubble(b, t, X + 450, Y - 230, 520, 220, "Wer ist das?", 60, INK)
t = S(4, "Sie sollten nur", "Mitmach-Test", "Großer Knopf A oder B, Frage WER WIRKT KOMPETENTER?", ("geschehen",), "exakt", "frage:treffer")
X, Y = pan(4, 3, t)
for i, l_ in enumerate("AB"):
    b.s(t + i * 0.2, 0.3, circle(X - 300 + i * 600, Y + 150, 130), INK, 9); b.txt(t + 0.3 + i * 0.2, 0.2, l_, X - 300 + i * 600, Y + 195, 140, INK)
label(b, A(4, "Wer wirkt"), "Wer wirkt kompetenter?", X, Y - 250, 90, INK)
t = S(4, "Und dann kam", "Zwei Wege", "Board teilt sich: links URTEIL, rechts ECHTE WAHL, Pfeil dazwischen", ("vergleich",), "schema", "antwort:wer")
X, Y = pan(4, 4, t)
zwei_wege(b, t, X, Y + 40, "Bauch-Urteil", "echte Wahl", 860, 76); urne(t + 0.6, X + 450, Y + 300, 1.0)
gesicht(t + 0.4, X - 450, Y + 120, 0.9, 0, "neutral"); halo(t + 1.0, X - 450, Y - 50, 90)
t = S(4, "Bei den Wahlen zum Senat", "100 Figuren", "Zehn Wahlen als Kästchen, sieben davon füllen sich rot: 7 VON 10 · SENAT", ("zahl",), "exakt", num="7 von 10")
X, Y = pan(4, 5, t)
for i in range(10):
    b.s(t + i * 0.06, 0.12, rect(X - 700 + i * 140, Y - 120, 110, 110), INK, 6)
    if i < 7: b.s(t + 1.2 + i * 0.12, 0.15, poly((X - 690 + i * 140, Y - 20), (X - 600 + i * 140, Y - 110), n=4), RED, 10)
label(b, t, "Senat", X, Y - 300, 80, INK); zahl2(A(4, "sieben von zehn"), X + 550, Y + 250, "7 von 10", 110)
t = S(4, "Beim Repräsentantenhaus", "Zahl in Handschrift", "Darunter: REPRÄSENTANTENHAUS – 2 VON 3", ("zahl",), "exakt", num="2 von 3")
label(b, t, "Repräsentantenhaus:", X - 350, Y + 250, 64, INK); label(b, t + 0.6, "2 von 3", X - 350, Y + 360, 80, RED)
t = S(4, "Und selbst wenn", "Tagesuhr", "Stoppuhr mit 1 SEKUNDE, daneben blitzen zwei Gesichter auf und verschwinden", ("zeit",), "exakt", num="1 Sekunde")
X, Y = pan(4, 6, t)
tagesuhr(b, t, X - 550, Y - 50, [(t, 0.0), (t + 0.6, 1.0)], 160, "1 Sekunde")
_mg = b.mark(); gesicht(t + 0.3, X + 100, Y - 60, 0.9, 1, "neutral", dur=0.4); gesicht(t + 0.3, X + 450, Y - 60, 0.9, 0, "neutral", dur=0.4); b.clear(_mg, b.mark(), t + 1.6)
t = S(4, "lag das Bauchurteil", "Zahl in Handschrift", "An der Stelle der Gesichter: rot eingekreist 2 VON 3 RICHTIG", ("zahl",), "exakt", num="2 von 3")
zahl2(t, X + 280, Y - 80, "2 von 3", 120); label(b, t + 0.7, "noch immer richtig", X + 280, Y + 160, 60, INK)
t = S(4, "Wohlgemerkt", "Mythos durchstreichen", "Satz KOMPETENT = SCHÖN wird geschrieben und rot durchgestrichen", ("erklaerung",), "schema")
X, Y = pan(4, 7, t)
streich(t, X, Y - 250, "kompetent = schön", 100, A(4, "nicht dasselbe"))
t = S(4, "Aber es ist", "Ursache-Wirkungs-Kette", "Kette: GESICHT → EINDRUCK → URTEIL ÜBER ALLES", ("erklaerung",), "schema")
for i, (w_, ph) in enumerate((("Gesicht", "Mechanismus"), ("Eindruck", "Ein Gesicht"), ("ganze Person", "ganze Person"))):
    label(b, A(4, ph), w_, X - 600 + i * 600, Y + 120, 76, RED if i == 2 else INK)
kette(b, A(4, "Ein Gesicht"), [(X - 600, Y + 100), (X, Y + 100), (X + 600, Y + 100)])
t = S(4, "Vier Jahre später", "Kamerafahrt übers Board", "Kamera fliegt zur Ortsmarke LAUSANNE, SCHWEIZ, darunter Berge", ("ort", "zeit"), "exakt", num="2009")
X, Y = pan(4, 8, t)
pin(b, t, X - 500, Y - 60, "Lausanne, Schweiz", RED, 70)
b.s(t + 0.3, 0.7, poly((X - 900, Y + 380), (X - 650, Y + 80), (X - 480, Y + 250), (X - 250, Y + 30), (X, Y + 380)), INK, 8)
t = S(4, "John Antonakis", "Studien-Karteikarte", "Karteikarte 2009 · Antonakis & Dalgas · 681 Kinder, 5–13 Jahre", ("zeit", "person", "zahl"), "exakt", num="2009, 681 Kinder")
karteikarte(b, t, X + 400, Y - 150, "2009", "Antonakis & Dalgas", "681 Kinder, 5–13 J.")
t = S(4, "Kinder zwischen", "Zahl in Handschrift", "Neben der Karte wird 5–13 JAHRE groß geschrieben und rot eingekreist", ("zahl",), "exakt", num="5 bis 13 Jahre")
zahl2(t, X + 400, Y + 200, "5–13", 90)
t = S(4, "Computerspiel spielen", "Live-Strich", "Ein Kind sitzt vor einem gezeichneten Computerbildschirm und spielt", ("geschehen",), "exakt")
fig(t, X + 400, Y + 450, 0.6, face="happy", w=6); b.s(t + 0.3, 0.3, rect(X + 330, Y + 270, 140, 70), INK, 6)
t = S(4, "eine Schiffsreise", "Figur bewegt sich", "Ein Boot segelt über gezeichnete Wellen von TROJA nach ITHAKA", ("ort", "geschehen"), "exakt")
X, Y = pan(4, 9, t)
welle(t, X, Y + 280, 1700); label(b, t, "Troja", X - 750, Y - 300, 64, INK); label(b, t + 0.3, "Ithaka", X + 750, Y - 300, 64, INK)
def segel(ctx, tt, t0=t, X=X, Y=Y):
    if tt < t0 + 0.3: return
    x = X - 600 + 1100 * ease(prog(tt, t0 + 0.3, t0 + 6.0)); y = Y + 250 + 8 * math.sin(tt * 3)
    ctx.set_source_rgba(*INK); ctx.set_line_width(8)
    ctx.move_to(x - 200, y - 60); ctx.line_to(x + 200, y - 60); ctx.line_to(x + 140, y + 20); ctx.line_to(x - 140, y + 20); ctx.close_path(); ctx.stroke()
    ctx.move_to(x, y - 60); ctx.line_to(x, y - 360); ctx.stroke()
    ctx.move_to(x + 10, y - 350); ctx.line_to(x + 170, y - 110); ctx.line_to(x + 10, y - 110); ctx.close_path(); ctx.stroke()
b.dyn.append(segel)
t = S(4, "Sie sollten aussuchen", "Mitmach-Test", "Über dem Boot: WER STEUERT? zwei Kapitäns-Gesichter zur Wahl", ("geschehen",), "schema")
label(b, t, "Wer steuert?", X, Y - 380, 80, RED); gesicht(t + 0.3, X - 300, Y - 150, 0.6, 0, "neutral", dur=0.5); gesicht(t + 0.5, X + 300, Y - 150, 0.6, 1, "happy", dur=0.5)
t = S(4, "Zur Auswahl", "Studien-Karteikarte", "Karteikarte: Frankreich · Parlamentswahl 2002 · Stichwahlen", ("zeit", "ort"), "exakt", num="2002")
X, Y = pan(4, 10, t)
karteikarte(b, t, X - 400, Y - 120, "2002", "Frankreich", "Stichwahlen", rot=0.03)
t = S(4, "Die Kinder tippten", "Zwei Wege", "Links ein Kind, rechts ein Erwachsener – beide zeigen auf dasselbe Gesicht", ("vergleich",), "schema", "antwort:treffer")
fig(t, X + 150, Y + 450, 0.6, face="happy", w=6); fig(t + 0.3, X + 650, Y + 450, 1.0, face="neutral")
gesicht(t + 0.5, X + 400, Y - 230, 0.7, 1, "happy", dur=0.5)
arrow(b, t + 0.9, X + 180, Y + 250, X + 340, Y - 120, RED, 6); arrow(b, t + 1.1, X + 640, Y + 150, X + 460, Y - 120, RED, 6)
t = S(4, "In rund zwei", "Zahl in Handschrift", "Rote 2 VON 3 eingekreist neben den beiden Figuren", ("zahl",), "exakt", num="2 von 3")
zahl2(t, X - 400, Y + 300, "2 von 3", 100)
t = S(4, "Station Nummer vier", "Mitmach-Test", "Rückkehr zum Hook: Station 4 GESICHTER wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(4, 11, t); stationen(4, t, X, Y)
t = S(4, "Das Urteil kommt", "Zwei Wege", "Wettrennen: Blitz URTEIL ist schon am Ziel, Schnecke NACHDENKEN kriecht hinterher", ("vergleich",), "schema")
X, Y = pan(4, 12, t)
b.s(t, 0.3, poly((X - 100, Y - 300), (X - 180, Y - 160), (X - 100, Y - 160), (X - 180, Y - 20), n=4), RED, 10); label(b, t + 0.3, "Urteil", X - 140, Y + 80, 64, RED)
b.many(t + 0.5, 0.6, [spiral(X - 600, Y + 280, 70, 2.0), line(X - 700, Y + 350, X - 450, Y + 350, n=6)], INK, 7); label(b, t + 1.0, "Nachdenken", X - 600, Y + 450, 56, INK)
b.s(t + 0.2, 0.3, line(X + 50, Y - 350, X + 50, Y + 450, n=10), INK, 6); label(b, t + 0.4, "Ziel", X + 150, Y - 380, 56, INK)
t = S(4, "Aber kann es", "Schlüsselwort erscheint", "Abgedeckte Karte mit Warnschild: GEFÄHRLICH?", ("geschehen",), "schema", "frage:gefaehrlich")
deckkarte(t, X + 550, Y + 150, "gefährlich?", 520, 200)

# ===================== K5 Im Gerichtssaal =====================
t = S(5, "Stell dir einen", "Kamerafahrt übers Board", "Kamera fährt in einen gezeichneten Gerichtssaal: Richterpult mit Hammer", ("ort",), "exakt", "antwort:gefaehrlich")
X, Y = pan(5, 0, t)
richter(t, X, Y + 40); label(b, t + 0.8, "Gerichtssaal", X, Y - 380, 80, INK)
t = S(5, "Eine Angeklagte", "Hauptfigur (blaue Locke, oranger Schal)", "Eine Angeklagte steht vor dem Pult, Hände vor dem Körper", ("person",), "exakt")
fig(t, X - 650, Y + 450, 0.9, face="worried")
t = S(5, "Ein Einbruch", "Live-Strich", "Sprechblase des Richters: EINBRUCH, daneben eine aufgebrochene Tür", ("geschehen",), "exakt")
door(b, t, X + 700, Y + 450); b.s(t + 0.4, 0.2, poly((X + 600, Y + 250), (X + 640, Y + 300), (X + 610, Y + 330)), RED, 7); label(b, t + 0.3, "Einbruch", X + 700, Y - 230, 70, RED)
t = S(5, "Neunzehnhundertfünfundsiebzig", "Studien-Karteikarte", "Karteikarte 1975 · Univ. Maryland · Sigall & Ostrove, 120 Studierende", ("zeit", "ort", "zahl"), "exakt", num="1975, 120")
X, Y = pan(5, 1, t)
karteikarte(b, t, X - 400, Y - 150, "1975", "Univ. Maryland", "Sigall & Ostrove, 120")
t = S(5, "mit hundertzwanzig", "Experiment nachgespielt", "Zwölf Mini-Figuren in Reihen, darüber die eingekreiste 120: Studierende urteilen einzeln", ("zahl",), "exakt", num="120")
figuren(t, X + 450, Y + 200, 12, cols=6, dx=90, dy=130); zahl2(t + 0.5, X + 450, Y - 220, "120", 120)
t = S(5, "Alle lasen", "Live-Strich", "Eine Akte AKTE wird aufgeklappt, für alle gleich", ("geschehen",), "exakt")
X, Y = pan(5, 2, t)
blatt(t, X - 450, Y + 20, 380, 480, 7); label(b, t + 0.4, "gleiche Akte", X - 450, Y - 320, 64, INK)
t = S(5, "Nur das Foto", "Live-Strich", "Drei Fotos werden an die Akte geklemmt: attraktiv, weniger attraktiv, keines", ("vergleich",), "exakt")
gesicht(t, X + 100, Y - 80, 0.7, 1, "happy", dur=0.5); gesicht(t + 0.4, X + 400, Y - 80, 0.7, 2, "neutral", dur=0.5)
b.s(t + 0.8, 0.3, rect(X + 620, Y - 170, 160, 190), GREY, 5); b.txt(t + 1.0, 0.2, "?", X + 700, Y - 50, 90, GREY)
t = S(5, "War sie attraktiv", "Handgezeichnetes Diagramm", "Diagramm EINBRUCH: Balken attraktiv knapp 3 Jahre", ("zahl", "vergleich"), "exakt", num="3 Jahre")
X, Y = pan(5, 3, t)
label(b, t - 0.2, "Einbruch: Jahre Haft", X - 300, Y - 360, 64, INK)
bars(b, X - 300, Y + 330, [(t + 0.2, 0.28 * 2, RED, "attraktiv: knapp 3"), (A(5, "Ohne Foto"), 0.52 * 2 / 1.05, GREY, "andere: rund 5")], h=500, bw=200, gap=200, lab=44)
t = S(5, "Ohne Foto", "Zahl in Handschrift", "Zweiter Balken wächst auf rund 5 Jahre, die 5 wird eingekreist", ("zahl",), "exakt", num="5 Jahre")
zahl2(t + 0.8, X + 450, Y - 100, "5", 160)
t = S(5, "Doch dann kam", "Schlüsselwort erscheint", "Riesiges Wort WENDUNG, Musik setzt kurz aus", ("geschehen",), "schema", "frage:wendung")
X, Y = pan(5, 4, t)
schluesselwort(b, t, X, Y - 100, "Die Wendung", 140, RED, INK)
t = S(5, "In einer zweiten", "Zwei Wege", "Board teilt sich: links EINBRUCH, rechts BETRUG", ("vergleich",), "schema")
X, Y = pan(5, 5, t)
zwei_wege(b, t, X, Y + 40, "Einbruch", "Betrug", 860, 90)
door(b, t + 0.3, X - 450, Y + 420)
t = S(5, "Sie hatte einen", "Experiment nachgespielt", "Rechts: Angeklagte lächelt einen Mann an, ein Geldsack wandert zu ihr", ("geschehen",), "schema")
fig(t, X + 250, Y + 450, 0.8, face="happy", w=7); fig(t + 0.2, X + 700, Y + 450, 0.8, face="happy", w=7)
heart(b, t + 0.4, X + 480, Y + 50, 2.0)
b.many(t + 0.7, 0.5, [circle(X + 480, Y + 250, 60), line(X + 450, Y + 190, X + 510, Y + 190, n=3)], INK, 7); b.txt(t + 1.0, 0.2, "€", X + 480, Y + 275, 60, INK)
arrow(b, t + 1.2, X + 560, Y + 330, X + 360, Y + 330, RED, 6)
t = S(5, "Jetzt drehte", "Handgezeichnetes Diagramm", "Diagramm BETRUG: jetzt ist der Balken attraktiv der höhere", ("vergleich",), "schema", "antwort:wendung")
X, Y = pan(5, 6, t)
label(b, t - 0.2, "Betrug: Jahre Haft", X - 300, Y - 360, 64, INK)
bars(b, X - 300, Y + 330, [(A(5, "fünfeinhalb"), 0.94, RED, "attraktiv: 5,5"), (A(5, "die anderen gut"), 0.76, GREY, "andere: gut 4")], h=500, bw=200, gap=200, axis_t=t, lab=44)
t = S(5, "Die attraktive Angeklagte", "Pose wechselt", "Die lächelnde Angeklagte bekommt ein trauriges Gesicht", ("person",), "schema")
fig(t, X + 600, Y + 450, 0.9, face="sad")
t = S(5, "fünfeinhalb Jahre", "Zahl in Handschrift", "Über dem höheren Balken: 5,5 Jahre, rot eingekreist", ("zahl",), "exakt", num="5,5 Jahre")
zahl2(t + 0.3, X + 600, Y - 200, "5,5", 140)
t = S(5, "Wenn Schönheit", "Mythos durchstreichen", "Der Heiligenschein über der Angeklagten wird rot durchgestrichen", ("erklaerung",), "schema")
halo(t, X + 600, Y + 170, 90); b.s(t + 0.9, 0.3, line(X + 470, Y + 210, X + 730, Y + 130, n=8), RED, 11); b.snd("gs_paper.wav", t + 0.9, 0.3)
t = S(5, "Auch bei echten", "Kamerafahrt übers Board", "Ortsmarke PENNSYLVANIA, darunter 74 Mini-Figuren", ("ort", "zahl"), "exakt", num="74")
X, Y = pan(5, 7, t)
pin(b, t, X - 550, Y - 80, "Pennsylvania", RED, 70); figuren(t + 0.4, X + 300, Y - 50, 74, cols=15, dx=55, dy=95)
label(b, A(5, "vierundsiebzig"), "74 Angeklagte", X + 300, Y + 300, 64, INK)
t = S(5, "Die attraktiveren", "Handgezeichnetes Diagramm", "Eine fallende Linie: je attraktiver, desto mildere Strafe", ("vergleich",), "schema")
X, Y = pan(5, 8, t)
b.many(t, 0.4, [poly((X - 600, Y - 300), (X - 600, Y + 250), (X + 200, Y + 250))], INK, 8)
label(b, t + 0.3, "Strafe", X - 720, Y - 250, 50, INK); label(b, t + 0.4, "Attraktivität", X - 200, Y + 340, 50, INK)
b.s(t + 0.7, 0.8, bez((X - 550, Y - 220), (X - 300, Y - 150), (X - 100, Y + 50), (X + 150, Y + 150)), RED, 8)
t = S(5, "Das ist ein", "Mythos durchstreichen", "Daneben: URSACHE? wird geschrieben und rot gestrichen, ZUSAMMENHANG bleibt", ("erklaerung",), "schema")
streich(t, X + 550, Y - 150, "Beweis", 100, A(5, "Ursache")); label(b, t + 0.2, "Zusammenhang", X + 550, Y + 50, 70, INK)
t = S(5, "Station Nummer fünf", "Mitmach-Test", "Rückkehr zum Hook: Station 5 GERICHT wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(5, 9, t); stationen(5, t, X, Y)
t = S(5, "Und das Unheimlichste", "Blick in den Kopf", "Kopf eines Schöffen, drinnen ein halb verdeckter Heiligenschein", ("gefuehl",), "schema", "frage:merken")
X, Y = pan(5, 10, t)
head_profile(b, t - 0.2, X - 300, Y + 40, 320, INK, 10, 0.7); halo(t + 0.5, X - 320, Y - 50, 70)
t = S(5, "Die Urteilenden", "Pose wechselt", "Augenbinde wird über das Kopfprofil gezeichnet: MERKEN ES NICHT", ("gefuehl",), "schema")
b.s(t, 0.4, line(X - 520, Y - 60, X - 120, Y - 60, n=8), INK, 22); label(b, t + 0.4, "merkt es nicht", X + 450, Y - 50, 80, RED)

# ===================== K6 Du merkst es nicht =====================
t = S(6, "Das zeigt ein", "Kamerafahrt übers Board", "Ortsmarke UNIVERSITÄT MICHIGAN, Campusgebäude", ("ort",), "exakt", "antwort:merken")
X, Y = pan(6, 0, t)
pin(b, t, X - 550, Y - 80, "Univ. Michigan", RED, 70); building(b, t + 0.4, X - 100, Y + 380, None)
t = S(6, "Neunzehnhundertsiebenundsiebzig", "Studien-Karteikarte", "Karteikarte 1977 · Nisbett & Wilson · Video-Experiment", ("zeit", "person"), "exakt", num="1977")
karteikarte(b, t, X + 400, Y - 230, "1977", "Nisbett & Wilson", "Video-Experiment", rot=0.03)
t = S(6, "Er stammte", "Live-Strich", "Ein Fernseher mit Dozent, Sprechblase mit Akzent-Wellen, Ortsmarke Belgien", ("person", "ort"), "exakt")
X, Y = pan(6, 1, t)
b.s(t - 0.2, 0.5, rect(X - 450, Y - 330, 700, 480), INK, 8); fig(t + 0.2, X - 100, Y + 120, 0.8, face="neutral", w=7)
pin(b, t + 0.3, X + 550, Y - 100, "Belgien", RED, 60); wave(b, A(6, "Akzent"), X + 250, Y + 300, 500, 25, 4, RED, 0.6)
t = S(6, "Es gab zwei", "Zwei Wege", "Board teilt sich: Video A und Video B", ("vergleich",), "schema")
X, Y = pan(6, 2, t)
zwei_wege(b, t, X, Y + 40, "Version A", "Version B", 860, 76)
t = S(6, "In der einen", "Pose wechselt", "Links: Dozent lächelt, winkt freundlich, Herz", ("vergleich",), "schema")
fig(t, X - 450, Y + 450, 1.0, face="happy", pose="arms_up"); heart(b, t + 0.4, X - 450, Y - 50, 3.0)
t = S(6, "In der anderen", "Pose wechselt", "Rechts: derselbe Dozent kalt, verschränkte Haltung, Eiswürfel", ("vergleich",), "schema")
fig(t, X + 450, Y + 450, 1.0, face="sad"); b.s(t + 0.4, 0.3, rect(X + 380, Y - 120, 140, 140), INK, 7); label(b, t + 0.5, "kalt", X + 450, Y - 200, 60, INK)
t = S(6, "Danach sollten", "Studie im Zeitraffer", "Bewertungstabelle: Aussehen, Gesten, Akzent – Zeilen werden gezeichnet", ("geschehen",), "schema")
X, Y = pan(6, 3, t)
b.s(t - 0.2, 0.4, rect(X - 700, Y - 300, 1400, 620), INK, 7); b.s(t, 0.3, line(X - 200, Y - 300, X - 200, Y + 320, n=8), INK, 6)
b.s(t + 0.1, 0.3, line(X + 250, Y - 300, X + 250, Y + 320, n=8), INK, 6)
label(b, t + 0.1, "warm", X + 25, Y - 220, 60, INK); label(b, t + 0.2, "kalt", X + 475, Y - 220, 60, INK)
for i, (w_, ph) in enumerate((("Aussehen", "Aussehen"), ("Gesten", "Gesten"), ("Akzent", "Akzent"))):
    label(b, A(6, ph), w_, X - 450, Y - 60 + i * 140, 64, INK)
t = S(6, "Dinge, die in beiden", "Schlüsselwort erscheint", "Unter der Tabelle: IN BEIDEN VIDEOS GLEICH, rot unterstrichen", ("erklaerung",), "schema", "frage:akzent")
schluesselwort(b, t, X, Y + 420, "in beiden Videos gleich!", 64, INK)
t = S(6, "Beim freundlichen", "Studie im Zeitraffer", "In der Spalte WARM tragen sich Haken ein: angenehm", ("vergleich",), "schema", "antwort:akzent")
for i in range(3): check(b, t + 0.2 + i * 0.25, X + 25, Y - 60 + i * 140, 0.7, RED)
t = S(6, "Beim kalten", "Studie im Zeitraffer", "In der Spalte KALT tragen sich Kreuze ein: störend", ("vergleich",), "schema")
for i in range(3): cross(b, t + 0.2 + i * 0.25, X + 475, Y - 60 + i * 140, 0.5)
t = S(6, "Richard Nisbett", "Experiment nachgespielt", "Ein Forscher mit Klemmbrett fragt eine Versuchsperson", ("geschehen",), "schema")
X, Y = pan(6, 4, t)
fig(t, X - 550, Y + 450, 1.0, face="neutral"); fig(t + 0.2, X - 100, Y + 450, 1.0, face="neutral"); b.s(t + 0.4, 0.3, rect(X - 500, Y + 180, 90, 120), INK, 6)
t = S(6, "Hat deine Sympathie", "Live-Strich", "Sprechblase: HAT DEINE SYMPATHIE DEIN URTEIL BEEINFLUSST?", ("geschehen",), "exakt")
bubble(b, t, X - 400, Y - 230, 820, 200, "Hat Sympathie dein Urteil beeinflusst?", 46, INK)
t = S(6, "Die meisten verneinten", "Pose wechselt", "Versuchsperson schüttelt den Kopf: NEIN!", ("gefuehl",), "schema")
bubble(b, t, X + 350, Y - 120, 300, 150, "Nein!", 80, RED, tail=(-1, 1))
t = S(6, "Wer den kalten", "Ursache-Wirkungs-Kette", "Pfeil wird umgedreht: AKZENT → ABNEIGUNG statt ABNEIGUNG → AKZENT", ("erklaerung",), "schema")
X, Y = pan(6, 5, t)
label(b, t, "Abneigung", X - 450, Y - 200, 80, INK); label(b, t, "Akzent nervt", X + 450, Y - 200, 80, INK); arrow(b, t + 0.4, X - 200, Y - 210, X + 180, Y - 210, INK)
label(b, A(6, "Der Akzent habe"), "Akzent nervt", X - 450, Y + 150, 80, RED); label(b, A(6, "Der Akzent habe"), "Abneigung", X + 450, Y + 150, 80, RED)
arrow(b, A(6, "Der Akzent habe") + 0.4, X - 200, Y + 140, X + 180, Y + 140, RED)
t = S(6, "Der Akzent habe", "Mythos durchstreichen", "Der obere, echte Pfeil wird halb verdeckt, der falsche rote bleibt groß", ("erklaerung",), "schema")
b.s(t + 1.2, 0.3, line(X - 700, Y - 330, X + 700, Y - 330, n=10), GREY, 4)
t = S(6, "Station Nummer sechs", "Mitmach-Test", "Rückkehr zum Hook: Station 6 UNBEWUSST wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(6, 6, t); stationen(6, t, X, Y)
t = S(6, "Der Halo-Effekt fühlt", "Blick in den Kopf", "Zoom in ein Auge: darin spiegelt sich ein Heiligenschein", ("gefuehl",), "schema")
X, Y = pan(6, 7, t)
eye(b, t, X - 300, Y - 50, 4.0); halo(t + 0.5, X - 300, Y - 50, 45)
v.go(t + 0.3, X - 300, Y - 50, 1.35); b.snd("schwenk.wav", t + 0.3, 0.25)
t = S(6, "Er fühlt sich an", "Schlüsselwort erscheint", "Kamera zieht zurück: WAHRNEHMUNG, nicht FEHLER", ("erklaerung",), "schema")
v.go(t - 0.2, X, Y, 1.0); schluesselwort(b, t, X + 450, Y - 100, "Wahrnehmung", 100, INK); label(b, t + 0.6, "nicht: Fehler", X + 450, Y + 120, 64, GREY)
t = S(6, "Doch er braucht", "Schlüsselwort erscheint", "Abgedeckte Karte: OHNE MENSCH?", ("geschehen",), "schema", "frage:ding")
deckkarte(t, X, Y + 350, "ohne Mensch?", 560, 170)

# ===================== K7 Auch bei Dingen =====================
t = S(7, "Stell dir zwei", "Live-Strich", "Zwei identische Kekse werden gezeichnet", ("geschehen",), "exakt", "antwort:ding")
X, Y = pan(7, 0, t)
keks(t, X - 400, Y + 80); keks(t + 0.4, X + 400, Y + 80)
t = S(7, "Genau gleich", "Ursache-Wirkungs-Kette", "Gleichheitszeichen zwischen den Keksen", ("vergleich",), "schema")
b.txt(t, 0.3, "=", X, Y + 130, 180, RED)
t = S(7, "Auf einem steht", "Schlüsselwort erscheint", "Über dem rechten Keks erscheint: BIO-MEHL & BIO-ZUCKER, dann ein Heiligenschein", ("geschehen",), "exakt")
b.txt(A(7, "mit Bio-Mehl"), 0.6, "Bio-Mehl & Bio-Zucker", X + 400, Y - 180, 56, RED); halo(A(7, "Bio-Zucker") + 0.3, X + 400, Y - 300, 120)
t = S(7, "Zweitausendzehn", "Studien-Karteikarte", "Karteikarte 2010 · Michigan · Schuldt & Schwarz", ("zeit", "ort", "person"), "exakt", num="2010")
X, Y = pan(7, 1, t)
karteikarte(b, t, X - 450, Y - 150, "2010", "Michigan", "Schuldt & Schwarz")
t = S(7, "mit derselben", "Live-Strich", "Zwei identische Nährwerttabellen: je 160 kcal pro Portion", ("zahl",), "exakt", num="160 kcal")
for i in range(2):
    b.s(t + i * 0.3, 0.3, rect(X + 120 + i * 380, Y - 200, 300, 380), INK, 6); b.txt(t + 0.3 + i * 0.3, 0.3, "160 kcal", X + 270 + i * 380, Y - 80, 56, INK)
    for j in range(3): b.s(t + 0.5 + i * 0.3 + j * 0.05, 0.06, line(X + 150 + i * 380, Y + j * 50, X + 390 + i * 380, Y + j * 50, n=4), GREY, 4)
t = S(7, "Trotzdem schätzten", "Handgezeichnetes Diagramm", "Geschätzte Kalorien: Balken BIO niedriger als NORMAL", ("vergleich",), "schema")
X, Y = pan(7, 2, t)
label(b, t - 0.2, "geschätzte Kalorien", X - 300, Y - 360, 60, INK)
bars(b, X - 300, Y + 330, [(t + 0.2, 0.8, GREY, "normal"), (t + 0.7, 0.6, RED, "Bio")], h=520, bw=180, gap=120, lab=48)
t = S(7, "Und fanden", "Pose wechselt", "Eine Figur greift fröhlich zu einem zweiten Keks: ÖFTER", ("geschehen",), "schema")
fig(t, X + 400, Y + 450, 1.0, face="happy", pose="arms_up"); keks(t + 0.3, X + 650, Y - 50, 60); label(b, t + 0.5, "öfter!", X + 650, Y + 80, 64, RED)
t = S(7, "Ein gutes Merkmal", "Ursache-Wirkungs-Kette", "Vom Wort BIO laufen Strahlen zu GESUND, LEICHT, LECKER", ("erklaerung",), "schema")
X, Y = pan(7, 3, t)
schluesselwort(b, t, X - 500, Y, "Bio", 130, RED, INK)
for i, w_ in enumerate(("gesund", "leicht", "lecker")):
    arrow(b, t + 0.4 + i * 0.3, X - 330, Y - 30, X + 150, Y - 280 + i * 260, INK, 6); label(b, t + 0.6 + i * 0.3, w_, X + 400, Y - 260 + i * 260, 70, INK)
t = S(7, "Auch auf Dinge", "Mythos durchstreichen", "LEICHT wird rot durchgestrichen – hat mit Bio nichts zu tun", ("erklaerung",), "schema")
b.s(t + 0.4, 0.3, line(X + 300, Y - 10, X + 520, Y - 30, n=8), RED, 11); b.snd("gs_paper.wav", t + 0.4, 0.3)
t = S(7, "Und es gibt", "Metapher verwandelt sich", "Der Heiligenschein dreht sich um und wird zu zwei roten Hörnern", ("erklaerung",), "schema", "frage:rueckseite")
X, Y = pan(7, 4, t)
fig(t - 0.2, X - 300, Y + 450, 1.3, face="neutral"); _mh = b.mark(); halo(t, X - 300, Y + 450 - 235 * 1.3 - 80, 100); b.clear(_mh, b.mark(), A(7, "Man nennt"))
t = S(7, "Man nennt sie", "Schlüsselwort erscheint", "Hörner wachsen auf dem Kopf, daneben HORN-EFFEKT", ("erklaerung",), "exakt", "antwort:rueckseite")
hoerner(t, X - 300, Y + 450 - 235 * 1.3 - 30, 1.0); schluesselwort(b, t + 0.3, X + 400, Y - 150, "Horn-Effekt", 120, RED, INK)
t = S(7, "Ein einziger schlechter", "Live-Strich", "Drei kleine Bilder: Fleck auf dem Hemd, Tippfehler im Brief, dann alles grau", ("geschehen",), "schema")
X, Y = pan(7, 5, t)
fig(t, X - 600, Y + 300, 0.9, face="neutral"); b.s(A(7, "Fleck"), 0.3, circle(X - 590, Y + 170, 22), RED, 9)
t = S(7, "ein Tippfehler", "Live-Strich", "Ein Anschreiben, ein Tippfehler wird rot eingekreist", ("geschehen",), "schema")
blatt(A(7, "Tippfehler"), X, Y + 50, 260, 320, 5); b.s(A(7, "Tippfehler") + 0.5, 0.3, circle(X - 40, Y - 45, 50, ry=25), RED, 6)
t = S(7, "und plötzlich", "Pose wechselt", "Pfeil nach unten, die Figur wird grau: ALLES SCHLECHTER", ("gefuehl",), "schema")
label(b, A(7, "plötzlich"), "alles schlechter", X + 550, Y + 50, 76, RED); arrow(b, A(7, "plötzlich") + 0.3, X + 550, Y - 250, X + 550, Y - 50, RED)
t = S(7, "Spannend ist", "Kamerafahrt übers Board", "Gezeichnete Weltkugel dreht sich, der Heiligenschein darüber flackert", ("ort",), "schema", "frage:kultur")
X, Y = pan(7, 6, t)
b.many(t, 0.7, [circle(X - 400, Y + 80, 260), arc(X - 400, Y + 80, 110, -math.pi / 2, math.pi / 2, ry=260), line(X - 660, Y + 80, X - 140, Y + 80, n=12)], INK, 7)
halo(t + 0.6, X - 400, Y - 260, 160)
t = S(7, "In einer Studie", "Studien-Karteikarte", "Karteikarte 1997 · Südkorea · Wheeler & Kim, Ortsmarke Korea auf der Kugel", ("zeit", "ort"), "exakt", num="1997")
karteikarte(b, t, X + 450, Y - 180, "1997", "Südkorea", "Wheeler & Kim"); pin(b, t + 0.2, X - 230, Y + 30, "Korea", RED, 50)
t = S(7, "anders als in", "Zwei Wege", "Zwei Spalten: NORDAMERIKA – beliebt, stark / SÜDKOREA – ehrlich, rücksichtsvoll", ("vergleich",), "schema", "antwort:kultur")
X, Y = pan(7, 7, t)
zwei_wege(b, t, X, Y + 40, "Nordamerika", "Südkorea", 860, 76)
label(b, t + 0.6, "beliebt", X - 450, Y + 50, 70, INK); label(b, A(7, "Ehrlichkeit"), "ehrlich", X + 450, Y + 50, 70, INK)
label(b, A(7, "Rücksicht"), "rücksichtsvoll", X + 450, Y + 200, 70, INK)
t = S(7, "Also mit dem", "Netz der Menschen", "Unter SÜDKOREA verbinden sich Figuren zu einer Gruppe", ("erklaerung",), "schema")
netz(b, t, [(X + 250, Y + 450), (X + 450, Y + 450), (X + 650, Y + 450)], [(0, 1), (1, 2)], s=0.45)
t = S(7, "Station Nummer sieben", "Mitmach-Test", "Rückkehr zum Hook: Station 7 DINGE wird rot abgehakt – alle sieben erledigt", ("zahl",), "exakt", "antwort:stationen")
X, Y = pan(7, 8, t); stationen(7, t, X, Y)
t = S(7, "Der Schein strahlt", "Metapher verwandelt sich", "Über dem Weg wird der Heiligenschein zu einem Scheinwerfer, der auf ein Herz zeigt", ("erklaerung",), "schema")
heart(b, t + 0.3, X + 600, Y + 330, 2.5)
t = S(7, "Aber wie kommt", "Schlüsselwort erscheint", "Die abgedeckte TRICK-Karte vom Anfang taucht wieder auf", ("geschehen",), "schema", "teaser:trick")
X, Y = pan(7, 9, t)
fig(t - 0.2, X - 500, Y + 450, 1.0, hero=True, face="worried"); deckkarte(t, X + 250, Y, "Trick: ???", 700, 220)

# ===================== K8 So trickst du ihn aus =====================
t = S(8, "Der Psychologe Daniel", "Studien-Karteikarte", "Karteikarte 2011 · Daniel Kahneman · Buch", ("zeit", "person"), "exakt", "antwort:trick", num="2011")
X, Y = pan(8, 0, t)
karteikarte(b, t, X - 450, Y - 150, "2011", "Daniel Kahneman", "Schnelles Denken ...")
book(b, A(8, "langsames"), X + 400, Y + 50, "", INK); label(b, A(8, "langsames") + 0.5, "Buch", X + 400, Y + 320, 64, INK)
t = S(8, "wie er früher", "Experiment nachgespielt", "Ein Professor am Schreibtisch vor einem Stapel Prüfungshefte", ("geschehen",), "exakt")
X, Y = pan(8, 1, t)
fig(t, X - 500, Y + 450, 1.0, face="neutral", pose="sit"); b.many(t + 0.2, 0.4, [line(X - 400, Y + 330, X + 100, Y + 330, n=6)], INK, 8)
for i in range(4): b.s(t + 0.4 + i * 0.1, 0.12, rect(X - 250 + i * 10, Y + 250 - i * 15, 200, 70), INK, 5)
t = S(8, "Er las alle", "Live-Strich", "Ein Heft wird aufgeklappt: Antwort 1, 2, 3 einer Person untereinander", ("geschehen",), "exakt")
X, Y = pan(8, 2, t)
b.s(t - 0.1, 0.4, rect(X - 700, Y - 380, 600, 760), INK, 7)
for i in range(3): label(b, t + i * 0.3, f"Antwort {i + 1}", X - 400, Y - 230 + i * 230, 60, INK)
t = S(8, "War die erste", "Ursache-Wirkungs-Kette", "Antwort 1 bekommt eine rote Eins, Pfeile ziehen die nächsten Noten mit nach oben", ("erklaerung",), "schema")
note(t, X - 180, Y - 250, "1", RED, 80)
for i in range(2): arrow(b, t + 0.6 + i * 0.3, X - 180, Y - 170 + i * 230, X - 180, Y - 30 + i * 230, RED, 6); note(t + 0.9 + i * 0.3, X - 180, Y + 0 + i * 230, "1", RED, 60)
label(b, t + 1.4, "wohlwollend", X + 350, Y - 50, 80, RED)
t = S(8, "Also änderte", "Pose wechselt", "Professor steht auf, Glühbirne über dem Kopf", ("gefuehl",), "schema")
X, Y = pan(8, 3, t)
fig(t, X - 500, Y + 450, 1.0, face="happy"); bulb(b, t + 0.3, X - 500, Y - 100)
t = S(8, "Er bewertete erst", "Studie im Zeitraffer", "Tabelle: Spalte FRAGE 1 bei allen Heften wird von oben nach unten gefüllt, dann FRAGE 2", ("geschehen",), "schema")
b.s(t - 0.2, 0.4, rect(X - 150, Y - 350, 900, 620), INK, 7)
label(b, t, "Frage 1", X + 100, Y - 270, 56, INK); label(b, A(8, "dann Frage"), "Frage 2", X + 450, Y - 270, 56, INK)
for i in range(4):
    label(b, t - 0.1, f"Heft {i + 1}", X - 30, Y - 140 + i * 120, 44, GREY)
    check(b, t + 0.5 + i * 0.25, X + 100, Y - 150 + i * 120, 0.5, INK); check(b, A(8, "dann Frage") + 0.5 + i * 0.25, X + 450, Y - 150 + i * 120, 0.5, INK)
t = S(8, "Und er notierte", "Live-Strich", "Ein Heft dreht sich um, Punkte werden hinten versteckt notiert", ("geschehen",), "schema")
X, Y = pan(8, 4, t)
b.s(t, 0.4, rect(X - 600, Y - 300, 500, 600), INK, 7); label(b, t + 0.3, "hinten im Heft", X - 350, Y - 380, 56, INK)
_mp = b.mark(); b.txt(t + 0.8, 0.3, "8 Punkte", X - 350, Y + 30, 64, RED); b.clear(_mp, b.mark(), t + 2.4)
deckkarte(t + 2.2, X - 350, Y, "???", 400, 200)
t = S(8, "Plötzlich waren", "Handgezeichnetes Diagramm", "Notenreihe vorher: alles 1, nachher: 1, 3, 2, 4 – gemischt", ("vergleich",), "schema")
label(b, t, "vorher: 1 1 1 1", X + 400, Y - 150, 70, GREY); label(b, t + 0.8, "nachher: 1 3 2 4", X + 400, Y + 0, 70, RED)
t = S(8, "Er fühlte sich", "Innerer Regler", "Regler SICHER – UNSICHER kippt nach unsicher", ("gefuehl",), "schema")
dial(b, t, X + 400, Y + 300, "sicher  ·  unsicher"); dial_needle(b, X + 400, Y + 300, [(t + 0.2, 0.2), (t + 1.0, 0.8)], t + 0.2)
t = S(8, "Aber genau das", "Schlüsselwort erscheint", "Über dem Regler: EHRLICHER, rot unterstrichen", ("erklaerung",), "schema")
b.snd("stift_klick.wav", t, 0.25); schluesselwort(b, t, X + 400, Y + 470, "ehrlicher", 70, INK)
t = S(8, "Das ist der Trick", "Schlüsselwort erscheint", "Die TRICK-Karte vom Anfang wird aufgedeckt", ("geschehen",), "schema")
X, Y = pan(8, 5, t)
_mt = b.mark(); deckkarte(t - 0.4, X, Y - 150, "Trick: ???", 1100, 240); b.clear(_mt, b.mark(), A(8, "Zerlege") - 0.1)
t = S(8, "Zerlege dein", "Metapher verwandelt sich", "Darunter ZERLEGE DEIN URTEIL, ein Gesicht zerfällt in vier Kästchen", ("erklaerung",), "exakt")
schluesselwort(b, t, X, Y - 150, "Zerlege dein Urteil.", 120, RED, INK)
for i in range(4): b.s(t + 0.6 + i * 0.15, 0.2, rect(X - 560 + i * 300, Y + 150, 220, 220), INK, 7)
t = S(8, "Bewerte jede", "Live-Strich", "In die vier Kästchen schreiben sich Fragen: Fakten? Leistung? Text? Ziel?", ("erklaerung",), "schema")
for i, w_ in enumerate(("Fakten?", "Leistung?", "Inhalt?", "Ziel?")): label(b, t + 0.3 + i * 0.3, w_, X - 450 + i * 300, Y + 280, 50, INK)
t = S(8, "Genau so arbeiten", "Experiment nachgespielt", "Bewerbungstisch mit Fragebogen auf dem Tisch: STRUKTURIERT", ("geschehen",), "schema")
X, Y = pan(8, 6, t)
b.many(t, 0.5, [line(X - 300, Y + 250, X + 300, Y + 250, n=6), line(X - 260, Y + 250, X - 260, Y + 420, n=3), line(X + 260, Y + 250, X + 260, Y + 420, n=3)], INK, 8)
fig(t + 0.2, X - 450, Y + 420, 0.9, face="neutral"); fig(t + 0.4, X + 450, Y + 420, 0.9, face="neutral"); blatt(t + 0.5, X, Y + 120, 160, 200, 4)
label(b, t + 0.8, "strukturiert", X, Y - 300, 90, INK)
t = S(8, "Sie sagen im Schnitt", "Handgezeichnetes Diagramm", "Zwei Balken TREFFSICHERHEIT: strukturiert höher als nach Gefühl", ("vergleich",), "schema")
X, Y = pan(8, 7, t)
bars(b, X - 300, Y + 330, [(t + 0.2, 0.85, RED, "strukturiert"), (A(8, "lockeres"), 0.5, GREY, "nach Gefühl")], h=520, bw=200, gap=150, lab=46)
t = S(8, "Ein zweiter Trick", "Netz der Menschen", "Hauptfigur fragt eine zweite Person, die den ersten Eindruck nicht kennt (Augenbinde)", ("geschehen",), "schema")
X, Y = pan(8, 8, t)
fig(t, X - 500, Y + 450, 1.0, hero=True, face="neutral"); fig(t + 0.3, X + 300, Y + 450, 1.0, face="neutral")
t = S(8, "von jemandem", "Pose wechselt", "Der zweiten Person wird eine Augenbinde gezeichnet: kennt den ersten Eindruck nicht", ("geschehen",), "schema")
b.s(A(8, "ersten Eindruck"), 0.3, line(X + 230, Y + 450 - 240, X + 370, Y + 450 - 240, n=4), INK, 16); label(b, t + 0.6, "zweite Meinung", X - 100, Y - 200, 80, INK)
arrow(b, t + 0.8, X - 380, Y + 100, X + 180, Y + 100, INK)
t = S(8, "Und im Alltag", "Blick in den Kopf", "Zoom in den Kopf der Hauptfigur: drinnen steht ein Gesicht mit Heiligenschein", ("gefuehl",), "schema")
X, Y = pan(8, 9, t)
fig(t - 0.3, X - 600, Y + 450, 1.0, hero=True, face="neutral"); bubble(b, t, X + 150, Y - 120, 1000, 600, None)
gesicht(t + 0.4, X + 150, Y - 120, 1.0, 1, "happy"); halo(t + 0.9, X + 150, Y - 330, 110)
v.go(t + 0.3, X + 150, Y - 120, 1.3); b.snd("schwenk.wav", t + 0.3, 0.25)
t = S(8, "Woran genau", "Mitmach-Test", "Drei Fragen schreiben sich in die Blase: WORAN GENAU?", ("erklaerung",), "schema")
label(b, t, "Woran genau?", X + 150, Y + 80, 60, RED)
t = S(8, "Woran an der Sache", "Mitmach-Test", "Zweite Frage: AN DER SACHE?", ("erklaerung",), "schema")
label(b, t, "An der Sache?", X + 150, Y + 150, 54, INK)
t = S(8, "Und was davon", "Mythos durchstreichen", "Der Heiligenschein im Kopf wird rot durchgestrichen", ("erklaerung",), "schema")
v.go(t - 0.2, X, Y, 1.0)
b.s(t + 0.8, 0.3, line(X + 0, Y - 300, X + 300, Y - 360, n=8), RED, 11); b.snd("gs_paper.wav", t + 0.8, 0.3)

# ===================== K9 Schluss =====================
X, Y = v.P(9, 0); v.go(v.CT[9], X, Y, 1.0, d=0.7, sound=False)
t = S(9, "Schöne Menschen sind", "Mythos durchstreichen", "SCHÖN = KLUG wird geschrieben und rot durchgestrichen", ("erklaerung",), "schema")
streich(t, X, Y - 300, "schön = klug", 120, A(9, "automatisch"))
t = S(9, "Unser Kopf macht", "Gehirn-Skizze", "Gezeichnetes Gehirn, aus dem ein Heiligenschein aufsteigt", ("erklaerung",), "schema")
brain(b, t, X - 400, Y + 150, 1.3, INK); halo(t + 0.6, X - 400, Y - 100, 120)
t = S(9, "Er spart sich", "Ursache-Wirkungs-Kette", "Kette: EIN EINDRUCK → GANZES URTEIL, schneller Pfeil", ("erklaerung",), "schema", "antwort:warum")
label(b, t, "1 Eindruck", X + 150, Y + 100, 70, INK); label(b, t + 0.5, "ganzes Urteil", X + 650, Y + 100, 70, RED)
kette(b, t + 0.2, [(X + 150, Y + 80), (X + 650, Y + 80)])
t = S(9, "Bei Noten", "Live-Strich", "Drei Mini-Symbole: Zeugnis, Wahlurne, Richterhammer", ("geschehen",), "schema")
X, Y = pan(9, 1, t)
blatt(A(9, "Noten"), X - 550, Y - 50, 200, 260, 4); urne(A(9, "Wahlen"), X, Y + 30, 0.8)
b.many(A(9, "Gericht"), 0.4, [rect(X + 480, Y - 80, 120, 60), line(X + 540, Y - 20, X + 580, Y + 80, n=3)], INK, 8)
t = S(9, "Das Gute ist", "Pose wechselt", "Hauptfigur hebt eine Lupe, der Heiligenschein wird sichtbar umrandet", ("gefuehl",), "schema")
X, Y = pan(9, 2, t)
fig(t, X - 300, Y + 450, 1.2, hero=True, face="happy")
b.many(t + 0.3, 0.4, [circle(X + 50, Y - 50, 120), line(X - 30, Y + 40, X - 150, Y + 160, n=4)], INK, 9)
t = S(9, "Wenn du den", "Schlüsselwort erscheint", "In der Lupe: ein Heiligenschein, daneben ERKANNT", ("erklaerung",), "schema")
halo(t, X + 50, Y - 40, 70); schluesselwort(b, t + 0.6, X + 550, Y - 150, "erkannt!", 110, INK)
t = S(9, "Jetzt bin ich", "Mitmach-Test", "Großes Kommentarfeld wird gezeichnet", ("geschehen",), "exakt")
X, Y = pan(9, 3, t)
comment_box(b, t, X, Y - 80)
t = S(9, "Bei welcher", "Live-Strich", "Im Kommentarfeld: BEI WELCHER STATION HAT ER DICH ERWISCHT?", ("geschehen",), "exakt")
b.txt(t, 1.0, "Bei welcher Station hat", X, Y - 110, 44, INK); b.txt(t + 0.8, 0.8, "der Halo-Effekt dich erwischt?", X, Y - 40, 44, RED)
t = S(9, "Schreib es", "Schlüsselwort erscheint", "SCHREIB'S IN DIE KOMMENTARE! unter dem Feld, unterstrichen", ("geschehen",), "schema")
schluesselwort(b, t, X, Y + 250, "Schreib's in die Kommentare!", 80, INK)
t = S(9, "Und wie viele", "Zahl in Handschrift", "Rechts oben: ? / 7 in Handschrift, eingekreist", ("zahl",), "exakt", num="7")
zahl2(t, X + 650, Y - 380, "? / 7", 110)
t = S(9, "Abonniere", "Hauptfigur (blaue Locke, oranger Schal)", "DENKMUSTER-Schriftzug, Hauptfigur jubelt, eine Glocke wird gezeichnet", ("geschehen",), "exakt")
X, Y = pan(9, 4, t)
b.txt(t, 0.8, "Denkmuster", X, Y - 250, 170, INK); b.txt(t + 0.5, 0.3, "abonnieren", X, Y - 120, 80, INK)
tt = A(9, "Glocke"); bell(b, tt, X + 520, Y + 150); b.snd("pop.wav", tt + 0.4, 0.4)
fig(t + 0.3, X - 450, Y + 450, 1.0, hero=True, face="happy", pose="arms_up")
t = S(9, "Dann verpasst", "Live-Strich", "Unter dem Schriftzug: WARUM MENSCHEN TUN, WAS SIE TUN", ("geschehen",), "schema")
label(b, t, "warum Menschen tun, was sie tun", X, Y + 20, 60, GREY)
t = S(9, "Bis zum", "Board-Panorama", "Kamera fährt weit zurück: das ganze Schluss-Board als ein Bild", ("gefuehl",), "stimmung")
v.go(t, v.P(9, 2)[0], v.P(9, 2)[1], 0.32, d=2.5, sound=False); b.snd("klang.wav", t + 2.0, 0.15)

# ---------------- Bild-Drehbuch aus den Einstellungen ----------------
def drehbuch():
    shots = sorted(SHOTS, key=lambda s: s["t"])
    for k, ttl in enumerate(TITLES):
        if ttl: shots.append(dict(t=v.CT[k] + 0.3, k=k, animation="Schlüsselwort erscheint", zeigt=f"Kapitelkarte {k}: Nummer im Kreis, Titel „{ttl}“ wird geschrieben und rot unterstrichen",
                                  inhalt=["erklaerung"], genauigkeit="schema", neugier="", num="", satz=f"(Kapitelkarte) {ttl}"))
    shots.sort(key=lambda s: s["t"])
    allw = [(v.VSTART[i] + w["s"], w["w"]) for i, d in enumerate(v.words) for w in d["words"]]
    out = []
    for i, s in enumerate(shots):
        t1 = shots[i + 1]["t"] if i + 1 < len(shots) else v.TOTAL
        satz = s.get("satz") or " ".join(w for tw, w in allw if s["t"] - 0.05 <= tw < t1 - 0.05)
        if s["num"]: satz += f" [{s['num']}]"
        out.append(dict(satz=satz, sek=round(t1 - s["t"], 2), zeigt=s["zeigt"], animation=s["animation"], inhalt=s["inhalt"],
                        genauigkeit=s["genauigkeit"], neugier=s["neugier"], kapitel=s["k"]))
    json.dump(out, open(os.path.join(v.dir, "bilddrehbuch.json"), "w"), ensure_ascii=False, indent=1)
    print("bilddrehbuch.json:", len(out), "Einstellungen")

if __name__ == "__main__":
    if "--check" in sys.argv:
        print("FEHLEND:", v.missing, "TOTAL", round(v.TOTAL, 1)); sys.exit(0)
    if "--drehbuch" in sys.argv:
        drehbuch(); sys.exit(0)
    v.render()
