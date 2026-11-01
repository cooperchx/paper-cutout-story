# Paris Citywalk v2 — gait correction

User identified distorted walking legs. Replaced moving full-body cutouts with three new built-in imagegen assets: A (screen-left leg forward), P (neutral parallel legs), B (screen-right leg forward). All derive from the same aligned source; upper body and outfit stay stable. Cycle is A 8 frames, P 4 frames, B 8 frames, P 4 frames at 24fps. No mesh deformation, limb rotation, separate lower-leg stretching, or crossfade. Whole source photo stays intact. Removed body tilt during the loop and reduced travelling scale change to 0.98–1.02.

Inspected two consecutive cycles in scene at 3.05–5.05s plus source passing pose. Knees are nearly straight, legs follow separate parallel tracks, feet exchange foreground depth. This remains photographic stop motion, not interpolated live action. Face and coffee cup stay stable. Existing static introductory portrait and city collage preserved.

HyperFrames check passed. Retained prior intentional duplicate-postcard warning and small secondary 27px label. City scenes, typography, postcard transitions, original synthesized soundtrack and 9-second duration are unchanged. Soundtrack was measured in v1, not listened to.

Final MP4 verified: 9.000 seconds, 1080×1920 H.264, 24fps,216 frames, AAC audio. Encoded A/P/B/P sequence inspected across two cycles; opposite forward legs and neutral passing pose present. Final figure stays entirely inside frame.
