"""Technische Endkontrolle für ein Denkmuster-Video + Prüfbericht qa.md.

python3 engine/qa.py videos/NNN-slug/video.mp4 videos/NNN-slug/thumbnail.png
Prüft: Länge > 8 Min., Lautheit ≈ −15 LUFS, Bild 1920×1080, Ton vorhanden, Thumbnail ≤ 2 MB und 1280×720.
Schreibt videos/NNN-slug/qa.md mit Technik-Ergebnis + Checklisten (Faktencheck, Recht/Lizenzen, YouTube), die abgehakt werden müssen.
"""
import json, os, re, subprocess, sys

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,width,height,duration", "-of", "json", path], capture_output=True, text=True).stdout
    return json.loads(out)["streams"]

def lufs(path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[0-9.]+) LUFS", err); return float(m[-1]) if m else None

def main(video, thumb):
    res = []; ok = True
    st = probe(video); v = next(s for s in st if s["codec_type"] == "video"); a = [s for s in st if s["codec_type"] == "audio"]
    dur = float(v["duration"]); res.append(("Länge > 8:00", dur > 480, f"{int(dur // 60)}:{int(dur % 60):02d}"))
    res.append(("Auflösung 1920×1080", (v["width"], v["height"]) == (1920, 1080), f'{v["width"]}×{v["height"]}'))
    res.append(("Tonspur vorhanden", bool(a), "ja" if a else "nein"))
    L = lufs(video); res.append(("Lautheit −16…−14 LUFS", L is not None and -16.5 <= L <= -13.5, f"{L} LUFS"))
    if thumb and os.path.exists(thumb):
        from PIL import Image
        im = Image.open(thumb); sz = os.path.getsize(thumb)
        res.append(("Thumbnail 1280×720", im.size == (1280, 720), f"{im.size}"))
        res.append(("Thumbnail ≤ 2 MB", sz <= 2 * 1024 * 1024, f"{sz / 1e6:.2f} MB"))
    for _, good, _ in res: ok = ok and good
    md = ["# Prüfbericht", "", "## Technik (automatisch)", "", "| Prüfung | OK | Wert |", "|---|---|---|"]
    md += [f"| {n} | {'✅' if g else '❌'} | {w} |" for n, g, w in res]
    md += ["", "## Faktencheck (separater Agent, Pflicht)", "- [ ] Jede Zahl/Studie gegen Original geprüft, MUSS-Korrekturen umgesetzt",
           "", "## Recht / Lizenzen / YouTube", "- [ ] Keine echten Personenfotos, keine Logos/Marken im Bild oder Thumbnail",
           "- [ ] Äußerungsrecht: keine Tatsachenbehauptungen über Personen/Firmen ohne Beleg", "- [ ] Sounds: assets/sfx (CC0, SOUNDS.md) – keine Goldsmith-Sounds",
           "- [ ] Musik: assets/music (eigene Higgsfield/ElevenLabs-Tracks)", "- [ ] Stimme: Higgsfield „Helena“; KI-Hinweis in der Beschreibung",
           "- [ ] Gezeichnete Animation → „veränderte/synthetische Inhalte“ i. d. R. nicht nötig (nur wenn realistisch wirkend)",
           "- [ ] Gesundheitsthemen: Hinweis „ersetzt keine Beratung“ in der Beschreibung", "- [ ] Quellen vollständig in der Beschreibung"]
    out = os.path.join(os.path.dirname(os.path.abspath(video)), "qa.md")
    open(out, "w").write("\n".join(md) + "\n")
    print("\n".join(md[:len(res) + 6])); print("TECHNIK OK" if ok else "TECHNIK FEHLER"); return ok

if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None) else 1)
