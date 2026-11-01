# London Citywalk

workflow: general-video
flow: autonomous

15 seconds · 1080 × 1920 · 24 fps. Follow-on to Shanghai Citywalk, built as a separate London project so earlier versions remain intact. The user requests final video delivery; no intermediate approval gate.

Creative sentence: A woman in acid-lime knitwear takes a paper walk through London, then steps into the pages of a fashion editorial before returning to a quiet street corner.

Identity/outfit reference: user image 1. Composition reference only: image 2, large bust plus smaller full-body stickers and detail crops. Do not borrow the identity or clothing from image 2.

Palette: acid lime #d6ed43, chocolate #352822, warm ivory #eee8d8, cool newsprint #d6d8d5, oxblood #792c2d. Buildings muted so the outfit is the colour anchor. Paper fibres and ink texture belong to the paper, print and edges, never noisy overlays on the face.

Three distinct paper backgrounds and compositions; each transition is ONE sticker, not a swarm. Full-body cycle uses exactly two generated A/B walking photographs, alternating left and right footfall every 8 frames at 24 fps. Carrying arm and bag change together in the source photographs. No joint puppet. Types: full-body walking sticker, large waist-up portrait, small full-body echoes, glasses crop, sneaker crop, and a waist-up crop of the walking sequence. All have fine irregular ivory edges and restrained shadows; independent low amplitude 8 Hz paper sway.

Main title: London Citywalk. English editorial captions only; if Chinese is added later use supplied SmileySans-Oblique font.

Built-in image generation used for 8 separate photographic assets. All prompts and original paths recorded in generation-manifest.json. No text-to-video generation. Typography, newspaper backgrounds and motion are native compositing. Both transitions use photographic image assets: a bus and a London-themed newspaper.

CLI usage command unavailable in installed 0.7.103; usage unknown. Existing local render path retained. Transition catalog returned no suitable entries. Bespoke alpha-verified cutout wipe needed.

Revision 3: user explicitly requests two generated walking images. Face and torso stay registered; image B lower body mapping adjusts its floor height by 43 pixels. Paper outline and tiny whole-sticker bob are compositor effects.


Revision 4 supersedes the two-frame motion: replace B with an opposite-depth stride (foreground leg back, far leg forward) and add passing photograph C, knees close together, single support. Source order A-C-B-C, six frames each at24fps, one-second cycle. Lower source image mapping B1.117 and C1.015 aligns feet. Transitions unchanged photographic bus/newspaper.
