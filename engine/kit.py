"""Denkmuster-Video-Baukasten: Kapitel-Timeline mit wortgenauen Zeiten, Kamera, Sounds, Musik, Endmischung.

Benutzung in videos/NNN-slug/scenes.py:
    import sys; sys.path.insert(0, "../../engine")   # bzw. absoluter Pfad
    from kit import *
    v = Video(__file__, titles=[None, "Kapitel 1", ..., None])   # titles[0]=None -> Hook ohne Kapitelkarte, letztes None -> Schluss
    b = v.b
    k = 0; X, Y = v.P(k, 0); v.gop(0, k, 0)
    t = v.at(k, "Fünfzehn Minuten"); label(b, t, "15 Min.", X, Y, 90, RED)
    ...
    if __name__ == "__main__": v.render()

Voraussetzungen im Videoordner: vo/k0.mp3 … vo/kN.mp3 (eine Datei pro Kapitel, Stimme Helena) und vo/kI.json (engine/wordtimes.py).
Regeln (Laurin): KEINE Zeichen-/Marker-Sounds; Kapitelkarte bleibt ~2 s stehen; Musik wechselt pro Kapitel, Pause während der Karte;
Hook startet ohne Musik; Musik deutlich unter der Stimme; Endlautheit −15 LUFS.
"""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from wb import *
from icons import *

MUSIC = os.path.join(HERE, "..", "assets", "music", "dm_music_{}.mp3")
DROP_SFX = ("marker_strich.wav", "marker_kurz.wav")   # Laurin 17.11.2026: keine Zeichen-Sounds

