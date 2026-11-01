# Portable rendering and project reuse

The skill is independent of its renderer. Use an existing editor/framework when it already solves the task; the included Canvas implementation is a local fallback and a readable reference for another agent.

## Browser-only preview

From repository root run `python3 -m http.server 8000`, then open:

`http://localhost:8000/templates/player.html?manifest=../examples/paris-portable.json`

Use Play/pause and the frame slider. HTTP serving is needed for manifest/image loading. Rendering is deterministic through `window.renderFrame(frame)`, separate from preview wall-clock playback. The browser player currently previews visuals only; the encoder muxes the specified audio.

## Encode

Node22.12+, FFmpeg on PATH, Chromium via Puppeteer:

```bash
npm install
node scripts/render.mjs examples/paris-portable.json rendered/example.mp4
python3 scripts/make_gif.py rendered/example.mp4 rendered/example.gif --width 270 --fps 12
```

For a short proof: append `--width 270 --seconds 2`. The output width must be even. Existing outputs are never overwritten. `CHROME_PATH` selects a locally installed browser; `PUPPETEER_MODULE` optionally selects an installed module path. These are optional environment overrides, not required private paths. The supplied script serves only repository files, captures PNGs and pipes them to FFmpeg. It does not call a hosted API or send assets elsewhere.

The example contains 9 seconds, three scenes, an A/C/B/C pose loop, one postcard image per wipe, simple paper borders and an optional local soundtrack. It is an alternate production recipe, not a promise to match the archived GSAP video exactly. For complex masks, sophisticated cut typography or advanced page turns, extend the compositor or use a capable timeline editor.

## JSON timeline contract

Top-level fields:

- `width`, `height`, `fps`, `duration`: output canvas and timing.
- `assets`: id → `{src}` or `{frames, holds, fps}`. Each `frames` entry is a relative image path; a repeated passing image can appear twice. `holds` contains positive output-frame counts, matching the sequence length. Images resolve relative to the JSON file, not process cwd.
- `scenes`: ordered `{start,end,background,layers}`. Visible on `[start,end)`. Keep ordinary scenes nonoverlapping. A layer uses time relative to its scene.
- `overlays`: layers above all scenes, using global time. Suitable for wipe images.
- `audio`: optional file path relative to JSON. The encoder pads short audio and trims to the chosen duration. No automatic beat inference or listening.

Image layer fields: `asset`, `x`, `y`, `width`, `anchorX` (default .5), `anchorY` (default1), `rotation` in degrees, `opacity`, `scale`, optional `start`/`end`, `paperEdge` in output pixels. Aspect ratio is preserved. No independent x/y stretch or limb warp.

Motion: `keyframes:[{t,x,y,width,rotation,opacity,scale,ease}]`, chronological and in seconds. Use explicit values for animated properties at each key. Eases: `linear` (default), `smooth`, `out`. Deterministic `jitter:{x,y,degrees,hz,phase}` is optional and should be small. Scene coordinates remain separate from pose selection.

Text: `type:"text"`, `text`, `fontSize`, `font`, `weight`, `color`, optional `paper`. It is editable text; meaningful wording should not be generated into scenery. Paper strip: `type:"paper"`, `color`, `width`, `height` plus transform fields.

Layers paint in listed order. Alpha holes remain holes. A giant overlay must actually be opaque at the scene cut; do not assume that choosing a large `width` proves coverage. Sample before/at/after the cut. Add a mask or select another object where needed.

## Historical projects

`projects/` contains the actual HTML/GSAP timelines, build scripts, prompts, PNGs, WAVs and geometry records. HyperFrames version used for most exports:0.8.226. To preview/render those projects with a compatible installation:

```bash
npx hyperframes preview projects/paris-citywalk-v2
npx hyperframes render projects/paris-citywalk-v2 --output rendered/paris-historical.mp4 --fps 24
```

Check the installed CLI's help when syntax/version differs. These commands may use that application's account/plan; they are not required for the portable route. The exported historical MP4s are the exact original files. Host-specific proprietary fonts are omitted from editable sources and replaced by generic-family fallbacks; their typography can differ on another machine. SmileySans is included with OFL. Read each historical `REVIEW.md` or production note before editing. Earlier London/Paris algorithms intentionally retain rejected limb scaling as historical evidence; **use current gait instructions and Paris v2 for new work**.

## Inspect and make previews

```bash
python3 -m pip install Pillow
python3 scripts/inspect_video.py rendered/example.mp4 --out rendered/inspection --start 3 --end 5 --fps 12
python3 scripts/make_gif.py rendered/example.mp4 rendered/example.gif
python3 scripts/verify_package.py
```

Contact sheets are visual analysis, not audio review. GIF reduces frame rate/colour/resolution, has no audio, and is not a mastering format. Original MP4 remains the quality reference.
