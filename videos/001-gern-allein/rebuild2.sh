set -e
cd /home/claude/pilot
python3 intro.py > intro_render.log 2>&1
python3 main.py > main_render.log 2>&1
python3 remix.py
ffmpeg -y -loglevel error -i denkmuster_pilot_intro.mp4 -i intro_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest intro48b.mp4
ffmpeg -y -loglevel error -i denkmuster_main.mp4 -i main_mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest main48b.mp4
printf "file 'intro48b.mp4'\nfile 'main48b.mp4'\n" > concat.txt
ffmpeg -y -loglevel error -f concat -safe 0 -i concat.txt -c copy joined.mp4
python3 music.py
ffmpeg -y -loglevel error -i joined.mp4 -i music_bed.wav -filter_complex "[1:a]volume=0.75[m];[0:a][m]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=11[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 Denkmuster_001_Pilot.mp4
echo FERTIG
