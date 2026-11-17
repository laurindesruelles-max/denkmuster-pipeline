# Denkmuster – Produktions-Pipeline

YouTube: **Denkmuster** (@denkmustertv, Channel-ID UCJxoOFwP2Ezx188RZKi4Y8A), über vidIQ verbunden.
Nische: Psychologie im Alltag – „warum Menschen tun, was sie tun“, deutsch, Themen aus aller Welt.
Stil: **Whiteboard** (Marker-Zeichnungen, die live entstehen, Kamera fährt übers Board), feste Hauptfigur mit **blauer Spirallocke + orangem Schal**.
Stimme: Higgsfield **„Helena“** (`text2speech_v2`, variant `elevenlabs`, voice_id `3c2b83c0-2e0a-5ae8-998a-a5fe71b7eccd`).
Rhythmus: **jeden Tag ein Video** (Laurin 17.11.2026). Laurin erlaubt, direkt öffentlich zu veröffentlichen, wenn Faktencheck + Prüfbericht sauber sind.

## Ordner
| Pfad | Inhalt |
|---|---|
| `engine/wb.py` | Whiteboard-Engine: zeitgesteuerte Marker-Striche, Handschrift (Caveat), Kamera, Stift, Ausblenden (`mark`/`clear`) |
| `engine/icons.py` | Icon-Bibliothek (Figur `stick`, Auge, Buch, Tür, Herz, Haken, Kreuz, Sprechblase, Couch, Zitrone, Tropfen, Gehirn, Kopfprofil, Akku + Füllung, Regler + Nadel, Scanner, Münze, Molekül, Uhr, zzz, Uni-Gebäude, Glühbirne, Wolke, Dimmer, Welle, Stecker, Glocke, Kommentar-Box) |
| `engine/kit.py` | **Baukasten für neue Videos**: Kapitel-Timeline mit wortgenauen Zeiten (`v.at(k, "Stichwort")`), Kapitelkarten, Kamera (`v.gop`), Musik pro Kapitel, Endmischung −15 LUFS |
| `engine/wordtimes.py` | Wortzeiten aus der Sprachaufnahme (Parakeet, lokal, kostenlos) – nie Zeiten schätzen |
| `engine/thumbnail.py` | Hero-Thumbnail: Higgsfield-Motiv + 2–3 Zeilen Text |
| `engine/qa.py` | Technische Endkontrolle + Prüfbericht `qa.md` |
| `assets/sfx` | **Denkmuster-eigene Effekte** (SOUNDS.md) – nie die Goldsmith-Bibliothek |
| `assets/music` | **Denkmuster-eigene Musik** (MUSIC.md), modern & cinematic |
| `assets/fonts`, `assets/brand` | Caveat, Fredoka; Profilbild + Banner |
| `videos/NNN-slug/` | ein Ordner pro Video (Skript, vo/, scenes.py, video.mp4, thumbnail.png, beschreibung.txt, qa.md) |

## Neues Video – Ablauf
1. `sh setup.sh`
2. **Thema** (Format-Mix: ~50 % „Die Psychologie von Menschen, die …“, ~25 % Denkfehler & Effekte, ~25 % aktuelle Studien/Trends mit Psychologie-Blickwinkel). Nicht doppeln: `videos/` prüfen. Ideen: `NEXT_TOPIC.md`.
3. **Recherche**: echte Studien (Original/Abstract/Uni-Pressemitteilung). Jede Zahl belegen. Schwache Studien offen als schwach benennen.
4. **Skript** (`skript.md`): Hook (Kapitel 0, ohne Kapitelkarte, ~60–75 s, vom Großen ins Kleine, überraschende Studie), 6–8 Kapitel, Schluss mit
   Kommentar-Frage + „Abonniere Denkmuster und aktiviere die Glocke“. **Gesamtlänge über 8 Minuten** (~1250+ Wörter inkl. Hook). Zahlen als Wörter, „...“ = Pause.
   Ein Satz = ein Bild. Gesundheitsnahe Themen: Hinweis auf Hilfe, keine Diagnosen.
5. **Stimme**: pro Kapitel eine Datei `vo/kI.mp3` (Batch max. 4 gleichzeitig, sonst Rate-Limit), Text auch als `vo/kI.txt`;
   dann `python3 engine/wordtimes.py vo/kI.mp3 vo/kI.txt vo/kI.json`.
6. **Szenen** `scenes.py` mit `engine/kit.py` (Vorlage: `videos/001-gern-allein/main.py` zeigt, wie jede Szene gebaut wird). Pro Satz ein neues Bild,
   Hauptfigur `hero=True`, animierte Grafiken (Balken, Regler, Akku, Dimmer, Zähler), Labels in Caveat. Sonderzeichen ↑ ↓ → gibt es in Caveat NICHT – Wörter nehmen.
   Testlauf: `python3 scenes.py` bricht ab, wenn ein Stichwort fehlt. Kontaktabzug ansehen (ffmpeg Frames), Überlappungen fixen.
7. **Thumbnail** (`engine/thumbnail.py`), Motiv über Higgsfield. Titel: neugierig statt beschreibend.
8. **Prüfung (Pflicht)**: `python3 engine/qa.py …`; **unabhängiger Faktencheck durch separaten Agenten** (alle Zahlen/Studien gegen Originale, MUSS-Korrekturen umsetzen,
   Stimme der betroffenen Kapitel neu erzeugen); Recht/Lizenz-Checkliste in `qa.md`.
9. **Upload**: Video + Thumbnail über Higgsfield `media_upload` (PUT auf upload_url, `media_confirm`) → cloudfront-URL →
   `vidiq_video_upload(url=…)` / `vidiq_upload_image(image=…)` → `vidiq_social_post_draft_create` (YOUTUBE, platformAccountId UCJxoOFwP2Ezx188RZKi4Y8A,
   Titel, Beschreibung mit Kapiteln + Quellen, Tags, `thumbnailImageId`, categoryId 27 Bildung) – keine `<` `>` im Text. mcp.vidiq.com ist aus der Sandbox NICHT erreichbar → immer Higgsfield-URL nehmen.
10. Kurzfassung des Prüfberichts an Laurin. Video-Ordner + Lessons committen.

## Regeln (Laurin)
- Jeder Kanal hat **eigene Effekte und eigene Musik**. Denkmuster nutzt nur `assets/sfx` und `assets/music`.
- **Keine Zeichen-/Marker-Sounds** (Laurin 17.11.2026: „ganz ganz schlimm“). Sounds nur bei wichtigen Momenten (Pop, Klang, Aha-Funkeln) und zu dem, was man sieht (Uhr, Stromschlag, Schritte). Nie selbst synthetisieren.
- Kapitelkarten **~2 s stehen lassen** (kit.py: CARD = 5.0).
- Musik: Hook-Anfang ohne Musik, pro Kapitel ein Track, Pause während der Kapitelkarte, deutlich unter der Stimme.
- Videos **immer über 8 Minuten**, Ende mit Kommentar-Frage + Glocke, Quellen in der Beschreibung.
- Thumbnails professionell (illustriertes Motiv + große Schrift), keine Strichmännchen, keine Logos, keine echten Personen.
- Fakten müssen stimmen, sonst nicht veröffentlichen.
