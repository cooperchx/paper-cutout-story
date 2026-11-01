# Review — Paris Citywalk

9-second, 1080×1920, 24 fps film. Deliberate sequence: warm editorial outfit close-up → denim-paper diagonal street walk → collected postcard. A single Paris photo postcard covers each scene cut; the second shrinks into the final composition. Four identity-based pose assets alternate A/P/B/Q. Full-body, cropped portrait, waist detail and coffee detail vary the scale without changing the outfit.

Measured: HyperFrames check passed, zero runtime/layout/motion errors; all 43 contrast checks passed. Transition coverage source crop alpha is recorded in coverage-check.json and made opaque in the compositor. Inspected beat, phone-width and both seam sheets. Corrected portrait crop overflow, the registered lower-leg overlap, and matching postcard handoff origin. Confirmed both cuts are hidden beneath the postcard. Sound is synthesized locally; waveform/level and stream presence are measured, not heard.

Kept warning: the small secondary “A little detour.” label briefly measures 27 px during its scale animation versus the 28 px floor. Main title and story reading do not depend on this label. The duplicate postcard asset is deliberate: one physical visual motif performs two separate transitions.

Weakest shot: the bookstall vignette appears briefly behind the full-body street portrait. The final collected spread repeats it at a larger readable scale. A longer cut could dedicate a separate bookseller close-up, but the requested 8–10 seconds prioritizes three distinct compositions.

Visual limitation: walking is a four-photo paper-stop-motion cycle, not interpolated live-action footage. Architecture is generated Paris-inspired photographic collage, not sourced documentary photography.

Final encoded-file verification: H.264 1080×1920, 24 fps, 216 frames, 9.000 s; AAC audio 9.000 s. Extracted and inspected 12 encoded frames covering the opening, a full A/P/B/Q cycle plus repeat, both covered cuts, postcard handoff and last frame. Audio mean −22.4 dBFS, maximum −5.9 dBFS; not listened to. Output 16,280,223 bytes.
