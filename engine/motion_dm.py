"""2D-Motion-Graphics fuer Denkmuster (Remotion, engine/motion/) – Erweiterung aus der ANOM-Stilprobe (Laurin 23.11.2026:
"Genau so sollte ein Video aussehen" – vor allem die vielen 2D-Animationen). Ersetzt nichts aus EFFEKTE.md/ANIMATION.md
(Board, Hauptfigur, Live-Strich, Blick in den Kopf, Studien-Karteikarte ... bleiben), sondern ergänzt sie für Stellen, an denen
eine schnelle Grafik mehr erklärt (Zahlen, Vergleiche, Abläufe, Weltkarte, Chat).

Look (engine/motion/src/theme.tsx): weißes Whiteboard, schwarzer Marker mit leicht zittrigem Strich, Rot nur zur Betonung,
Blau sparsam, Handschrift Caveat, Zahlen werden rot eingekreist. KEINE Zeichen-/Marker-Sounds (Laurin).

Bausteine (Deutsch): flow (Ursache -> Gefühl -> Reaktion, Abzweig z. B. „Grübeln“), flip (Mythos -> Wahrheit), counter (Zahl rot
eingekreist), grid (z. B. „1 von 3“ mit Personen, "hot": 3), bars (Erwartet vs. Tatsächlich), stack (Studien stapeln sich + Frage),
map (weltweit), phone (gezeichnetes Handy mit Chat + Zitat). props wie bei Goldsmith; Icons auch brain, heart, clock, person.
Studien immer mit Autor + Jahr (Quelle im Skript).

Im Video-Skript (scenes.py):
    import motion_dm as MO
    K = MO.clip("flip", {...}, len=4.0); MO.build(WORK)          # rendert fehlende Clips nach WORK/motion/
    frame = MO.frame(K, t - t0)                                   # PIL-RGBA 1920x1080
    events += MO.sounds(K, t0)                                    # [(t, name, gain, dur)] mit Denkmuster-Sounds
Einmalig: `cd engine/motion && npm install`. Faustregel ANOM: alle 2–4 s ein neues Bild.
"""
import os, json, hashlib, subprocess
import numpy as np, cv2
from PIL import Image

W, H, FPS = 1920, 1080, 30
HERE = os.path.dirname(os.path.abspath(__file__))
_JOBS = {}
_WK = {"dir": "."}


def clip(comp, props, len=5.0):
    j = json.dumps({"c": comp, "p": props, "l": float(len)}, sort_keys=True, ensure_ascii=False)
    k = hashlib.sha1(j.encode()).hexdigest()[:12]
    _JOBS[k] = {"comp": comp, "props": props, "len": float(len)}
    return k


def path(k): return os.path.join(_WK["dir"], "motion", f"{k}.mp4")


def build(wk="."):
    _WK["dir"] = wk; os.makedirs(os.path.join(wk, "motion"), exist_ok=True)
    todo = [dict(v, out=os.path.abspath(path(k))) for k, v in _JOBS.items() if not os.path.exists(path(k))]
    if not todo: return
    jf = os.path.abspath(os.path.join(wk, "motion", "jobs.json")); json.dump(todo, open(jf, "w"), ensure_ascii=False, indent=1)
    print(f"motion: {len(todo)} Clips rendern ...")
    subprocess.run(["node", os.path.join(HERE, "motion", "render.mjs"), jf], check=True)


_CAP = {}
def frame(k, lt):
    p = path(k); c = _CAP.get(p)
    if c is None:
        cap = cv2.VideoCapture(p); c = _CAP[p] = [cap, -1, None, int(cap.get(cv2.CAP_PROP_FRAME_COUNT))]
    i = max(0, min(int(lt * FPS), c[3] - 1))
    if i != c[1]:
        if i != c[1] + 1: c[0].set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, fr = c[0].read()
        if ok: c[1], c[2] = i, cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(c[2]).convert("RGBA")


def sounds(k, t0=0.0):
    """Ton-Ereignisse ab Clip-Start t0 (Denkmuster-Sounds, keine Zeichen-/Marker-Sounds). Zeitpunkte = comps.tsx."""
    j = _JOBS[k]; c, q, L = j["comp"], j["props"], j["len"]
    ev = []   # kein Wisch-Sound am Clip-Start (Gemini 23.11.: klang wie Marker-Quietschen)
    if q.get("label"): ev += [(0.1, "pop", 0.3, None)]
    if c == "map":
        ev += [(0.45 + i * 0.55, "pop_klein", 0.35, None) for i in range(len(q.get("pins", [])))]
        if q.get("counter"): ev += [(1.6, "pop", 0.4, None)]
    elif c == "flow":
        n = len(q.get("nodes", []))
        ev += [(0.1 + i * 0.15, "pop_klein", 0.3, None) for i in range(n)]
        b = q.get("branch")
        if b: bt = 0.6 + 0.75 * (b["after"] + 0.5); ev += [(bt + 0.5, "pop", 0.45, None)]
    elif c == "flip":
        at = q.get("at", 2.4); ev += [(at + 0.15, "pop", 0.5, None)]
    elif c == "counter":
        ev += [(0.9, "pop", 0.4, None)]
    elif c == "grid":
        ev += [(0.9, "pop_klein", 0.3, None), (1.6, "pop", 0.35, None)]
    elif c == "bars":
        ev += [(0.4 + i * 0.35, "pop_klein", 0.3, None) for i in range(len(q.get("bars", [])))]
    elif c == "stack":
        ev += [(1.5, "pop", 0.45, None)]   # Stapel: Karten im 0,45-s-Takt (lesbar), stackStep im Theme
    elif c == "phone":
        ev += [(0.15 + i * 0.4, "pop_klein", 0.3, None) for i in range(len(q.get("messages", [])))]
    elif c == "cipher":
        ev += [(0.9, "pop", 0.35, None)]
    return [(t0 + t, n, g, d) for t, n, g, d in ev if t < L and g > 0]
