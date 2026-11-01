#!/usr/bin/env python3
"""Convert a video to a looping GIF using ffmpeg palette generation/use."""
import argparse, subprocess, shutil, math
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('input',type=Path);p.add_argument('output',type=Path)
 p.add_argument('--width',type=int,default=270);p.add_argument('--fps',type=float,default=12)
 p.add_argument('--start',type=float,default=0);p.add_argument('--duration',type=float)
 a=p.parse_args()
 if not a.input.is_file():p.error('Input does not exist')
 if a.input.resolve()==a.output.resolve():p.error('Output must differ from input')
 if not 64<=a.width<=1920 or not math.isfinite(a.fps) or not 1<=a.fps<=30:p.error('width 64–1920; fps 1–30')
 if not math.isfinite(a.start) or a.start<0 or (a.duration is not None and (not math.isfinite(a.duration) or a.duration<=0)):p.error('Invalid interval')
 if not shutil.which('ffmpeg'):p.error('ffmpeg required on PATH')
 if a.output.exists():p.error('Output exists; choose a versioned filename')
 a.output.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-ss',str(a.start),'-i',str(a.input.resolve())]
 if a.duration is not None:cmd+=['-t',str(a.duration)]
 vf=f'fps={a.fps},scale={a.width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=192:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle'
 subprocess.run(cmd+['-filter_complex',vf,'-loop','0',str(a.output.resolve())],check=True)
 print(a.output)
if __name__=='__main__':main()
