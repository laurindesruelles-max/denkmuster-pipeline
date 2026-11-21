"""Denkmuster-Bausteine (ANIMATION.md, freigegeben 21.11.2026) – erstmals gebaut für Video 003.

Alle Funktionen bekommen das Board `b` und zeichnen im Kanal-Look (Schwarz auf Weiß, Blau/Orange nur an der Hauptfigur, Rot = Betonung).
Einblendungen 200–400 ms ease-out, Ausblendungen ease-in (Motion-Regeln 19.11.2026).

    from bausteine import *
    counter(b, x, y, t0, t1, 0, 20)            # Zähler läuft hoch
    karteikarte(b, t, x, y, "2008", "New York", "Columbia University")   # Studien-Karteikarte
    zahl(b, t, x, y, "20")                      # Zahl in Handschrift, wird eingekreist
    durchstreichen(b, t, x, y, "Fragen = schwach")   # Mythos durchstreichen
    schluesselwort(b, t, x, y, "Selbstwert")    # Schlüsselwort erscheint + unterstrichen
    walker(b, t0, t1, x0, x1, y, hero=True)     # Figur bewegt sich (läuft von x0 nach x1)
    schleife(b, t0, t1, x, y)                   # Gedankenschleife um einen Kopf, wird schneller
    gewicht(b, x, y, keys)                      # Gewicht auf den Schultern wächst/schrumpft
    netz(b, t, pts, links)                      # Netz der Menschen
    zwei_wege(b, t, x, y, "links", "rechts")    # Zwei Wege: Board teilt sich
    tagesuhr(b, t, x, y, keys)                  # Tagesuhr, Zeiger springt
    hundert(b, t, x, y, n_rot)                  # 100 Figuren, n_rot rot schraffiert
    kette(b, t, [(x, y), ...])                  # Ursache-Wirkungs-Kette (Pfeile)
"""
import math
import cairo
from wb import *
from icons import *

def dtext(ctx, s, x, y, size, col, font="Caveat"):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s); ctx.move_to(x - e.width / 2 - e.x_bearing, y); ctx.set_source_rgba(*col); ctx.show_text(s)

def fmt_de(n, dec=0):
    s = f"{n:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def counter(b, x, y, t0, t1, v0, v1, size=120, col=INK, pre="", post="", hide=1e9, dec=0):
    def fn(ctx, t):
        if t < t0 or t > hide: return
        val = v0 + (v1 - v0) * ease_out(prog(t, t0, t1))
        dtext(ctx, pre + fmt_de(val, dec) + post, x, y, size, col)
    b.dyn.append(fn)

def arrow(b, t, x0, y0, x1, y1, col=INK, w=8, dur=0.35):
    b.s(t, dur, line(x0, y0, x1, y1, n=10), col, w)
    a = math.atan2(y1 - y0, x1 - x0); L = 38
    b.s(t + dur, 0.12, poly((x1 + L * math.cos(a + 2.6), y1 + L * math.sin(a + 2.6)), (x1, y1), (x1 + L * math.cos(a - 2.6), y1 + L * math.sin(a - 2.6)), n=3), col, w)
    return t + dur + 0.12

def karteikarte(b, t, x, y, jahr, ort, zeile3="", rot=-0.04, sound=True):
    """Studien-Karteikarte: gezeichnete Karte mit Jahr, Ort, Zeile 3 (z. B. Teilnehmer), wird mit einem Pin angeheftet."""
    w, h = 560, 330
    c, s = math.cos(rot), math.sin(rot)
    P = lambda a, d: (x + a * c - d * s, y + a * s + d * c)
    b.s(t, 0.35, poly(P(-w / 2, -h / 2), P(w / 2, -h / 2), P(w / 2, h / 2), P(-w / 2, h / 2), closed=True, n=6), INK, 7)
    b.s(t + 0.3, 0.15, line(*P(-w / 2 + 25, -h / 2 + 95), *P(w / 2 - 25, -h / 2 + 95), n=8), RED, 5)
    b.s(t + 0.3, 0.12, circle(*P(0, -h / 2 + 8), 16, n=12), RED, 9)
    b.txt(t + 0.4, 0.3, jahr, *P(0, -h / 2 + 75), 80, RED, rot=rot)
    b.txt(t + 0.65, 0.35, ort, *P(0, 25), 62, INK, rot=rot)
    if zeile3: b.txt(t + 0.95, 0.35, zeile3, *P(0, 110), 54, INK, rot=rot)
    if sound: b.snd("pop_klein.wav", t + 0.3, 0.4)
    return t + 1.3

