# Nachbearbeitung nach kit.py-Render (004): Musikbett unter Kapitelkarten, Wendungs-Moment, Ende trimmen. Danach EQ: bass=g=3:f=80, equalizer 2200 -1.5, treble -3 @9k, alimiter 0.74.
import json, subprocess
CARD,GAP=5.0,0.7; T=[None,1,1,1,1,1,1,1,1,None]; plan=[1,3,2,4,3,4,1,2,2,5]
t=0; CT=[]; VS=[]
for i in range(10):
    d=json.load(open(f'vo/k{i}.json'))['dur']; lead=CARD if T[i] else (0.5 if i==0 else 0.8)
    CT.append(t); VS.append(t+lead); t+=lead+d+GAP
vend = VS[9]+json.load(open('vo/k9.json'))['dur']
M="/home/claude/denkmuster-pipeline/assets/music/dm_music_{}.mp3"
inp=["-i","video.mp4"]; f=["[0:a]volume=0.4dB,volume='if(gt(t,%.2f),1+1.1*min((t-%.2f)/1.2,1),1)':eval=frame,volume='1+1.0*(min(max((t-396.3)/0.4,0),1)*min(max((399.6-t)/0.6,0),1))':eval=frame[a0]"%(vend+0.2,vend+0.2)]; lab="[a0]"
inp+=["-i","/home/claude/dm_sfx/gs_sub_drop.wav"]; f.append("[1:a]aformat=channel_layouts=stereo,aresample=48000,volume=0.6,adelay=398150|398150[hit]"); lab+="[hit]"
n=2
for k in range(1,9):
    inp+=["-i",M.format(plan[k])]; ms=int((CT[k]-0.2)*1000); L=CARD+0.8
    f.append(f"[{n}:a]atrim=20:{20+L:.2f},asetpts=PTS-STARTPTS,aformat=channel_layouts=stereo,aresample=48000,loudnorm=I=-30,afade=t=in:d=0.6,afade=t=out:st={L-1.0:.2f}:d=1.0,adelay={ms}|{ms}[c{k}]"); lab+=f"[c{k}]"; n+=1
f.append(lab+f"amix=inputs={n}:normalize=0:duration=first,alimiter=limit=0.72:attack=2:release=50:level=false,aresample=192000,alimiter=limit=0.74:level=false,aresample=48000[o]")
end=703.9
subprocess.run(["ffmpeg","-y","-loglevel","error"]+inp+["-filter_complex",";".join(f),"-map","0:v","-map","[o]","-t",str(end),"-c:v","copy","-c:a","aac","-b:a","192k","video_v3.mp4"],check=True); print("end",end)
