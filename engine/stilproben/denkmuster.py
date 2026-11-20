"""Stilprobe Denkmuster (20.11.2026): neue Effekte aus dem Katalog, ohne Ton.
Hauptfigur, Studien-Karteikarte, Blick in den Kopf, Experiment nachgespielt, innerer Regler,
Mythos durchstreichen, handgezeichnetes Diagramm + Zahl in Handschrift, Board-Panorama."""
import sys, math, subprocess
sys.path.insert(0, "/home/claude/repos/denkmuster-pipeline/engine")
from wb import *
from icons import *

b = Board()
D = 22.0

# --- 1) Hauptfigur + Studien-Karteikarte (0-4 s) ---
HX, HY = 560, 900
b.key(0, 900, 640, 1.35)
stick(b, 0.3, HX, HY, 1.25, dur=1.4, face="worried", hero=True, w=10)
def card(t, x, y, lines):
    w, h = 470, 270
    b.s(t, 0.5, rect(x - w / 2, y - h / 2, w, h), INK, 7)
    b.s(t + 0.45, 0.15, line(x - w / 2 + 20, y - h / 2 + 70, x + w / 2 - 20, y - h / 2 + 70, n=6), RED, 4)
    b.s(t + 0.55, 0.12, circle(x, y - h / 2 - 8, 14, n=14), RED, 7)  # Pinnnadel
    for i, s in enumerate(lines):
        b.txt(t + 0.7 + i * 0.35, 0.35, s, x, y - h / 2 + 52 + i * 70, 50 if i else 54, INK if i else RED)
card(1.8, 1350, 470, ["STUDIE", "Beispiel-Uni, 2019", "1.200 Teilnehmer"])

# --- 2) Blick in den Kopf: Gedankenblase, Kamera taucht ein (4-8.5 s) ---
BX, BY = 880, 560
b.s(4.0, 0.5, circle(BX, BY, 150, ry=110), INK, 4)
for k, (dx, dy, r) in enumerate([(-170, 140, 22), (-215, 200, 14)]):
    b.s(4.4 + k * 0.1, 0.1, circle(BX + dx, BY + dy, r, n=14), INK, 6)
b.key(4.6, 900, 640, 1.35)
b.key(5.6, BX, BY, 4.2)
# Experiment im Kopf (klein gezeichnet, nach dem Zoom gross): zwei Figuren, eine wendet sich ab
stick(b, 5.6, BX - 55, BY + 70, 0.38, dur=0.7, face="happy", w=4)
stick(b, 6.1, BX + 55, BY + 70, 0.38, dur=0.7, face="neutral", w=4)
b.s(6.8, 0.3, line(BX - 30, BY + 20, BX + 30, BY + 20, n=6), BLUE, 3)
b.txt(7.0, 0.5, "Experiment", BX, BY - 75, 22, BLUE)

# --- 3) Innerer Regler (8.5-12 s) ---
RX, RY = 2150, 640
b.key(8.0, BX, BY, 4.2)
b.key(9.0, RX, RY - 80, 1.15)
dial(b, 9.0, RX, RY)
b.txt(9.9, 0.4, "Angst", RX - 250, RY + 20, 56, INK)
b.txt(10.1, 0.4, "Neugier", RX + 260, RY + 20, 56, INK)
dial_needle(b, RX, RY, [(10.2, 0.15), (10.9, 0.85), (11.4, 0.35), (11.9, 0.7)], 10.2)

# --- 4) Mythos durchstreichen (12-15 s) ---
MX, MY = 2150, 1150
b.key(12.0, RX, RY - 80, 1.15)
b.key(12.7, MX, MY, 1.15)
b.txt(12.8, 1.0, "„Introvertierte sind schüchtern“", MX, MY, 72, INK)
b.s(14.0, 0.35, line(MX - 520, MY - 22, MX + 520, MY - 30, n=20), RED, 12)

# --- 5) Diagramm + Zahl in Handschrift (15-19 s) ---
CX, CY = 3250, 880
b.key(15.0, MX, MY, 1.15)
b.key(15.7, CX, CY - 220, 1.05)
b.many(15.8, 0.5, [poly((CX - 450, CY - 520), (CX - 450, CY), (CX + 450, CY))], INK, 8)
b.s(16.3, 0.9, bez((CX - 430, CY - 40), (CX - 150, CY - 60), (CX + 50, CY - 420), (CX + 420, CY - 460)), BLUE, 10)
b.txt(17.3, 0.5, "62 %", CX + 260, CY - 560, 130, RED)
b.s(17.8, 0.45, circle(CX + 260, CY - 600, 150, ry=95), RED, 8)

# --- 6) Board-Panorama (19-22 s) ---
b.key(18.8, CX, CY - 220, 1.05)
b.key(20.6, 2080, 720, 0.5)
b.key(D, 2080, 720, 0.48)

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(D), "/tmp/stille.wav"], check=True)
render(b, "/home/claude/stilproben/stilprobe_denkmuster.mp4", D, "/tmp/stille.wav", voice_start=0)
print("ok")