def zahl(b, t, x, y, s, size=200, col=RED, kreis=True, sound=True):
    """Zahl in Handschrift: groß geschrieben, dann eingekreist (Treffer beim Einkreisen)."""
    b.txt(t, 0.45, s, x, y + size * 0.32, size, col)
    if kreis:
        r = max(size * 0.75, len(s) * size * 0.33)
        b.s(t + 0.55, 0.4, circle(x, y, r, ry=size * 0.7, turns=1.08), col, 8)
        if sound: b.snd("pop.wav", t + 0.6, 0.35)
    return t + 1.0

def durchstreichen(b, t, x, y, s, size=90, t_strike=None):
    """Mythos durchstreichen: Satz wird geschrieben, dann rot durchgestrichen."""
    b.txt(t, max(0.4, 0.04 * len(s)), s, x, y, size, INK)
    ts = t_strike if t_strike is not None else t + 1.0
    L = len(s) * size * 0.25
    b.s(ts, 0.3, line(x - L, y - size * 0.2, x + L, y - size * 0.35, n=10), RED, 11)
    b.snd("stift_klick.wav", ts, 0.3)
    return ts + 0.3

def schluesselwort(b, t, x, y, s, size=140, col=INK, ul=RED):
    """Schlüsselwort erscheint: Fachbegriff groß in Handschrift, wird unterstrichen."""
    b.txt(t, max(0.35, 0.05 * len(s)), s, x, y, size, col)
    L = len(s) * size * 0.24
    b.s(t + 0.5, 0.3, line(x - L, y + size * 0.22, x + L, y + size * 0.18, n=10), ul, 9)
    return t + 0.8

def _stick_draw(ctx, x, y, s, ph, hero, col=INK, w=8):
    """bewegte Strichfigur (dyn): ph = Schrittphase."""
    hy = y - 235 * s; R = 40 * s
    ctx.set_source_rgba(*col); ctx.set_line_width(w); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.new_path(); ctx.arc(x, hy, R, 0, 2 * math.pi); ctx.stroke()
    ctx.move_to(x, hy + R); ctx.line_to(x, y - 95 * s); ctx.stroke()
    sw = math.sin(ph) * 0.45
    hip = (x, y - 95 * s); sh = (x, y - 165 * s)
    for sg in (1, -1):
        a = sg * 0.32 + sw * sg            # Bein: Grundspreizung + Schwung
        ctx.move_to(*hip); ctx.line_to(hip[0] + math.sin(a) * 100 * s, hip[1] + math.cos(a) * 95 * s); ctx.stroke()
        aa = sg * 0.7 - sw * sg            # Arm: gegenläufig
        ctx.move_to(*sh); ctx.line_to(sh[0] + math.sin(aa) * 75 * s, sh[1] + math.cos(aa) * 70 * s); ctx.stroke()
    for ex in (-13, 13):
        ctx.new_path(); ctx.arc(x + ex * s + 8 * s, hy - 5 * s, 3 * s, 0, 2 * math.pi); ctx.fill()
    if hero:
        ctx.set_source_rgba(*BLUE); ctx.set_line_width(max(5, w - 2)); ctx.new_path()
        for i in range(40):
            u = i / 39; a = 6.28 * 1.6 * u
            ctx.line_to(x + 6 * s + 16 * s * u * math.cos(a), hy - R - 12 * s + 16 * s * u * math.sin(a))
        ctx.stroke()
        ctx.set_source_rgba(*ORANGE); ctx.set_line_width(w + 3)
        ctx.move_to(x - 22 * s, hy + R + 6 * s); ctx.line_to(x + 22 * s, hy + R + 6 * s); ctx.line_to(x + 30 * s, hy + R + 40 * s); ctx.stroke()

