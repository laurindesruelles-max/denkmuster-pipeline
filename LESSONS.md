# Lessons (Denkmuster)

> **Seit 20.11.2026 zuerst lesen:** `HANDWERK.md` (Regeln für alle Kanäle) und `EFFEKTE.md` (Handschrift und erlaubte Effekte dieses Kanals, von Laurin abgenommen). Bei Widerspruch gelten diese beiden Dateien.


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
| 003 | 21.11.2026 | Warum Menschen, die nie um Hilfe bitten, sich so oft irren (https://www.youtube.com/watch?v=aBJTAT7Wwac) | 10:30 | ~37 | geplant: öffentlich 22.11.2026, 17:00 |

## Ton & Musik mit audiokit (Laurin 18.11.2026)
Problem: Soundeffekte oft unpassend/billig, Musik zu gleichförmig – Laurin schaut die eigenen Videos nicht zu Ende. vidIQ-Auswertung 18.11.: größter Absprung in den ersten ~30 s; Musik läuft 1,5–3 Min. gleich durch, kein Spannungsaufbau vor Enthüllungen; Passagen von 25–60 s ohne neuen Reiz.
- `setup.sh` lädt audiokit (Repo sound-mediathek) nach /home/claude/audiokit. Die Engine nutzt es automatisch und schreibt `ton_bericht.txt` – Bericht in qa.md übernehmen.
- Sounds werden vor dem Mischen aufgeräumt: gleiche Lautheit, Einblendungs-Sounds nicht im Dauerfeuer, max. 2 Sounds gleichzeitig, keine Endlos-Schleifen, defekte Dateien fliegen raus. Geräusche zu sichtbarer Bewegung bleiben.
- Musik nach Spannungskurve: Wechsel der Stelle/des Tracks spätestens alle ~60–80 s, Anschwellen vor Enthüllungen/Zahlen, Bogen pro Kapitel, Pegel automatisch unter der Stimme. Weiterhin nur die eigene Musik-Bibliothek, keine neuen Tracks.
- Im Skript Enthüllungen klar formulieren (Zahl, „aber“, „doch“, Frage → Antwort): daraus baut die Spannungskurve.
- Bericht meldet Lücken > 22 s ohne neuen Reiz → dort Bild/Effekt/Schnitt ergänzen, bevor gerendert wird.

## Hook-Regeln (Laurin 19.11.2026 – gilt ab dem nächsten Video)
Grundlage: Auswertung erfolgreicher Ausreißer-Videos in allen 5 Nischen (vidIQ), Hook-Studie mit über 4.000 Hooks aus Videos mit über 1 Mio. Aufrufen, Aprilynne Alters Intro-Formel. Es gibt keinen einzelnen besten Hook-Typ – aber alle erfolgreichen Hooks haben diesen Aufbau:
1. **Thema in 0–5 s gesagt UND gezeigt** – genau das, was Titel und Thumbnail versprechen; das Thumbnail-Motiv ist im ersten Bild zu sehen. Kein Datum, kein Logo, keine Vorrede als erster Satz.
2. **Offene Frage / Rätsel spätestens bei 10–15 s.** Die Antwort kommt frühestens im letzten Drittel.
3. **Konkretes Versprechen vor Hook-Ende** (was man am Ende weiß, wie viele Punkte, wer dahintersteckt).
4. **Bestes Material zuerst:** die stärkste Animation / das stärkste Bild gehört in den Hook.
5. **Kurz:** Hook-Länge siehe Kanal-Regel unten. Kontext erst danach, nicht vorne stapeln.
6. **Rehook:** Jedes Kapitel endet mit einer neuen offenen Frage.

**Prüfung vor dem Rendern** (in qa.md eintragen): Sekunde, ab der das Thema klar ist (≤ 5), Sekunde der offenen Frage (≤ 15), Versprechen ja/nein, Hook-Länge (Wörter ÷ 2,4 = Sekunden).
**Nach 48 h:** Retention bei 30 s per vidIQ (audience_retention) ins Video-Log. Ziel ≥ 70 %. Unter 50 % → beim nächsten Video den Alternativ-Typ unten nehmen.
**Denkmuster-Hook:** **Du-Alltagsszene im Präsens**, die der Zuschauer selbst kennt („Freitag, 18 Uhr. Dein Handy vibriert …“) → die Selbstzweifel-Frage („Stimmt etwas nicht mit mir?“) → Versprechen („Ich zeige dir sieben Gründe. Zähl mit, wie viele auf dich zutreffen.“). „du/dein“ ab dem ersten Satz. Die Studie kommt erst NACH dem Hook als Beleg. **Länge 30–40 s** (vorher 60–75 s – zu lang, Hook von 002 begann mit einem Datum, „dein Kopf“ erst nach ~50 s). Alternative: Du-Frage mit Gegen-Erwartung („Weißt du, was an … so seltsam ist? Sie sind ganz anders, als man denkt.“).

## Sound-Bibliothek aus Laurins Sammlung (19.11.2026)
- setup.sh lädt `bibliothek/denkmuster/` (NUR die Effekte dieses Kanals) + `bibliothek/gemeinsam/` (Foley, Atmos, Waffen) nach /home/claude/sfx-bibliothek/bibliothek. Liste: `bibliothek/denkmuster/LISTE.md` im Repo sound-mediathek.
- **Reihenfolge bei der Sound-Wahl:** 1. eigene assets/sfx (abgenommen) → 2. Bibliothek (`import bibliothek as BIB; BIB.pick("denkmuster", "whoosh", seed=<video-ordner>)`, `BIB.suche("auto")`) → 3. Hugging Face/SFXMint nur, wenn nichts passt.
- `seed` = Video-Ordner: so wechseln die Sounds von Video zu Video, ohne dass es zufällig klingt. Alle Bibliotheks-Sounds sind geprüft (audit.py), Memes/geschützte/kommerzielle Sounds sind aussortiert.
- Nie Effekte aus fremden Kanal-Ordnern nehmen; `reserve/` nur nach Rückfrage bei Laurin.

## Video 003 (21.11.2026)
- Laurin 21.11.2026: Bei Widerspruch zwischen geplantem Task („direkt öffentlich“) und HANDWERK.md („nur nach Laurins Ja“) → erst Entwurf, Laurin gibt frei.
- Neu: `engine/bausteine.py` mit den ANIMATION.md-Bausteinen (Karteikarte, Zahl in Handschrift, Mythos durchstreichen, Schlüsselwort, laufende Figur, Gedankenschleife, Gewicht, Netz, Zwei Wege, Tagesuhr, 100 Figuren, Kette, Skala, Ortsmarke).
- Bild-Drehbuch direkt aus scenes.py erzeugen: jede Einstellung mit `S(k, "Stichwort", Animation, zeigt, …)` setzen, `python3 scenes.py --drehbuch` schreibt bilddrehbuch.json (spart doppelte Arbeit, Zeiten stimmen exakt).
- Achtung `from kit import *` überschreibt eine eigene Variable `HERE` → im Videoordner `v.dir` nehmen.
- bilddrehbuch.py: „am/pm“-Regex meldete jedes deutsche „am“ als Uhrzeit → nur noch mit Ziffer davor (in den anderen Kanal-Repos genauso korrigieren).
- Farbregel streng: Blau/Orange nur an der Hauptfigur → Labels INK, Betonung RED (icons-Defaults wie check/bell/bulb/coin/building überschreiben).
- kit.py-Endmix landete bei True Peak +0,1 dBTP → danach zweistufig loudnorm I=−14/TP=−2 (Ergebnis −14,5 LUFS, −2,4 dBTP).
- Goldsmith-Sounds (paper_slide, sub_drop, slap) aus EFFEKTE.md durften aus der Sandbox nicht kopiert werden (Zugriff verweigert) → stattdessen eigene Sounds (stift_klick beim Durchstreichen, pop beim Einkreisen). Laurin: bitte diese drei Sounds in assets/sfx übernehmen, wenn sie für Denkmuster gelten sollen.
- Kosten: 10 Kapitel Helena = 27,6 Credits, Thumbnail 1,5 → ~29 Credits.
- Thumbnail 003 (Laurin 21.11.2026): „ALLES ALLEIN?“ abgelehnt („check ich nicht“, „als Zuschauer würde ich nicht verstehen, worum es geht“). Gewählt: Kistenberg + helfende Hand, Text „NIE UM HILFE BITTEN? / Das Nein kommt / seltener als gedacht.“ → Regel: Zeile 1 nennt das Thema wörtlich (wie im Titel), keine Rätsel-Kurzformel.
