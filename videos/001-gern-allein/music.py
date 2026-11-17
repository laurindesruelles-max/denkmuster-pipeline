import subprocess, sys
sys.argv=['x']
import main
import intro
M="/home/claude/dm_music/hf/dm_music_{}.mp3"; IO=round(78.0 + intro.DELTA, 2)
segs=[(10.6, 77.0 + intro.DELTA, 1)]; plan=[2,3,1,2,4,3,4,2,5]
for k in range(9):
    s=IO+main.VSTART[k]-0.2; e=IO+(main.CT[k+1] if k<8 else main.TOTAL)-0.5; segs.append((s,e,plan[k]))
inp=[];f=[];lab=""
for i,(s,e,tr) in enumerate(segs):
    L=e-s; inp+=["-i",M.format(tr)]; ms=int(s*1000)
    f.append(f"[{i}:a]aformat=channel_layouts=stereo,aresample=48000,loudnorm=I=-24,atrim=0:{L:.2f},afade=t=in:d=2,afade=t=out:st={max(0,L-1.6):.2f}:d=1.6,adelay={ms}|{ms}[m{i}]"); lab+=f"[m{i}]"
f.append(lab+f"amix=inputs={len(segs)}:normalize=0:duration=longest,volume=0.55[o]")
subprocess.run(["ffmpeg","-y","-loglevel","error"]+inp+["-filter_complex",";".join(f),"-map","[o]","-ar","48000","music_bed.wav"],check=True)
print("music ok")
