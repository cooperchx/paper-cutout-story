from pathlib import Path
import json,re
p=Path(__file__).parent
s=(p/'index.html').read_text()
s=re.sub(r"@font-face\{font-family:(Song|Hei);[^}]+\}",'',s)
s=s.replace('<style>',"<style>\n@font-face{font-family:Smiley;src:url('assets/smiley.ttf')}")
s=s.replace('font-family:Song,','font-family:Smiley,').replace('font-family:Hei,','font-family:Smiley,').replace(' Song,',' Smiley,')
s=s.replace('上海散步 · 纸上日记','Shanghai Citywalk')
s=s.replace('THE EVERYDAY JOURNAL','Shanghai Citywalk').replace('SH / 01','01 / 03')
s=s.replace('<div class="issue">CITY WALK / LOOK 01<b>城市穿搭日记</b></div>','')
s=s.replace('SHANGHAI / WALK','01').replace('A LITTLE DETOUR','02')
s=s.replace('<span>顺路喝杯</span><span>咖啡</span>','<span>咖啡小憩</span>')
s=s.replace('<div>take the</div><div>scenic way.</div>','<div>慢慢逛</div>')
s=s.replace('COLLECT LITTLE MOMENTS.','Shanghai Citywalk').replace('PAPER / SHANGHAI','01 — 03')
s=s.replace('id="title-zh"','id="title-citywalk"').replace('#title-zh','#title-citywalk')
s=s.replace('#title-citywalk{left:72px;top:271px;gap:12px}#title-citywalk .scrap{width:109px;height:116px;font-size:91px}', '#title-citywalk{left:73px;top:270px;gap:8px}#title-citywalk .scrap{width:98px;height:112px;font-size:92px}')
s=s.replace('top:1170px;z-index:17;font:italic 28px Serif,serif','top:1170px;z-index:17;font:32px Smiley,sans-serif')
s=s.replace('<filter id="ink"', '<filter id="opaque-paper" x="-1%" y="-1%" width="102%" height="102%"><feComponentTransfer><feFuncA type="table" tableValues="0 0 0 0 0 0 0 0 1 1 1"/></feComponentTransfer></filter>\n<filter id="ink"')
# Motion wrappers keep entrances, scene changes and small paper sway independent.
for id in ['building','tree','road','sign','cafe-tree','cafe','bike','cup']:
 pattern=r'(<div id="'+id+r'"[^>]*>)(<img[^>]+>)(</div>)'
 s=re.sub(pattern,lambda m:m[1]+'<div id="'+id+'-sway" class="sway">'+m[2]+'</div>'+m[3],s)
