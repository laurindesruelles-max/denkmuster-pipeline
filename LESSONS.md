# Lessons (Denkmuster)

- 17.11.2026 Pilot 001 „Menschen, die gern allein sind“: Whiteboard-Stil gewählt (statt 2D-Flat/Comic). Strichmännchen im Thumbnail abgelehnt („muss mehr Klicks, professioneller“) → illustriertes Higgsfield-Motiv + große Inter-Black-Schrift (Variante „GERN ALLEIN? Dein Gehirn tickt anders.“).
- Marker-/Zeichen-Sounds komplett raus (Laurin: „ganz ganz schlimm“, auch SFX-Kit-Alternativen abgelehnt).
- Freie CC0-Musik (Komiku/HoliznaCC0/xik …) abgelehnt; eigene cinematic Tracks (Higgsfield ElevenLabs Music) angenommen.
- Kapitelkarten ~2 s stehen lassen.
- Faktencheck-Agent fand 2 echte Fehler: „die meisten“ statt „viele“ (Wilson 2014: nur 18 von 42 drückten) und eine Schlussaussage, die einem eigenen Kapitel widersprach. → Überall vorsichtig formulieren („im Schnitt“, „vieles spricht dafür“), Zusammenhang ≠ Ursache, Ausreißer kennzeichnen.
- Korrekturen ohne komplettes Neueinsprechen: nur betroffene Kapitel neu erzeugen; im Hook einzelne Sätze einsetzen (siehe videos/001/intro.py V()).
- Caveat hat keine Pfeile (↑↓→) → Wörter verwenden.
- Higgsfield text2speech: max. ~4 parallel, sonst 429.
- mcp.vidiq.com ist aus der Sandbox gesperrt → Uploads über Higgsfield-cloudfront-URL an vidIQ geben.
- sfxmint.com drosselt Downloads (429) → zuerst Hugging-Face-Sample bzw. SFX Kit (GitHub).
- 18.11.2026 Kamera-Bug in kit.py behoben: Kapitelkarten wurden im Konstruktor angelegt, dadurch startete jede Fahrt an der zuletzt *programmierten* Position (Hook-Anfang zeigte leeres Board, Sprünge vor Kapitelkarten). Jetzt sammelt `go()` Fahrten und `build_cam()` baut die Keyframes chronologisch. Neu: `engine/preview.py videos/NNN [Kapitel]` = Kontaktabzug ohne Rendern (Layout prüfen vor dem 16-Min-Render).
- Faktencheck VOR dem Einsprechen laufen lassen (Skript als skript.md) spart Credits und Neu-Renders; danach am fertigen Video nur noch Kurzcheck.
- Kosten: Helena kostet ~4–5 Credits pro Kapitel (10 Kapitel ≈ 45). Für ~30 Credits: weniger, längere Kapitel-Dateien (z. B. 2 Kapitel pro Datei) prüfen.
- vidIQ-Guthaben kann 0 sein (Reset 7.12.) → Titel-Scoring überspringen, Upload/Entwurf/Veröffentlichen kosten 0 Credits.

## Video-Log
| Nr. | Datum | Titel | Länge | Credits (Higgsfield) | Status |
|---|---|---|---|---|---|
| 001 | 17.11.2026 | Menschen, die gern allein sind, haben diese seltene Eigenschaft | >8 Min. | – | öffentlich |
| 002 | 18.11.2026 | Warum das Warten auf GTA 6 schöner sein kann als das Spiel (https://www.youtube.com/watch?v=v4u2cwV5TzM) | 11:58 | ~50 | öffentlich |

## Ton & Musik mit audiokit (Laurin 18.11.2026)
Problem: Soundeffekte oft unpassend/billig, Musik zu gleichförmig – Laurin schaut die eigenen Videos nicht zu Ende. vidIQ-Auswertung 18.11.: größter Absprung in den ersten ~30 s; Musik läuft 1,5–3 Min. gleich durch, kein Spannungsaufbau vor Enthüllungen; Passagen von 25–60 s ohne neuen Reiz.
- `setup.sh` lädt audiokit (Repo sound-mediathek) nach /home/claude/audiokit. Die Engine nutzt es automatisch und schreibt `ton_bericht.txt` – Bericht in qa.md übernehmen.
- Sounds werden vor dem Mischen aufgeräumt: gleiche Lautheit, Einblendungs-Sounds nicht im Dauerfeuer, max. 2 Sounds gleichzeitig, keine Endlos-Schleifen, defekte Dateien fliegen raus. Geräusche zu sichtbarer Bewegung bleiben.
- Musik nach Spannungskurve: Wechsel der Stelle/des Tracks spätestens alle ~60–80 s, Anschwellen vor Enthüllungen/Zahlen, Bogen pro Kapitel, Pegel automatisch unter der Stimme. Weiterhin nur die eigene Musik-Bibliothek, keine neuen Tracks.
- Im Skript Enthüllungen klar formulieren (Zahl, „aber“, „doch“, Frage → Antwort): daraus baut die Spannungskurve.
- Bericht meldet Lücken > 22 s ohne neuen Reiz → dort Bild/Effekt/Schnitt ergänzen, bevor gerendert wird.