def walker(b, t0, t1, x0, x1, y, s=1.0, hero=False, hide=1e9, steps=None, col=INK):
    """Figur bewegt sich: läuft zwischen t0 und t1 von x0 nach x1 (ease in-out), danach steht sie."""
    n = steps or max(2, int(abs(x1 - x0) / (90 * s)))
    def fn(ctx, t):
        if t < t0 or t > hide: return
        u = prog(t, t0, t1); x = x0 + (x1 - x0) * ease(u)
        ph = (u * n * math.pi) if 0 < u < 1 else 0.0
        _stick_draw(ctx, x, y, s, ph, hero, col)
    b.dyn.append(fn)

def schleife(b, t0, t1, x, y, r=170, col=RED, hide=1e9):
    """Gedankenschleife: Pfeil kreist um den Kopf, wird immer schneller."""
    def fn(ctx, t):
        if t < t0 or t > hide: return
        u = t - t0; ang = 2.0 * u + 1.2 * u * u
        ctx.set_source_rgba(*col); ctx.set_line_width(8); ctx.new_path()
        for i in range(30):
            a = ang + i * 0.12
            ctx.line_to(x + r * math.cos(a), y + 0.55 * r * math.sin(a))
        ctx.stroke()
        a = ang + 29 * 0.12; hx, hy = x + r * math.cos(a), y + 0.55 * r * math.sin(a)
        d = a + math.pi / 2
        ctx.move_to(hx + 26 * math.cos(d + 2.5), hy + 26 * math.sin(d + 2.5)); ctx.line_to(hx, hy)
        ctx.line_to(hx + 26 * math.cos(d - 2.5), hy + 26 * math.sin(d - 2.5)); ctx.stroke()
    b.dyn.append(fn)

def gewicht(b, x, y, keys, t_show, hide=1e9, label_txt=None):
    """Gewicht auf den Schultern: Stein über dem Kopf (x, y = Schulterhöhe), Größe nach keys [(t, 0..1)]."""
    def fn(ctx, t):
        if t < t_show or t > hide: return
        v = keys[0][1]
        for (ta, va), (tb, vb) in zip(keys, keys[1:]):
            if t >= ta: v = va + (vb - va) * ease(prog(t, ta, tb))
        if v <= 0.02: return
        w = 60 + 260 * v; h = 40 + 150 * v
        ctx.set_source_rgba(*GREY[:3], 0.35); ctx.set_line_width(7)
        ctx.new_path(); ctx.move_to(x - w / 2, y); ctx.curve_to(x - w / 2 - 20, y - h, x + w / 2 + 20, y - h, x + w / 2, y); ctx.close_path(); ctx.fill_preserve()
        ctx.set_source_rgba(*INK); ctx.stroke()
        if label_txt: dtext(ctx, label_txt, x, y - h * 0.3, 40 + 30 * v, INK)
    b.dyn.append(fn)

def netz(b, t, pts, links, s=0.55, col=INK, link_col=GREY, hero_i=None):
    """Netz der Menschen: Figuren an pts, dann Verbindungslinien (links = [(i, j)])."""
    for i, (x, y) in enumerate(pts):
        stick(b, t + i * 0.08, x, y, s, dur=0.3, face="happy", hero=(i == hero_i), w=6)
    tt = t + len(pts) * 0.08 + 0.3
    for k, (i, j) in enumerate(links):
        (x0, y0), (x1, y1) = pts[i], pts[j]
        b.s(tt + k * 0.06, 0.2, line(x0, y0 - 140 * s, x1, y1 - 140 * s, n=8), link_col, 5)
    return tt + len(links) * 0.06 + 0.2

def zwei_wege(b, t, x, y, links, rechts, h=820, size=80):
    """Zwei Wege: Board teilt sich durch eine Linie, links/rechts Überschrift."""
    b.s(t, 0.4, line(x, y - h / 2, x, y + h / 2, n=20), INK, 7)
    b.txt(t + 0.3, 0.35, links, x - 450, y - h / 2 + 70, size, INK)
    b.txt(t + 0.5, 0.35, rechts, x + 450, y - h / 2 + 70, size, RED)
    return t + 0.9

