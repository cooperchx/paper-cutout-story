# Tool-neutral image recipes

Replace braces. These are visual contracts, not an API. Attach actual reference images through the available tool. Generate individual assets so they remain composable; a contact sheet is a review artifact, not a substitute for separate transparent files.

## Master subject

> Create one photographic full-body cutout of the exact subject in the reference. Preserve {face/hair/outfit/materials/accessories}. Camera {view}, soft consistent lighting, normal anatomy, modest relaxed posture. Entire head, hands, bag and shoes inside the same {canvas} with generous margins. True transparency outside the subject if supported. No background, text, ground shadow or paper edge; compositing will add the border. Clean natural face, no random grain, glare patches or changed skin tone. Lock {head/pelvis/ground landmarks}.

## Alternating step edit

> Edit the master into walking phase {A/B/C}. Preserve everything above {belt} and all identity/clothing details. Change only the required lower-body pose: {specific anatomical leg and screen position forward; other trailing; or passing pose}. Legs stay on separate tracks under their hips, knees relaxed, no crossing, high knee raise or bent S-shaped trousers. Both shoes visible. Same canvas, head size, pelvis position, lighting and outfit. {Bag attachment} remains coherent.

Inspect output rather than trusting that the prompt was obeyed. The generated Paris v2 A/B/C prompts are stored in `projects/paris-citywalk-v2/gait-prompts.json`.

## City object

> One standalone photographic cutout of {object/location fragment}, {angle}. A coherent silhouette, all object edges inside generous margins. Palette {palette}; matte photographic print with a thin irregular cream paper rim and subtle fibres. True transparent background outside silhouette. No unrelated people, vehicles, surrounding rectangular sky or desk. No invented readable signage; leave meaningful text for compositing. {Function in scene}.

Select city-specific but daily-life details. If the user needs a real named façade, use a verified reference; generated scenery should not be described as an exact documentary capture.

## Single transition carrier

> One {postcard/newspaper page/receipt/ticket/packaging flap}, flat photographic scan of physical paper, {ratio}, slightly worn edges. Fully opaque face with no transparent holes; generous transparent margin outside. {Relevant image or exact supplied graphic}. No hands or surrounding table. Needs enough opaque surface to sweep over the full video canvas without destructive stretching.

A vehicle with windows or cup silhouette may need a coordinated reveal mask. Do not declare coverage from its bounding box alone.

## Crop/detail variants

Prefer cropping an approved high-resolution photo into full-body, half-body, face, garment/hand/shoe details. If crop resolution is insufficient, ask the generator to create a higher-resolution faithful detail edit, not a new person. An oversized head can be a deliberate collage choice; do not turn it into an anatomical mismatch in a walking body.

## Log each asset

Record id, local relative filename, role, reference/master IDs, full prompt, generator/tool label when known, output dimensions/alpha, selected/rejected status and review note. Never store credentials or private machine paths. Keep rejected poses labelled as study material, not recommended defaults.
