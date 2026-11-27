"""Denkmuster 005 – Aufschieben: Warum wir Dinge aufschieben, obwohl wir es besser wissen.
Szenen mit engine/kit.py + engine/bausteine.py (ein Satz = ein Bild, Wortzeiten aus vo/k*.json).
Jede Einstellung wird mit S(...) gesetzt – daraus entsteht bilddrehbuch.json (python3 scenes.py --drehbuch).
Sounds: assets/sfx + Laurins Goldsmith-Sounds sub_drop/slap/paper als gs_*.wav (DM_SFX, siehe INFO.md)."""
import os, sys, math, json
import cairo
HERE_ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE_, "..", "..", "engine"))
from kit import *
from bausteine import *

TITLES = [None, "Nicht faul", "Es geht ums Gefühl", "Dein Zukunfts-Ich", "Erst gut, dann teuer",
          "Die lange Spur", "Das Gegenteil", "Der Fristen-Mythos", "So trickst du es aus", None]
v = Video(__file__, titles=TITLES, music_plan=[1, 2, 4, 3, 2, 4, 1, 3, 2, 5], hook_music_from=8.0)
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


# ---------- 2D-Motion-Graphics (engine/motion_dm.py, Erweiterung 23.11.2026) ----------
import motion_dm as MO
import numpy as np
MCLIPS = []
MANIM = {"flow": "Gedankenwolken-Ablauf (`motion` flow)", "flip": "Mythos dreht sich um (`motion` flip)", "counter": "Zahl rot eingekreist (`motion` counter)",
         "grid": "Strichmännchen-Raster (`motion` grid)", "bars": "Schraffur-Balken (`motion` bars)", "stack": "Studien-Stapel (`motion` stack)", "phone": "Gezeichnetes Handy (`motion` phone)"}
SNDMAP = {"pop": ("pop_klein.wav", 0.8), "pop_klein": ("pop_klein.wav", 1.0)}
def motion(k, phrase, comp, props, ln, zeigt, inhalt=("erklaerung",), gen="schema", neu="", num="", sound=True):
    """Motion-Clip als Vollbild über dem Board (weiche Blende 0,25 s); das Board läuft darunter weiter."""
    t = S(k, phrase, MANIM[comp], zeigt, inhalt, gen, neu, num)
    key = MO.clip(comp, props, len=ln); MCLIPS.append((t, key, ln))
    if sound:
        for tt, n, g, d in MO.sounds(key, t):
            f, m = SNDMAP.get(n, (n + ".wav", 1.0)); b.snd(f, tt, g * m)
    return t

def _motion_overlay(ctx, t):
    for t0, key, ln in MCLIPS:
        if t0 <= t < t0 + ln:
            a = min(1.0, (t - t0) / 0.25, (t0 + ln - t) / 0.25)
            fr = np.array(MO.frame(key, t - t0))           # RGBA
            bgra = np.ascontiguousarray(fr[:, :, [2, 1, 0, 3]])
            surf = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, 1920, 1080)
            ctx.save(); ctx.identity_matrix(); ctx.set_source_surface(surf, 0, 0); ctx.paint_with_alpha(max(0.0, a)); ctx.restore()
b.overlay.append(_motion_overlay)

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
STAT[:] = ["weiß es", "Gefühl", "Fremder", "Kredit", "Spur", "Gegenteil", "Frist"]

# ---------- Zeichnungen dieses Videos ----------
def tisch(t, x, y, w=700):
    """Schreibtisch mit Laptop (Tischkante bei y)."""
    b.many(t, 0.5, [line(x - w / 2, y, x + w / 2, y, n=10), line(x - w / 2 + 40, y, x - w / 2 + 40, y + 260, n=4), line(x + w / 2 - 40, y, x + w / 2 - 40, y + 260, n=4)], INK, 8)
    b.many(t + 0.4, 0.4, [poly((x - 150, y - 10), (x + 70, y - 10), (x + 40, y - 170), (x - 180, y - 170), closed=True), line(x - 190, y - 4, x + 110, y - 4, n=6)], INK, 7)

def handy(t, x, y, s=1.0, txt=None, col=INK):
    b.many(t, 0.35, [rect(x - 55 * s, y - 100 * s, 110 * s, 200 * s), line(x - 15 * s, y + 80 * s, x + 15 * s, y + 80 * s, n=3)], col, 7)
    if txt: label(b, t + 0.3, txt, x, y - 10 * s, int(34 * s), RED)

def kerze(t, x, y, s=1.0):
    b.many(t, 0.5, [rect(x - 45 * s, y - 180 * s, 90 * s, 180 * s), line(x, y - 180 * s, x, y - 215 * s, n=3)], INK, 8)
    b.s(t + 0.5, 0.3, poly((x, y - 290 * s), (x + 25 * s, y - 235 * s), (x, y - 212 * s), (x - 25 * s, y - 235 * s), closed=True, n=4), RED, 7)

def eimer(t, x, y, s=1.0, col=INK):
    b.many(t, 0.4, [poly((x - 70 * s, y - 140 * s), (x + 70 * s, y - 140 * s), (x + 50 * s, y), (x - 50 * s, y), closed=True), arc(x, y - 140 * s, 70 * s, math.pi, 2 * math.pi, ry=60 * s)], col, 8)

def kalender(t, x, y, w=420, h=360, rot_tag=None):
    b.s(t, 0.4, rect(x - w / 2, y - h / 2, w, h), INK, 7); b.s(t + 0.3, 0.2, line(x - w / 2, y - h / 2 + 70, x + w / 2, y - h / 2 + 70, n=8), INK, 7)
    for i in range(4): b.s(t + 0.4 + i * 0.03, 0.1, line(x - w / 2, y - h / 2 + 70 + (i + 1) * (h - 70) / 5, x + w / 2, y - h / 2 + 70 + (i + 1) * (h - 70) / 5, n=6), GREY, 4)
    for i in range(6): b.s(t + 0.5 + i * 0.03, 0.1, line(x - w / 2 + (i + 1) * w / 7, y - h / 2 + 70, x - w / 2 + (i + 1) * w / 7, y + h / 2, n=6), GREY, 4)
    if rot_tag: b.s(rot_tag, 0.35, circle(x + w * 0.29, y + h * 0.3, 45, n=30), RED, 8)

def glas(t, x, y, fill=0.2, s=1.0, txt=None):
    b.many(t, 0.4, [poly((x - 70 * s, y - 220 * s), (x - 55 * s, y), (x + 55 * s, y), (x + 70 * s, y - 220 * s))], INK, 8)
    yy = y - 220 * s * fill
    b.s(t + 0.4, 0.25, line(x - 55 * s - 15 * s * fill, yy, x + 55 * s + 15 * s * fill, yy, n=6), RED, 7)
    for i in range(int(fill * 8)): b.s(t + 0.5 + i * 0.03, 0.06, line(x - 50 * s, y - 15 * s - i * 26 * s, x + 50 * s, y - 15 * s - i * 26 * s, n=4), RED, 4)
    if txt: label(b, t + 0.6, txt, x, y + 70 * s, int(50 * s), INK)

def stapel(t, x, y, n=8, w=260):
    for i in range(n): b.s(t + i * 0.06, 0.1, rect(x - w / 2 + (i % 2) * 12, y - i * 28, w, 24), INK, 5)

def kurve(t, X, Y, w, h, pts, col, dur=1.2):
    """Linie im Diagramm, pts = Werte 0..1 gleichmäßig über die Breite."""
    P = [(X + w * i / (len(pts) - 1), Y - h * p) for i, p in enumerate(pts)]
    b.s(t, dur, poly(*P, n=10), col, 9)

def achsen(t, X, Y, w, h, xl="", yl=""):
    b.many(t, 0.5, [line(X, Y, X + w, Y, n=10), line(X, Y, X, Y - h, n=8)], INK, 7)
    if xl: label(b, t + 0.4, xl, X + w / 2, Y + 70, 48, GREY)
    if yl: label(b, t + 0.4, yl, X - 20, Y - h - 50, 48, GREY)

# ===================== K0 Hook =====================
X, Y = v.P(0, 0)
t = S(0, "Sonntag", "Tagesuhr", "Uhr zeigt 22 Uhr, daneben SONNTAG; darunter die Hauptfigur am Schreibtisch mit Laptop", ("zeit",), "exakt", num="22 Uhr")
tagesuhr(b, t, X + 520, Y - 260, [(t, 9.0), (t + 0.8, 10.0)], 130, "Sonntag, 22 Uhr")
tisch(t + 0.3, X - 300, Y + 220); fig(t + 0.6, X - 640, Y + 480, 1.0, hero=True, face="neutral", pose="sit")
t = S(0, "Die Abgabe ist", "Live-Strich", "Auf dem Laptop-Bildschirm erscheint ABGABE: MORGEN 8 UHR in Rot", ("zeit",), "exakt", num="morgen")
label(b, t + 0.1, "Abgabe:", X - 355, Y + 90, 42, INK); label(b, t + 0.4, "morgen!", X - 355, Y + 140, 42, RED)
t = S(0, "Seit drei Wochen", "Live-Strich", "Ein Kalender wird neben die Uhr gehängt, drei Wochen werden rot durchgestrichen", ("zeit",), "exakt", num="3 Wochen")
kalender(t, X + 520, Y + 250, 380, 300)
for i in range(3): b.s(t + 0.6 + i * 0.25, 0.2, line(X + 340, Y + 180 + i * 46, X + 700, Y + 180 + i * 46, n=6), RED, 7)
t = S(0, "Und was machst", "Kamerafahrt übers Board", "Kamera fährt weiter: Fragezeichen über der Hauptfigur", ("geschehen",), "schema")
X, Y = pan(0, 1, t)
fig(t - 0.2, X, Y + 450, 1.2, hero=True, face="worried"); b.txt(t + 0.2, 0.3, "?", X + 150, Y - 120, 160, RED)
t = S(0, "Du räumst den", "Figur bewegt sich", "Hauptfigur läuft nach links zum Schreibtisch, ordnet Stifte: SCHREIBTISCH AUFRÄUMEN", ("geschehen",), "exakt")
walker(b, t, t + 1.2, X - 300, X - 650, Y - 80, 0.6, hero=True)
b.many(t + 0.3, 0.4, [line(X - 850, Y - 80, X - 450, Y - 80, n=6)] + [line(X - 780 + i * 40, Y - 90, X - 770 + i * 40, Y - 180, n=3) for i in range(4)], INK, 6)
label(b, t + 0.6, "aufräumen", X - 650, Y + 40, 54, INK); check(b, t + 1.0, X - 650, Y - 260, 0.6, INK)
t = S(0, "Du schaust kurz", "Live-Strich", "In der Mitte oben ein gezeichnetes Handy mit Herz und rotem Punkt: kurz aufs Handy", ("geschehen",), "exakt")
handy(t, X + 350, Y - 220, 1.0, "1 neue"); label(b, t + 0.4, "kurz aufs Handy", X + 350, Y - 30, 54, INK)
t = S(0, "Du schaust noch", "Live-Strich", "Rechts ein Bildschirm mit Play-Dreieck: NOCH EIN VIDEO", ("geschehen",), "exakt")
b.many(t, 0.4, [rect(X + 600, Y + 80, 280, 180), poly((X + 710, Y + 120), (X + 790, Y + 170), (X + 710, Y + 220), closed=True)], INK, 7)
label(b, t + 0.5, "noch ein Video", X + 740, Y + 330, 50, INK)
t = S(0, "Bist du einfach", "Schlüsselwort erscheint", "FAUL? wird groß in Handschrift geschrieben", ("gefuehl",), "schema", "frage:faul")
X, Y = pan(0, 2, t)
schluesselwort(b, t, X, Y - 250, "Faul?", 220, INK)
t = S(0, "Die Forschung sagt", "Mythos durchstreichen", "FAUL wird rot durchgestrichen: WAHRSCHEINLICH NICHT", ("erklaerung",), "schema")
b.s(t + 0.6, 0.3, line(X - 240, Y - 300, X + 240, Y - 330, n=10), RED, 12); b.snd("gs_paper.wav", t + 0.6, 0.35)
label(b, t + 0.9, "wahrscheinlich nicht", X, Y - 60, 70, RED)
t = S(0, "Aufschieben ist vor", "Mythos durchstreichen", "Eine Uhr mit dem Wort ZEITPROBLEM wird durchgestrichen", ("erklaerung",), "schema")
clock(b, t, X - 450, Y + 250, 110); label(b, t + 0.3, "Zeitproblem", X - 100, Y + 260, 70, INK)
b.s(t + 1.0, 0.3, line(X - 600, Y + 260, X + 120, Y + 240, n=10), RED, 10); b.snd("gs_paper.wav", t + 1.0, 0.3)
t = S(0, "Es ist etwas", "Blick in den Kopf", "Gedankenblase über einem Kopfprofil, darin ein abgedecktes Fragezeichen-Feld ???", ("gefuehl",), "schema", "frage:was")
X, Y = pan(0, 3, t)
head_profile(b, t - 0.3, X - 550, Y + 120, 300, INK, 10, 0.6); bubble(b, t, X + 200, Y - 120, 900, 520, None)
deckkarte(t + 0.4, X + 200, Y - 120, "???", 560, 200)
t = S(0, "In diesem Video", "Mitmach-Test", "Ein Weg mit sieben leeren Stationen wird gezogen, Überschrift 7 STATIONEN", ("zahl",), "exakt", "frage:stationen", num="7 Stationen")
X, Y = pan(0, 4, t)
b.txt(t, 0.5, "7 Stationen", X, Y - 340, 130, RED)
pts = [(X - 720 + i * 240, Y + 40 + 50 * math.sin(i * 1.3)) for i in range(7)]
b.s(t + 0.3, 0.6, poly(*pts, n=6), GREY, 5)
for i, (x, y) in enumerate(pts): b.s(t + 0.5 + i * 0.08, 0.12, circle(x, y, 42, n=20), INK, 7)
t = S(0, "Zähl mit", "Figur bewegt sich", "Die Hauptfigur läuft klein an den Start des Weges: ZÄHL MIT!", ("geschehen",), "schema")
walker(b, t, t + 1.4, X - 1000, X - 820, Y - 20, 0.45, hero=True); label(b, t + 0.3, "Zähl mit!", X, Y + 300, 90, INK)
t = S(0, "Und am Ende", "Schlüsselwort erscheint", "Am Ende des Weges eine abgedeckte Karte DER TRICK: ??? – Auflösung erst in Kapitel 8", ("geschehen",), "schema", "frage:trick")
deckkarte(t + 0.3, X + 560, Y + 400, "Trick: ???", 520, 150)
t = S(0, "mehr als doppelt", "Zahl in Handschrift", "Neben der Karte: x2 in Handschrift, rot eingekreist", ("zahl",), "exakt", num="2x")
zahl2(t + 0.2, X - 450, Y + 380, "x 2", 130)

