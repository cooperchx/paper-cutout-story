#!/usr/bin/env python3
"""Create bounded video contact sheets. Dependencies: ffmpeg, ffprobe, Pillow.
Labels are requested sampling times, not frame-accurate edit points. No audio analysis.
"""
import argparse
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path


def positive(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError('must be finite and positive')
    return number


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('video', type=Path)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--start', type=float, default=0)
    p.add_argument('--end', type=positive)
    p.add_argument('--fps', type=positive, default=2)
    p.add_argument('--width', type=int, default=180)
    p.add_argument('--columns', type=int, default=6)
    p.add_argument('--per-sheet', type=int, default=30)
    p.add_argument('--max-samples', type=int, default=240)
    a = p.parse_args()
    if not a.video.is_file():
        p.error('video does not exist')
    if not math.isfinite(a.start) or a.start < 0:
        p.error('--start must be finite and nonnegative')
    if not 64 <= a.width <= 1000 or not 1 <= a.columns <= 12:
        p.error('width must be 64–1000 and columns 1–12')
    if not 1 <= a.per_sheet <= 120 or not 1 <= a.max_samples <= 5000:
        p.error('per-sheet must be 1–120 and max-samples 1–5000')
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            p.error(f'{tool} is required on PATH')
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        p.error('Pillow is required: install it in your chosen Python environment')
    try:
        metadata = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json',
            str(a.video.resolve())], text=True))
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        p.error(f'ffprobe failed: {exc}')
    videos = [s for s in metadata['streams'] if s['codec_type'] == 'video'
              and not s.get('disposition', {}).get('attached_pic')]
    if not videos:
        p.error('no video stream found')
    stream = videos[0]
    duration = float(stream.get('duration') or metadata['format']['duration'])
    end = min(a.end if a.end is not None else duration, duration)
    if a.start >= end:
        p.error('start must be before end of selected video interval')
    count = math.ceil((end - a.start) * a.fps - 1e-9)
    if count > a.max_samples:
        p.error(f'{count} samples exceeds max-samples; lower fps, narrow interval or increase cap')
    if a.out.exists() and any(a.out.iterdir()):
        p.error('output directory must be empty; choose a fresh directory')
    a.out.mkdir(parents=True, exist_ok=True)
    manifest = []
    # Accurate seeking for each sample avoids labels drifting due to fps filter phases.
    with tempfile.TemporaryDirectory(prefix='paper-cutout-') as tmp:
        for i in range(count):
            requested = a.start + i / a.fps
            dst = Path(tmp) / f'{i:05d}.jpg'
            cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin',
                   '-ss', f'{requested:.9f}', '-i', str(a.video.resolve()),
                   '-map', f'0:{stream["index"]}', '-frames:v', '1',
                   '-vf', f'scale={a.width}:-1', '-q:v', '3', str(dst)]
            subprocess.run(cmd, check=True)
            if not dst.is_file():
                raise RuntimeError(f'No decoded frame near {requested:.3f}s')
            manifest.append({'index': i, 'requested_time_seconds': round(requested, 6),
                             'sheet': f'contact-{i // a.per_sheet + 1:02d}.jpg',
                             'cell': i % a.per_sheet})
        frames = sorted(Path(tmp).glob('*.jpg'))
        with Image.open(frames[0]) as first:
            cell_h = first.height + 24
        for offset in range(0, count, a.per_sheet):
            group = frames[offset:offset + a.per_sheet]
            rows = math.ceil(len(group) / a.columns)
            canvas = Image.new('RGB', (a.width * a.columns, cell_h * rows), '#222222')
            draw = ImageDraw.Draw(canvas)
            for j, path in enumerate(group):
                x, y = j % a.columns * a.width, j // a.columns * cell_h
                with Image.open(path) as frame:
                    canvas.paste(frame, (x, y))
                t = manifest[offset + j]['requested_time_seconds']
                draw.text((x + 5, y + cell_h - 19), f'~{t:.3f}s', fill='white')
            canvas.save(a.out / f'contact-{offset // a.per_sheet + 1:02d}.jpg', quality=90)
    # Do not retain the source's private absolute path in a shareable report.
    metadata.get('format', {}).pop('filename', None)
    report = {'source_name': a.video.name, 'metadata': metadata,
              'sampling': {'start': a.start, 'end': end, 'fps': a.fps,
                           'note': 'Requested times; not exact cut points. Audio not analyzed.'},
              'frames': manifest}
    (a.out / 'inspection.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'samples': count, 'sheets': math.ceil(count / a.per_sheet),
                      'output': str(a.out.resolve())}, ensure_ascii=False))


if __name__ == '__main__':
    main()
