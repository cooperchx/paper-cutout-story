# Identity and walking without twisted legs

## Diagnose the failure before changing timing

An alternating sequence can still be wrong: A and B may advance the same leg, the knee may bend inward, the torso may change angle, or alignment code may stretch the lower body. Inspect anatomy in the individual images before blaming frame rate.

The Paris v1 rejection came after four generated poses plus separate lower-body scale corrections. V2 regenerated clean near-straight steps and removed those corrections. This is evidence for rejecting that deformation, not a claim that every four-frame walk fails.

## Build a minimal robust loop

1. Choose a modest walking angle the generator can hold. Keep pelvis and torso direction consistent. Ask for separate tracks from each hip to its foot, nearly straight relaxed knees, ordinary stride, both shoes visible. Avoid cross-legged runway poses when the user wants everyday walking.
2. Generate **A** with one anatomical leg forward; explicitly describe both anatomical side and screen location, since three-quarter views can confuse them. Record which shoe is closer/lower and which trouser leg is in front.
3. Edit A into **B**, changing the legs below the belt to the opposite phase. Preserve head, cup, face and outfit. Opposite forward foot must be visually verifiable; merely changing folds is not sufficient. Do not horizontally flip the person: it swaps bag, cup, closures and logos.
4. Generate **C**, the intermediate passing position: knees relaxed, feet beneath hips, no high knee raise. A shared neutral C can work for a deliberately restrained scrapbook walk. For larger strides, distinct passing poses P and Q preserve support-leg continuity better.
5. Keep all poses on the same canvas. Align by stable landmarks (head centre, pelvis and support foot), not by automatic per-image bounding-box resize. A small uniform translate/scale is acceptable; independent leg length warps are not a gait repair.
6. Preview A→C→B→C twice. One tested 24fps schedule was 8/4/8/4 frames = 1 second. It is a starting point, not fixed pacing. At 30fps use time durations or an explicitly rounded hold schedule rather than silently changing the speed.
7. Inspect at playback speed and as a contact sheet. Reject identity jumps, same-leg repeats, crossed knees, large height oscillations, cup jumps, shoulder-bag teleportation or changing shoe size. Regenerate only the failing pose where possible.

For a side view, modest forward/back foot separation and a true contact/passing sequence matter. Match whole-person translation with support-foot contact; a faster scene path does not create a better stride. For a close-up with no legs, use an honest action such as sipping, head turn or adjusting glasses rather than hallucinating unseen anatomy.

## Bag and face

A shoulder bag moves a little with the body; a hand-carried bag can swing more around the hand. Keep attachment points fixed and make phase differences small. Do not swing the arm and bag independently into disconnection. A static upper body is preferable to distorted anatomy when correcting only legs.

Use even lighting for every edit. Do not add per-frame noise, grain or glare over faces. Maintain hair outline and earrings; let paper fibres live at the border. Preserve identity in the source, rather than covering errors with a strong grade.

## Pose manifest example

```json
{"id":"walk","frames":["A.png","C.png","B.png","C.png"],"holds":[8,4,8,4],"fps":24,"anchor":[0.5,1],"intent":"restrained paper stop-motion"}
```

“Smooth” in this form means coherent silhouette, support and timing; it does not automatically mean optical flow or photoreal continuous motion. If the user wants continuous realism, propose more valid poses or a segmented motion clip, without presenting interpolation as a cure for bad anatomy.