def tagesuhr(b, t, x, y, keys, r=150, label_txt=None):
    """Tagesuhr: Zifferblatt, Stundenzeiger springt nach keys [(t, stunde)]."""
    b.s(t, 0.4, circle(x, y, r), INK, 8)
    for k in range(12):
        a = k * math.pi / 6
        b.s(t + 0.4 + k * 0.02, 0.04, line(x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82, x + math.cos(a) * r * 0.95, y + math.sin(a) * r * 0.95, n=2), INK, 5)
    def fn(ctx, tt):
        if tt < t + 0.5: return
        h = keys[0][1]
        for (ta, ha), (tb, hb) in zip(keys, keys[1:]):
            if tt >= ta: h = ha + (hb - ha) * ease_out(prog(tt, ta, ta + 0.5))
        a = -math.pi / 2 + (h % 12) / 12 * 2 * math.pi
        ctx.set_source_rgba(*INK); ctx.set_line_width(11); ctx.move_to(x, y); ctx.line_to(x + math.cos(a) * r * 0.5, y + math.sin(a) * r * 0.5); ctx.stroke()
        m = -math.pi / 2 + (h % 1) * 2 * math.pi
        ctx.set_line_width(7); ctx.move_to(x, y); ctx.line_to(x + math.cos(m) * r * 0.75, y + math.sin(m) * r * 0.75); ctx.stroke()
        ctx.arc(x, y, 10, 0, 6.3); ctx.fill()
    b.dyn.append(fn)
    if label_txt: b.txt(t + 0.6, 0.4, label_txt, x, y + r + 80, 64, RED)

def hundert(b, t, x, y, n_rot, cols=20, rows=5, dx=46, dy=92, t_rot=None, rot_label=None):
    """100 Figuren (Mini-Strichmännchen), die ersten n_rot werden rot."""
    x0 = x - (cols - 1) * dx / 2; y0 = y - (rows - 1) * dy / 2
    tr = t_rot if t_rot is not None else t + 1.6
    def fn(ctx, tt):
        if tt < t: return
        shown = int(100 * ease_out(prog(tt, t, t + 1.2)))
        nr = int(n_rot * ease_out(prog(tt, tr, tr + 1.0)))
        ctx.set_line_width(4); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for i in range(shown):
            cx = x0 + (i % cols) * dx; cy = y0 + (i // cols) * dy
            ctx.set_source_rgba(*(RED if i < nr else INK))
            ctx.new_path(); ctx.arc(cx, cy - 26, 9, 0, 6.3); ctx.stroke()
            ctx.move_to(cx, cy - 17); ctx.line_to(cx, cy + 8); ctx.move_to(cx - 12, cy - 6); ctx.line_to(cx + 12, cy - 6)
            ctx.move_to(cx, cy + 8); ctx.line_to(cx - 9, cy + 26); ctx.move_to(cx, cy + 8); ctx.line_to(cx + 9, cy + 26); ctx.stroke()
    b.dyn.append(fn)
    if rot_label: b.txt(tr + 0.6, 0.4, rot_label, x, y + rows * dy / 2 + 80, 70, RED)

def kette(b, t, nodes, col=INK, gap=70, dy=80):
    """Ursache-Wirkungs-Kette: Pfeile zwischen Knotenpunkten (Zeichnungen/Labels setzt der Aufrufer); Pfeile laufen dy unter der Textzeile."""
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(nodes, nodes[1:])):
        L = math.dist((x0, y0), (x1, y1)); ux, uy = (x1 - x0) / L, (y1 - y0) / L
        arrow(b, t + i * 0.5, x0 + ux * gap * 2.4, y0 + uy * gap + dy, x1 - ux * gap * 2.4, y1 - uy * gap + dy, col)
    return t + (len(nodes) - 1) * 0.5

def phone(b, t, x, y, s=1.0, col=INK, txt=None, txt_col=BLUE):
    b.many(t, 0.4, [rect(x - 80 * s, y - 150 * s, 160 * s, 300 * s), line(x - 20 * s, y + 125 * s, x + 20 * s, y + 125 * s, n=2)], col, 8)
    if txt: b.txt(t + 0.4, 0.4, txt, x, y, 34 * s, txt_col)

