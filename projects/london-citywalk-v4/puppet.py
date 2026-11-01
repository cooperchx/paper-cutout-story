def rig_markup(prefix):
    # All parts are photographic image layers. Masks only separate layers for motion;
    # one outline around the assembled silhouette prevents white seams at joints.
    p=prefix
    defs=f'''<defs>
    <clipPath id="{p}-body"><path d="M0 0H1024V808H425L431 720 463 600 473 430 485 350 435 270 0 250Z"/></clipPath>
    <clipPath id="{p}-arm"><path d="M405 270Q450 263 485 320L472 423 454 600 436 722 433 809Q394 831 360 792L378 720 385 600 387 445Z"/></clipPath>
    <clipPath id="{p}-bag"><path d="M365 783L379 786 343 936 402 960 412 793 429 795 425 968 477 988 476 1045 457 1144 411 1182 194 1080 233 916 299 939Z"/></clipPath>
    <clipPath id="{p}-thigh"><path d="M0 0H1024V535H605Q605 619 510 619Q415 619 415 535H0Z"/></clipPath>
    <clipPath id="{p}-calf"><path d="M415 568Q415 510 510 510Q605 510 605 568H1024V1277H0V568Z"/></clipPath>
    <clipPath id="{p}-joint"><circle cx="510" cy="560" r="88"/></clipPath>
    <clipPath id="{p}-shoe"><rect x="0" y="1246" width="1024" height="300"/></clipPath>
    </defs>'''
    def layer(clip):
        return f'<g transform="translate(-250 -45) scale(.5)"><image href="assets/leg.png" width="1024" height="1536" clip-path="url(#{p}-{clip})"/></g>'
    def leg(which,x):
        return f'''<g transform="translate({x} 770)"><g class="{which}-thigh">
        {layer('thigh')}
        <g transform="translate(5 235)"><g class="{which}-shin"><g transform="translate(-5 -235)">{layer('calf')}</g>
        <g transform="translate(-5 350)"><g class="{which}-foot"><g transform="translate(0 -585)">{layer('shoe')}</g></g></g>
        </g></g><circle cx="5" cy="235" r="38" fill="#edc2a4"/>{layer('joint')}</g></g>'''
    return f'''<svg class="rig" id="{p}-rig" viewBox="0 0 1024 1536" width="100%" height="100%" overflow="visible" aria-label="Alternating left and right walking legs with swinging bag">{defs}<g class="gait-bob" filter="url(#paper-edge)">
    <g style="filter:brightness(.94)">{leg('far',570)}</g>{leg('near',550)}
    <image href="assets/rig.png" width="1024" height="1536" clip-path="url(#{p}-body)"/>
    <g transform="translate(440 315)"><g class="carry-arm"><g transform="translate(-440 -315)"><image href="assets/rig.png" width="1024" height="1536" clip-path="url(#{p}-arm)"/>
    <g transform="translate(399 791)"><g class="carry-bag"><image href="assets/rig.png" x="-399" y="-791" width="1024" height="1536" clip-path="url(#{p}-bag-local)"/></g></g>
    </g></g></g></g>
    <defs><clipPath id="{p}-bag-local"><path transform="translate(-399 -791)" d="M365 783L379 786 343 936 402 960 412 793 429 795 425 968 477 988 476 1045 457 1144 411 1182 194 1080 233 916 299 939Z"/></clipPath></defs></svg>'''

GAIT_JS=r'''
// A measured 2-link leg rig: alternate stance and swing, exactly half a cycle apart.
// Feet move backwards linearly while planted; the recovery foot lifts only 35 source pixels.
function legAngles(p){
 p=((p%1)+1)%1;const stanceX=130-520*(p%.5),baseY=Math.sqrt(582*582-stanceX*stanceX);let x,y=baseY,pitch=0;
 if(p<.5){const q=p*2;x=130-260*q;pitch=q<.18?-8*(1-q/.18):q>.82?10*(q-.82)/.18:0;}
 else{const q=(p-.5)*2;x=-130+260*(.5-.5*Math.cos(Math.PI*q));y-=35*Math.sin(Math.PI*q);pitch=-4*Math.sin(Math.PI*q);}
 const a=Math.hypot(5,235),b=Math.hypot(5,350),d=Math.hypot(x,y);
 const bend=-Math.acos(Math.max(-1,Math.min(1,(d*d-a*a-b*b)/(2*a*b))));
 const upper=Math.atan2(x,y)+Math.acos(Math.max(-1,Math.min(1,(a*a+d*d-b*b)/(2*a*d))));
 const baseA=Math.atan2(5,235),baseB=Math.atan2(-5,350),deg=180/Math.PI;
 const thigh=(baseA-upper)*deg,shin=(baseB-baseA-bend)*deg;
 return {thigh,shin,foot:-thigh-shin+pitch,x,y,bob:550-baseY};
}
window.__gait=legAngles;
for(let i=0;i<180;i++){
 const t=i/12,p=t/(4/3),near=legAngles(p),far=legAngles(p+.5);
 for(const [side,v] of [['near',near],['far',far]]){
  tl.set('.'+side+'-thigh',{attr:{transform:'rotate('+v.thigh+')'}},t);
  tl.set('.'+side+'-shin',{attr:{transform:'rotate('+v.shin+')'}},t);
  tl.set('.'+side+'-foot',{attr:{transform:'rotate('+v.foot+')'}},t);
 }
 tl.set('.gait-bob',{attr:{transform:'translate(0 '+near.bob+')'}},t);
 const arm=13*Math.cos(2*Math.PI*p),bag=5*Math.cos(2*Math.PI*(p-.12));
 tl.set('.carry-arm',{attr:{transform:'rotate('+arm+')'}},t);
 tl.set('.carry-bag',{attr:{transform:'rotate('+bag+')'}},t);
}
tl.to('#street-ground',{backgroundPositionX:-4665,duration:15,ease:'none'},0);
'''
