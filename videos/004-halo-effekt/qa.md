# Prüfbericht

## Technik (automatisch)

| Prüfung | OK | Wert |
|---|---|---|
| Länge > 8:00 | ✅ | 11:43 |
| Auflösung 1920×1080 | ✅ | 1920×1080 |
| Tonspur vorhanden | ✅ | ja |
| Lautheit −16…−14 LUFS | ✅ | -14.8 LUFS |
| Thumbnail 1280×720 | ✅ | (1280, 720) |
| Thumbnail ≤ 2 MB | ✅ | 0.88 MB |

## Faktencheck (separater Agent, Pflicht)
- [ ] Jede Zahl/Studie gegen Original geprüft, MUSS-Korrekturen umgesetzt

## Recht / Lizenzen / YouTube
- [ ] Keine echten Personenfotos, keine Logos/Marken im Bild oder Thumbnail
- [ ] Äußerungsrecht: keine Tatsachenbehauptungen über Personen/Firmen ohne Beleg
- [ ] Sounds: assets/sfx (CC0, SOUNDS.md) – keine Goldsmith-Sounds
- [ ] Musik: assets/music (eigene Higgsfield/ElevenLabs-Tracks)
- [ ] Stimme: Higgsfield „Helena“; KI-Hinweis in der Beschreibung
- [ ] Gezeichnete Animation → „veränderte/synthetische Inhalte“ i. d. R. nicht nötig (nur wenn realistisch wirkend)
- [ ] Gesundheitsthemen: Hinweis „ersetzt keine Beratung“ in der Beschreibung
- [ ] Quellen vollständig in der Beschreibung

## Ton (audiokit + earshot + Gemini, Skill doku-ohren)
| Prüfung | Ergebnis |
|---|---|
| Lautheit / Spitze (Master) | ✅ −14,8 LUFS / −2,3 dBTP |
| Musik unter Stimme (audiokit) | ✅ 15,6 dB |
| Lücken ohne neuen Reiz > 22 s | ✅ 0 |
| Sounds | 70 Effekte (~6/Min.), keine Marker-/Zeichen-Sounds; neu für Denkmuster: Goldsmith sub_drop + slap (Zahl eingekreist), paper (Durchstreichen) laut EFFEKTE.md |
| Sound-Casting Gemini (gemini-3-flash-preview) | sub_drop+slap PREMIUM, paper-Wisch PREMIUM; pop als Zahl-Sound CHEAP → Stationen jetzt pop_klein, Zahlen nur noch Treffer; stift_klick OK |
| earshot critique (Profil fern/Simplicissimus/Netflix) | Rohmix: „needs work“, 3 major (Stille unter Kapitelkarten bis 3,2 s, lautester Moment zu flach, 0,4 s Leerlauf am Ende) → behoben: leises Musikbett unter allen Kapitelkarten, Wendungs-Moment (6:37) +3 LU mit tiefem Treffer, Ende getrimmt, milde EQ (Bass +3 dB/80 Hz, −1,5 dB/2,2 kHz, Höhen −3 dB) → **„close“, 18/23, 0 critical, 0 major** (Rest minor: Höhen, Mono, dünner Bass der Musikbibliothek) |
| Gemini-Vorschau (2 × 2 Min.) | Wendungs-Treffer „zu laut“ → um ~6 dB gesenkt. Gemini meldete „Marker-Quietschen“, „Glitzer-Sound“, „Pling bei Häkchen“ – diese Sounds gibt es laut Effektliste nicht (geprüft), vermutlich Zischlaute der Stimme bei 16 kbps (bekannte Grenze) |
| Spracherkennung am fertigen Ton (Parakeet) | ✅ 94,2 % wörtlich; Abweichungen fast nur Zahlen als Ziffern (1920, 137, 60 …) und Namen → inhaltlich > 97 %; Stellprobe K4 „Troja nach Ithaka“ in der Einzeldatei korrekt |

## Hook-Prüfung
| Punkt | Wert |
|---|---|
| Thema klar ab | 0–5 s („Zwei Gesichter … Wer von beiden wirkt kompetenter?“, Bild: zwei Gesichter, Heiligenschein) ✅ |
| Offene Frage | ~4 s „Wer wirkt kompetenter?“ + ~20 s „Aber warum?“ ✅ |
| Versprechen | ✅ „sieben Stationen“ + „am Ende ein Trick“ |
| Hook-Länge | 44 s (Ziel 30–40 s, leicht drüber) ⚠️ |

