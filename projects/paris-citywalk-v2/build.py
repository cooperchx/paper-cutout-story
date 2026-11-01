from pathlib import Path
import re

P=Path(__file__).parent
(P/'compositions').mkdir(exist_ok=True)
common=r'''
@font-face{font-family:Smiley;src:url('assets/smiley.ttf')}
*{box-sizing:border-box}#root{position:relative;width:100%;height:100%;overflow:hidden;font-family:Sans,sans-serif;color:#293744}.layer{position:absolute}.paper{background:#f1ebdb;clip-path:polygon(1% 0,30% 1%,57% 0,80% 1%,99% 0,100% 30%,99% 60%,100% 99%,76% 100%,47% 99%,18% 100%,0 99%,1% 66%,0 30%)}.grain:after{content:"";position:absolute;inset:0;pointer-events:none;mix-blend-mode:multiply;opacity:.16;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='150'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.7' numOctaves='3' seed='16' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' opacity='.45' filter='url(%23n)'/%3E%3C/svg%3E")}.base{position:absolute;inset:0}.sticker{position:absolute;transform-origin:50% 90%;filter:drop-shadow(3px 5px 2px #28303c33)}.sticker img{width:100%;height:auto;display:block}.sway{width:100%;height:100%;position:relative;transform-origin:50% 90%}.label{position:absolute;font:28px Mono,monospace;line-height:1.3;padding:13px 22px;z-index:30}.folio{position:absolute;left:70px;right:70px;top:65px;display:flex;justify-content:space-between;font:28px Mono,monospace;letter-spacing:1px;z-index:40}.word{position:absolute;display:flex;gap:7px;z-index:35}.letter{display:flex;align-items:center;justify-content:center;line-height:1;background:#f4edda;color:#293744;clip-path:polygon(1% 2%,39% 0,70% 2%,99% 0,100% 46%,98% 75%,100% 98%,55% 100%,0 98%,1% 54%)}.letter:nth-child(3n){background:#f0e6a7}.letter:nth-child(4n+2){background:#273c4b;color:#eee8d7;font-family:Sans;font-weight:800}.letter:nth-child(4n+1){font-family:Serif}.letter:nth-child(4n+3){font-family:Mono}.letter:nth-child(4n){font-family:Serif}.photo-card{position:absolute;background:#f5efdf;padding:13px;box-shadow:4px 7px 2px #1f2d3829;clip-path:polygon(0 1%,98% 0,100% 98%,1% 100%)}.photo-card svg{display:block;width:100%;height:100%}.figure{position:absolute;transform-origin:50% 100%}.pose{position:absolute;inset:0;opacity:0;visibility:hidden}.pose svg{width:100%;height:100%;overflow:visible}.fine-rule{position:absolute;height:2px;background:currentColor}.caption{font:28px Mono;line-height:1.4}.news{position:absolute;font:22px Serif;line-height:1.7;color:#263d49;opacity:.11;columns:3;column-gap:35px;overflow:hidden}
'''
def defs(key):
 return f'''<svg width="0" height="0" style="position:absolute"><defs><filter id="{key}-edge" x="-12%" y="-8%" width="124%" height="120%"><feComponentTransfer in="SourceAlpha" result="solid"><feFuncA type="discrete" tableValues="0 0 0 0 1 1 1 1"/></feComponentTransfer><feMorphology in="solid" operator="dilate" radius="5" result="wide"/><feTurbulence baseFrequency=".065" numOctaves="2" seed="9" result="noise"/><feDisplacementMap in="wide" in2="noise" scale="1.5" xChannelSelector="R" yChannelSelector="G" result="edge"/><feFlood flood-color="#f6efdd"/><feComposite in2="edge" operator="in" result="paper"/><feMerge><feMergeNode in="paper"/><feMergeNode in="SourceGraphic"/></feMerge></filter><filter id="{key}-opaque"><feComponentTransfer><feFuncA type="table" tableValues="0 0 0 0 0 0 0 0 1 1 1"/></feComponentTransfer></filter></defs></svg>'''
def word(ident,text):
 return '<div id="'+ident+'" class="word">'+''.join(f'<span class="letter grain">{c}</span>' for c in text)+'</div>'
def sticker(ident,src):
 return f'<div id="{ident}" class="sticker"><div class="sway"><img src="assets/{src}.png" alt="{src} photographic paper cutout"></div></div>'
def crop(ident,src,view,cls='photo-card grain'):
 return f'<div id="{ident}" class="{cls}"><svg viewBox="{view}"><image href="assets/{src}.png" width="1024" height="1536"/></svg></div>'
