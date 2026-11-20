"""Ton fuer die Denkmuster-Stilprobe, Version 2 (Laurin 20.11.: Zahl und Durchstreichen klangen nicht passend).
Sound-Plan: nur 7 Stellen in 22 s, jede an einem echten Bild-Ereignis, alles andere traegt die Musik.
1 Karte angeheftet (Pop) | 2 Fahrt in den Kopf (Schwenk) | 3 Regler rastet bei "Neugier" ein (ein Klick)
4 Mythos: Musik setzt aus, roter Strich = kurzer trockener Papier-Wisch (Laurins paper_slide), Musik kommt zurueck
5 "62 %": Musik setzt aus, Zahl erscheint in der Stille, beim Einkreisen trockener tiefer Treffer + Musik schwillt an
6 Rueckfahrt aufs Board (Schwenk) | 7 Kanal-Klang am Ende"""
import sys; sys.path.insert(0, "/home/claude/stilproben")
from mixer import mix
D = "/home/claude/repos/denkmuster-pipeline/assets/sfx/"; G = "/home/claude/gs_sfx/"; M = "/home/claude/repos/denkmuster-pipeline/assets/music/"
f = lambda n: D + n + ".wav"
ev = [(2.35, f("pop_klein"), 0.4),
      (4.6, f("schwenk"), 0.32),
      (11.85, f("stift_klick"), 0.35),
      (13.98, G + "paper_slide.wav", 0.75),
      (17.78, G + "sub_drop.wav", 1.0), (17.78, G + "slap.wav", 0.35),
      (18.8, f("schwenk"), 0.18),
      (20.5, f("klang"), 0.14)]
music = (M + "dm_music_1.mp3", 0.22, 0.3, 1.5, 2.5,
         [(13.85, -20, 0.35), (16.9, -22, 0.75), (18.3, 6, 1.2)])
print(mix("/home/claude/stilproben/stilprobe_denkmuster.mp4", "/home/claude/stilproben/ton_denkmuster_v2.mp4", ev, 22.0, music))
