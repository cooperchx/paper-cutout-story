def sticker(ident,asset,alt):
 return f'<div id="{ident}" class="sticker city-sticker"><div class="sway"><img src="assets/{asset}.png" alt="{alt}"></div></div>'
CITY_ONE=sticker('tube-entry','tube','London Underground entrance cutout')+sticker('street-taxi','taxi','Black London cab driving along the street')
CITY_TWO=sticker('flower-store','flower-shop','Neighbourhood flowers and books shop')+sticker('phone-box','phone','Red London telephone box')+sticker('road-two','road','Paper zebra crossing')
CITY_THREE=sticker('cafe-table','cafe','Cafe table chairs newspaper and potted tree')+sticker('road-three','road','Cutout pedestrian crossing')
CITY_CSS=r'''
.city-sticker img{filter:url(#paper-edge)}
#hero-one{left:190px;top:650px;width:680px;height:1020px}
#westminster{left:-80px;top:720px;width:600px}
#street-ground{left:-70px;top:1460px;width:1220px;height:auto;border:0;background:none;z-index:12;clip-path:none}
#tube-entry{left:720px;top:980px;width:420px;z-index:6}
#street-taxi{left:-510px;top:1320px;width:490px;z-index:11}
#paper-frag{left:690px;top:670px;width:480px;height:750px;opacity:.45}
#first-note{left:70px;top:490px;max-width:700px;font-size:28px}
#first-caption{font-size:28px;top:1775px}
#bust{left:650px;top:600px;width:390px;height:520px}
#mini-left{left:30px;top:670px;width:630px;height:945px}
#mini-right{left:790px;top:1260px;width:220px;height:330px}
#flower-store{left:350px;top:1005px;width:720px;z-index:5}
#phone-box{left:22px;top:1225px;width:170px;z-index:9}
#road-two{left:-70px;top:1445px;width:1220px;z-index:10}
#tag-lime{left:62px;top:530px;font-size:28px}
#onfoot{left:690px;top:1735px;font-size:68px;padding:10px 25px}
#thin-line{top:1792px}
#hero-three{left:20px;top:700px;width:650px;height:975px}
#terrace{left:180px;top:910px;width:1020px}
#cafe-table{left:610px;top:1260px;width:460px;z-index:16}
#road-three{left:-70px;top:1460px;width:1220px;z-index:11}
#end-caption{top:813px;font-size:25px}
#end-line{font-size:28px;top:340px}
'''
CITY_JS=r'''
// Opening title gives the stage to the street after city identification.
tl.to('#london-open',{scale:.72,y:-18,transformOrigin:'0 0',duration:.5,ease:'power2.inOut'},1.6);
tl.to('#city-open',{scale:.8,y:-72,transformOrigin:'0 0',duration:.5,ease:'power2.inOut'},1.6);
arrive('#tube-entry',1.5,{x:300,y:60,rotation:8},{x:0,y:0,rotation:1},.4);
arrive('#street-taxi',2.05,{x:-250,y:0,rotation:0},{x:0,y:0,rotation:0},.25);
tl.to('#street-taxi',{x:1440,duration:2.1,ease:'none'},2.3);
arrive('#road-two',5.35,{x:1000,y:0,rotation:0},{x:0,y:0,rotation:-1},.45);
arrive('#flower-store',5.8,{x:480,y:30,rotation:5},{x:0,y:0,rotation:1},.45);
arrive('#phone-box',6.65,{x:-200,y:70,rotation:-7},{x:0,y:0,rotation:-2},.35);
arrive('#road-three',10.4,{x:950,y:0,rotation:0},{x:0,y:0,rotation:0},.45);
arrive('#cafe-table',11.65,{x:380,y:80,rotation:7},{x:0,y:0,rotation:-1},.45);
sway('#tube-entry .sway',.6,1,1,1.8,.4);
sway('#street-taxi .sway',.25,0,1,1.2,.9);
sway('#flower-store .sway',.5,2,1,2.2,1.4);
sway('#phone-box .sway',.7,1,1,1.7,.5);
sway('#cafe-table .sway',.7,2,1,2.0,1.2);
sway('#road-two .sway',.2,1,0,2.2,.3);
sway('#road-three .sway',.2,1,0,2.1,1.4);
'''