def figure(ident,key):
 parts=[]
 for pose in ['A','P','B']:
  parts.append(f'<div id="{ident}-{pose}" class="pose"><svg viewBox="0 0 1024 1536" style="filter:url(#{key}-edge)"><image href="assets/gait-{pose}.png" width="1024" height="1536"/></svg></div>')
 return f'<div id="{ident}" class="figure"><div class="sway">'+''.join(parts)+'</div></div>'
helpers=r'''
const tl=gsap.timeline({paused:true});
function arrive(sel,t,from={},to={},d=.3){tl.fromTo(sel,{opacity:0,y:45,rotation:-5,...from},{opacity:1,y:0,rotation:0,...to,duration:d,ease:'power3.out'},t)}
function letters(sel,t){document.querySelectorAll(sel+' .letter').forEach((el,i)=>arrive(el,t+i*.045,{y:45,rotation:8-i*2},{rotation:[-3,2,-2,3,-1,2,-3,1][i%8]},.23))}
function sway(sel,deg,x,y,phase=0){for(let f=0;f<=72;f++){let t=f/8;tl.set(sel,{rotation:deg*Math.sin(t*3.2+phase),x:x*Math.sin(t*2.1+phase),y:y*Math.sin(t*3.6+phase)},t)}}
function cycle(id,seconds){const poses=['A','P','B'];const seq=[[0,'A'],[8/24,'P'],[12/24,'B'],[20/24,'P']];for(let c=0;c<=Math.ceil(seconds);c++)for(const [off,active] of seq)for(const p of poses)tl.set('#'+id+'-'+p,{autoAlpha:p===active?1:0},c+off)}
'''
def scene(name,duration,css,body,js):
 text=f'''<template><style>{common}{css}</style><div id="root" data-composition-id="{name}" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920" data-layout-allow-overlap="" data-layout-allow-overflow="" data-layout-allow-occlusion="">{defs(name)}{body}</div><script>{helpers}{js}\nwindow.__timelines=window.__timelines||{{}};window.__timelines['{name}']=tl;</script></template>'''
 (P/'compositions'/f'{name}.html').write_text(text)

introcss='''
#intro-title{left:70px;top:170px}#intro-title .letter{width:135px;height:170px;font-size:145px}
#intro-city{left:70px;top:1710px;gap:5px}#intro-city .letter{width:104px;height:108px;font-size:83px}
#intro-bust{left:250px;top:360px;width:820px;height:1230px;z-index:12;filter:drop-shadow(4px 6px 2px #42312333)}#intro-bust svg{width:100%;height:100%;overflow:hidden;filter:url(#intro-edge)}
#intro-coffee{left:55px;top:1260px;width:350px;height:410px;z-index:20;background:#733b39}
#intro-belt{left:65px;top:800px;width:260px;height:315px;z-index:14;background:#879ca7}
#intro-card{left:-125px;top:450px;width:590px;z-index:2}
#intro-building{left:610px;top:1320px;width:530px;z-index:6}
#intro-note{left:70px;top:1150px;width:245px;font:29px Mono;line-height:1.35;z-index:22}
#intro-sub{left:70px;top:355px;font-size:27px;padding:0}
'''
introbody='''<div class="base grain" style="background:#ede7ce"></div><div class="folio"><span>THE PARIS EDIT</span><span>01 / COFFEE</span></div>'''+word('intro-title','Paris')+word('intro-city','Citywalk')+sticker('intro-card','postcard')+crop('intro-bust','walk-A','250 20 580 870','layer')+crop('intro-coffee','walk-A','610 380 200 245')+crop('intro-belt','walk-A','330 520 380 460')+sticker('intro-building','haussmann')+'''<div id="intro-sub" class="label">A little detour.</div><div id="intro-note" class="layer">BUTTER<br>+ DENIM</div>'''.replace('<br>','<div></div>')
introjs='''
letters('#intro-title',.05);letters('#intro-city',.6);arrive('#intro-sub',.3,{x:-70,y:0},{x:0},.3);
arrive('#intro-bust',0,{opacity:1,x:80,y:70,scale:1.06,rotation:0},{x:0,y:0,scale:1,rotation:0},.5);
tl.to('#intro-bust',{x:-20,y:-24,scale:.97,duration:1.5,ease:'none'},.65);
arrive('#intro-card',.28,{x:-150,y:0,rotation:-18},{x:0,rotation:-9},.35);
arrive('#intro-coffee',.72,{x:-100,y:90,rotation:10},{x:0,y:0,rotation:-6},.35);
arrive('#intro-belt',.48,{x:-140,y:0,rotation:-8},{x:0,rotation:5},.32);
arrive('#intro-note',1.05,{y:35},{rotation:-3},.25);
arrive('#intro-building',1.2,{x:250,y:70,rotation:8},{x:0,y:0,rotation:4},.38);
tl.to('#intro-coffee',{x:25,y:-20,duration:1,ease:'none'},1.1);sway('#intro-building .sway',.5,2,1,.4);
'''
scene('intro',2.55,introcss,introbody,introjs)

