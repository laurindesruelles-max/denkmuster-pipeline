# Denkmuster – Animations-Möglichkeiten (Laurin, 21.11.2026)

Ergänzt `EFFEKTE.md` (abgenommener Kern-Katalog) um alles, was zur Nische passt: Psychologie im Alltag, warum Menschen tun, was sie tun. Alles bleibt **ein großes Whiteboard**, live gezeichnet (Schwarz auf Weiß, Blau/Orange nur an der Hauptfigur, Rot für Betonung, Handschrift Caveat). Keine Zeichen-/Marker-Sounds. Für jedes Skript gilt das Bild-Drehbuch aus `HANDWERK.md`.

## Zeit und Geschehen in dieser Nische
- **Zeit:** Alltagsszenen spielen in einem erkennbaren Moment („Sonntag, 23 Uhr, Handy in der Hand“) – die Uhrzeit wird gezeichnet, wenn sie im Satz steht. Studien immer mit **exaktem Jahr, Ort, Teilnehmerzahl** (Karteikarte).
- **Geschehen:** Psychologie ist unsichtbar – deshalb jede Aussage an **einer konkreten Handlung der Hauptfigur** zeigen (sie zögert, greift zum Handy, sagt Nein). Gefühle werden zu Bildern (Regler, Gedankenblase, Gewicht).
- **Erklärung:** Immer als **Schema** (Kette, Kreislauf, Diagramm), nie nur Figur + Text.
- **Neugier-Lücke:** Das Board zeigt eine Situation, die Auflösung („warum“) ist noch weiß; ein halb gezeichnetes Bild, das erst später fertig wird; Mitmach-Frage an den Zuschauer.

## Animations-Katalog (zusätzlich zu EFFEKTE.md)
| Animation | Was passiert | Wann | Genauigkeit | Werkzeug | Status |
| --- | --- | --- | --- | --- | --- |
| Figur bewegt sich | Die Hauptfigur läuft, dreht sich weg, gestikuliert – gezeichnete Gelenkfigur statt Standbild | durchgehend, Handlung | exakt (Geschehen) | wb.py + 2D-Rig | bauen |
| 100 Figuren | 100 Strichmännchen, der genaue Anteil färbt sich orange | Prozent, Studienergebnis | exakt | wb.py | bauen |
| Gedankenschleife | Pfeile kreisen um den Kopf, die Schleife wird immer schneller | Grübeln, Teufelskreis | schema | wb.py | bauen |
| Gehirn-Skizze | Ein gezeichnetes Gehirn, die zuständige Region wird orange schraffiert, Pfeil zum Verhalten | Biologie dahinter | schema (belegt) | wb.py | bauen |
| Zwei Wege | Das Board teilt sich: links die gewohnte Reaktion, rechts die andere – beide laufen gleichzeitig | Entscheidung, Alternative | schema | wb.py | bauen |
| Tagesuhr | Eine gezeichnete Uhr, der Zeiger springt, die Figur in der jeweiligen Tagessituation | Tagesablauf, Gewohnheit | exakt | wb.py | bauen |
| Mitmach-Test | Eine Frage oder ein Bildrätsel an den Zuschauer, gezeichneter Countdown 3–2–1, dann Auflösung | Selbsttest, Wahrnehmungsfehler | exakt | wb.py | bauen |
| Metapher verwandelt sich | Eine Zeichnung wird weitergezeichnet zu etwas anderem (Handy → Käfig, Waage kippt) | Bild für das Prinzip | schema | wb.py | bauen |
| Schlüsselwort erscheint | Der Fachbegriff wird groß in Handschrift geschrieben, wenn er fällt, und unterstrichen | neuer Begriff | exakt | wb.py | bauen |
| Gewicht auf den Schultern | Gezeichnete Last wächst/schrumpft auf der Figur | Stress, Erleichterung | stimmung → exakt im Kontext | wb.py | bauen |
| Zeitstrahl Leben | Ein Lebensstrahl mit gezeichneten Stationen (Kindheit, Schule, Job) | Entstehung eines Musters | schema | wb.py | bauen |
| Netz der Menschen | Figuren verbinden sich mit Linien, Linien werden dicker/dünner | Beziehungen, Gruppen | schema | wb.py (Layout per Manim) | bauen |
| Studie im Zeitraffer | Das Experiment läuft mit Uhr in der Ecke ab, Ergebnisse tragen sich in eine Tabelle ein | Ablauf einer Studie | exakt | wb.py | bauen (ergänzt Experiment nachgespielt) |

## Werkzeuge (alle ohne Credits, getestet 21.11.2026)
| Werkzeug | Wofür | Einrichten |
| --- | --- | --- |
| Blender (`bpy`) | echtes 3D, Physik (Rigid Body, Flüssigkeit, Stoff, Partikel), Geometry Nodes für Wachstum/Aufbau, Grease Pencil für gezeichnete Linien im Raum, Rigging für Figuren | `pip install bpy` (setup.sh) |
| 2,5D-Tiefe (`depth25d.py`, Depth Anything) | jedes Standbild in Ebenen zerlegen, Kamera fährt mit Tiefe hindurch, Ebenen bewegen sich einzeln | im Goldsmith-/Unterbau-Repo vorhanden |
| PIL + numpy + ffmpeg | eigene Motion-Grafik, Partikel, Licht, Übergänge, Compositing | vorhanden |
| Manim | exakte, animierte Diagramme, Netzwerke, Abläufe, Formeln, Zählwerke – danach im Kanal-Look eingefärbt | `apt-get install -y libpango1.0-dev libcairo2-dev && pip install manim` |
| rlottie | Lottie-Vektoranimationen (Icons, kleine Abläufe) als Vorlage, immer im Kanal-Stil nachgezeichnet | `pip install rlottie-python` |
| Pixabay, Wikimedia, Archive | echte Clips und Fotos, nur innerhalb der Kanal-Welt eingebaut (siehe HANDWERK.md) | `stock.py`, `sources.py` |
| Higgsfield | nur KI-**Bilder** (0,25 Credits), Freistellen, 3D-Modell aus Bild. **Keine KI-Videoclips** (Laurin 21.11.2026) | – |

Status in den Tabellen: **steht** = in der Engine vorhanden · **bauen** = freigegeben (Laurin 21.11.2026), beim ersten Einsatz als Baustein in die Engine aufnehmen und kurz Stilprobe an Laurin.