## Bild-Drehbuch
`python3 engine/bilddrehbuch.py …/bilddrehbuch.json --kanal denkmuster` → OK ✅ (202 Einstellungen, 17,2 Ereignisse/Min.). Kontaktabzüge aller Kapitel angesehen; behoben: Waage/Boot (Koordinaten-Bug in dyn-Funktionen), Notenkreise, Heiligenschein-Position, Karte/Gebäude-Überlappung.

## Faktencheck (separater Agent)
- [x] Vor dem Einsprechen: alle Studien gegen Originale/Abstracts (Thorndike 1920, Dion u. a. 1972, Eagly u. a. 1991, Landy & Sigall 1974, Clifford & Walster 1973, Todorov u. a. 2005, Antonakis & Dalgas 2009, Sigall & Ostrove 1975, Stewart 1980, Nisbett & Wilson 1977, Schuldt & Schwarz 2010, Wheeler & Kim 1997, Kahneman 2011, Schmidt & Hunter 1998)
- [x] 2 MUSS umgesetzt: Todorov – 7 von 10 (Senat) gilt ohne Zeitlimit, bei 1 Sekunde rund 2 von 3; Nisbett & Wilson – „die meisten verneinten“ statt „fast alle“, Dozent aus Belgien statt „belgischer Akzent“
- [x] SOLL umgesetzt: Thorndike = Vorgesetzte/137 Flugschüler; Dion – Eltern „am wenigsten“; Meta-Analyse-Abstufung (sozial stark, Klugheit mittel, Ehrlichkeit/Rücksicht kaum); Antonakis – Lausanne, 681 Kinder, Troja–Ithaka, 2002; Sigall & Ostrove – Zahlen + Maryland; Stewart – Pennsylvania, 74; Schuldt & Schwarz – „Bio-Mehl und Bio-Zucker“, gleiche Nährwerttabelle; Horn-Effekt als Alltagsbegriff; Wheeler & Kim – Vergleich Nordamerika; Kahneman – Punkte hinten im Heft
- [x] Kurzcheck nach Rendern: 0 MUSS; 3 SOLL umgesetzt (Hook „Ehrlichkeit/Schuld“ → „Sympathie/Strafe vor Gericht“, „fünfter Klassen“ gestrichen, „viel klüger“ → „klüger“) → K0, K3, K9 neu eingesprochen und neu gerendert; Bildtexte und Quellenliste geprüft ✅
- [ ] Restunsicherheit (gering): N=60 (Dion) und „Eltern am wenigsten“ aus Fachwissen des Prüfers, nicht im Volltext gesehen

## Recht / Lizenzen / YouTube
- [x] Keine echten Personenfotos, keine Logos/Marken (alle Gesichter gezeichnet/erfunden; Thumbnail: KI-Illustration einer fiktiven Person)
- [x] Äußerungsrecht: nur belegte Studienaussagen, Forschende sachlich genannt; Kahneman-Buch nur inhaltlich wiedergegeben
- [x] Sounds: assets/sfx (CC0) + Laurins Goldsmith-Sounds (für alle Kanäle freigegeben 22.11.2026); Kapitel-Sound nur klang
- [x] Musik: assets/music (eigene ElevenLabs-Tracks), keine neue Musik erzeugt
- [x] Stimme: Higgsfield „Helena“ (ElevenLabs); KI-Hinweis in der Beschreibung
- [x] Kein Gesundheitsthema → kein Beratungshinweis nötig
- [x] Quellen vollständig in der Beschreibung, keine Zeichen < >

## Ergebnis
Technik ✅ · Ton ✅ (0 major) · Faktencheck ✅ · Recht ✅ → bei vidIQ als **Entwurf** angelegt (postId 631471ed-8c91-47df-9fbd-cb1e4bc98ee4, öffentlich vorgesehen, nicht veröffentlicht). Grund: LESSONS 21.11.2026 – bei Widerspruch zwischen geplantem Task („direkt öffentlich“) und HANDWERK.md („nur nach Laurins Ja“) erst Entwurf, Laurin gibt frei.
