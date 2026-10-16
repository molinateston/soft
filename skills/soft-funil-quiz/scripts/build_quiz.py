#!/usr/bin/env python3
"""Build an offline quiz from the validated JSON contract."""
import argparse,json,shutil
from pathlib import Path
from urllib.parse import urlparse
from validate_quiz import validate
ap=argparse.ArgumentParser();ap.add_argument('config',type=Path);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
c=json.loads(args.config.read_text());errors=validate(c)
if errors:raise SystemExit('\n'.join(errors))
args.out.mkdir(parents=True,exist_ok=True)
shutil.copytree(Path(__file__).resolve().parent.parent/'assets/fonts',args.out/'fonts',dirs_exist_ok=True)
# Never interpolate configuration as JavaScript or HTML executable content.
payload=json.dumps(c,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
html=(Path(__file__).resolve().parent.parent/'assets/quiz-template.html').read_text().replace('__QUIZ_CONFIG__',payload)
(args.out/'index.html').write_text(html);(args.out/'config.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
resources=[]
for d in [c.get('destination'),c.get('ineligible',{}).get('destination')]+[p.get('destination') for p in c['profiles']]:
    if d and d.get('url'):resources.append(d['url'])
for m in [c.get('resultMedia')]+[p.get('media') for p in c['profiles']]+[s.get('media') for s in c['steps']]:
    if m:
        resources.extend(m[k] for k in ['src','poster','captions'] if m.get(k))
for u in set(resources):
    if urlparse(u).scheme:continue
    rel=Path(urlparse(u).path);src=args.config.parent/rel;dst=args.out/rel
    if not src.is_file():raise SystemExit(f'Missing local resource: {src}')
    if src.resolve()!=dst.resolve():dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
public=[]
for key in ['title','brand','offer','tieText']:public.append(c[key])
if c.get('qualificationTitle'):public.append(c['qualificationTitle'])
for s in c['steps']+c.get('qualification',[]):
    public.extend(str(s[k]) for k in ['title','description','body','label'] if s.get(k));public.extend(o['label'] for o in s.get('options',[]))
for p in c['profiles']:public.extend(p[k] for k in ['title','body','recommendation'])
for m in [c.get('resultMedia')]+[p.get('media') for p in c['profiles']]+[s.get('media') for s in c['steps']]:
    if m:public.extend(m[k] for k in ['title','transcript','absentText'] if m.get(k))
for d in [c.get('destination'),c.get('ineligible',{}).get('destination')]+[p.get('destination') for p in c['profiles']]:
    if d:public.extend(d[k] for k in ['label','pendingText'] if d.get(k))
if c.get('ineligible'):public.append(c['ineligible']['message'])
if c['capture']['mode']=='local':public.extend(c['capture'][k] for k in ['title','purpose','label','consent'])
(args.out/'copy.md').write_text('\n\n'.join(public)+'\n')
print(args.out.resolve()/'index.html')