streetcss='''
#street-title{left:70px;top:175px;font:83px Serif;line-height:1.05;color:#f2eddc;width:690px;z-index:25}
#street-building{left:-200px;top:500px;width:950px;z-index:5}
#street-metro{left:690px;top:850px;width:420px;z-index:7}
#street-books{left:550px;top:1195px;width:650px;z-index:8}
#street-hero{left:160px;top:650px;width:700px;height:1050px;z-index:20}
#street-road{left:-300px;top:1480px;width:1680px;height:290px;background:#d8d5c6;z-index:9;border-top:15px solid #f1ecda;background-image:repeating-linear-gradient(90deg,transparent 0,transparent 195px,#4c596a20 197px,#4c596a20 200px)}
#street-label{left:66px;top:1785px;background:#f1e6ab;z-index:30;font-size:28px}
#street-news{left:400px;top:280px;width:750px;height:1240px;background:#e8e5d5;z-index:1}
.street-copy{inset:35px;font-size:25px;columns:2}
'''
streetbody='''<div class="base grain" style="background:#718ca1"></div><div class="folio" style="color:#f4eedc"><span>02 / ON FOOT</span><span>PARIS CITYWALK</span></div><div id="street-title" class="layer">Take the<br>long way.</div>'''.replace('<br>','<div></div>')+'''<div id="street-news" class="paper grain layer"><div class="news street-copy">'''+('PARIS — Streets unfold around a quiet corner. A coffee to go, a book to keep. The afternoon is a collection of small details. '*12)+'''</div></div>'''+sticker('street-building','haussmann')+sticker('street-metro','metro')+sticker('street-books','seine')+'''<div id="street-road" class="paper grain layer"></div>'''+figure('street-hero','street')+'''<div id="street-label" class="label paper grain">Coffee. Corners. Bookstalls.</div>'''
streetjs='''
gsap.set('#street-road',{rotation:12});gsap.set('#street-news',{rotation:7});
arrive('#street-title',.2,{y:-80},{y:0},.3);arrive('#street-building',.08,{x:-350,y:90,rotation:-4},{x:0,y:0,rotation:0},.4);
arrive('#street-road',0,{x:-1000,y:0,rotation:12},{x:0,y:0,rotation:12},.38);
arrive('#street-hero',.18,{x:-140,y:-145,scale:.98,rotation:0},{x:-100,y:-120,scale:.98,rotation:0},.25);
tl.to('#street-hero',{x:120,y:48,scale:1.02,duration:2.9,ease:'none'},.45);
tl.to('#street-building',{x:-95,y:-55,duration:2.8,ease:'none'},.6);
arrive('#street-metro',.65,{x:230,y:-180,rotation:9},{x:0,y:0,rotation:-3},.4);
arrive('#street-books',1.7,{x:420,y:80,rotation:6},{x:-70,y:0,rotation:-4},.45);
arrive('#street-label',1.25,{x:-240,y:0},{x:0,rotation:-2},.28);
cycle('street-hero',3.7);sway('#street-hero .sway',0,0,1,.2);sway('#street-building .sway',.4,2,1,.5);sway('#street-metro .sway',.7,1,1,1.5);sway('#street-books .sway',.6,1,1,2.2);
'''
scene('street',3.7,streetcss,streetbody,streetjs)