# ===================== K1 Nicht faul =====================
t = S(1, "Fangen wir", "Zwei Wege", "Board teilt sich: links FAUL, rechts AUFSCHIEBEN", ("vergleich",), "schema")
X, Y = pan(1, 0, t)
zwei_wege(b, t, X, Y + 40, "faul", "aufschieben", 860, 90)
t = S(1, "Aber Faulheit heißt", "Pose wechselt", "Links: eine Figur liegt entspannt in der Hängematte, lächelt: KEINE LUST", ("vergleich",), "schema")
b.many(t, 0.5, [arc(X - 450, Y + 120, 300, 0.2, math.pi - 0.2, ry=110), line(X - 760, Y - 60, X - 760, Y + 420, n=5), line(X - 140, Y - 60, X - 140, Y + 420, n=5)], INK, 8)
fig(t + 0.4, X - 450, Y + 160, 0.7, face="happy", pose="arms_up"); label(b, t + 0.8, "keine Lust – aber zufrieden", X - 450, Y + 380, 46, INK)
t = S(1, "Wer aufschiebt, will", "Pose wechselt", "Rechts: Hauptfigur vor einer Aufgabe, will sie erledigen, schaut aber besorgt", ("vergleich",), "schema")
fig(t, X + 400, Y + 420, 1.0, hero=True, face="worried"); blatt(t + 0.4, X + 650, Y + 150, 200, 260, 4)
label(b, t + 0.7, "will es erledigen", X + 450, Y - 220, 54, INK)
t = S(1, "Und fühlt sich", "Gewicht auf den Schultern", "Über der Hauptfigur wächst ein schwerer Stein: MIES", ("gefuehl",), "schema")
gewicht(b, X + 400, Y + 420 - 235, [(t, 0.0), (t + 1.0, 0.8)], t, label_txt="mies")
t = S(1, "Der Psychologe Piers", "Studien-Karteikarte", "Karteikarte 2007 · Piers Steel · Univ. Calgary · über 200 Arbeiten", ("zeit", "person", "zahl"), "exakt", num="2007, über 200")
X, Y = pan(1, 1, t)
pin(b, t - 0.2, X - 600, Y - 280, "Calgary, Kanada", RED, 60)
karteikarte(b, t + 0.2, X - 350, Y + 80, "2007", "Piers Steel, Calgary", "über 200 Arbeiten")
motion(1, "über zweihundert", "stack", {"label": "STEEL 2007", "cards": [["Ellis & Knaus", "1977"], ["Harriott & Ferrari", "1996"], ["O'Brien", "2002"], ["Steel: Meta-Analyse", "2007"]], "symbol": "?", "question": "Was ist Aufschieben?"}, 4.4,
       "Studien-Stapel: Karten Ellis & Knaus 1977, Harriott & Ferrari 1996, O'Brien 2002 und Steel-Meta-Analyse 2007 stapeln sich, Frage WAS IST AUFSCHIEBEN?", ("zeit",), "exakt", num="2007")
t = S(1, "Seine Definition", "Schlüsselwort erscheint", "Rechts schreibt sich die Definition: VORGENOMMEN – FREIWILLIG VERSCHOBEN – OBWOHL ES SCHADET", ("erklaerung",), "schema")
label(b, t, "vorgenommen", X + 450, Y - 250, 66, INK)
label(b, A(1, "freiwillig zu"), "freiwillig verschoben", X + 450, Y - 120, 66, INK)
label(b, A(1, "obwohl man erwartet"), "obwohl es schadet", X + 450, Y + 10, 66, RED)
t = S(1, "Freiwillig. Obwohl", "Zahl in Handschrift", "Das Wort FREIWILLIG wird rot eingekreist", ("erklaerung",), "schema")
b.s(t, 0.4, circle(X + 450, Y - 140, 330, ry=70), RED, 8); treffer(t + 0.3, 0.35)
t = S(1, "Und das betrifft", "Kamerafahrt übers Board", "Kamera fährt zu einer großen Menge kleiner Figuren", ("zahl",), "schema")
X, Y = pan(1, 2, t)
figuren(t, X, Y + 120, 100, cols=20, dx=46, dy=92)
t = S(1, "In seiner Übersicht", "100 Figuren", "Von 100 Figuren werden 80 bis 95 rot: STUDIERENDE (ältere Schätzung)", ("zahl",), "exakt", num="80–95 Prozent")
hundert(b, t + 0.6, X, Y + 120, 88, t_rot=A(1, "Achtzig"), rot_label=None)
label(b, A(1, "Achtzig"), "80–95 % der Studierenden", X, Y - 330, 80, RED); label(b, A(1, "Achtzig") + 0.6, "(ältere Schätzungen)", X, Y - 240, 46, GREY)
t = S(1, "In einer kleinen", "Kamerafahrt übers Board", "Kamera fährt weiter: Hauptfigur zwischen anderen Erwachsenen", ("zahl",), "schema")
X, Y = pan(1, 3, t)
motion(1, "wurde etwa jeder", "grid", {"label": "HARRIOTT & FERRARI 1996", "n": 60, "icon": "person", "hot": 5, "value": 1, "suffix": " von 5", "caption": "ERWACHSENE: CHRONISCH"}, 4.4,
       "Strichmännchen-Raster: 60 Figuren, jede fünfte rot und traurig, 1 VON 5 ERWACHSENEN chronisch (211 Befragte, 1996)", ("zahl",), "exakt", num="1 von 5, 1996")
