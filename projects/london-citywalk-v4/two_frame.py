def pose_markup(prefix,filename):
    parts=[]
    for pose in ['A','B']:
        # Continuous source mapping below the shorts aligns the photographic
        # floor heights while preserving identical face/torso registration.
        extra = ''
        if pose=='B':
            extra=f'<defs><clipPath id="{prefix}-upper"><rect width="1024" height="850.5"/></clipPath><clipPath id="{prefix}-lower"><rect y="850" width="1024" height="686"/></clipPath></defs><image href="assets/walk-B.png" width="1024" height="1536" clip-path="url(#{prefix}-upper)"/><g transform="translate(0 -61.45) scale(1 1.072294)"><image href="assets/walk-B.png" width="1024" height="1536" clip-path="url(#{prefix}-lower)"/></g>'
        else:
            extra='<image href="assets/walk-A.png" width="1024" height="1536"/>'
        parts.append(f'<div id="{prefix}-{pose}" class="pose" data-pose="{pose}"><svg width="100%" height="100%" viewBox="0 0 1024 1536" style="overflow:visible;filter:url(#paper-edge)">{extra}</svg></div>')
    return '<div class="gait-bob" style="position:absolute;inset:0">'+''.join(parts)+'</div>'

GAIT_JS=r'''
// Exactly two independently generated full-body images. Each photograph holds
// eight export frames: A-B-A-B. No articulated limbs or pose morphing.
for(const [prefix,offset] of [['walk',0],['end',0],['mini',0],['right',1]]){
 for(let step=0;step<46;step++){
  const active=((step+offset)%2===0)?'A':'B';
  tl.set('#'+prefix+'-A',{autoAlpha:active==='A'?1:0},step/3);
  tl.set('#'+prefix+'-B',{autoAlpha:active==='B'?1:0},step/3);
 }
}
for(let f=0;f<360;f++){
 const t=f/24;
 tl.set('.gait-bob',{y:-3*Math.sin(Math.PI*(f%8)/8)},t);
}
tl.to('#street-ground',{backgroundPositionX:-900,duration:15,ease:'none'},0);
window.__walkCycle={imageCount:2,holdFrames:8,fps:24,cycleFrames:16};
'''