finalcss='''
#end-heading{left:70px;top:165px;font:65px Serif;letter-spacing:-1px;z-index:25}
#end-label{left:70px;top:275px;padding:0;font-size:28px}
#end-card{left:70px;top:390px;width:940px;z-index:10;opacity:0}
#end-hero{left:530px;top:750px;width:550px;height:825px;z-index:20}
#end-face{left:65px;top:1000px;width:370px;height:450px;z-index:18;background:#f0e6a7}
#end-books{left:-70px;top:1320px;width:690px;z-index:7}
#end-paris{left:70px;top:1580px}#end-paris .letter{width:125px;height:140px;font-size:120px}
#end-city{left:90px;top:1740px;gap:5px}#end-city .letter{width:101px;height:100px;font-size:78px}
#end-note{left:590px;top:1480px;font:24px Mono;background:#f0e6a7;padding:12px 20px;z-index:30}
'''
finalbody='''<div class="base grain" style="background:#eee9dd"></div><div class="folio"><span>03 / COLLECTED</span><span>PARIS</span></div><div id="end-heading" class="layer">Collected moments.</div><div id="end-label" class="label">A POCKET POSTCARD</div>'''+sticker('end-card','postcard')+figure('end-hero','finale')+crop('end-face','walk-A','300 15 470 570')+sticker('end-books','seine')+word('end-paris','Paris')+word('end-city','Citywalk')+'''<div id="end-note" class="label paper">Keep wandering.</div>'''
finaljs='''
gsap.set('#end-card',{rotation:-7,transformOrigin:'0 0'});tl.set('#end-card',{opacity:1},.8);
arrive('#end-heading',.25,{y:30},{y:0},.3);arrive('#end-label',.4,{y:20},{y:0},.3);
arrive('#end-hero',.8,{x:170,y:60,rotation:8,scale:.92},{x:0,y:0,rotation:3,scale:1},.4);
arrive('#end-face',.9,{x:-180,y:60,rotation:-15},{x:0,y:0,rotation:-7},.38);
arrive('#end-books',.95,{x:-260,y:100,rotation:5},{x:0,y:0,rotation:0},.4);
letters('#end-paris',1.2);letters('#end-city',1.35);arrive('#end-note',1.38,{x:100,y:0},{x:0,rotation:4},.3);
cycle('end-hero',2.75);sway('#end-hero .sway',0,0,1,1.2);sway('#end-books .sway',.4,1,1,.3);
'''
scene('finale',2.75,finalcss,finalbody,finaljs)

wipecss='''#wipe-one,#wipe-two{position:absolute;left:-1260px;top:-240px;width:3600px;height:2400px;opacity:0;visibility:hidden;transform-origin:0 0}#wipe-one img,#wipe-two img{width:100%;height:100%;display:block;filter:url(#postcards-opaque)}'''
wipebody='''<div id="wipe-one"><img src="assets/postcard.png" alt="One Paris postcard diagonal wipe"></div><div id="wipe-two"><img src="assets/postcard.png" alt="Paris postcard shrinks into final collection"></div>'''
wipejs='''
tl.set('#wipe-one',{autoAlpha:1,x:-4200,y:1500,rotation:-28},2.12);
tl.to('#wipe-one',{x:0,y:0,rotation:0,duration:.34,ease:'power2.inOut'},2.12);
tl.to('#wipe-one',{x:4200,y:-1400,rotation:20,duration:.32,ease:'power2.inOut'},2.63);
tl.set('#wipe-one',{autoAlpha:0},2.96);
tl.set('#wipe-two',{autoAlpha:1,x:3000,y:-2200,rotation:28,scale:1},5.94);
tl.to('#wipe-two',{x:0,y:0,rotation:0,duration:.26,ease:'power2.inOut'},5.94);
tl.to('#wipe-two',{x:1330,y:630,scale:940/3600,rotation:-7,duration:.73,ease:'power3.out'},6.32);
tl.set('#wipe-two',{autoAlpha:0},7.05);
'''
scene('postcards',9,wipecss,wipebody,wipejs)

root='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>Paris Citywalk — a pocket postcard</title><script src="assets/gsap.min.js"></script><style>html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:#eee9dd}#root{position:relative;width:100%;height:100%;overflow:hidden}.clip{position:absolute;inset:0}</style></head><body><div id="root" data-composition-id="paris-citywalk" data-start="0" data-duration="9" data-fps="24" data-width="1080" data-height="1920">
<div id="intro" data-composition-id="intro" class="clip" data-start="0" data-duration="2.55" data-track-index="0" data-track-kind="graphics" data-composition-src="compositions/intro.html" style="z-index:1"></div>
<div id="street" data-composition-id="street" class="clip" data-start="2.55" data-duration="3.7" data-track-index="0" data-track-kind="graphics" data-composition-src="compositions/street.html" style="z-index:2"></div>
<div id="finale" data-composition-id="finale" class="clip" data-start="6.25" data-duration="2.75" data-track-index="0" data-track-kind="graphics" data-composition-src="compositions/finale.html" style="z-index:3"></div>
<div id="postcards" data-composition-id="postcards" class="clip" data-start="0" data-duration="9" data-track-index="1" data-track-kind="graphics" data-composition-src="compositions/postcards.html" style="z-index:100"></div>
<audio id="music" class="clip" src="assets/soundtrack.wav" data-start="0" data-duration="9" data-track-index="2" data-volume=".75"></audio>
</div><script>window.__timelines=window.__timelines||{};window.__timelines['paris-citywalk']=gsap.timeline({paused:true});</script></body></html>'''
(P/'index.html').write_text(root)
print('Built Paris9s: intro, diagonal street, postcard finale, image transitions')