s=s.replace('<img id="pose-A"','<div id="model-sway" class="model-sway"><img id="pose-A"').replace('alt="迈步 D"></div>','alt="迈步 D"></div></div>')
sign='''<svg class="sign-print" viewBox="0 0 1024 1536" aria-label="武康路"><rect x="263" y="230" width="499" height="203" fill="#f2ead9"/><text x="512" y="337" text-anchor="middle" font-family="Smiley" font-size="112" fill="#173552">武康路</text><text x="512" y="401" text-anchor="middle" font-family="Sans" font-size="51" font-weight="700" fill="#173552">WUKANG RD.</text></svg>'''
s=s.replace('alt="武康路纸牌"></div>', 'alt="武康路纸牌">'+sign+'</div>')
cover=json.loads((p/'cover-geometry.json').read_text())
css='''\n.sway{width:100%;height:100%;position:relative;transform-origin:50% 90%}.model-sway{position:absolute;inset:0;transform-origin:50% 94%}.sign-print{position:absolute;inset:0;width:100%;height:100%;overflow:visible}#note{font-family:Smiley,sans-serif}#loc-b .big{font-family:Smiley,sans-serif}.wipe{position:absolute;z-index:110;opacity:0;visibility:hidden;pointer-events:none;transform-origin:center}.wipe img{display:block;width:100%;filter:url(#opaque-paper)}.wipe-support{position:absolute;z-index:100;opacity:0;visibility:hidden;pointer-events:none}.wipe-support img{width:100%;display:block}#wipe-tree{width:1650px;left:-400px;top:-200px}#wipe-cafe{width:1850px;left:-400px;top:-80px}\n'''
for name,g in cover.items():css+=f'#wipe-{name}'+'{'+f'left:{g["left"]}px;top:{g["top"]}px;width:{g["width"]}px;height:{g["height"]}px'+'}\n'
s=s.replace('</style>',css+'</style>')
overlays='''<div id="wipe-tree" class="wipe-support" data-layout-allow-overflow=""><img src="assets/02-plane-tree.png" alt="巨型梧桐贴片转场"></div><div id="wipe-cafe" class="wipe-support" data-layout-allow-overflow=""><img src="assets/03-corner-cafe.png" alt="巨型店面贴片转场"></div>'''
for name,g in cover.items():overlays+=f'<div id="wipe-{name}" class="wipe" data-layout-allow-overflow=""><img src="assets/{g["file"]}" alt="巨型{name}纸片转场"></div>'
s=s.replace('<div class="footline">',overlays+'<div class="footline">')
script='''
const styles=['serif','sans ink','serif clear','mono','sans rust','serif','sans ink','serif'];
const rotations=[-5,3,-2,4,-3,2,-4,3];
function word(id,text,classes){const box=document.getElementById(id);[...text].forEach((c,i)=>{const s=document.createElement('span');s.className='scrap '+(classes?classes[i%classes.length]:styles[i%styles.length]);const g=document.createElement('span');g.className='glyph';g.textContent=c;s.appendChild(g);box.appendChild(s);});}
word('title-en','Shanghai');word('title-citywalk','Citywalk');word('coffee-title','咖啡小憩',['song','hei ink','song rust','hei']);word('closing','把日常剪成风景',['song','hei','song rust','hei ink','song','hei','song']);
window.__timelines=window.__timelines||{};const tl=gsap.timeline({paused:true});
function appear(sel,time,from={},to={},duration=.35){tl.fromTo(sel,{opacity:0,y:80,rotation:-5,...from},{opacity:1,y:0,rotation:0,...to,duration,ease:'power3.out'},time);}
document.querySelectorAll('#title-en .scrap').forEach((e,i)=>appear(e,.06+i*.06,{y:-150,rotation:rotations[i]-10},{rotation:rotations[i]},.3));
document.querySelectorAll('#title-citywalk .scrap').forEach((e,i)=>appear(e,.32+i*.06,{y:-90,rotation:8},{rotation:rotations[i]},.3));
appear('#dots',1.3,{scale:.85},{scale:1},.25);
appear('#road',.35,{x:1050,y:50,rotation:4},{x:0,rotation:-1},.65);appear('#building',.95,{y:270,rotation:-8},{rotation:-3},.55);appear('#tree',1.4,{x:500,y:50,rotation:8},{x:0,rotation:1},.5);appear('#sign',2.05,{y:300,rotation:10},{rotation:2},.38);
appear('#model',.32,{y:80,scale:.97},{y:0,scale:1},.38);
tl.set('.pose',{autoAlpha:0},0);for(let i=0;i<47;i++){const t=.25+i*.25;const id='#pose-'+['A','B','C','D'][i%4];tl.set(id,{autoAlpha:1},t);tl.set(id,{autoAlpha:0},t+.25);}
appear('#loc-a',1.7,{x:-330,y:0,rotation:-7},{x:0,rotation:-3},.4);appear('#tape',1.95,{y:-50,rotation:10},{rotation:-7},.2);appear('#note',2.5,{x:-80,y:0,rotation:-6},{x:0,rotation:-6},.3);appear('#arrow',2.75,{scale:.5,y:0},{scale:1,rotation:-5},.3);appear('#walk-note',2.25,{y:50,rotation:-3},{rotation:-2},.3);
tl.to('#building',{x:-55,duration:3.6,ease:'none'},1.5);tl.to('#tree',{x:-65,duration:3.5,ease:'none'},1.9);
tl.fromTo('#bike',{x:0,rotation:-2},{x:1950,rotation:1,duration:1.8,ease:'none'},3.35);
tl.set('#coffee-world',{autoAlpha:0},0);
// Scene switches happen only while the opaque core of a real giant sticker fills the viewport.
tl.set('#street',{autoAlpha:0},5.55);tl.set('#coffee-world',{autoAlpha:1,x:0},5.55);tl.set('#model',{x:-88},5.55);tl.set('.paper',{backgroundColor:'#e8ded2'},5.55);
tl.set(['#loc-a','#tape','#note','#arrow','#walk-note'],{autoAlpha:0},5.55);appear('#loc-b',6.12,{x:160,y:0,rotation:6},{x:0,rotation:-3},.35);appear('#cup',6.7,{y:300,rotation:17,scale:.7},{rotation:9,scale:1},.5);
document.querySelectorAll('#coffee-title .scrap').forEach((e,i)=>appear(e,6.85+i*.09,{y:95,rotation:12},{rotation:rotations[i]},.3));
tl.set('#coffee-world',{autoAlpha:0},9.8);tl.set('#street',{autoAlpha:1,x:0},9.8);tl.set('#model',{x:0},9.8);tl.set('.paper',{backgroundColor:'#e4e4d2'},9.8);tl.set(['#loc-b','#cup','#coffee-title'],{autoAlpha:0},9.8);tl.set('#loc-a',{autoAlpha:1},9.8);
document.querySelectorAll('#closing .scrap').forEach((e,i)=>appear(e,10.5+i*.045,{y:100,rotation:8},{rotation:rotations[i]},.28));
// Independent, low-amplitude stop-motion paper sway. Feet remain close to the anchor.
function sway(sel,deg,dx,dy,period,phase){for(let i=0;i<96;i++){let t=i/8;tl.set(sel,{rotation:deg*Math.sin(t*2*Math.PI/period+phase),x:dx*Math.sin(t*2*Math.PI/(period*1.17)+phase),y:dy*Math.sin(t*2*Math.PI/(period*.73)+phase+.6)},t);}}
sway('#model-sway',.72,4,3,1.1,.2);sway('#building-sway',.85,4,3,1.9,1.2);sway('#tree-sway',1.35,7,4,1.5,2.1);sway('#sign-sway',1.4,3,2,1.4,.8);sway('#road-sway',.35,3,2,2.2,2.8);sway('#cafe-sway',.85,4,3,1.7,.4);sway('#cafe-tree-sway',1.2,6,3,1.65,2.4);sway('#cup-sway',1.5,3,3,1.2,1.3);
tl.set(['#wipe-tree','#wipe-cafe','#wipe-cup','#wipe-building'],{autoAlpha:0},0);
tl.set('#wipe-tree',{autoAlpha:1,x:-1750,rotation:-14},4.55);tl.to('#wipe-tree',{x:80,rotation:4,duration:.55,ease:'power2.inOut'},4.55);tl.to('#wipe-tree',{x:1850,rotation:12,duration:.65,ease:'power2.inOut'},5.5);tl.set('#wipe-tree',{autoAlpha:0},6.2);
__CUP_WIPE__
tl.set('#wipe-cafe',{autoAlpha:1,y:-1550,rotation:-6},9.02);tl.to('#wipe-cafe',{y:0,rotation:3,duration:.55,ease:'power2.inOut'},9.02);tl.to('#wipe-cafe',{y:2200,rotation:-5,duration:.6,ease:'power2.inOut'},9.8);tl.set('#wipe-cafe',{autoAlpha:0},10.5);
__BUILDING_WIPE__
tl.seek(0);window.__timelines['shanghai-walk']=tl;
'''
g=cover['cup'];cup=f"tl.set('#wipe-cup',{{autoAlpha:1,y:{1920-g['top']+60},x:0}},4.82);tl.to('#wipe-cup',{{y:0,duration:.66,ease:'power2.inOut'}},4.82);tl.to('#wipe-cup',{{y:{-g['height']-g['top']-100},duration:.66,ease:'power2.inOut'}},5.64);tl.set('#wipe-cup',{{autoAlpha:0}},6.31);"
g=cover['building'];building=f"tl.set('#wipe-building',{{autoAlpha:1,x:{1080-g['left']+60},y:0}},9.1);tl.to('#wipe-building',{{x:0,duration:.64,ease:'power2.inOut'}},9.1);tl.to('#wipe-building',{{x:{-g['width']-g['left']-100},duration:.68,ease:'power2.inOut'}},9.86);tl.set('#wipe-building',{{autoAlpha:0}},10.55);"
script=script.replace('__CUP_WIPE__',cup).replace('__BUILDING_WIPE__',building)
s=re.sub(r'<script>.*?</script>',lambda m:'<script>'+script+'</script>',s,flags=re.S)
s=s.replace('#coffee-title .scrap{width:79px;height:98px;font-size:76px}','#coffee-title .scrap{width:109px;height:108px;font-size:79px}')
(p/'index.html').write_text(s)
(p/'BRIEF.md').write_text('''# Shanghai Citywalk · v2
12 seconds, 1080×1920, 24 fps. User requests more relaxed paper motion, giant multidirectional sticker occlusion transitions, exact English title Shanghai Citywalk without Chinese translation, and Smiley Sans for all visible Chinese.
Preserve previous v1. Keep four-pose character cycle. Add independent 8 Hz subtle paper sway, 0.35–1.5 degrees; character sway .72 degrees about feet. Two transitions: tree from left plus giant cup from below at 4.55–6.31s, then cafe facade from above plus giant building from right at 9.02–10.55s. Scene switches at 5.55 and 9.8 while opaque sticker core fully covers viewport. Font file assets/smiley.ttf is the actual SmileySans-Oblique font. Street-sign Chinese is re-typeset over the photographic sign in composition, not left as the old baked font. No translated Chinese main title. Ending Chinese is a separate original line in Smiley Sans.
''')
print('v2 written')
