# Capability routes and installation

The creative workflow is tool-neutral. “Any image-capable agent can use it” means it can follow the planning, reference use, prompt, generation and review instructions; video encoding additionally needs an execution or editing surface.

| Available capabilities | Useful route | Honest delivery |
|---|---|---|
| Image generator with reference editing and alpha | Generate master → pose edits → individual objects | PNG assets + manifest + storyboard; render if a compositor exists |
| Reference editing but no alpha | Generate against a separable background; use an available segmentation tool or built-in background removal; inspect edges | Cutouts when segmentation exists; otherwise intentional rectangular photo cards |
| Text-to-image only, no identity reference | Design new consistent fictional subject; retain supplied photo as a static crop if identity must stay exact | Do not promise exact identity from a text description |
| Images + Node + Chromium/Puppeteer + FFmpeg | Included Canvas renderer or an installed framework | MP4 + GIF + editable JSON/HTML |
| Images + a timeline editor | Import PNGs, align anchors, hold frames, keyframe each layer; export with editor | Equivalent result with that editor's project |
| Images + FFmpeg only | Simple overlay/crop/concat or provide prepared timeline; complex compositing needs a renderer | Scope to supportable motion; do not silently flatten the whole film |
| No execution/editor | Design and generate the complete asset pack and explicit timed recipe | State which render step remains; no fabricated MP4 link |
| No image generation, existing adequate assets | Reuse assets; do not require regeneration unnecessarily | Compose available material; flag missing action frames |

## Install as an agent skill

Clone or download this repository. The **root directory is the skill**: `SKILL.md`, `references/`, `scripts/`, `templates/` and examples. Any agent can be told to read `SKILL.md`; no special slash command is required.

For Codex, place/clone the folder at `~/.codex/skills/paper-cutout-story`. For Claude Code use `~/.claude/skills/paper-cutout-story`, where supported by the local version. For other agents, use their documented skill/instruction discovery directory, or attach/link `SKILL.md` directly. Agent-specific discovery changes over time; reading the entrypoint works independently of it.

A lightweight install needs `SKILL.md`, `references/`, `agents/`, `scripts/` and `templates/`. The showcase media are optional for running new work; the sample JSON additionally needs its referenced assets. The full clone contains all showcase data.

## Generator adapter

Record actual capabilities before a batch: reference images accepted? edits? true alpha? size control? result saved locally or URL? cost/limits? Do not infer that parameters named `transparent_background`, `num_last_images_to_include` or `referenced_image_paths` exist outside the original host.

Use the agent's native generator first when appropriate. If the user chooses another service, preserve the same visual contract in that service's syntax. Supply master/reference image, requested delta, locked features, canvas/anchor guide and rejection conditions. Store the final tool-neutral prompt plus provider metadata when available, never credentials.
