import subprocess, os, sys, importlib
from wb import SFX
DROP = ("marker_strich.wav", "marker_kurz.wav")
def mix(board, voice, vstart, dur, out):
    ev = [e for e in board.sfx if e[0] not in DROP]
    inputs = ["-i", voice]; vs = int(vstart * 1000)
    filt = [f"[0:a]aformat=channel_layouts=stereo,aresample=48000,adelay={vs}|{vs}[vo]"]; lab = "[vo]"
    for k, (f, t, v) in enumerate(ev, 1):
        inputs += ["-i", os.path.join(SFX, f)]; ms = int(t * 1000)
        filt.append(f"[{k}:a]aformat=channel_layouts=stereo,aresample=48000,adelay={ms}|{ms},volume={v}[s{k}]"); lab += f"[s{k}]"
    filt.append(lab + f"amix=inputs={len(ev)+1}:normalize=0:duration=longest,apad,atrim=0:{dur},alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filt), "-map", "[a]", "-ar", "48000", out], check=True)
    print(out, "sfx:", len(ev), "(entfernt:", len(board.sfx) - len(ev), ")")
import intro, main
mix(intro.b, "intro_vo2.wav", intro.O, round(78.0 + intro.DELTA, 2), "intro_mix.wav")
mix(main.b, "vo/main_vo.wav", 0.0, main.TOTAL, "main_mix.wav")
