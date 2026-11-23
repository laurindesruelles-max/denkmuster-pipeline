# Denkmuster – Handschrift und Effekte (von Laurin abgenommen am 20.11.2026)

Gemeinsame Regeln: `HANDWERK.md`. Hier steht nur, was Denkmuster von den anderen Kanälen unterscheidet.
Weitere freigegebene Animationsarten für die Nische und die Bild-Drehbuch-Regeln: `ANIMATION.md` (21.11.2026).

## Erkennungsmerkmale
| | Denkmuster |
| --- | --- |
| Sprache | Deutsch |
| Welt | weißes Whiteboard. Das ganze Video ist ein großes Board |
| Technik | 2D-Strich, live gezeichnet (`engine/wb.py`) |
| Farben | Schwarz auf Weiß, Blau und Orange nur an der Hauptfigur, Rot für Betonung |
| Kamera | fährt über das Board, zoomt in Gedankenblasen |
| Tempo | Strich synchron zum Wort |
| Schrift | Handschrift (Caveat) |
| Übergang | Board wird weitergezeichnet, die Kamera folgt |
| Zahlen und Karten | handgezeichnetes Diagramm, Zahl in Handschrift eingekreist |
| Musik | modern-cinematic, leicht |
| Stimme | Helena |

## Effekt-Katalog (nur diese verwenden)
| Effekt | Was passiert | Wann | Status |
| --- | --- | --- | --- |
| Hauptfigur (blaue Locke, oranger Schal) | Sie erlebt jede Situation selbst, sie ist „du“ | durchgehend | steht |
| Live-Strich | Jede Zeichnung entsteht sichtbar | durchgehend | steht |
| Kamerafahrt übers Board | Die Kamera folgt dem Gedanken | Übergang | steht |
| Blick in den Kopf | Zoom in eine Gedankenblase, drinnen eine eigene kleine Welt | was jemand denkt oder fühlt | neu, Stilprobe 20.11. |
| Experiment nachgespielt | Mehrere Figuren spielen die Studie nach | jede Studie | neu, Stilprobe 20.11. |
| Studien-Karteikarte | Gezeichnete Karte mit Jahr, Ort und Teilnehmerzahl wird angeheftet | Quelle nennen | neu, Stilprobe 20.11. |
| Innerer Regler | Ein Regler schlägt zwischen zwei Gefühlen aus | innerer Konflikt | neu, Stilprobe 20.11. |
| Pose wechselt | Dieselbe Figur in Vorher- und Nachher-Haltung | Wirkung zeigen | neu |
| Ursache-Wirkungs-Kette | Pfeile verbinden Zeichnungen | Erklärung in Schritten | neu |
| Mythos durchstreichen | Ein Satz wird geschrieben und rot durchgestrichen | Irrtum auflösen | neu, Stilprobe 20.11. |
| Handgezeichnetes Diagramm | Achsen und Kurve werden mit dem Marker gezogen | Vergleich | neu, Stilprobe 20.11. |
| Zahl in Handschrift | Die Zahl wird groß geschrieben und eingekreist | harte Zahl | neu, Stilprobe 20.11. |
| Board-Panorama | Am Ende fährt die Kamera zurück, das ganze Video ist ein Bild | Schluss | neu, Stilprobe 20.11. |

| Gedankenwolken-Ablauf (`motion` flow) | Reiz → Gefühl → Reaktion als Gedankenwolken mit Pfeilen, Abzweig („Grübeln“) | Erklärung in Schritten | neu, ANOM-Wissen 23.11. |
| Mythos dreht sich um (`motion` flip) | Notizzettel mit Klebestreifen dreht sich → Wahrheit in Rot | Irrtum auflösen | neu, ANOM-Wissen 23.11. |
| Zahl rot eingekreist (`motion` counter) | Zahl zählt in Handschrift hoch, roter Kreis drumherum | harte Zahl | neu, ANOM-Wissen 23.11. |
| Strichmännchen-Raster (`motion` grid) | 60 Strichmännchen, betroffene rot und traurig | „1 von 3“ | neu, ANOM-Wissen 23.11. |
| Schraffur-Balken (`motion` bars) | Erwartet vs. Tatsächlich, schraffiert | Vergleich | neu, ANOM-Wissen 23.11. |
| Studien-Stapel (`motion` stack) | Studienkarten (Autor, Jahr) stapeln sich, Frage in Handschrift | Forschungslage | neu, ANOM-Wissen 23.11. |
| Gezeichnetes Handy (`motion` phone) | Chat auf einem gezeichneten Handy, Zitat in Handschrift | Alltagssituation | neu, ANOM-Wissen 23.11. |

**Erweiterung 23.11.2026 (ANOM-Stilprobe):** `motion`-Bausteine **zusätzlich** zum Board (nichts ersetzt). Eigene Formen statt nur Farben: Kritzel-Doodles, Gedankenwolken, Strichmännchen, Notizzettel, Handschrift, rote Kreise. Keine Marker-Sounds. Doku: `engine/motion_dm.py`. Demo `Denkmuster_Motion_Bausteine.mp4` (23.11.2026). Gemini 23.11.: Ablauf, Raster, Balken, Studien-Stapel PREMIUM; Wisch-Sound am Clip-Start klang wie Marker-Quietschen → raus.

**Raus:** Zeichen- und Marker-Sounds (Laurin hat sie abgelehnt).

Stilprobe: `stilprobe_denkmuster.mp4` (20.11.2026). Sounds folgen nach dem Casting (`doku-ohren`).

## Sound je Effekt (Stand 20.11.2026, Version 2 von Laurin als besser bewertet (20.11.2026))
Geplant nach dem Grundsatz aus `HANDWERK.md`: erst festlegen, wo überhaupt ein Sound hingehört, dann je Stelle genau einen. Skripte: `engine/stilproben/ton_*.py`.

| Effekt | Sound |
| --- | --- |
| Grundsatz | wenige Sounds: 7 Stellen in 22 s, nur an echten Bild-Ereignissen, Kamerafahrten meist ohne Sound |
| Studien-Karteikarte | pop_klein |
| Blick in den Kopf | schwenk |
| Innerer Regler | ein stift_klick beim Einrasten (nicht bei jedem Ausschlag) |
| Mythos durchstreichen | Musik setzt kurz aus, trockener Papier-Wisch (paper_slide aus Laurins Goldsmith-Sammlung). Nicht: Papierknüllen |
| Zahl in Handschrift | Musik setzt aus, Zahl erscheint in der Stille, beim Einkreisen tiefer trockener Treffer (sub_drop + leiser slap), Musik schwillt an. Nicht: aha_funkeln |
| Board-Panorama | schwenk leise, Kanal-Klang (klang) leise am Ende |