def kiste(b, t, x, y, s=1.0, col=INK, offen=False):
    w, h = 220 * s, 150 * s
    b.many(t, 0.4, [rect(x - w / 2, y - h, w, h), line(x - w / 2, y - h * 0.75, x + w / 2, y - h * 0.75, n=6)] +
           ([poly((x - w / 2, y - h), (x - w / 2 - 40 * s, y - h - 60 * s)), poly((x + w / 2, y - h), (x + w / 2 + 40 * s, y - h - 60 * s))] if offen else []), col, 7)

def bars(b, X, Y, items, h=480, bw=150, gap=60, axis_t=None, lab=48):
    """Handgezeichnetes Diagramm: items = [(t, wert 0..1, farbe, label)], Balken wachsen schraffiert."""
    n = len(items); W_ = n * bw + (n - 1) * gap; x0 = X - W_ / 2
    t_ax = axis_t if axis_t is not None else min(i[0] for i in items) - 0.5
    b.many(t_ax, 0.4, [poly((x0 - 40, Y - h - 40), (x0 - 40, Y), (x0 + W_ + 40, Y))], INK, 8)
    for i, (tk, val, col, lb) in enumerate(items):
        x = x0 + i * (bw + gap)
        if lb: b.txt(tk, 0.35, lb, x + bw / 2, Y + 70, lab, col)
        def fn(ctx, t, tk=tk, val=val, col=col, x=x):
            if t < tk: return
            hh = h * val * ease_out(prog(t, tk, tk + 0.9))
            ctx.save(); ctx.rectangle(x, Y - hh, bw, hh); ctx.clip(); ctx.set_source_rgba(*col); ctx.set_line_width(6)
            for kk in range(-30, 40): ctx.move_to(x + kk * 18, Y); ctx.line_to(x + kk * 18 + 60, Y - 700)
            ctx.stroke(); ctx.restore(); ctx.set_source_rgba(*col); ctx.set_line_width(7); ctx.rectangle(x, Y - hh, bw, hh); ctx.stroke()
        b.dyn.append(fn)
    return x0, W_

def skala(b, t, x, y, w, vals, lo=0, hi=10, size=56):
    """Skala 0–10 mit Markern: vals = [(t, wert, farbe, label)] – Marker gleiten auf ihren Wert."""
    b.s(t, 0.4, line(x - w / 2, y, x + w / 2, y, n=20), INK, 8)
    for k in range(hi - lo + 1):
        px = x - w / 2 + w * k / (hi - lo)
        b.s(t + 0.4 + k * 0.02, 0.05, line(px, y - 18, px, y + 18, n=2), INK, 5)
        if k in (0, 5, 10): b.txt(t + 0.5, 0.2, str(lo + k), px, y + 75, 46, GREY)
    for (tk, val, col, lb) in vals:
        def fn(ctx, tt, tk=tk, val=val, col=col, lb=lb):
            if tt < tk: return
            v = val * ease_out(prog(tt, tk, tk + 0.9)); px = x - w / 2 + w * (v - lo) / (hi - lo)
            ctx.set_source_rgba(*col); ctx.move_to(px, y - 22); ctx.line_to(px - 22, y - 62); ctx.line_to(px + 22, y - 62); ctx.close_path(); ctx.fill()
            dtext(ctx, lb, px, y - 85, size, col)
        b.dyn.append(fn)

def pin(b, t, x, y, ort, col=RED, size=70):
    """Ortsmarke: Pin + Ortsname."""
    b.s(t, 0.3, bez((x, y), (x - 70, y - 90), (x - 40, y - 150), (x, y - 150)) + bez((x, y - 150), (x + 40, y - 150), (x + 70, y - 90), (x, y))[1:], col, 8)
    b.s(t + 0.3, 0.1, circle(x, y - 105, 16, n=10), col, 7)
    b.txt(t + 0.35, 0.35, ort, x, y + 70, size, INK)
