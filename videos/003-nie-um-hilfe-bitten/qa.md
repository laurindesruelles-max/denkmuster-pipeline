# Prüfbericht

## Technik (automatisch)

| Prüfung | OK | Wert |
|---|---|---|
| Länge > 8:00 | ✅ | 10:30 |
| Auflösung 1920×1080 | ✅ | 1920×1080 |
| Tonspur vorhanden | ✅ | ja |
| Lautheit −16…−14 LUFS | ✅ | -14.5 LUFS |
| Thumbnail 1280×720 | ✅ | (1280, 720) |
| Thumbnail ≤ 2 MB | ✅ | 1.07 MB |

## Ton (audiokit Endkontrolle)
| Prüfung | Ergebnis |
|---|---|
| Lautheit | ✅ −14,5 LUFS (Master nachträglich zweistufig auf −14 / TP −2 normalisiert) |
| Spitze | ✅ −2,4 dBTP |
| Stille-Löcher > 2,5 s | ✅ 0 |
| Musik unter Stimme | ✅ 15,6 dB |
| Musik ohne Bewegung > 75 s | ✅ keine |
| Sounds | 63 Effekte (~6/Min.), nur assets/sfx + bibliothek/denkmuster, keine Marker-/Zeichen-Sounds |
| Spracherkennung am fertigen Ton (Parakeet) | ✅ 95,3 % Übereinstimmung mit dem Skript (Abweichungen nur Namen/Zahlen-Schreibweise) |

## Hook-Prüfung
| Punkt | Wert |
|---|---|
| Thema klar ab | 0–3 s („Du hilfst jedem sofort. Aber selbst um Hilfe bitten?“) ✅ |
| Offene Frage | ~1,7 s + 25 s („Warum fällt uns eine Frage aus vier Wörtern so schwer?“) ✅ |
| Versprechen | ✅ „sieben Gründe“ + „am Ende ein Satz“ |
| Hook-Länge | 37,7 s ✅ |

## Bild-Drehbuch
`python3 engine/bilddrehbuch.py …/bilddrehbuch.json` → OK ✅ (178 Einstellungen, 16,9 Ereignisse/Min., nur Warnungen zu kurz gehaltenen Kapitel-Fragen).
Hinweis: Regex für „am/pm“ in bilddrehbuch.py korrigiert (meldete jedes deutsche „am“ als Uhrzeit).

## Faktencheck (separater Agent, vor dem Einsprechen)
- [x] Jede Zahl/Studie gegen Original geprüft (Flynn & Lake 2008, Bohns & Flynn 2010, Zhao & Epley 2022, Taylor et al. 2004, Kim et al. 2008, Deelstra et al. 2003, Brooks et al. 2015, Addis & Mahalik 2003, Nadler & Fisher 1986, Jecker & Landy 1969, Franklin)
- [x] 5 MUSS-Korrekturen umgesetzt: Zhao = Stanford (nicht Chicago); Foto-Experiment im botanischen Garten (nicht Park); Bohns & Flynn 2010 = studentische Mentoren/Tutoren (nicht „Studienberater/Nachhilfelehrer“); Beziehungssorgen aus Studie 3 in den USA (nicht „in Korea“), „niemanden belasten“ gestrichen; „stille Unterstützung“ = spätere Arbeiten (Kim et al. 2008), „gemeinsam essen“ gestrichen
- [x] SOLL umgesetzt: „Studie, die 2008 erschien“; „gut zwei Anfragen“ statt „jeder Zweite“; Gino nicht genannt („Forschende um Alison Wood Brooks“); „Die Forschenden vermuten“; Deelstra vorsichtig („Vielleicht übertragen wir …“); Jecker & Landy präzisiert; Franklin: Gegner im Parlament von Pennsylvania
- [ ] Restunsicherheit (gering): Brooks, Gino & Schweitzer 2015 ist nicht zurückgezogen und nicht unter den von Harvard untersuchten Gino-Papern; Many-Co-Authors-Eintrag war aus der Sandbox nicht abrufbar. Im Video nur qualitative Aussage, keine Zahlen.
- [x] Bildschirm-Texte gegen Quellen geprüft (12,6 / 7,6; 57 % / 39 %; 3,21 / 0,51 gerundet; 48 Zeitarbeitskräfte; 6 Experimente, 2.118 Personen)

## Recht / Lizenzen / YouTube
- [x] Keine echten Personenfotos, keine Logos/Marken im Bild oder Thumbnail (Thumbnail: KI-Illustration einer fiktiven Person)
- [x] Äußerungsrecht: nur belegte Studienaussagen, Forschende sachlich genannt, keine Wertung über Personen
- [x] Sounds: assets/sfx (CC0) + Laurins sound-bibliothek (denkmuster) – keine Goldsmith-Sounds
- [x] Musik: assets/music (eigene ElevenLabs-Tracks)
- [x] Stimme: Higgsfield „Helena“; KI-Hinweis in der Beschreibung
- [x] Gezeichnete Animation → keine Kennzeichnung „synthetische Inhalte“ nötig
- [x] Gesundheitsnah: Hinweis „ersetzt keine Beratung“ + TelefonSeelsorge in der Beschreibung
- [x] Quellen vollständig in der Beschreibung, keine Zeichen < >

## Ergebnis
Technik ✅ · Ton ✅ · Faktencheck ✅ (alle MUSS umgesetzt) · Recht ✅ → als **Entwurf** bei vidIQ angelegt (postId 47ef3c0c-ddf9-4b5a-81b5-e365d93bed3d). Laurin am 21.11.2026: erst Entwurf, er gibt frei.
