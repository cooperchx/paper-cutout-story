def pose_markup(prefix,filename):
    parts=[]
    for pose in ['A','B','C']:
        scale={'A':1,'B':1.117,'C':1.015}[pose]
        ident=f'{prefix}-{pose}'
        src=f'assets/walk-{pose}.png'
        # Keep photographic face/torso fixed; align the source foot baselines.
        images=f'<defs><clipPath id="{ident}-upper"><rect width="1024" height="850.5"/></clipPath><clipPath id="{ident}-lower"><rect y="850" width="1024" height="686"/></clipPath></defs><image href="{src}" width="1024" height="1536" clip-path="url(#{ident}-upper)"/><g transform="translate(0 {850*(1-scale)}) scale(1 {scale})"><image href="{src}" width="1024" height="1536" clip-path="url(#{ident}-lower)"/></g>'
        parts.append(f'<div id="{ident}" class="pose" data-pose="{pose}"><svg width="100%" height="100%" viewBox="0 0 1024 1536" style="overflow:visible;filter:url(#paper-edge)">{images}</svg></div>')
    return '<div class="gait-bob" style="position:absolute;inset:0">'+''.join(parts)+'</div>'
GAIT_JS=r'''
// Left stride -> passing pose -> right stride -> passing pose.
// Three source photographs; four phases, six export frames per phase.
const walkOrder=['A','C','B','C'];
for(const [prefix,offset] of [['walk',0],['end',0],['mini',0],['right',2]]){
 for(let phase=0;phase<61;phase++){
  const active=walkOrder[(phase+offset)%4];
  for(const pose of ['A','B','C'])tl.set('#'+prefix+'-'+pose,{autoAlpha:active===pose?1:0},phase/4);
 }
}
for(let f=0;f<360;f++)tl.set('.gait-bob',{y:-2*Math.sin(Math.PI*(f%6)/6)},f/24);
tl.to('#street-ground',{backgroundPositionX:-900,duration:15,ease:'none'},0);
window.__walkCycle={imageCount:3,order:walkOrder,holdFrames:6,fps:24,cycleFrames:24};
'''