class Video:
    CARD = 5.0      # Kapitelkarte: ~2,3 s Zeichnen + ~2 s Stehen (Laurin)
    GAP = 0.7
    HOOK_LEAD = 0.5

    def __init__(self, scenes_file, titles, music_plan=None, hook_music_from=None):
        self.dir = os.path.dirname(os.path.abspath(scenes_file))
        self.titles = titles
        self.words = [json.load(open(os.path.join(self.dir, "vo", f"k{i}.json"))) for i in range(len(titles))]
        self.CT, self.VSTART = [], []
        t = 0.0
        for i, d in enumerate(self.words):
            lead = self.CARD if titles[i] else (self.HOOK_LEAD if i == 0 else 0.8)
            self.CT.append(t); self.VSTART.append(t + lead); t += lead + d["dur"] + self.GAP
        self.TOTAL = t + 1.5
        # Musik: 1 geheimnisvoll/Hook, 2 Erklären, 3 Wissenschaft, 4 nachdenklich, 5 positiv/Schluss
        n = len(titles)
        self.music_plan = music_plan or ([1] + [[2, 3, 1, 2, 4, 3, 4, 2][(i - 1) % 8] for i in range(1, n - 1)] + [5])
        self.hook_music_from = hook_music_from   # Sekunden ab Videostart, ab wann im Hook Musik einsetzt (None = 8 s)
        self.missing = []
        self.moves = []   # Kamerafahrten (t, d, x, y, z) – Keyframes werden erst beim Rendern chronologisch gebaut
        self.b = Board()
        self.cam = list(self.P(0, 0)) + [1.0]
        self.b.key(0, *self.cam)
        for k, ttl in enumerate(titles):
            if ttl: self.card(k)

    # ---------- Zeit ----------
    @staticmethod
    def norm(w): return re.sub(r"[^\wäöüß]", "", w.lower())

    def at(self, k, phrase, nth=0, end=False):
        ws = self.words[k]["words"]; ph = [self.norm(x) for x in phrase.split()]
        hits = [i for i in range(len(ws) - len(ph) + 1) if all(self.norm(ws[i + j]["w"]).startswith(ph[j]) for j in range(len(ph)))]
        if len(hits) <= nth:
            self.missing.append(f"K{k}: {phrase}"); return self.VSTART[k] + 1.0
        w = ws[hits[nth] + len(ph) - 1] if end else ws[hits[nth]]
        return self.VSTART[k] + (w["e"] if end else w["s"])

    # ---------- Raum / Kamera ----------
    @staticmethod
    def P(k, p): return (p * 2000 + 960, k * 1700 + 540)

    def go(self, t, x, y, z=1.0, d=0.6, sound=True):
        self.moves.append((t, d, x, y, z)); self.cam[:] = [x, y, z]
        if sound: self.b.snd("schwenk.wav", t, 0.3)

    def gop(self, t, k, p, z=1.0, dx=0, dy=0):
        x, y = self.P(k, p); self.go(t, x + dx, y + dy, z)

    def pop(self, t, v=0.45): self.b.snd("pop.wav", t, v)

    def card(self, k):
        b = self.b; x, y = self.P(k, -1); t0 = self.CT[k]
        self.go(t0, x, y, 1.0, d=0.7)
        t1 = t0 + 0.5
        num = sum(1 for i in range(k + 1) if self.titles[i])
        b.s(t1, 0.5, circle(x - 560, y, 95), BLUE, 10); b.txt(t1 + 0.4, 0.3, str(num), x - 560, y + 42, 130, BLUE)
        b.txt(t1 + 0.6, 1.1, self.titles[k], x + 120, y + 40, 100, INK)
        b.s(t1 + 1.7, 0.3, line(x - 400, y + 85, x + 640, y + 92), RED, 8)
        b.snd("klang.wav", t1 + 0.4, 0.35)

    def fig(self, t, x, y, s=1.0, dur=0.7, **kw): return stick(self.b, t, x, y, s, dur=dur, **kw)

    def build_cam(self):
        """Kamera-Keyframes chronologisch aufbauen: jede Fahrt startet dort, wo die Kamera zu diesem Zeitpunkt wirklich ist
        (Fix 18.11.2026: vorher startete jede Fahrt an der Position der zuletzt *programmierten* Fahrt -> Sprünge zu Kapitelkarten)."""
        x0, y0 = self.P(0, 0); cur = (x0, y0, 1.0); keys = [(0.0,) + cur]
        for t, d, x, y, z in sorted(self.moves):
            keys.append((t,) + cur); keys.append((t + d, x, y, z)); cur = (x, y, z)
        self.b.cam = keys

    # ---------- Ausgabe ----------
    def _voice(self, out):
        inputs, filt, lab = [], [], ""
        for i in range(len(self.titles)):
            inputs += ["-i", os.path.join(self.dir, "vo", f"k{i}.mp3")]; ms = int(self.VSTART[i] * 1000)
            filt.append(f"[{i}:a]aformat=channel_layouts=stereo,aresample=48000,adelay={ms}|{ms}[v{i}]"); lab += f"[v{i}]"
        filt.append(lab + f"amix=inputs={len(self.titles)}:normalize=0:duration=longest,apad,atrim=0:{self.TOTAL}[o]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filt), "-map", "[o]", out], check=True)

    def _music(self, out):
        n = len(self.titles); segs = []
        hs = self.hook_music_from if self.hook_music_from is not None else 8.0
        segs.append((hs, self.CT[1] - 0.5 if n > 1 else self.TOTAL - 0.5, self.music_plan[0]))
        for k in range(1, n):
            s = self.VSTART[k] - 0.2; e = (self.CT[k + 1] if k < n - 1 else self.TOTAL) - 0.5
            segs.append((s, e, self.music_plan[k]))
        inp, f, lab = [], [], ""
        for i, (s, e, tr) in enumerate(segs):
            L = e - s; inp += ["-i", MUSIC.format(tr)]; ms = int(s * 1000)
            f.append(f"[{i}:a]aformat=channel_layouts=stereo,aresample=48000,loudnorm=I=-24,atrim=0:{L:.2f},afade=t=in:d=2,"
                     f"afade=t=out:st={max(0, L - 1.6):.2f}:d=1.6,adelay={ms}|{ms}[m{i}]"); lab += f"[m{i}]"
        f.append(lab + f"amix=inputs={len(segs)}:normalize=0:duration=longest,volume=0.41[o]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inp + ["-filter_complex", ";".join(f), "-map", "[o]", "-ar", "48000", out], check=True)

    def render(self, out_name="video.mp4", duration=None):
        if self.missing:
            print("FEHLENDE STICHWÖRTER:", self.missing); sys.exit(1)
        self.build_cam()
        self.b.sfx = [e for e in self.b.sfx if e[0] not in DROP_SFX]
        d = self.dir; dur = duration or self.TOTAL
        self._voice(os.path.join(d, "vo", "voice_all.wav"))
        raw = os.path.join(d, "_raw.mp4")
        render(self.b, raw, dur, os.path.join(d, "vo", "voice_all.wav"), 0.0)
        self._music(os.path.join(d, "music_bed.wav"))
        out = os.path.join(d, out_name)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-i", os.path.join(d, "music_bed.wav"), "-filter_complex",
                        "[0:a][1:a]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=11[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out], check=True)
        os.remove(raw)
        print("FERTIG:", out, f"{dur:.1f} s")
