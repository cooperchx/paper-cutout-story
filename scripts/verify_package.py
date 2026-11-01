#!/usr/bin/env python3
"""Validate local catalogs, media durations, asset links and public-package hygiene."""
from pathlib import Path
import json,hashlib,re,subprocess,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
errors=[];report={}
def fail(s):errors.append(s)
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
imgs=json.loads((ROOT/'assets/catalog.json').read_text())
for a in imgs:
 f=ROOT/a['path']
 if not f.is_file() or sha(f)!=a['sha256']:fail('Image missing/hash mismatch: '+a['path'])
report['catalog_images']=len(imgs)
media=json.loads((ROOT/'media/catalog.json').read_text())
if not shutil.which('ffprobe'):fail('ffprobe unavailable: media duration verification requires it')
else:
 for m in media:
  for key in ['path','gif']:
   f=ROOT/m[key]
   if not f.is_file():fail('Missing '+str(f));continue
   if key=='path' and sha(f)!=m['sha256']:fail('Video hash mismatch '+m['id'])
   data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(f)]))
   if abs(float(data['format']['duration'])-m['duration'])>.2:fail('Duration mismatch '+m[key])
report['videos']=len(media)
# Root, operative references and authored docs must have valid relative Markdown links.
for f in [ROOT/'README.md',ROOT/'README.en.md',ROOT/'SKILL.md',ROOT/'ATTRIBUTION.md',* (ROOT/'references').glob('*.md'),* (ROOT/'docs').glob('*.md')]:
 text=f.read_text();text=re.sub(r'```.*?```','',text,flags=re.S)
 for link in re.findall(r'\]\(([^)]+)\)',text):
  link=link.split('#')[0].strip('<>')
  if not link or re.match(r'\w+://',link):continue
  if not (f.parent/link).exists():fail(f'Broken documentation link {f.relative_to(ROOT)} -> {link}')
# Actual HTML asset references, including root-relative subcomposition resolution.
for project in (ROOT/'projects').iterdir():
 for f in project.rglob('*.html'):
  text=f.read_text()
  for ref in re.findall(r'(?:src|href)=["\'](assets/[^"\']+)["\']',text):
   if not (project/ref).is_file():fail(f'Missing project asset {project.name}/{ref}')
# Portable manifests resolve paths relative to manifest, not working directory.
for f in (ROOT/'examples').glob('*.json'):
 s=json.loads(f.read_text());paths=[]
 for a in s['assets'].values():paths+=a.get('frames',[a.get('src')])
 if s.get('audio'):paths.append(s['audio'])
 for q in paths:
  if not q or not (f.parent/q).is_file():fail('Missing manifest asset '+str(q))
 for a in s['assets'].values():
  if 'holds' in a and (len(a['holds'])!=len(a['frames']) or any(not isinstance(n,int) or n<=0 for n in a['holds'])):fail('Invalid pose hold schedule')
for f in ROOT.rglob('*'):
 if not f.is_file() or any(x in ['.git','node_modules','.hyperframes'] for x in f.parts):continue
 if f.stat().st_size>=100*1024*1024:fail('File exceeds 100MiB '+str(f.relative_to(ROOT)))
 if f.suffix.lower() in ['.md','.json','.py','.html','.js','.mjs','.cjs','.yaml'] and f.name not in ['gsap.min.js','verify_package.py']:
  text=f.read_text()
  if re.search(r'/Users/[^\s/]+/|/var/folders/|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{30,}',text):fail('Private path/credential-like string '+str(f.relative_to(ROOT)))
report['errors']=errors;report['ok']=not errors
print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
