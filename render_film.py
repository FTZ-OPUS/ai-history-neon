"""Render scenes in order and join them into a soundtrack-backed 1080p60 film."""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
MANIM = Path('/Users/fengtianzhu/venvs/manim/bin/manim')
FFMPEG = Path('/opt/homebrew/bin/ffmpeg')
FFPROBE = Path('/opt/homebrew/bin/ffprobe')
SCENES = ['S00_Prologue','S01_Turing','S02_Dartmouth','S03_Perceptron',
          'S03b_Activation','S04_Winter','S05_Backprop','S05b_ChainRule',
          'S06_DeepBlue','S07_ImageNet','S08_AlphaGo','S09_Transformer',
          'S09b_AttentionMap','S10_Generative','S10b_Leap',
          'S11a_Cast','S12_Claude','S13_Astra','S14_DeepSeek','S15_Compare','S11_Finale']


def run(args):
    print('RUN', ' '.join(str(x) for x in args), flush=True)
    subprocess.run([str(x) for x in args], check=True)


def duration(path):
    return float(subprocess.check_output([str(FFPROBE),'-v','error','-show_entries','format=duration',
                       '-of','default=noprint_wrappers=1:nokey=1',str(path)],text=True))


def make_audio(length, output, cue_times):
    """Original synthesized drone, harmonic pulses, sparse impacts; no borrowed music."""
    from scipy.io import wavfile
    sr = 32000
    rng = np.random.default_rng(286)
    n = int((length + .1) * sr)
    t = np.arange(n,dtype=np.float32)/sr
    sound = np.zeros(n,dtype=np.float32)
    for f,amp in [(55,.11),(82.4,.052),(110,.036),(164.8,.020)]:
        phase=2*np.pi*f*t + .18*np.sin(2*np.pi*.11*t)
        sound += amp*np.sin(phase)
    sound *= (.76+.24*np.sin(2*np.pi*.063*t))
    for tm in np.arange(0,length,1.58):
        start=int(tm*sr)
        size=min(int(.56*sr),n-start)
        if size<=0:continue
        tt=np.arange(size)/sr
        pulse=(np.sin(2*np.pi*220*tt)+.35*np.sin(2*np.pi*440*tt))*.055*np.exp(-tt*8)
        sound[start:start+size]+=pulse.astype(np.float32)
    for tm in cue_times:
        start=int(tm*sr)
        size=min(int(.95*sr),n-start)
        tt=np.arange(size)/sr
        impact=(.12*rng.standard_normal(size)*np.exp(-tt*12)
                +.15*np.sin(2*np.pi*(90-48*tt)*tt)*np.exp(-tt*5))
        sound[start:start+size]+=impact.astype(np.float32)
    fade=np.minimum(1,np.arange(n)/max(sr*.7,1))*np.minimum(1,np.arange(n)[::-1]/max(sr*2.2,1))
    sound*=fade.astype(np.float32)
    sound=np.clip(sound,-.7,.7)
    wavfile.write(output,sr,(sound*32767).astype(np.int16))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--preview',action='store_true')
    parser.add_argument('--rebuild',action='store_true',help='Re-render every scene, including existing scenes')
    args=parser.parse_args()
    quality='-ql' if args.preview else '-qh'
    folder='1080p15' if args.preview else '1080p60'
    paths=[]
    for name in SCENES:
        path=ROOT/'media'/'videos'/'ai_history'/folder/f'{name}.mp4'
        if args.rebuild or not path.exists():
            run([MANIM,quality,'--disable_caching','--media_dir',ROOT/'media',ROOT/'ai_history.py',name])
        if not path.exists():
            raise FileNotFoundError(path)
        paths.append(path)
    concat=ROOT/'media'/('preview_v2_concat.txt' if args.preview else 'final_v2_concat.txt')
    concat.write_text(''.join(f"file '{p}'\n" for p in paths),encoding='utf-8')
    lengths=[duration(path) for path in paths]
    starts=np.cumsum([0]+lengths[:-1]).tolist()
    audio=ROOT/'media'/('preview_v2_audio.wav' if args.preview else 'final_v2_audio.wav')
    make_audio(sum(lengths),audio,starts)
    out=ROOT/('AI史诗_角色版_预览.mp4' if args.preview else 'AI史诗_2026角色版_1080p60.mp4')
    run([FFMPEG,'-y','-v','error','-f','concat','-safe','0','-i',concat,'-i',audio,
         '-c:v','libx264','-preset','medium','-crf','18','-r','15' if args.preview else '60',
         '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out])
    meta={'scenes':[{'scene':s,'start':round(t,2),'duration':round(d,2)} for s,t,d in zip(SCENES,starts,lengths)],
          'duration':round(sum(lengths),2),'output':out.name}
    (ROOT/('preview_timeline_v2.json' if args.preview else 'timeline_v2.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
    print('DONE',out,'duration',round(sum(lengths),2),flush=True)


if __name__=='__main__':
    main()
