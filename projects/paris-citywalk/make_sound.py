"""Original synthesized 9s instrumental and light paper accents; no sampled music."""
import math, random, wave, struct
from pathlib import Path
RATE=44100
DURATION=9
samples=[0.0]*int(RATE*DURATION)
rng=random.Random(94)
def tone(start,length,freq,level,kind='key'):
    begin=int(start*RATE)
    for j in range(min(int(length*RATE),len(samples)-begin)):
        t=j/RATE
        if kind=='bass':
            v=math.sin(2*math.pi*freq*t)+.14*math.sin(4*math.pi*freq*t)
            env=min(t/.008,1)*math.exp(-t*6)
        else:
            v=math.sin(2*math.pi*freq*t)+.22*math.sin(4*math.pi*freq*t)*math.exp(-t*5)+.09*math.sin(6*math.pi*freq*t)*math.exp(-t*9)
            env=min(t/.004,1)*math.exp(-t*3.9)
        samples[begin+j]+=v*env*level
def midi(n):return 440*2**((n-69)/12)
chords=[[50,54,57,61],[47,50,54,57],[52,55,59,62],[45,52,55,59],[50,54,57,61]]
for bar,notes in enumerate(chords[:5]):
    t0=bar*2
    for offset,amp in [(0,.045),(.75,.032),(1.5,.038)]:
        for n in notes:tone(t0+offset,1.2,midi(n+12),amp)
    for beat in range(4):tone(t0+beat*.5,.45,midi(notes[0]-12+(7 if beat==2 else 0)),.115,'bass')
for beat in range(18):
    start=int(beat*.5*RATE)
    for j in range(int(.16*RATE)):
        if start+j>=len(samples):break
        t=j/RATE
        samples[start+j]+=.08*math.sin(2*math.pi*(52*t+26*(1-math.exp(-t*35))/35))*math.exp(-t*30)
for step in range(36):
    start=int((step*.25+.004)*RATE);prev=0
    for j in range(int(.047*RATE)):
        if start+j>=len(samples):break
        n=rng.uniform(-1,1);v=n-prev;prev=n
        samples[start+j]+=v*.012*math.exp(-j/(RATE*.009))
for start in [.08,.45,.95,1.4,2.15,3.0,3.6,4.5,5.4,5.95,6.9,7.6]:
    prev=0;begin=int(start*RATE)
    for j in range(int(.095*RATE)):
        n=rng.uniform(-1,1);prev=.7*prev+.3*n
        samples[begin+j]+=prev*.075*math.sin(math.pi*j/(RATE*.095))**2
# Soft brushed paper swishes follow the two foreground sticker wipes.
for start,length in [(2.15,.38),(2.63,.32),(5.95,.3),(6.32,.68)]:
    begin=int(start*RATE);prev=0
    for j in range(int(length*RATE)):
        n=rng.uniform(-1,1);prev=.86*prev+.14*n
        samples[begin+j]+=prev*.12*math.sin(math.pi*j/(RATE*length))**2
peak=max(abs(x) for x in samples)
out=Path(__file__).parent/'assets/soundtrack.wav'
with wave.open(str(out),'wb') as f:
    f.setparams((2,2,RATE,0,'NONE','not compressed'))
    data=bytearray()
    for i,x in enumerate(samples):
        t=i/RATE;fade=min(1,t/.12,max(0,(DURATION-t)/.7))
        v=int(x/max(peak,.001)*.67*fade*32767)
        data+=struct.pack('<hh',v,v)
    f.writeframes(data)
print(f'{out}: {DURATION}s stereo, peak limited to -3.5 dBFS')
