"""Wortgenaue Zeiten aus der Julian-Tonspur (kostenlos, lokal): Parakeet (sherpa-onnx) + Abgleich mit dem Skripttext.
Nie Satzzeiten schätzen (Laurin, Pilotvideo)!

python3 engine/wordtimes.py <audio.wav|mp3> <skripttext.txt> <out.json>
-> {"words": [{"w": "Ostsee.", "s": 1.23, "e": 1.71}, ...], "dur": 41.7}
Modell: /home/claude/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8 (setup.sh lädt es von GitHub, ~490 MB).
"""
import sys, os, json, re, difflib, subprocess, numpy as np
MODEL = os.environ.get("PARAKEET", "/home/claude/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8")
SR = 16000

def load(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"])
    return np.frombuffer(raw, np.float32)

def chunks(a, maxlen=18.0):
    """an leisen Stellen schneiden, Stücke <= maxlen s"""
    win = int(0.05*SR); e = np.sqrt(np.convolve(a**2, np.ones(win)/win, "same"))
    out, s = [], 0
    while s < len(a):
        if len(a)-s <= maxlen*SR: out.append((s, len(a))); break
        lo, hi = s+int(8*SR), s+int(maxlen*SR)
        cut = lo+int(np.argmin(e[lo:hi])); out.append((s, cut)); s = cut
    return out

def recognize(a):
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=f"{MODEL}/encoder.int8.onnx", decoder=f"{MODEL}/decoder.int8.onnx", joiner=f"{MODEL}/joiner.int8.onnx",
        tokens=f"{MODEL}/tokens.txt", model_type="nemo_transducer", num_threads=2)
    words = []
    for s, e in chunks(a):
        st = rec.create_stream(); st.accept_waveform(SR, a[s:e]); rec.decode_stream(st)
        r = st.result; off = s/SR
        for tok, ts in zip(r.tokens, r.timestamps):
            if tok.startswith("▁") or tok.startswith(" ") or not words:
                words.append({"w": tok.lstrip("▁ "), "s": off+ts, "e": off+ts+0.08})
            else:
                words[-1]["w"] += tok; words[-1]["e"] = off+ts+0.08
    for i in range(len(words)-1): words[i]["e"] = min(max(words[i]["e"], words[i]["s"]+0.12), words[i+1]["s"])
    return [w for w in words if w["w"]]

norm = lambda w: re.sub(r"[^\wäöüß]", "", w.lower())

def align(script_words, rec):
    A = [norm(w) for w in script_words]; B = [norm(w["w"]) for w in rec]
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False); res = [None]*len(A)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2-i1): res[i1+k] = (rec[j1+k]["s"], rec[j1+k]["e"])
        elif tag == "replace" and j2 > j1:   # Zahlwörter etc.: Zeitraum gleichmäßig aufteilen
            s, e = rec[j1]["s"], rec[j2-1]["e"]; n = i2-i1
            for k in range(n): res[i1+k] = (s+(e-s)*k/n, s+(e-s)*(k+1)/n)
    for i in range(len(res)):   # Lücken interpolieren
        if res[i] is None:
            p = next((res[j][1] for j in range(i-1, -1, -1) if res[j]), 0.0)
            q = next((res[j][0] for j in range(i+1, len(res)) if res[j]), p+0.3)
            res[i] = (p, max(p+0.05, min(q, p+0.4)))
    return [{"w": w, "s": round(s, 3), "e": round(e, 3)} for w, (s, e) in zip(script_words, res)]

if __name__ == "__main__":
    audio, txt, out = sys.argv[1:4]
    a = load(audio); rec = recognize(a)
    words = align(open(txt).read().split(), rec)
    json.dump({"words": words, "dur": round(len(a)/SR, 3), "recognized": " ".join(w["w"] for w in rec)}, open(out, "w"), ensure_ascii=False, indent=0)
    print(f"{len(words)} Wörter, {len(a)/SR:.1f} s ->", out)
