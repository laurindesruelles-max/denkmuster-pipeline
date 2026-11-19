#!/bin/sh
# Usage: sh setup.sh
# Richtet alles Kostenlose für Denkmuster ein: Python-Pakete, Schriften, Spracherkennung (Wortzeiten).
set -e
REPO=$(cd "$(dirname "$0")" && pwd)
pip install pycairo numpy pillow onnxruntime sherpa-onnx --break-system-packages -q 2>/dev/null || true
mkdir -p ~/.fonts && cp "$REPO"/assets/fonts/*.ttf ~/.fonts/ && fc-cache -f >/dev/null 2>&1 || true
mkdir -p /home/claude/models
if [ ! -d /home/claude/models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8 ]; then
  curl -sSfL -o /tmp/parakeet.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8.tar.bz2
  tar xjf /tmp/parakeet.tar.bz2 -C /home/claude/models && rm /tmp/parakeet.tar.bz2
fi
# Denkmuster hat eigene Effekte (assets/sfx) und eigene Musik (assets/music) – nie die Goldsmith-Bibliothek einbinden.
# Ton-Werkzeug audiokit (18.11.2026): Sounds aufräumen, Musik nach Spannungskurve, Endkontrolle.
# Gemeinsam sind nur die Regeln – Sounds und Musik bleiben kanal-eigen. Repo: laurindesruelles-max/sound-mediathek
AK="${AUDIOKIT:-/home/claude/audiokit}"
if [ ! -f "$AK/adapter.py" ] || [ -n "$AK_UPDATE" ]; then
  AKT=$(mktemp -d); git clone -q --depth 1 https://github.com/laurindesruelles-max/sound-mediathek "$AKT/r" && mkdir -p "$AK" && cp "$AKT"/r/audiokit/*.py "$AKT"/r/audiokit/*.json "$AK"/ && echo "audiokit bereit: $AK"; rm -rf "$AKT"
fi
# Laurins Sound-Bibliothek (19.11.2026): eigene Effekte dieses Kanals + gemeinsame Geräusche -> /home/claude/sfx-bibliothek/bibliothek
python3 -c "import sys; sys.path.insert(0, '$AK'); import bibliothek; print('Sound-Bibliothek bereit:', bibliothek.ensure('denkmuster'))" || echo "WARNUNG: Sound-Bibliothek nicht geladen"
echo "Denkmuster bereit. Neues Video: videos/NNN-slug anlegen (siehe README.md)."
