# Prüfbericht 005 – Aufschieben

## Technik (engine/qa.py, video_final.mp4)
| Prüfung | OK | Wert |
|---|---|---|
| Länge > 8:00 | ✅ | 12:51 |
| Auflösung 1920×1080 | ✅ | 1920×1080 |
| Tonspur vorhanden | ✅ | ja |
| Lautheit −16…−14 LUFS | ✅ | −14,4 LUFS |
| True Peak ≤ −2 dBTP | ✅ | −2,8 dBTP |
| Thumbnail 1280×720 | ✅ | 1280×720 |
| Thumbnail ≤ 2 MB | ✅ | 0,97 MB |

## Ton (audiokit + earshot + Gemini, Skill doku-ohren)
| Prüfung | Ergebnis |
|---|---|
| Sounds | 79 Effekte (~6,2/Min.), nur abgenommene assets/sfx + Goldsmith sub_drop/slap/paper; keine Marker-/Zeichen-Sounds; **keine neuen Sounds** → kein Casting nötig |
| Lücken ohne neuen Reiz > 22 s (audiokit) | ✅ 0 |
| earshot critique (Doku-Profil fern/Simplicissimus/Netflix) | ✅ „close“, 18/23, **0 critical, 0 major** (Rest minor: Höhen, Mono, dünner Bass der Musikbibliothek) |
| Nachbearbeitung (master.py) | Musikbett unter allen Kapitelkarten, Wendungs-Moment 9:14 (Rückzug der Fristen-Studie, +sub_drop, kurzer Swell), Ende getrimmt, milde EQ (Bass +3 dB/80 Hz, −1,5 dB/2,2 kHz, Höhen −3 dB), Limiter |
| Gemini-Vorschau (gemini-3-flash-preview, 2 × 2 Min.) | Hook: „launch-ready“, Musik gut balanciert, Stimme klar. K7-Ausschnitt: „fast“ – wünscht mehr Sounddesign (bewusst wenige Sounds laut EFFEKTE.md). Gemini erfand Effekte (Handyvibration, Mausklick), die es nicht gibt (bekannte 16-kbps-Grenze) |
| Spracherkennung am fertigen Ton (Parakeet) | ✅ 94,7 % wörtlich (Abweichungen fast nur Zahlen als Ziffern und Namen). Erster Render: in K7 hatte die TTS das Wort „fertig“ verschluckt → Satz umformuliert, K7 neu eingesprochen, neu gerendert |

## Hook-Prüfung
| Punkt | Wert |
|---|---|
| Thema klar ab | 0–5 s („Sonntag, 22 Uhr. Die Abgabe ist morgen früh“, Bild: Uhr 22 Uhr, Figur am Schreibtisch) ✅ |
| Offene Frage | ~10 s „Bist du einfach faul?“ ✅ |
| Versprechen | ✅ „sieben Stationen“ + „Trick, mit dem mehr als doppelt so viele …“ |
| Hook-Länge | 36 s ✅ |

## Bild-Drehbuch
`python3 engine/bilddrehbuch.py …/bilddrehbuch.json --kanal denkmuster` → OK ✅ (208 Einstellungen, 16,1 Ereignisse/Min.). 13 Motion-Clips (stack ×2, grid, bars ×3, flow ×3, flip ×2, counter, phone). Kontaktabzüge angesehen; behoben: Ortsmarke/Uni-Name überlappend, Pfeil durch „änderbar“, Sprechblase über Balken, Hängematten-Figur im Diagramm, „→“ (fehlt in Caveat), zu lange Deckkarten-Schrift, Karteikarten-Text zu breit.

## Faktencheck (separate Agenten)
- [x] Recherche-Agent: 10 Primärquellen verifiziert (u. a. Kerze statt Pille bei Tice 2001, N = 88; Steels 80–95 % sind zitierte ältere Schätzungen).
- [x] Faktencheck vor dem Einsprechen: **1 schwerer Fund** – Ariely & Wertenbroch 2002 (Fristen-Experiment) wurde am 02.09.2026 von Psychological Science zurückgezogen (selbst gegen Retraction Watch geprüft) → K7 komplett neu als „Der Fristen-Mythos“; außerdem SOLL umgesetzt (Steel-Definition „vorgenommen“, Harriott & Ferrari „eingestuft“, Pronin „in derselben Sitzung“, Tice 1997 „kleine Kurse, Zusammenhang“, Johansson „andere Ursachen nicht ausgeschlossen“, Wohl „vor allem starke Aufschieber“, Gollwitzer „von denen, die zurückschickten“, Sheeran „94 Tests“, Hook „vor allem kein Zeitproblem“).
- [x] Unabhängige Endkontrolle nach dem Rendern: 0 inhaltliche MUSS; Quellentitel ergänzt (Untertitel, Replikation + Retraction-DOI), K6 „dieses Jahr“ → „2026“, K7 fairer formuliert („Verlässlichkeit nicht mehr bestätigen“, „Beide Autoren stimmten der Rücknahme zu“, Replikation von Hyndman & Bisin benannt), Karteikarte Bisin & Hyndman mit Jahr 2020 → K6 + K7 neu eingesprochen, neu gerendert.

## Recht / Lizenzen / YouTube
- [x] Keine echten Personenfotos, keine Logos/Marken (Figuren gezeichnet; Thumbnail: KI-Illustration einer fiktiven Person, keine Marke auf dem Handy)
- [x] Äußerungsrecht: zurückgezogene Studie nur mit belegten Fakten (Rückzug, Replikation, „Auffälligkeiten in den Daten“), keine Fälschungs-Unterstellung an Personen
- [x] Sounds: assets/sfx (CC0) + Laurins Goldsmith-Sounds (für alle Kanäle frei); Kapitel-Sound nur klang
- [x] Musik: assets/music (eigene Tracks), keine neue Musik
- [x] Stimme: Higgsfield „Helena“ (ElevenLabs); KI-Hinweis in der Beschreibung
- [x] Gesundheitsnah: Hinweis „ersetzt keine Beratung“ im Video (K9) und in der Beschreibung
- [x] Quellen vollständig in der Beschreibung (15 Einträge)