for i in range(5): fig(t + 0.2 + i * 0.12, X - 600 + i * 300, Y + 440, 0.9, face="sad" if i == 2 else "neutral", w=7, hero=(i == 2))
t = S(1, "Station Nummer eins", "Mitmach-Test", "Rückkehr zum Hook: Station 1 WEISS ES wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(1, 4, t); stationen(1, t, X, Y)
t = S(1, "Du weißt genau", "Pose wechselt", "Hauptfigur steht vor der Aufgabe, dreht sich weg", ("geschehen",), "schema")
X, Y = pan(1, 5, t)
blatt(t, X - 400, Y + 60, 300, 400, 6); walker(b, t + 0.3, t + 1.6, X - 50, X + 450, Y + 450, 1.0, hero=True)
t = S(1, "Aber warum handelt", "Gedankenschleife", "Rote Schleife kreist um ein Kopfprofil: WARUM?", ("gefuehl",), "schema", "frage:warum")
X, Y = pan(1, 6, t)
head_profile(b, t - 0.3, X - 200, Y + 80, 320, INK, 10, 0.6); schleife(b, t, t + 5, X - 200, Y - 60, 220)
label(b, t + 0.4, "Warum?", X + 450, Y - 200, 120, RED)

# ===================== K2 Es geht ums Gefühl =====================
t = S(2, "Die Antwort liegt", "Mythos durchstreichen", "Ein Kalender wird gezeichnet und rot durchgestrichen", ("erklaerung",), "schema")
X, Y = pan(2, 0, t)
kalender(t, X - 450, Y, 420, 360); b.s(t + 0.9, 0.3, line(X - 700, Y + 170, X - 200, Y - 170, n=10), RED, 12); b.snd("gs_paper.wav", t + 0.9, 0.3)
t = S(2, "Sie liegt in", "Gehirn-Skizze", "Rechts ein Gehirn, die Mitte (Gefühl) wird rot schraffiert: GEFÜHL", ("erklaerung",), "schema", "antwort:warum")
brain(b, t, X + 450, Y - 50, 1.4, INK); b.s(t + 0.8, 0.4, spiral(X + 450, Y - 20, 60, 2.5), RED, 6); label(b, t + 1.0, "Gefühl", X + 450, Y + 250, 90, RED)
t = S(2, "Zweitausendeins machten", "Studien-Karteikarte", "Karteikarte 2001 · Tice u. a. · Case Western, Ohio · 88 Studierende", ("zeit", "person", "zahl", "ort"), "exakt", num="2001, 88")
X, Y = pan(2, 1, t)
pin(b, t - 0.2, X - 650, Y - 300, "Ohio, USA", RED, 60)
karteikarte(b, t + 0.2, X - 350, Y + 60, "2001", "Tice u. a., Ohio", "88 Studierende")
t = S(2, "achtundachtzig", "Zahl in Handschrift", "Rechts wird 88 geschrieben und rot eingekreist", ("zahl",), "exakt", num="88")
zahl2(t, X + 450, Y - 50, "88", 200)
t = S(2, "Zuerst wurden manche", "Pose wechselt", "Studentin liest ein Blatt, ihr Gesicht wird traurig, Regenwolke darüber", ("gefuehl",), "schema")
X, Y = pan(2, 2, t)
fig(t, X - 500, Y + 450, 1.1, face="sad"); blatt(t + 0.3, X - 300, Y + 130, 160, 220, 4); cloud(b, t + 0.6, X - 500, Y - 130, 1.0)
label(b, t + 0.8, "schlechte Stimmung", X - 450, Y + 560 - 60, 50, INK)
t = S(2, "Dann hieß es", "Live-Strich", "Rechts ein Mathe-Blatt mit 347 × 268 = ? MATHETEST", ("geschehen",), "exakt")
blatt(t, X + 400, Y - 50, 380, 460, 3); label(b, t + 0.4, "347 × 268 = ?", X + 400, Y - 150, 54, INK); label(b, t + 0.6, "Mathetest", X + 400, Y + 240, 70, RED)
t = S(2, "Ihr habt fünfzehn", "Tagesuhr", "Stoppuhr erscheint: 15 MINUTEN ÜBEN, Zeiger startet", ("zeit", "zahl"), "exakt", num="15 Minuten")
tagesuhr(b, t, X + 50, Y - 300, [(t, 0.0), (t + 3.0, 3.0)], 100, "15 Min. üben")
t = S(2, "Im Raum lagen", "Live-Strich", "Kamera fährt: Tisch mit Puzzleteil, Gamepad, Zeitschrift – verlockend", ("geschehen",), "exakt")
X, Y = pan(2, 3, t)
b.s(t, 0.5, line(X - 700, Y + 200, X + 700, Y + 200, n=12), INK, 8)
tp = A(2, "Puzzle"); b.s(tp, 0.4, poly((X - 600, Y + 180), (X - 600, Y + 60), (X - 520, Y + 60), (X - 520, Y + 20), (X - 460, Y + 20), (X - 460, Y + 60), (X - 380, Y + 60), (X - 380, Y + 180), closed=True), INK, 7)
tg = A(2, "Videospiel"); b.many(tg, 0.4, [rect(X - 150, Y + 80, 300, 110), circle(X - 80, Y + 135, 18, n=10), circle(X + 80, Y + 135, 18, n=10)], INK, 7)
tz = A(2, "Zeitschriften"); b.many(tz, 0.4, [rect(X + 400, Y + 20, 220, 170), line(X + 430, Y + 60, X + 590, Y + 60, n=4)], INK, 7)
label(b, tg + 0.4, "verlockend", X, Y - 150, 80, RED)
t = S(2, "Und jetzt kommt", "Schlüsselwort erscheint", "TRICK DER FORSCHER wird groß geschrieben, Fragezeichen", ("geschehen",), "schema", "frage:kerze")
X, Y = pan(2, 4, t)
schluesselwort(b, t, X, Y - 300, "Der Trick der Forscher", 100, INK)
t = S(2, "Einigen wurde gesagt", "Experiment nachgespielt", "Eine Duftkerze wird gezeichnet, darüber ein Eiskristall: STIMMUNG EINGEFROREN", ("geschehen",), "exakt")
kerze(t, X - 300, Y + 350, 1.3); label(b, t + 0.6, "Duftkerze", X - 300, Y + 440, 60, INK)
for a in range(6): b.s(A(2, "einfrieren") + a * 0.05, 0.1, line(X + 300, Y, X + 300 + 110 * math.cos(a * 1.047), Y + 110 * math.sin(a * 1.047), n=3), INK, 7)
label(b, A(2, "einfrieren"), "Stimmung eingefroren", X + 300, Y + 200, 60, RED, dur=0.6)
t = S(2, "Egal, was sie", "Innerer Regler", "Regler LAUNE schlägt aus, bleibt aber festgefroren in der Mitte", ("gefuehl",), "schema")
X, Y = pan(2, 5, t)
dial(b, t, X - 400, Y, "mies  ·  gut"); dial_needle(b, X - 400, Y, [(t + 0.2, 0.3), (t + 0.8, 0.3)], t + 0.2)
b.snd("stift_klick.wav", t + 0.8, 0.25); label(b, t + 0.6, "bleibt, wie sie ist", X - 400, Y + 300, 56, INK)
t = S(2, "Was passierte", "Mitmach-Test", "Rechts eine Frage an den Zuschauer: WER SCHIEBT AUF? Countdown 3-2-1", ("geschehen",), "schema", "frage:ergebnis")
label(b, t, "Wer schiebt auf?", X + 450, Y - 200, 80, INK)
for i, n_ in enumerate("321"):
    _m = b.mark(); b.txt(t + 0.4 + i * 0.4, 0.15, n_, X + 450, Y, 120, RED); b.clear(_m, b.mark(), t + 0.8 + i * 0.4)
t = S(2, "Wer schlecht gelaunt", "Ursache-Wirkungs-Kette", "Kette: SCHLECHTE LAUNE + ABLENKUNG + ÄNDERBAR → GREIFT ZUM SPIEL", ("erklaerung",), "schema")
X, Y = pan(2, 6, t)
for i, (w_, ph) in enumerate((("schlechte Laune", "schlecht gelaunt"), ("Ablenkung da", "Ablenkungen vor"), ("änderbar", "lasse sich"))):
    label(b, A(2, ph), w_, X - 650 + i * 420, Y - 200, 56, INK)
    if i: arrow(b, A(2, ph) - 0.2, X - 650 + (i - 1) * 420 + 170, Y - 220, X - 650 + i * 420 - 170, Y - 220, INK, 6)
tg = A(2, "griff zur"); arrow(b, tg, X + 320, Y - 220, X + 440, Y - 220, RED, 7)
b.many(tg + 0.3, 0.4, [rect(X + 460, Y - 270, 260, 100), circle(X + 520, Y - 220, 14, n=10), circle(X + 660, Y - 220, 14, n=10)], RED, 7)
t = S(2, "Im Schnitt übten", "Zahl in Handschrift", "Stoppuhr: nur gut 1 von 15 Minuten geübt, rote 1 eingekreist", ("zahl",), "exakt", "antwort:ergebnis", num="1 von 15 Minuten")
label(b, t, "geübt:", X - 400, Y + 200, 70, INK); zahl2(t + 0.3, X - 120, Y + 230, "1", 170); label(b, t + 0.5, "von 15 Min.", X + 250, Y + 230, 70, INK)
motion(2, "nur gut eine Minute", "bars", {"label": "TICE U. A. 2001", "title": "Minuten geübt (von 15)", "unit": " Min.", "bars": [["schlecht + änderbar", 1.3, True], ["schlecht + eingefroren", 9.3, False]]}, 4.6,
       "Schraffur-Balken: schlechte Laune + änderbar nur 1,3 Min. geübt (rot), schlecht + eingefroren 9,3 Min. (Tice u. a. 2001, mit verlockenden Ablenkungen)", ("vergleich", "zeit"), "exakt", num="2001, 1,3 Minuten")
t = S(2, "Wer dagegen glaubte", "Pose wechselt", "Figur mit eingefrorener Laune sitzt am Mathe-Blatt und übt", ("vergleich",), "schema", "antwort:kerze")
X, Y = pan(2, 7, t)
fig(t, X - 400, Y + 450, 1.0, face="neutral", pose="sit"); blatt(t + 0.3, X - 150, Y + 180, 200, 260, 5); check(b, t + 0.7, X - 150, Y - 60, 0.8, RED)
t = S(2, "Das heißt", "Ursache-Wirkungs-Kette", "Kette: MIESES GEFÜHL → HANDY → KURZ BESSER", ("erklaerung",), "schema")
label(b, t, "mieses Gefühl", X + 200, Y - 300, 64, INK); handy(t + 0.6, X + 450, Y - 40, 0.8); label(b, t + 1.2, "kurz besser", X + 700, Y + 200, 64, RED)
arrow(b, t + 0.4, X + 300, Y - 250, X + 420, Y - 150, INK, 6); arrow(b, t + 1.0, X + 500, Y + 60, X + 640, Y + 150, RED, 6)
t = S(2, "Die Forscher Fuschia", "Schlüsselwort erscheint", "STIMMUNGSREPARATUR wird groß geschrieben, darunter Sirois & Pychyl 2013", ("erklaerung", "person"), "exakt", num="2013")
X, Y = pan(2, 8, t)
schluesselwort(b, t, X, Y - 250, "Stimmungsreparatur", 130, INK); label(b, t + 0.4, "Sirois & Pychyl, 2013", X, Y - 100, 56, GREY)
t = S(2, "Die Aufgabe macht", "Metapher verwandelt sich", "Ein Blatt Papier verwandelt sich in eine dunkle Wolke mit LANGEWEILE, ANGST, ZWEIFEL", ("gefuehl",), "schema")
blatt(t, X - 550, Y + 220, 220, 280, 4); arrow(b, t + 0.5, X - 400, Y + 220, X - 200, Y + 220, INK, 6); cloud(b, t + 0.7, X + 100, Y + 200, 1.3, INK)
for i, w_ in enumerate(("Langeweile", "Angst", "Zweifel")): label(b, A(2, w_), w_, X + 350 + (i % 2) * 220, Y + 120 + i * 90, 50, RED)
motion(2, "Und das Handy", "flow", {"label": "STIMMUNGSREPARATUR", "nodes": [{"icon": "doc", "label": "Aufgabe"}, {"icon": "heart", "label": "mieses Gefühl"}, {"icon": "eye", "label": "Handy"}], "packet": "doc", "branch": {"after": 1, "label": "kurz besser"}}, 4.8,
       "Gedankenwolken-Ablauf: Aufgabe → mieses Gefühl → Handy, Abzweig KURZ BESSER", ("erklaerung",), "schema")
t = S(2, "Station Nummer zwei", "Mitmach-Test", "Rückkehr zum Hook: Station 2 GEFÜHL wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(2, 9, t); stationen(2, t, X, Y)
t = S(2, "Doch wer zahlt", "Live-Strich", "Eine Rechnung wird gezeichnet, Empfänger ???", ("geschehen",), "schema", "frage:rechnung")
X, Y = pan(2, 10, t)
blatt(t, X, Y, 360, 460, 5); label(b, t + 0.4, "Rechnung an: ???", X, Y - 280, 70, RED)

# ===================== K3 Dein Zukunfts-Ich =====================
t = S(3, "Die Rechnung zahlt", "Pose wechselt", "Zwei Hauptfiguren: links HEUTE (entspannt), rechts MORGEN (gebeugt mit Rechnung)", ("person",), "schema", "antwort:rechnung")
X, Y = pan(3, 0, t)
fig(t, X - 450, Y + 450, 1.1, hero=True, face="happy"); label(b, t + 0.3, "Ich heute", X - 450, Y - 200, 70, INK)
tm = A(3, "dein Ich"); fig(tm, X + 450, Y + 450, 1.1, hero=True, face="sad"); label(b, tm + 0.3, "Ich morgen", X + 450, Y - 200, 70, RED)
blatt(tm + 0.6, X + 620, Y + 200, 120, 160, 3)
t = S(3, "An der Princeton", "Studien-Karteikarte", "Karteikarte 2008 · Emily Pronin · Princeton · ekliges Getränk", ("zeit", "person", "ort"), "exakt", num="2008")
X, Y = pan(3, 1, t)
pin(b, t - 0.2, X - 650, Y - 300, "Princeton, USA", RED, 60)
karteikarte(b, A(3, "zweitausendacht"), X - 350, Y + 60, "2008", "Emily Pronin, Princeton", "ekliges Getränk")
t = S(3, "Eine Mischung aus", "Live-Strich", "Rechts ein Glas, drei Pfeile: KETCHUP + SOJASOSSE + WASSER", ("geschehen",), "exakt")
glas(t, X + 450, Y + 250, 0.6, 1.3)
for i, w_ in enumerate(("Ketchup", "Sojasoße", "Wasser")): label(b, A(3, w_), w_, X + 250 + i * 220, Y - 260 + (i % 2) * 70, 52, RED if i < 2 else INK)
b.s(A(3, "Wasser") + 0.3, 0.3, poly((X + 400, Y - 120), (X + 420, Y - 50), (X + 470, Y - 110), n=4), INK, 5)
t = S(3, "Sie sollten festlegen", "Mitmach-Test", "Messbecher mit Fragezeichen: WIE VIEL?", ("geschehen",), "schema", "frage:menge")
X, Y = pan(3, 2, t)
label(b, t, "Wie viel?", X, Y - 330, 110, INK)
t = S(3, "Sollten sie selbst", "Experiment nachgespielt", "Links: Figur JETZT bekommt ein fast leeres Glas: ca. 2 Esslöffel", ("vergleich", "zahl"), "exakt", "antwort:menge", num="2 Esslöffel")
fig(t, X - 650, Y + 450, 0.9, face="worried"); glas(t + 0.3, X - 400, Y + 350, 0.12, 1.0, "jetzt: 2 EL")
t = S(3, "Sollte ihr eigenes", "Experiment nachgespielt", "Mitte: dieselbe Figur NÄCHSTES SEMESTER bekommt ein halbvolles Glas (halbe Tasse)", ("vergleich",), "exakt", num="halbe Tasse")
fig(t, X - 100, Y + 450, 0.9, face="neutral"); glas(t + 0.3, X + 150, Y + 350, 0.55, 1.0, "nächstes Semester")
t = S(3, "Ungefähr so viel", "Experiment nachgespielt", "Rechts: ein FREMDER bekommt ebenfalls ein halbvolles Glas, Gleichheitszeichen", ("vergleich",), "schema")
fig(t, X + 450, Y + 450, 0.9, face="neutral", col=GREY); glas(t + 0.3, X + 700, Y + 350, 0.55, 1.0, "Fremder"); b.txt(t + 0.7, 0.3, "=", X + 420, Y + 150, 140, RED)
t = S(3, "Das Zukunfts", "Metapher verwandelt sich", "Die Zukunfts-Figur bekommt ein Namensschild: FREMDER?", ("erklaerung",), "schema")
X, Y = pan(3, 3, t)
fig(t - 0.2, X - 300, Y + 450, 1.2, hero=True, face="neutral"); b.s(t + 0.3, 0.3, rect(X - 460, Y + 20, 320, 90), INK, 6)
label(b, t + 0.6, "Fremder?", X - 300, Y + 65, 60, RED); label(b, t + 0.3, "Zukunfts-Ich", X + 400, Y - 200, 90, INK)
motion(3, "Das Zukunfts", "flip", {"teaser": "Mein Ich in der Zukunft …", "front": {"icon": "person", "title": "das bin doch ich"}, "back": {"title": "wie ein Fremder", "sub": "bekommt die halbe Tasse"}, "at": 2.0}, 4.2,
       "Notizzettel DAS BIN DOCH ICH dreht sich um: WIE EIN FREMDER in Rot", ("erklaerung",), "schema")
t = S(3, "Forscher der Stanford", "Studien-Karteikarte", "Karteikarte 2009 · Stanford · 18 Personen im Hirnscanner", ("zeit", "ort", "zahl"), "exakt", num="2009, 18")
X, Y = pan(3, 4, t)
karteikarte(b, t, X - 450, Y - 100, "2009", "Stanford, USA", "18 Personen")
t = S(3, "Sie legten achtzehn", "Experiment nachgespielt", "Ein Hirnscanner (Röhre) wird gezeichnet, eine Figur liegt darin", ("geschehen", "zahl"), "exakt", num="18")
b.many(t, 0.6, [circle(X + 400, Y + 50, 230), circle(X + 400, Y + 50, 120), line(X + 170, Y + 280, X + 630, Y + 280, n=6)], INK, 9)
b.many(t + 0.6, 0.4, [line(X + 50, Y + 60, X + 400, Y + 60, n=6), circle(X + 20, Y + 60, 32)], INK, 7)
label(b, t + 0.8, "18 Personen", X + 400, Y + 380, 60, RED)
t = S(3, "Die Teilnehmer dachten", "Zeitstrahl Leben", "Zeitstrahl: HEUTE – IN 10 JAHREN, auf beiden Seiten die Hauptfigur", ("zeit",), "exakt", num="10 Jahre")
X, Y = pan(3, 5, t)
b.s(t, 0.6, line(X - 700, Y + 100, X + 700, Y + 100, n=12), INK, 8); arrow(b, t + 0.5, X + 600, Y + 100, X + 720, Y + 100, INK, 8)
fig(t + 0.3, X - 550, Y + 60, 0.7, hero=True, face="happy"); label(b, t + 0.5, "heute", X - 550, Y + 200, 56, INK)
tz = A(3, "in zehn Jahren"); fig(tz, X + 450, Y + 60, 0.7, hero=True, face="neutral"); label(b, tz + 0.3, "in 10 Jahren", X + 450, Y + 200, 56, INK)
t = S(3, "Beim Gedanken an", "Gehirn-Skizze", "Gehirn über der Zukunfts-Figur, eine Region vorne wird nur schwach (grau) schraffiert: WENIGER AKTIV", ("erklaerung",), "schema")
brain(b, t, X + 450, Y - 280, 0.9, INK); b.s(t + 0.6, 0.5, spiral(X + 380, Y - 300, 40, 1.5), GREY, 5); label(b, t + 1.0, "weniger aktiv", X - 100, Y - 300, 64, RED)
t = S(3, "Ein bisschen so", "Netz der Menschen", "Neben der Zukunfts-Figur steht ein Fremder, Verbindungslinie zwischen beiden", ("erklaerung",), "schema")
X, Y = pan(3, 6, t)
netz(b, t, [(X - 400, Y + 200), (X + 400, Y + 200)], [(0, 1)], s=0.9, hero_i=0); label(b, t + 0.6, "wie jemand anderes", X, Y - 250, 80, INK)
t = S(3, "Wichtig: Diese Studie", "Schlüsselwort erscheint", "KLEINE STUDIE (18) wird geschrieben, gestrichelt umrandet", ("erklaerung", "zahl"), "exakt", num="18")
label(b, t, "kleine Studie: 18", X, Y + 450, 70, GREY)
t = S(3, "Station Nummer drei", "Mitmach-Test", "Rückkehr zum Hook: Station 3 FREMDER wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(3, 7, t); stationen(3, t, X, Y)
t = S(3, "Und dieser Fremde", "Pose wechselt", "Ein Paket wird von der Figur HEUTE zu ICH MORGEN geschoben", ("geschehen",), "schema")
X, Y = pan(3, 8, t)
fig(t - 0.3, X - 500, Y + 450, 1.0, hero=True, face="happy"); fig(t, X + 500, Y + 450, 1.0, hero=True, face="sad")
kiste(b, t + 0.3, X, Y + 350, 1.0); arrow(b, t + 0.7, X - 200, Y + 250, X + 300, Y + 250, RED, 7)
t = S(3, "Bleibt die Frage", "Innerer Regler", "Regler LOHNT SICH? schwankt zwischen JA und NEIN", ("gefuehl",), "schema", "frage:lohnt")
dial(b, t, X, Y - 250, "nein  ·  ja"); dial_needle(b, X, Y - 250, [(t + 0.2, 0.5), (t + 1.0, 0.8), (t + 1.8, 0.3), (t + 2.6, 0.6)], t + 0.2)

# ===================== K4 Erst gut, dann teuer =====================
t = S(4, "Neunzehnhundertsiebenundneunzig", "Studien-Karteikarte", "Karteikarte 1997 · Tice & Baumeister · Kurs Gesundheitspsychologie", ("zeit", "person"), "exakt", num="1997")
X, Y = pan(4, 0, t)
karteikarte(b, t, X - 450, Y - 80, "1997", "Tice & Baumeister", "1 Semester")
t = S(4, "Studierende eines", "Experiment nachgespielt", "Rechts eine Reihe Studierender im Hörsaal", ("geschehen",), "schema")
for i in range(5): fig(t + i * 0.1, X + 150 + i * 160, Y + 420, 0.6, face="neutral", w=6)
label(b, t + 0.6, "Gesundheitspsychologie", X + 470, Y - 150, 52, INK)
t = S(4, "Zuerst wurde gemessen", "Live-Strich", "Fragebogen: NEIGST DU ZUM AUFSCHIEBEN? mit Kästchen", ("geschehen",), "schema")
X, Y = pan(4, 1, t)
blatt(t, X - 450, Y, 380, 500, 6); label(b, t + 0.4, "schiebst du auf?", X - 450, Y - 300, 60, RED)
t = S(4, "Dann notierten", "Studie im Zeitraffer", "Tagebuch: Kalenderseiten blättern, Einträge STRESS und BESCHWERDEN", ("geschehen", "zeit"), "schema")
kalender(t, X + 400, Y - 50, 460, 380)
label(b, A(4, "Stress"), "Stress", X + 300, Y + 270, 60, INK); label(b, A(4, "körperlichen"), "Beschwerden", X + 560, Y + 270, 60, INK)
t = S(4, "Am Anfang des", "Handgezeichnetes Diagramm", "Achsen werden gezogen: SEMESTER (Anfang → Ende), STRESS nach oben", ("vergleich",), "schema", "frage:kurve")
X, Y = pan(4, 2, t)
achsen(t, X - 650, Y + 330, 1300, 650, "Semester: Anfang ... Ende", "Stress")
t = S(4, "Sie hatten weniger", "Handgezeichnetes Diagramm", "Rote Linie AUFSCHIEBER startet unten, graue Linie ANDERE höher", ("vergleich",), "schema")
kurve(t, X - 650, Y + 330, 650, 650, [0.15, 0.18, 0.2], RED, 0.8); kurve(t + 0.4, X - 650, Y + 330, 650, 650, [0.45, 0.47, 0.5], GREY, 0.8)
label(b, t + 0.5, "Aufschieber", X - 450, Y + 250, 50, RED); label(b, t + 0.8, "andere", X - 450, Y - 40, 50, GREY)
t = S(4, "Klar: Die Abgabe", "Pose wechselt", "Kleine Hauptfigur liegt in der Hängematte, die Abgabe-Flagge steht weit weg", ("geschehen",), "schema")
fig(t, X - 150, Y + 280, 0.4, hero=True, face="happy", pose="arms_up"); b.many(t + 0.3, 0.4, [line(X + 600, Y + 320, X + 600, Y + 120, n=4), poly((X + 600, Y + 120), (X + 700, Y + 150), (X + 600, Y + 180))], RED, 6)
label(b, t + 0.5, "Abgabe", X + 600, Y + 80, 46, RED)
t = S(4, "Doch gegen Ende", "Handgezeichnetes Diagramm", "Die rote Linie schießt steil nach oben, überholt die graue", ("vergleich",), "schema", "antwort:kurve")
kurve(t, X, Y + 330 - 650 * 0.2, 650, 650 * 0.75, [0.0, 0.3, 1.0], RED, 1.0); kurve(t + 0.3, X, Y + 330 - 650 * 0.5, 650, 650 * 0.2, [0.0, 0.2, 0.5], GREY, 0.8)
treffer(t + 1.0, 0.45)
t = S(4, "Jetzt hatten die", "Gewicht auf den Schultern", "Kamera fährt zur Hauptfigur, ein riesiger Stein wächst auf ihren Schultern: STRESS", ("gefuehl",), "schema")
X, Y = pan(4, 3, t)
fig(t - 0.3, X - 300, Y + 450, 1.2, hero=True, face="sad"); gewicht(b, X - 300, Y + 450 - 282, [(t, 0.1), (t + 1.2, 1.0)], t, label_txt="Stress")
t = S(4, "Über das ganze", "Zahl in Handschrift", "Daneben: INSGESAMT MEHR BESCHWERDEN, ein rotes Plus eingekreist", ("vergleich",), "schema")
label(b, t, "insgesamt mehr Beschwerden", X + 400, Y - 250, 60, INK); zahl2(t + 0.4, X + 400, Y + 50, "+", 220)
motion(4, "Und die Noten", "bars", {"label": "TICE & BAUMEISTER 1997", "title": "Zusammenhang Aufschieben – schlechtere Note (r)", "unit": "", "bars": [["Hausarbeit", 0.26, False], ["Prüfungen", 0.66, True]]}, 4.4,
       "Schraffur-Balken: Wie stark hängt Aufschieben mit schlechteren Noten zusammen – Hausarbeit r = 0,26, Prüfungen r = 0,66 (rot), Tice & Baumeister 1997, Studie 2", ("vergleich", "zeit"), "exakt", num="1997")
t = S(4, "Die waren bei", "Live-Strich", "Zeugnis mit roter schlechterer Note, Pfeil nach unten", ("vergleich",), "schema")
X, Y = pan(4, 4, t)
blatt(t, X - 450, Y, 320, 420, 5); note(t + 0.5, X - 450, Y + 120, "4", RED, 120)
t = S(4, "Bei der Hausarbeit", "Live-Strich", "Rechts: Hausarbeit (Blatt) und Prüfung (Uhr + Blatt), bei der Prüfung ein dickes rotes Minus", ("vergleich",), "schema")
label(b, t, "Hausarbeit –", X + 150, Y - 150, 60, INK); label(b, A(4, "Prüfungen"), "Prüfungen – –", X + 500, Y + 50, 70, RED)
t = S(4, "Wichtig: Das waren", "Schlüsselwort erscheint", "KLEINE KURSE · ZUSAMMENHANG, KEIN BEWEIS in Grau", ("erklaerung",), "schema")
label(b, t, "kleine Kurse", X, Y + 330, 60, GREY); label(b, A(4, "Zusammenhang"), "Zusammenhang, kein Beweis", X, Y + 420, 60, GREY)
t = S(4, "Die Erleichterung am", "Metapher verwandelt sich", "Ein Geschenk wird gezeichnet und verwandelt sich in einen Kreditvertrag mit ZINSEN", ("erklaerung",), "schema", "antwort:lohnt")
X, Y = pan(4, 5, t)
b.many(t, 0.5, [rect(X - 650, Y - 100, 280, 220), line(X - 510, Y - 100, X - 510, Y + 120, n=4), line(X - 650, Y + 10, X - 370, Y + 10, n=4)], INK, 8)
tk = A(4, "Kredit"); b.s(tk, 0.3, line(X - 680, Y + 140, X - 340, Y - 130, n=8), RED, 10); arrow(b, tk + 0.2, X - 300, Y, X - 50, Y, INK, 7)
blatt(tk + 0.4, X + 150, Y, 300, 380, 5); label(b, tk + 0.6, "Kredit", X + 150, Y - 250, 70, RED)
t = S(4, "Und der wird", "Zahl in Handschrift", "Neben dem Kredit: + ZINSEN, rot eingekreist", ("erklaerung",), "schema")
label(b, t, "+ Zinsen", X + 550, Y + 50, 90, RED); b.s(t + 0.4, 0.4, circle(X + 550, Y + 30, 200, ry=90), RED, 7)
t = S(4, "Station Nummer vier", "Mitmach-Test", "Rückkehr zum Hook: Station 4 KREDIT wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen", "")
X, Y = pan(4, 6, t); stationen(4, t, X, Y)
t = S(4, "Aber ist das", "Live-Strich", "Eine gestrichelte Spur führt aus dem Bild heraus, Fragezeichen am Ende", ("geschehen",), "schema", "frage:spur")
X, Y = pan(4, 7, t)
for i in range(9): b.s(t + i * 0.1, 0.1, line(X - 700 + i * 160, Y + 100 - i * 20, X - 620 + i * 160, Y + 90 - i * 20, n=3), INK, 8)
b.txt(t + 1.0, 0.3, "?", X + 750, Y - 150, 200, RED)

# ===================== K5 Die lange Spur =====================
t = S(5, "Zweitausenddreiundzwanzig", "Studien-Karteikarte", "Karteikarte 2023 · Johansson u. a. · Schweden · 3.525 Studierende", ("zeit", "person", "zahl", "ort"), "exakt", "antwort:spur", num="2023, 3525")
X, Y = pan(5, 0, t)
pin(b, t - 0.2, X - 600, Y - 300, "Schweden", RED, 60); karteikarte(b, t + 0.2, X - 350, Y + 60, "2023", "Johansson u. a.", "3.525 Studierende")
t = S(5, "Forschende um Fred", "Zahl in Handschrift", "Rechts wird 3.525 groß geschrieben und eingekreist", ("zahl",), "exakt", num="3525")
zahl2(A(5, "dreitausendfünfhundertfünfundzwanzig"), X + 450, Y - 50, "3.525", 160)
t = S(5, "acht Hochschulen", "Live-Strich", "Acht kleine Uni-Gebäude rund um STOCKHOLM und ÖREBRO", ("ort", "zahl"), "exakt", num="8 Hochschulen")
X, Y = pan(5, 1, t)
for i in range(8): b.many(t + i * 0.1, 0.25, [rect(X - 700 + i * 190, Y - 60, 130, 110), poly((X - 710 + i * 190, Y - 60), (X - 635 + i * 190, Y - 130), (X - 560 + i * 190, Y - 60))], INK, 6)
label(b, A(5, "Stockholm"), "Stockholm", X - 300, Y + 180, 70, INK); label(b, A(5, "Örebro"), "Örebro", X + 350, Y + 180, 70, INK)
t = S(5, "Neun Monate später", "Tagesuhr", "Kalender blättert 9 Monate weiter: 9 MONATE SPÄTER", ("zeit", "zahl"), "exakt", num="9 Monate")
X, Y = pan(5, 2, t)
kalender(t, X - 450, Y, 420, 360)
counter(b, X + 350, Y + 50, t + 0.2, t + 1.6, 0, 9, 220, RED); label(b, t + 1.0, "Monate später", X + 350, Y + 200, 70, INK)
t = S(5, "Das Ergebnis", "Handgezeichnetes Diagramm", "Achsen AUFSCHIEBEN → SYMPTOME, eine leicht ansteigende Linie", ("vergleich",), "schema")
X, Y = pan(5, 3, t)
achsen(t, X - 650, Y + 330, 800, 600, "mehr Aufschieben", "Symptome"); kurve(t + 0.6, X - 650, Y + 330, 800, 600, [0.3, 0.38, 0.46], RED, 1.2)
for i, w_ in enumerate(("Depression", "Angst", "Stress")): label(b, A(5, w_), w_, X + 500, Y - 250 + i * 110, 60, INK)
motion(5, "Dazu häufiger", "flow", {"label": "JOHANSSON U. A. 2023", "nodes": [{"icon": "clock", "label": "Aufschieben"}, {"icon": "brain", "label": "9 Monate später"}, {"icon": "heart", "label": "Schlaf, Einsamkeit, Geld"}], "packet": "doc"}, 4.6,
       "Gedankenwolken-Ablauf: Aufschieben → 9 Monate später → schlechter Schlaf, Einsamkeit, Geldsorgen (Johansson u. a. 2023)", ("erklaerung", "zeit"), "exakt", num="2023, 9 Monate")
t = S(5, "Und sogar öfter", "Pose wechselt", "Hauptfigur reibt sich die Schulter, rote Schmerz-Zacken an Schulter und Arm", ("person",), "schema")
X, Y = pan(5, 4, t)
fig(t - 0.2, X - 300, Y + 450, 1.3, hero=True, face="worried")
for i in range(3): b.s(t + 0.4 + i * 0.1, 0.15, poly((X - 200 + i * 30, Y + 60 - i * 20), (X - 170 + i * 30, Y + 30 - i * 20), (X - 150 + i * 30, Y + 70 - i * 20), n=3), RED, 6)
label(b, t + 0.5, "Schultern & Arme", X + 400, Y - 100, 70, INK)
t = S(5, "Jetzt ganz wichtig", "Schlüsselwort erscheint", "KLEINE UNTERSCHIEDE wird geschrieben und unterstrichen", ("erklaerung",), "schema")
X, Y = pan(5, 5, t)
schluesselwort(b, t, X, Y - 300, "kleine Unterschiede", 110, INK)
t = S(5, "Und so eine", "Zwei Wege", "Board teilt sich: ZUSAMMENHANG (Linie zwischen zwei Punkten) vs. URSACHE (Pfeil) – Pfeil wird rot durchgestrichen", ("erklaerung",), "schema")
zwei_wege(b, t, X, Y + 150, "Zusammenhang", "Ursache?", 600, 70)
b.many(t + 0.4, 0.4, [circle(X - 600, Y + 250, 40), circle(X - 300, Y + 250, 40), line(X - 560, Y + 250, X - 340, Y + 250, n=6)], INK, 7)
arrow(b, A(5, "Sie beweist"), X + 250, Y + 250, X + 600, Y + 250, INK, 7); b.s(A(5, "Ursache") + 0.3, 0.3, line(X + 230, Y + 330, X + 620, Y + 170, n=6), RED, 10)
t = S(5, "Vielleicht geht es", "Ursache-Wirkungs-Kette", "Umgekehrter Pfeil: SCHLECHTES BEFINDEN → MEHR AUFSCHIEBEN", ("erklaerung",), "schema")
X, Y = pan(5, 6, t)
label(b, t, "schlechtes Befinden", X - 400, Y - 100, 70, INK); arrow(b, t + 0.6, X - 60, Y - 120, X + 180, Y - 120, RED, 7); label(b, t + 0.9, "mehr Aufschieben", X + 450, Y - 100, 70, INK)
t = S(5, "Die Forscher haben", "Live-Strich", "Waagschale: FRÜHERE WERTE werden abgezogen, die Linie bleibt sichtbar", ("erklaerung",), "schema")
label(b, t, "frühere Werte eingerechnet", X, Y + 150, 64, INK); check(b, t + 0.8, X + 520, Y + 140, 0.7, RED)
t = S(5, "Ganz ausschließen", "Live-Strich", "Darunter in Grau: ANDERE URSACHEN MÖGLICH", ("erklaerung",), "schema")
label(b, t, "andere Ursachen möglich", X, Y + 300, 60, GREY)
t = S(5, "Station Nummer fünf", "Mitmach-Test", "Rückkehr zum Hook: Station 5 SPUR wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(5, 7, t); stationen(5, t, X, Y)
t = S(5, "Es kann sich", "Netz der Menschen", "Von der Hauptfigur gehen Linien zu Schlaf, Geld, Freunde, Gesundheit", ("erklaerung",), "schema")
X, Y = pan(5, 8, t)
fig(t, X, Y + 150, 0.8, hero=True, face="neutral")
for i, w_ in enumerate(("Schlaf", "Geld", "Freunde", "Körper")):
    a = -2.6 + i * 1.1; ex, ey = X + 600 * math.cos(a), Y - 40 + 330 * math.sin(a) + 100
    b.s(t + 0.3 + i * 0.15, 0.25, line(X, Y - 20, ex, ey, n=6), GREY, 5); label(b, t + 0.4 + i * 0.15, w_, ex, ey, 56, INK)
t = S(5, "Und jetzt kommt", "Metapher verwandelt sich", "Das Wort AUFSCHIEBEN wird gespiegelt und dreht sich um: ???", ("geschehen",), "schema", "frage:gegenteil")
X, Y = pan(5, 9, t)
label(b, t, "Aufschieben", X - 350, Y - 100, 100, INK); arrow(b, t + 0.6, X - 50, Y - 120, X + 150, Y - 120, RED, 8); deckkarte(t + 0.8, X + 450, Y - 100, "???", 420, 180)

# ===================== K6 Das Gegenteil =====================
t = S(6, "Zweitausendvierzehn", "Studien-Karteikarte", "Karteikarte 2014 · David Rosenbaum · Penn State, USA", ("zeit", "person", "ort"), "exakt", num="2014")
X, Y = pan(6, 0, t)
karteikarte(b, t, X - 450, Y - 100, "2014", "Rosenbaum, Penn State", "Eimer-Versuch")
t = S(6, "Studierende in einen", "Live-Strich", "Ein langer Gang wird mit zwei Linien gezogen", ("ort",), "schema")
X, Y = pan(6, 1, t)
b.many(t, 0.7, [line(X - 850, Y + 120, X + 850, Y + 120, n=14), line(X - 850, Y + 420, X + 850, Y + 420, n=14)], INK, 8)
label(b, t + 0.5, "Ende", X + 760, Y + 60, 56, RED); b.s(t + 0.6, 0.3, line(X + 800, Y + 120, X + 800, Y + 420, n=5), RED, 8)
t = S(6, "Im Gang standen", "Experiment nachgespielt", "Zwei Eimer erscheinen: einer vorne, einer weiter hinten", ("geschehen",), "exakt")
eimer(A(6, "vorne"), X - 400, Y + 330, 0.9); eimer(A(6, "hinten"), X + 300, Y + 330, 0.9)
label(b, A(6, "vorne") + 0.3, "vorne", X - 400, Y + 500, 46, GREY); label(b, A(6, "hinten") + 0.3, "hinten", X + 300, Y + 500, 46, GREY)
t = S(6, "Die Aufgabe: Nimm", "Figur bewegt sich", "Hauptfigur läuft in den Gang hinein", ("geschehen",), "schema")
walker(b, t, t + 2.0, X - 900, X - 650, Y + 400, 0.8, hero=True)
t = S(6, "Die vernünftige Wahl", "Ursache-Wirkungs-Kette", "Gestrichelte Linie vom hinteren Eimer zum Ende: KURZE STRECKE (grün gemeint, hier schwarz)", ("erklaerung",), "schema", "frage:eimer")
arrow(b, t + 0.3, X + 380, Y + 200, X + 780, Y + 200, INK, 6); label(b, t + 0.6, "kurz", X + 580, Y + 50, 60, INK)
t = S(6, "Doch fast alle", "Experiment nachgespielt", "Die Figur greift den VORDEREN Eimer – lange rote Strecke bis zum Ende", ("geschehen",), "exakt", "antwort:eimer")
arrow(b, t + 0.4, X - 330, Y + 160, X + 780, Y + 160, RED, 8); label(b, t + 0.8, "lang!", X + 200, Y - 10, 80, RED)
motion(6, "Doch fast alle", "counter", {"label": "ROSENBAUM U. A. 2014", "value": 9, "suffix": " Versuche", "caption": "FAST ALLE NAHMEN DEN NÄHEREN EIMER"}, 4.0,
       "Zahl rot eingekreist: 9 Versuche, Unterschrift FAST ALLE NAHMEN DEN NÄHEREN EIMER (Rosenbaum u. a. 2014)", ("zahl", "zeit"), "exakt", num="9 Versuche, 2014")
t = S(6, "Warum? Viele sagten", "Blick in den Kopf", "Gedankenblase über der Figur: SCHNELL ERLEDIGEN!", ("gefuehl",), "schema")
X, Y = pan(6, 2, t)
fig(t - 0.2, X - 550, Y + 450, 1.0, face="happy"); eimer(t, X - 380, Y + 400, 0.6)
bubble(b, t + 0.2, X + 200, Y - 150, 900, 450, None); label(b, t + 0.6, "schnell erledigen!", X + 200, Y - 150, 80, RED)
t = S(6, "Rosenbaum nannte das", "Schlüsselwort erscheint", "PRÄ-KRASTINATION wird groß geschrieben und unterstrichen", ("erklaerung",), "exakt")
X, Y = pan(6, 3, t)
schluesselwort(b, t, X, Y - 250, "Prä-Krastination", 150, INK)
t = S(6, "Das Gegenteil von", "Zwei Wege", "Darunter Board geteilt: AUFSCHIEBEN ↔ PRÄ-KRASTINATION", ("vergleich",), "schema", "antwort:gegenteil")
label(b, t, "Aufschieben", X - 450, Y + 50, 80, INK); label(b, t + 0.4, "Prä-Krastination", X + 450, Y + 50, 80, RED); b.txt(t + 0.7, 0.3, "vs.", X, Y + 60, 80, GREY)
t = S(6, "Er vermutet", "Gehirn-Skizze", "Gehirn mit einer Liste, ein Punkt wird abgehakt, der Kopf wird leichter", ("erklaerung",), "schema")
brain(b, t, X - 300, Y + 330, 0.9, INK); check(b, t + 0.6, X + 100, Y + 300, 0.9, RED); label(b, t + 0.8, "Kopf entlastet", X + 450, Y + 330, 60, INK)
t = S(6, "Und hier liegt", "Kamerafahrt übers Board", "Kamera fährt zu einer Waage mit JETZT und SPÄTER", ("erklaerung",), "schema")
X, Y = pan(6, 4, t)
b.many(t, 0.6, [line(X, Y + 380, X, Y - 100, n=6), line(X - 200, Y + 380, X + 200, Y + 380, n=6), line(X - 380, Y - 160, X + 380, Y - 40, n=8)], INK, 8)
label(b, t + 0.4, "jetzt", X - 380, Y - 240, 80, RED); label(b, t + 0.6, "später", X + 380, Y - 120, 80, GREY)
t = S(6, "Aufschieben und Prä", "Schlüsselwort erscheint", "Über der Waage: DAS JETZT GEWINNT, rot unterstrichen", ("erklaerung",), "schema")
schluesselwort(b, A(6, "gewinnt das"), X, Y - 400, "Das Jetzt gewinnt.", 100, INK)
t = S(6, "Der eine schiebt", "Zwei Wege", "Links Figur schiebt Kiste weg, rechts Figur hakt eine Liste ab", ("vergleich",), "schema")
X, Y = pan(6, 5, t)
zwei_wege(b, t, X, Y + 40, "wegschieben", "irgendwas abhaken", 860, 70)
fig(t + 0.2, X - 600, Y + 450, 0.9, face="worried"); kiste(b, t + 0.4, X - 300, Y + 370, 0.8); arrow(b, t + 0.7, X - 200, Y + 300, X - 80, Y + 300, INK, 6)
ta = A(6, "Der andere"); fig(ta, X + 300, Y + 450, 0.9, face="happy")
for i in range(3): check(b, ta + 0.4 + i * 0.2, X + 600, Y + 100 + i * 100, 0.5, INK)
motion(6, "Kennst du das", "phone", {"label": "KENNST DU DAS?", "app": "POSTEINGANG", "messages": [["10 neue E-Mails", False], ["Alle beantwortet!", True], ["Die große Aufgabe? Morgen.", True]]}, 4.6,
       "Gezeichnetes Handy: 10 NEUE E-MAILS – ALLE BEANTWORTET – DIE GROSSE AUFGABE? MORGEN.", ("geschehen",), "schema")
t = S(6, "Du beantwortest zehn", "Live-Strich", "Zehn kleine Briefumschläge mit Haken, daneben ein großer unberührter Stapel", ("geschehen", "zahl"), "exakt", num="10")
X, Y = pan(6, 6, t)
for i in range(10): b.many(t + i * 0.08, 0.15, [rect(X - 760 + (i % 5) * 150, Y - 200 + (i // 5) * 140, 120, 80), poly((X - 760 + (i % 5) * 150, Y - 200 + (i // 5) * 140), (X - 700 + (i % 5) * 150, Y - 160 + (i // 5) * 140), (X - 640 + (i % 5) * 150, Y - 200 + (i // 5) * 140))], INK, 5)
stapel(A(6, "die eine"), X + 450, Y + 250, 10, 300); label(b, A(6, "anzufangen"), "die eine große Aufgabe", X + 450, Y - 250, 56, RED)
t = S(6, "Station Nummer sechs", "Mitmach-Test", "Rückkehr zum Hook: Station 6 GEGENTEIL wird rot abgehakt", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(6, 7, t); stationen(6, t, X, Y)
t = S(6, "Doch was hilft", "Gedankenschleife", "Rote Schleife um ein großes WAS HILFT?", ("gefuehl",), "schema", "frage:hilft")
X, Y = pan(6, 8, t)
label(b, t, "Was hilft?", X, Y - 100, 130, INK); schleife(b, t + 0.2, t + 5, X, Y - 120, 300)
t = S(6, "Dazu gibt es", "Studien-Karteikarte", "Eine abgedeckte Karteikarte BERÜHMTES EXPERIMENT ??? wird angeheftet", ("geschehen",), "schema", "frage:fristen")
deckkarte(t, X, Y + 330, "Experiment ???", 700, 180)

# ===================== K7 Der Fristen-Mythos =====================
t = S(7, "Zweitausendzwei erschien", "Studien-Karteikarte", "Karteikarte 2002 · Fristen-Experiment · Korrekturlesen", ("zeit",), "exakt", num="2002")
X, Y = pan(7, 0, t)
karteikarte(b, t, X - 450, Y - 100, "2002", "Fristen-Experiment", "Korrekturlesen")
t = S(7, "Menschen sollten Texte", "Experiment nachgespielt", "Figur am Tisch, roter Stift, ein Text mit Fehlern wird markiert", ("geschehen",), "schema")
fig(t, X + 250, Y + 450, 0.9, face="neutral", pose="sit"); blatt(t + 0.3, X + 550, Y + 150, 260, 340, 6)
for i in range(3): b.s(t + 0.7 + i * 0.15, 0.15, circle(X + 500 + i * 40, Y + 80 + i * 60, 22, n=10), RED, 5)
t = S(7, "Wer feste Fristen", "Handgezeichnetes Diagramm", "Zwei Balken: FESTE FRISTEN fast doppelt so hoch wie EINE FRIST AM ENDE – mit Fragezeichen ANGEBLICH", ("vergleich",), "schema")
X, Y = pan(7, 1, t)
bars(b, X - 400, Y + 330, [(t + 0.3, 0.85, INK, "feste Fristen"), (t + 0.7, 0.45, GREY, "Frist am Ende")], h=560, bw=180, gap=120, lab=46)
label(b, A(7, "angeblich"), "angeblich!", X + 450, Y - 250, 90, RED)
t = S(7, "Die Studie wurde", "Studien-Stapel (`motion` stack)", "Studien-Stapel: Bücher, Vorträge, Ratgeber zitieren die Studie", ("erklaerung",), "schema")
motion(7, "Die Studie wurde", "stack", {"label": "ZITIERT IN ...", "cards": [["Bücher", "zitiert"], ["Vorträge", "zitiert"], ["Ratgeber", "zitiert"], ["Original", "2002"]], "symbol": "!", "question": "Stimmt das wirklich?"}, 4.4,
       "Studien-Stapel: Karten Buch, Vortrag, Ratgeber stapeln sich, Frage STIMMT DAS WIRKLICH?", ("erklaerung",), "schema", sound=True)
SHOTS.pop(-2)   # doppelter Eintrag (S + motion) entfernen
t = S(7, "Auch dieses Video", "Pose wechselt", "Hauptfigur hält schon eine Karteikarte hoch, zögert", ("geschehen",), "schema")
X, Y = pan(7, 2, t)
fig(t, X - 400, Y + 450, 1.1, hero=True, face="happy"); b.s(t + 0.3, 0.3, rect(X - 300, Y - 60, 200, 140), INK, 6)
t = S(7, "Doch zweitausendsechsundzwanzig", "Live-Strich", "Kalenderblatt 2026 erscheint, die Figur erschrickt", ("zeit",), "exakt", num="2026")
kalender(t + 0.2, X + 400, Y - 50, 420, 360); label(b, t + 0.5, "2026", X + 400, Y - 170, 70, RED)
b.txt(t + 0.9, 0.3, "!", X - 400, Y - 50, 140, RED)
t = S(7, "Die Ökonomen Kyle", "Experiment nachgespielt", "Das Experiment wird ein zweites Mal gezeichnet: WIEDERHOLT – Balken fast gleich hoch", ("vergleich",), "schema")
X, Y = pan(7, 3, t)
label(b, t, "wiederholt:", X - 450, Y - 330, 80, INK)
bars(b, X - 500, Y + 330, [(t + 0.4, 0.55, INK, "feste Fristen"), (t + 0.7, 0.5, GREY, "Frist am Ende")], h=520, bw=170, gap=100, lab=44)
label(b, A(7, "kaum einen"), "kaum ein Effekt", X - 450, Y - 230, 64, RED)
t = S(7, "Andere Forscher meldeten", "Blick in den Kopf", "Lupe über einer Datentabelle, einige Zeilen sind rot markiert: AUFFÄLLIG", ("geschehen",), "schema")
for i in range(6): b.s(t + i * 0.06, 0.12, line(X + 200, Y - 250 + i * 80, X + 750, Y - 250 + i * 80, n=6), GREY, 5)
b.many(t + 0.5, 0.4, [circle(X + 480, Y - 90, 150), line(X + 590, Y + 20, X + 700, Y + 130, n=4)], RED, 9)
b.s(t + 0.9, 0.2, rect(X + 210, Y - 115, 540, 50), RED, 5); label(b, t + 1.0, "auffällig", X + 480, Y + 250, 64, RED)
t = S(7, "Und im September", "Mythos durchstreichen", "Die Karteikarte 2002 wird rot durchgestrichen: ZURÜCKGEZOGEN (Sept. 2026)", ("zeit", "erklaerung"), "exakt", "antwort:fristen", num="September 2026")
X, Y = pan(7, 4, t)
karteikarte(b, t - 0.5, X - 300, Y - 100, "2002", "Fristen-Experiment", "Korrekturlesen", sound=False)
b.s(t + 0.3, 0.3, line(X - 600, Y + 60, X, Y - 260, n=10), RED, 12); b.snd("gs_paper.wav", t + 0.3, 0.4)
label(b, t + 0.7, "zurückgezogen", X + 450, Y - 150, 90, RED); label(b, t + 1.0, "September 2026", X + 450, Y - 50, 56, INK)
motion(7, "Sie könne die", "flip", {"teaser": "Feste Fristen wirken …", "front": {"icon": "doc", "title": "fast doppelt so gut"}, "back": {"title": "zurückgezogen", "sub": "Sept. 2026 – Ergebnis nicht haltbar"}, "at": 2.0}, 4.4,
       "Notizzettel FAST DOPPELT SO GUT dreht sich um: ZURÜCKGEZOGEN – SEPT. 2026 in Rot", ("erklaerung", "zeit"), "exakt", num="2026")
t = S(7, "Was bleibt also", "Mitmach-Test", "Großes Fragezeichen: WAS BLEIBT?", ("gefuehl",), "schema")
X, Y = pan(7, 5, t)
label(b, t, "Was bleibt?", X, Y - 300, 110, INK)
t = S(7, "Dieselben Ökonomen", "Studien-Karteikarte", "Karteikarte 2020 · Bisin & Hyndman · Experiment mit Studierenden", ("person", "zeit"), "exakt", num="2020")
karteikarte(b, t, X - 450, Y + 120, "2020", "Bisin & Hyndman", "Studierende")
t = S(7, "Viele Studierende setzen", "Live-Strich", "Figur trägt selbst Fristen in einen Kalender ein (rote Kreise)", ("geschehen",), "schema")
kalender(t, X + 400, Y + 120, 400, 330)
for i in range(3): b.s(t + 0.6 + i * 0.25, 0.25, circle(X + 290 + i * 110, Y + 100 + i * 50, 35, n=20), RED, 7)
t = S(7, "Sie ahnen also", "Blick in den Kopf", "Gedankenblase: ICH KENNE MICH ...", ("gefuehl",), "schema")
X, Y = pan(7, 6, t)
fig(t - 0.2, X - 550, Y + 450, 1.0, hero=True, face="worried"); bubble(b, t, X + 150, Y - 150, 900, 420, None); label(b, t + 0.4, "Ich kenne mich ...", X + 150, Y - 150, 80, INK)
t = S(7, "Aber sie wurden", "Handgezeichnetes Diagramm", "Zwei gleich hohe Balken: MIT EIGENEN FRISTEN = OHNE, Gleichheitszeichen", ("vergleich",), "schema")
bars(b, X + 330, Y + 400, [(t + 0.2, 0.5, INK, "eigene Fristen"), (t + 0.5, 0.5, GREY, "ohne")], h=300, bw=150, gap=100, lab=40)
b.txt(t + 0.9, 0.3, "=", X + 455, Y + 270, 120, RED)
t = S(7, "Station Nummer sieben", "Mitmach-Test", "Rückkehr zum Hook: Station 7 FRIST wird rot abgehakt – alle Stationen erreicht", ("zahl",), "exakt", "teaser:stationen")
X, Y = pan(7, 7, t); stationen(7, t, X, Y)
t = S(7, "Das ist übrigens", "Schlüsselwort erscheint", "EINFACHE, SCHÖNE GESCHICHTE wird geschrieben, daneben ein Gehirn mit Herz", ("erklaerung",), "schema")
X, Y = pan(7, 8, t)
schluesselwort(b, A(7, "Eine einfache"), X, Y - 250, "einfache, schöne Geschichte", 100, INK); brain(b, t, X - 300, Y + 250, 0.9, INK); heart(b, t + 0.8, X + 200, Y + 250, 1.2)
t = S(7, "Und damit sind", "Kamerafahrt übers Board", "Kamera fährt zur abgedeckten TRICK-Karte vom Anfang", ("geschehen",), "schema", "teaser:trick")
X, Y = pan(7, 9, t)
deckkarte(t - 0.3, X, Y - 100, "Trick: ???", 900, 220); label(b, A(7, "Wie kommt"), "Wie kommt man da raus?", X, Y + 250, 80, INK)

# ===================== K8 So trickst du es aus =====================
t = S(8, "Der erste Schritt", "Schlüsselwort erscheint", "SCHRITT 1: VERGIB DIR wird groß geschrieben", ("erklaerung",), "schema", "antwort:hilft")
X, Y = pan(8, 0, t)
label(b, t, "Schritt 1", X - 500, Y - 330, 80, RED); schluesselwort(b, A(8, "Vergib dir"), X, Y - 150, "Vergib dir.", 170, INK)
t = S(8, "An der Carleton", "Studien-Karteikarte", "Karteikarte 2010 · Wohl, Pychyl & Bennett · Ottawa · 119 Erstsemester", ("zeit", "person", "zahl", "ort"), "exakt", num="2010, 119")
X, Y = pan(8, 1, t)
pin(b, t - 0.2, X - 650, Y - 300, "Ottawa, Kanada", RED, 60); karteikarte(b, t + 0.3, X - 350, Y + 60, "2010", "Wohl, Pychyl & Bennett", "119 Erstsemester")
t = S(8, "hundertneunzehn", "Zahl in Handschrift", "Rechts: 119 groß, rot eingekreist; darunter zwei Prüfungsblätter", ("zahl",), "exakt", num="119")
zahl2(t, X + 450, Y - 150, "119", 170); blatt(t + 0.6, X + 300, Y + 280, 160, 200, 3); blatt(t + 0.8, X + 600, Y + 280, 160, 200, 3)
label(b, t + 1.0, "Prüfung 1", X + 300, Y + 430, 40, INK); label(b, t + 1.1, "Prüfung 2", X + 600, Y + 430, 40, INK)
t = S(8, "Wer sich verziehen", "Pose wechselt", "Hauptfigur legt sich die Hand aufs Herz, lächelt; Pfeil zu Prüfung 2 mit weniger Aufschieben", ("person",), "schema")
X, Y = pan(8, 2, t)
fig(t, X - 450, Y + 450, 1.2, hero=True, face="happy"); heart(b, t + 0.4, X - 450, Y + 120, 0.8)
arrow(b, A(8, "schob vor"), X - 200, Y + 100, X + 150, Y + 100, RED, 7); label(b, A(8, "schob vor") + 0.3, "weniger aufgeschoben", X + 450, Y + 90, 60, INK)
label(b, A(8, "vor allem"), "vor allem bei starken Aufschiebern", X + 300, Y + 300, 46, GREY)
t = S(8, "Die Erklärung der", "Innerer Regler", "Regler SCHLECHTE GEFÜHLE sinkt nach unten", ("gefuehl",), "schema")
X, Y = pan(8, 3, t)
dial(b, t, X - 450, Y - 50, "wenig  ·  viel"); dial_needle(b, X - 450, Y - 50, [(t + 0.2, 0.85), (t + 1.4, 0.2)], t + 0.2); b.snd("stift_klick.wav", t + 1.4, 0.25)
label(b, t + 0.3, "schlechte Gefühle", X - 450, Y + 250, 56, INK)
t = S(8, "Und weniger schlechte", "Ursache-Wirkungs-Kette", "Kette zurück zu Station 2: WENIGER GEFÜHL → WENIGER FLUCHT", ("erklaerung",), "schema")
label(b, t, "weniger Gefühl", X + 350, Y - 250, 64, INK); arrow(b, t + 0.6, X + 350, Y - 180, X + 350, Y - 20, RED, 7); label(b, A(8, "Flucht"), "weniger Flucht", X + 350, Y + 60, 64, RED)
label(b, A(8, "Station zwei"), "(Station 2)", X + 350, Y + 160, 46, GREY)
t = S(8, "Wer sich selbst", "Gedankenschleife", "Rote Schleife um eine traurige Figur: SELBSTVORWURF füttert das Gefühl", ("gefuehl",), "schema")
X, Y = pan(8, 4, t)
fig(t, X - 300, Y + 450, 1.1, face="sad"); schleife(b, t + 0.2, t + 4, X - 300, Y + 80, 200); label(b, t + 0.6, "Selbstvorwurf", X + 400, Y - 100, 80, RED)
t = S(8, "Der zweite Schritt", "Schlüsselwort erscheint", "Die TRICK-Karte vom Anfang wird aufgedeckt: SCHRITT 2", ("geschehen",), "schema", "antwort:trick")
X, Y = pan(8, 5, t)
_mt = b.mark(); deckkarte(t - 0.4, X, Y - 150, "Trick: ???", 1100, 240); b.clear(_mt, b.mark(), t + 1.4)
schluesselwort(b, t + 1.5, X, Y - 150, "Wenn-dann-Plan", 140, RED, INK)
label(b, t, "Schritt 2", X - 500, Y - 360, 80, RED)
t = S(8, "Er stammt von", "Studien-Karteikarte", "Karteikarte 1997 · Gollwitzer & Brandstätter · München", ("zeit", "person", "ort"), "exakt", num="1997")
karteikarte(b, t, X + 150, Y + 250, "1997", "Gollwitzer u. a.", "München")
t = S(8, "Kurz vor Weihnachten", "Live-Strich", "Kamera fährt: Weihnachtsbaum und Kalenderblatt 24. DEZEMBER", ("zeit",), "exakt", num="24. Dezember")
X, Y = pan(8, 6, t)
b.many(t, 0.6, [poly((X - 500, Y - 300), (X - 700, Y + 50), (X - 300, Y + 50), closed=True), poly((X - 500, Y - 150), (X - 750, Y + 250), (X - 250, Y + 250), closed=True), rect(X - 540, Y + 250, 80, 90)], INK, 8)
b.s(t + 0.6, 0.3, poly((X - 500, Y - 360), (X - 480, Y - 320), (X - 520, Y - 320), closed=True), RED, 7)
kalender(A(8, "Heiligabend") - 0.4, X + 350, Y - 50, 380, 320); label(b, A(8, "Heiligabend"), "24. Dez.", X + 350, Y - 280, 80, RED)
t = S(8, "Schreibt innerhalb", "Tagesuhr", "Uhr: INNERHALB VON 2 TAGEN, Bericht-Blatt", ("zeit", "zahl"), "exakt", num="2 Tage")
label(b, t + 0.3, "Bericht in 2 Tagen", X + 350, Y + 230, 64, INK); blatt(t + 0.6, X + 700, Y + 250, 130, 170, 3)
t = S(8, "Ein Teil legte", "Zwei Wege", "Board teilt sich: MIT PLAN (wann + wo) vs. OHNE PLAN", ("vergleich",), "schema", "frage:plan")
X, Y = pan(8, 7, t)
zwei_wege(b, t, X, Y + 40, "mit Plan", "ohne Plan", 860, 80)
label(b, A(8, "wann"), "wann?", X - 600, Y - 120, 60, INK); label(b, A(8, "wo sie"), "wo?", X - 300, Y - 120, 60, INK)
t = S(8, "Ein Wenn-dann-Plan", "Schlüsselwort erscheint", "WENN – DANN wird geschrieben und unterstrichen", ("erklaerung",), "exakt")
schluesselwort(b, t, X - 450, Y + 120, "Wenn – dann", 90, RED, INK)
t = S(8, "So ein Plan", "Ursache-Wirkungs-Kette", "Kette: FRÜHSTÜCK → KÜCHENTISCH → SCHREIBEN (gezeichnete Tasse, Tisch, Stift)", ("erklaerung",), "schema")
X, Y = pan(8, 8, t)
tf = A(8, "gefrühstückt"); b.many(tf, 0.4, [rect(X - 720, Y - 60, 140, 130), arc(X - 570, Y + 5, 40, -1.5, 1.5)], INK, 7); label(b, tf + 0.3, "Frühstück", X - 650, Y + 170, 52, INK)
tk = A(8, "Küchentisch"); arrow(b, tk - 0.3, X - 500, Y, X - 230, Y, RED, 6); tisch(tk, X, Y + 60, 400); label(b, tk + 0.5, "Küchentisch", X, Y + 170, 52, INK)
ts = A(8, "schreibe"); arrow(b, ts - 0.3, X + 230, Y, X + 450, Y, RED, 6); blatt(ts, X + 620, Y, 180, 230, 4); label(b, ts + 0.4, "schreiben", X + 620, Y + 170, 52, INK)
t = S(8, "Das Ergebnis: Von", "Zahl in Handschrift", "Zwei Zahlen: 71 % mit Plan (rot eingekreist), 32 % ohne Plan", ("zahl",), "exakt", "antwort:plan", num="71 Prozent, 32 Prozent")
X, Y = pan(8, 9, t)
label(b, t, "zurückgeschickt:", X, Y - 380, 60, GREY)
zahl2(A(8, "einundsiebzig"), X - 400, Y - 100, "71 %", 180); label(b, A(8, "einundsiebzig") + 0.4, "mit Plan", X - 400, Y + 110, 64, INK)
t = S(8, "Ohne Plan nur", "Zahl in Handschrift", "Rechts: 32 % ohne Plan in Grau", ("zahl",), "exakt", num="32 Prozent")
label(b, t + 0.3, "32 %", X + 400, Y - 70, 180, GREY); label(b, t + 0.6, "ohne Plan", X + 400, Y + 110, 64, INK)
motion(8, "Mehr als doppelt", "bars", {"label": "GOLLWITZER & BRANDSTÄTTER 1997", "title": "Bericht rechtzeitig geschrieben", "unit": " %", "bars": [["mit Plan", 71, True], ["ohne Plan", 32, False]]}, 4.6,
       "Schraffur-Balken: mit Plan 71 % (rot), ohne Plan 32 %, Gollwitzer & Brandstätter 1997", ("vergleich", "zahl", "zeit"), "exakt", num="71 Prozent, 32 Prozent, 1997")
t = S(8, "Die Gruppen waren", "Live-Strich", "In Grau: KLEINE GRUPPEN (17 und 19)", ("zahl",), "exakt", num="17 und 19")
X, Y = pan(8, 10, t)
label(b, t, "kleine Gruppen: 17 und 19", X, Y - 330, 70, GREY)
t = S(8, "Aber eine spätere", "Studien-Karteikarte", "Stapel aus Karteikarten: AUSWERTUNG VON 94 TESTS (2006)", ("zahl", "zeit"), "exakt", num="94, 2006")
for i in range(4): b.s(t + i * 0.12, 0.2, rect(X - 750 + i * 25, Y - 150 + i * 25, 420, 260), GREY if i < 3 else INK, 6)
karteikarte(b, t + 0.5, X - 450, Y + 60, "2006", "Meta-Analyse", "94 Tests", sound=False)
t = S(8, "Wenn-dann-Pläne helfen", "Schlüsselwort erscheint", "WENN-DANN HILFT DEUTLICH, rot unterstrichen", ("erklaerung",), "schema")
schluesselwort(b, t, X + 400, Y + 60, "hilft deutlich", 100, INK)
t = S(8, "Denn der Plan", "Blick in den Kopf", "Zoom in den Kopf: ein Weichensteller nimmt die Entscheidung ab – Schild AUTOMATISCH", ("erklaerung",), "schema")
X, Y = pan(8, 11, t)
head_profile(b, t - 0.3, X - 550, Y + 120, 300, INK, 10, 0.6); bubble(b, t, X + 200, Y - 120, 900, 520, None)
label(b, t + 0.4, "Entscheidung schon gefallen", X + 200, Y - 120, 60, INK); v.go(t + 0.3, X + 200, Y - 120, 1.25); b.snd("schwenk.wav", t + 0.3, 0.25)
t = S(8, "Du musst nicht", "Mythos durchstreichen", "ERST DIE RICHTIGE STIMMUNG wird geschrieben und rot durchgestrichen", ("erklaerung",), "schema")
v.go(t - 0.3, X, Y, 1.0, sound=False)
streich(t, X + 250, Y + 430, "erst die richtige Stimmung", 70, A(8, "warten"))
t = S(8, "Die Situation selbst", "Ursache-Wirkungs-Kette", "Situation (Uhr) → Startsignal (Startflagge)", ("erklaerung",), "schema")
X, Y = pan(8, 12, t)
clock(b, t, X - 400, Y - 50, 120); arrow(b, t + 0.5, X - 230, Y - 50, X + 100, Y - 50, RED, 7)
b.many(t + 0.8, 0.4, [line(X + 250, Y + 150, X + 250, Y - 250, n=5), poly((X + 250, Y - 250), (X + 450, Y - 180), (X + 250, Y - 110))], RED, 8); label(b, t + 1.0, "Startsignal", X + 300, Y + 250, 70, INK)
t = S(8, "Probier es heute", "Mitmach-Test", "Hauptfigur schaut den Zuschauer an: PROBIER ES HEUTE AUS!", ("geschehen",), "schema")
X, Y = pan(8, 13, t)
fig(t, X - 550, Y + 450, 1.2, hero=True, face="happy", pose="arms_up"); label(b, t + 0.3, "Probier's heute aus!", X + 250, Y - 300, 90, RED)
t = S(8, "Nimm die eine", "Live-Strich", "Die eine weggeschobene Aufgabe als Blatt mit Staubwolke", ("geschehen",), "schema")
blatt(t, X + 250, Y + 100, 280, 360, 5); cloud(b, t + 0.5, X + 450, Y - 80, 0.6)
t = S(8, "Wenn es morgen", "Tagesuhr", "Uhr springt auf 9 UHR, daneben: DATEI ÖFFNEN", ("zeit",), "exakt", num="9 Uhr")
X, Y = pan(8, 14, t)
tagesuhr(b, t, X - 400, Y - 50, [(t, 7.0), (t + 1.0, 9.0)], 140, "morgen, 9 Uhr"); label(b, A(8, "öffne ich"), "dann: Datei öffnen", X + 350, Y - 50, 80, INK)
t = S(8, "Nur öffnen", "Pose wechselt", "Laptop klappt auf, rotes NUR ÖFFNEN. Haken", ("geschehen",), "schema")
tisch(t, X + 350, Y + 300, 500); check(b, t + 0.8, X + 650, Y + 120, 0.8, RED); label(b, A(8, "Mehr nicht"), "mehr nicht.", X + 750, Y + 250, 64, GREY)

# ===================== K9 Schluss =====================
X, Y = v.P(9, 0); v.go(v.CT[9], X, Y, 1.0, d=0.7, sound=False)
t = S(9, "Aufschieben ist also", "Mythos durchstreichen", "FAUL wird geschrieben und rot durchgestrichen", ("erklaerung",), "schema", "antwort:faul")
streich(t, X, Y - 300, "faul", 160, A(9, "keine Faulheit"))
t = S(9, "Es ist ein", "Gedankenwolken-Ablauf (`motion` flow)", "Kopf schützt sich vor Gefühl und schickt die Rechnung an das Zukunfts-Ich (Ablauf)", ("erklaerung",), "schema", "antwort:was")
motion(9, "Es ist ein", "flow", {"label": "DAS MUSTER", "nodes": [{"icon": "heart", "label": "mieses Gefühl"}, {"icon": "brain", "label": "Kopf schützt sich"}, {"icon": "person", "label": "Rechnung an Ich morgen"}], "packet": "doc"}, 5.0,
       "Gedankenwolken-Ablauf: mieses Gefühl → Kopf schützt sich → Rechnung an Ich morgen", ("erklaerung",), "schema")
SHOTS.pop(-2)
SHOTS[-1]["neugier"] = "antwort:was"
brain(b, t, X - 400, Y + 200, 1.0, INK); arrow(b, t + 0.6, X - 150, Y + 200, X + 200, Y + 200, RED, 7); fig(t + 0.8, X + 450, Y + 450, 0.9, hero=True, face="sad")
t = S(9, "Das Gute: Wenn", "Pose wechselt", "Hauptfigur zerschneidet eine Kette mit einer Schere: MUSTER UNTERBROCHEN", ("geschehen",), "schema")
X, Y = pan(9, 1, t)
for i in range(5): b.s(t + i * 0.1, 0.15, circle(X - 500 + i * 120, Y - 100, 45, ry=28, n=16), INK, 7)
b.s(A(9, "unterbrechen"), 0.3, line(X - 200, Y - 200, X - 120, Y + 0, n=4), RED, 11); label(b, A(9, "unterbrechen") + 0.3, "unterbrochen!", X + 400, Y - 100, 80, RED)
t = S(9, "Mit Nachsicht statt", "Live-Strich", "Zwei Werkzeuge: Herz (NACHSICHT) und Wenn-dann-Karte", ("erklaerung",), "schema")
heart(b, t, X - 400, Y + 300, 1.3); label(b, t + 0.3, "Nachsicht", X - 400, Y + 450, 60, INK)
tw = A(9, "klaren"); b.s(tw, 0.3, rect(X + 200, Y + 220, 420, 160), INK, 7); label(b, tw + 0.3, "wenn – dann", X + 410, Y + 310, 64, RED)
t = S(9, "Und falls dich", "Netz der Menschen", "Hauptfigur spricht mit einer zweiten Person: SPRICH MIT JEMANDEM", ("geschehen",), "schema")
X, Y = pan(9, 2, t)
netz(b, t, [(X - 350, Y + 200), (X + 350, Y + 200)], [(0, 1)], s=0.9, hero_i=0); label(b, t + 0.6, "Sprich mit jemandem.", X, Y - 250, 80, INK)
t = S(9, "Dieses Video ersetzt", "Schlüsselwort erscheint", "ERSETZT KEINE BERATUNG, in Grau unterstrichen", ("erklaerung",), "schema")
schluesselwort(b, t, X, Y + 450, "ersetzt keine Beratung", 64, GREY, GREY)
t = S(9, "Jetzt bin ich", "Mitmach-Test", "Großes Kommentarfeld wird gezeichnet", ("geschehen",), "exakt")
X, Y = pan(9, 3, t)
comment_box(b, t, X, Y - 80)
t = S(9, "Welche Aufgabe", "Live-Strich", "Im Kommentarfeld: WELCHE AUFGABE SCHIEBST DU GERADE AUF?", ("geschehen",), "exakt")
b.txt(t, 1.0, "Welche Aufgabe schiebst", X, Y - 110, 44, INK); b.txt(t + 0.8, 0.8, "du gerade vor dir her?", X, Y - 40, 44, RED)
t = S(9, "Und wie viele", "Zahl in Handschrift", "Rechts oben: ? / 7 Stationen, eingekreist", ("zahl",), "exakt", "antwort:stationen", num="7")
zahl2(t, X + 650, Y - 380, "? / 7", 110)
t = S(9, "Schreib es", "Schlüsselwort erscheint", "SCHREIB'S IN DIE KOMMENTARE! unter dem Feld, unterstrichen", ("geschehen",), "schema")
schluesselwort(b, t, X, Y + 250, "Schreib's in die Kommentare!", 80, INK)
t = S(9, "Und wenn du", "Hauptfigur (blaue Locke, oranger Schal)", "DENKMUSTER-Schriftzug, Hauptfigur jubelt, eine Glocke wird gezeichnet", ("geschehen",), "exakt")
X, Y = pan(9, 4, t)
b.txt(A(9, "Abonniere"), 0.8, "Denkmuster", X, Y - 250, 170, INK); b.txt(A(9, "Abonniere") + 0.5, 0.3, "abonnieren", X, Y - 120, 80, INK)
tt = A(9, "Glocke"); bell(b, tt, X + 520, Y + 150); b.snd("pop.wav", tt + 0.4, 0.4)
fig(t + 0.3, X - 450, Y + 450, 1.0, hero=True, face="happy", pose="arms_up")
label(b, t + 0.2, "warum Menschen tun, was sie tun", X, Y + 20, 60, GREY)
t = S(9, "Dann verpasst", "Live-Strich", "Glocke wackelt, kleine Striche um die Glocke", ("geschehen",), "schema")
for i in range(3): b.s(t + i * 0.1, 0.12, line(X + 620 + i * 20, Y + 40 - i * 40, X + 680 + i * 20, Y + 10 - i * 40, n=3), RED, 6)
t = S(9, "Bis zum", "Board-Panorama", "Kamera fährt weit zurück: das ganze Schluss-Board als ein Bild", ("gefuehl",), "stimmung")
v.go(t, v.P(9, 2)[0], v.P(9, 2)[1], 0.32, d=2.5, sound=False); b.snd("klang.wav", t + 2.0, 0.15)

# ---------- Zusatz-Einstellungen in langen Sätzen (Bild-Drehbuch: max. 6 s ohne neues Ereignis) ----------
def PX(k, p): return v.P(k, p)
S(1, "freiwillig zu", "Live-Strich", "Zweite Zeile der Definition schreibt sich: FREIWILLIG VERSCHOBEN", ("erklaerung",), "schema")
S(1, "obwohl man erwartet", "Schlüsselwort erscheint", "Dritte Zeile in Rot: OBWOHL ES SCHADET", ("erklaerung",), "schema")
S(1, "Achtzig", "Zahl in Handschrift", "Über den 100 Figuren: 80–95 % DER STUDIERENDEN in Rot, die Figuren färben sich rot", ("zahl",), "exakt", num="80–95 Prozent")
X, Y = PX(2, 1); t = S(2, "Case Western", "Live-Strich", "Unter der Ortsmarke: CASE WESTERN RESERVE UNIVERSITY", ("ort",), "exakt")
label(b, t, "Case Western Reserve Univ.", X + 450, Y + 250, 46, INK)
S(2, "griff zur", "Ursache-Wirkungs-Kette", "Roter Pfeil zum Gamepad: GREIFT ZUR ABLENKUNG", ("erklaerung",), "schema")
S(3, "zweitausendacht", "Studien-Karteikarte", "Die Karteikarte 2008 · Emily Pronin wird angeheftet", ("zeit",), "exakt", num="2008")
X, Y = PX(3, 5); t = S(3, "weniger aktiv", "Gehirn-Skizze", "Roter Pfeil nach unten an der Hirnregion: WENIGER AKTIV", ("erklaerung",), "schema")
arrow(b, t, X + 650, Y - 400, X + 650, Y - 200, RED, 7)
S(5, "Depression", "Live-Strich", "Rechts schreiben sich DEPRESSION, ANGST, STRESS untereinander", ("erklaerung",), "schema")
S(6, "gewinnt das", "Schlüsselwort erscheint", "Über der Waage: DAS JETZT GEWINNT, rot unterstrichen", ("erklaerung",), "schema")
X, Y = PX(6, 8); t = S(6, "Und eine Wendung", "Live-Strich", "Neben der Karte: WENDUNG 2026! in Rot", ("zeit",), "exakt", num="2026")
label(b, t, "Wendung: 2026!", X + 600, Y + 470, 56, RED)
S(7, "angeblich", "Schlüsselwort erscheint", "ANGEBLICH! in Rot neben den Balken", ("vergleich",), "schema")
S(7, "kaum einen", "Zahl in Handschrift", "Über den Wiederholungs-Balken: KAUM EIN EFFEKT in Rot", ("vergleich",), "schema")
X, Y = PX(7, 7); t = S(7, "Du verlässt", "Live-Strich", "Unter dem Weg: FRIST ALLEIN REICHT NICHT", ("erklaerung",), "schema")
label(b, t, "Frist allein reicht nicht", X, Y + 330, 64, RED)
S(8, "schob vor", "Ursache-Wirkungs-Kette", "Roter Pfeil: WENIGER AUFGESCHOBEN vor Prüfung 2", ("erklaerung",), "schema")
S(8, "vor allem", "Live-Strich", "Grau darunter: VOR ALLEM BEI STARKEN AUFSCHIEBERN", ("erklaerung",), "schema")
S(8, "Küchentisch", "Live-Strich", "Pfeil zum gezeichneten Küchentisch", ("erklaerung",), "schema")
S(8, "einundsiebzig", "Zahl in Handschrift", "71 % wird geschrieben und rot eingekreist: MIT PLAN", ("zahl",), "exakt", num="71 Prozent")
X, Y = PX(9, 2); t = S(9, "Sprich mit", "Pose wechselt", "Die zweite Person legt der Hauptfigur die Hand auf die Schulter", ("geschehen",), "schema")
b.s(t, 0.4, line(X + 260, Y + 20, X - 300, Y + 0, n=8), INK, 7)
t = S(9, "Beratungsstelle", "Live-Strich", "Kleines Gebäude BERATUNG und ein Arztkoffer mit Kreuz", ("geschehen",), "schema")
building(b, t, X - 650, Y - 200, "Beratung"); b.many(t + 0.5, 0.4, [rect(X + 500, Y - 280, 200, 140), line(X + 600, Y - 250, X + 600, Y - 170, n=3), line(X + 560, Y - 210, X + 640, Y - 210, n=3)], RED, 7)
S(9, "Abonniere", "Schlüsselwort erscheint", "DENKMUSTER wird groß geschrieben, darunter ABONNIEREN", ("geschehen",), "exakt")

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
    MO.build(v.dir)
    v.render()
