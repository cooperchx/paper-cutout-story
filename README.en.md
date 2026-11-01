# Paper Cutout Story

A tool-neutral agent skill for photographic paper-cut collage films: consistent character pose loops, staged city/lifestyle fragments, paper typography and image-led transitions.

[Read the skill](SKILL.md) · [Chinese guide and showcased GIFs](README.md) · [All films](docs/gallery.md) · [Images](docs/assets.md)

Give any image-capable agent this repository's `SKILL.md`, your reference subject, setting, duration, aspect, copy and delivery format. It can produce an asset pack and explicit timeline. Encoded video additionally requires an editor or browser/FFmpeg runtime; the optional local renderer is included.

```bash
git clone https://github.com/cooperchx/paper-cutout-story.git
cd paper-cutout-story
npm install
node scripts/render.mjs examples/paris-portable.json rendered/paris.mp4
python3 scripts/make_gif.py rendered/paris.mp4 rendered/paris.gif
```

Requirements for that optional render path: Node22.12+, Chromium (installed by Puppeteer), Python3 for the GIF/inspection helpers, and FFmpeg on PATH. A browser-only preview needs no Puppeteer: serve the repository and open `templates/player.html`.

The archive contains 11 original MP4s and matching GIFs, 10 production-stage projects, 75 unique images and 6 supplied reference images. Earlier rejected attempts are labelled and explained. The original projects used HyperFrames/GSAP; those are not required by the skill or the independent Canvas template. The portable example is a different renderer demonstration, not a pixel-identical historical export.

Read [capabilities](references/capabilities.md), [gait repair](references/gait.md), [rendering](references/rendering.md) and [quality](references/quality.md) as needed. Original code/instructions: MIT. Example images, fonts and third-party runtime terms: [attribution](ATTRIBUTION.md).
