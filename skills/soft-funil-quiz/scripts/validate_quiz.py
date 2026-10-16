#!/usr/bin/env python3
"""Validate the portable quiz contract without requiring a fictional owner profile."""
import json,sys,math
from urllib.parse import urlparse
from pathlib import PurePosixPath
KINDS={'single','multi','number','text','info','video'}
def safe_url(u,media=False):
    if not isinstance(u,str) or not u or any(ord(c)<32 for c in u) or '\\' in u:return False
    p=urlparse(u)
    if p.scheme:return p.scheme=='https' and bool(p.netloc) and not p.username and not p.password
    return not u.startswith(('/','#','?')) and '..' not in PurePosixPath(p.path).parts and bool(p.path)
def validate(c):
    errors=[]
    def need(ok,msg):
        if not ok:errors.append(msg)
    if not isinstance(c,dict):return ['configuration must be an object']
    need(c.get('version')==1,'version must be 1')
    need(c.get('route') in ['checkout','meeting'],'route must be checkout or meeting')
    for k in ['title','brand','offer','tieText']:need(isinstance(c.get(k),str) and bool(c[k].strip()),f'{k} must be nonempty text')
    profiles=c.get('profiles',[]);steps=c.get('steps',[]);qual=c.get('qualification',[])
    if not isinstance(profiles,list) or not isinstance(steps,list) or not isinstance(qual,list):return errors+['profiles, steps and qualification must be arrays']
    need(bool(profiles) and bool(steps),'profiles and steps required')
    if any(not isinstance(s,dict) for s in profiles+steps+qual):return errors+['entries must be objects']
    pids=[p.get('id') for p in profiles];ids=[s.get('id') for s in steps+qual]
    need(all(isinstance(x,str) and x and x not in {'__proto__','constructor','prototype'} for x in ids+pids),'ids must be safe nonempty strings')
    need(len(set(ids))==len(ids),'duplicate question/step id');need(len(set(pids))==len(pids),'duplicate profile id')
    need(isinstance(c.get('tieOrder'),list) and set(c.get('tieOrder',[]))==set(pids) and len(c.get('tieOrder',[]))==len(pids),'tieOrder must list each profile once')
    questions={}
    def cond(v,known,where):
        if v is None:return
        if not isinstance(v,dict):errors.append(f'{where}: condition must be object');return
        q=known.get(v.get('question'));need(q is not None,f'{where}: condition must reference previous/known question')
        op=v.get('op');need(op in ['eq','ne','includes','gte','lte','answered'],f'{where}: unknown operator')
        if not q:return
        kind=q['type'];need(op=='answered' or (op in ['gte','lte'] and kind=='number') or (op=='includes' and kind=='multi') or (op in ['eq','ne'] and kind in ['single','text','number']),f'{where}: operator incompatible with question type')
        if kind in ['single','multi'] and op!='answered':need(v.get('value') in [o.get('id') for o in q.get('options',[])],f'{where}: unknown option in condition')
        if op in ['gte','lte']:need(isinstance(v.get('value'),(int,float)) and not isinstance(v.get('value'),bool),f'{where}: comparison needs number')
    def media(m,where):
        if not m:return
        if not isinstance(m,dict):errors.append(f'{where}: media must be object');return
        need(bool(m.get('title')) and bool(m.get('transcript')),f'{where}: media needs title and text alternative')
        for k in ['src','poster','captions']:
            if m.get(k):need(safe_url(m[k],True),f'{where}: unsafe {k}')
    def destination(d,where):
        if not isinstance(d,dict):errors.append(f'{where}: destination required');return
        need(bool(d.get('label')),f'{where}: destination label required')
        need(bool(d.get('url')) != bool(d.get('pendingText')),f'{where}: use url OR pendingText')
        if d.get('url'):need(safe_url(d['url']),f'{where}: unsafe destination URL')
    for s in steps:
        sid=s.get('id');t=s.get('type');need(t in KINDS,f'{sid}: invalid type');need(bool(s.get('title')),f'{sid}: title required');need(bool(s.get('purpose')),f'{sid}: purpose required')
        cond(s.get('when'),questions,str(sid))
        if t in ['single','multi']:
            options=s.get('options',[]);need(isinstance(options,list) and len(options)>1,f'{sid}: needs options')
            if not isinstance(options,list) or any(not isinstance(o,dict) for o in options):errors.append(f'{sid}: invalid options');continue
            oids=[o.get('id') for o in options];need(all(isinstance(x,str) and bool(x) for x in oids) and len(set(oids))==len(oids),f'{sid}: unique option ids required')
            for o in options:
                need(bool(o.get('label')),f'{sid}: label required');scores=o.get('scores',{})
                if not isinstance(scores,dict):errors.append(f'{sid}: scores must be object');continue
                for p,n in scores.items():need(p in pids and isinstance(n,(int,float)) and not isinstance(n,bool) and math.isfinite(n),f'{sid}: invalid score')
            if t=='multi':need(1<=s.get('minSelect',1)<=s.get('maxSelect',len(options))<=len(options),f'{sid}: invalid selection bounds')
        if t=='number':need(isinstance(s.get('min'),(int,float)) and isinstance(s.get('max'),(int,float)) and s['min']<=s['max'] and bool(s.get('unit')),f'{sid}: number needs min/max/unit')
        if t=='video':media(s.get('media'),str(sid));need(bool(s.get('media')),f'{sid}: missing media state')
        if t in ['single','multi','number','text']:questions[sid]=s
    for q in qual:
        need(q.get('type')=='single' and bool(q.get('title')) and bool(q.get('purpose')),f'{q.get("id")}: qualification is single with title/purpose')
        opts=q.get('options',[]);need(isinstance(opts,list) and len(opts)>1,f'{q.get("id")}: qualification options required')
        if isinstance(opts,list):need(all(isinstance(o,dict) and bool(o.get('id')) and bool(o.get('label')) and not o.get('scores') for o in opts),f'{q.get("id")}: invalid qualification options');need(len({o.get('id') for o in opts})==len(opts),f'{q.get("id")}: duplicate qualification options')
        questions[q.get('id')]=q
    media(c.get('resultMedia'),'resultMedia')
    for p in profiles:
        for k in ['title','body','recommendation']:need(bool(p.get(k)),f'{p.get("id")}: {k} required')
        if p.get('destination'):destination(p['destination'],p.get('id'))
        if p.get('media'):media(p['media'],p.get('id'))
    destination(c.get('destination'),'default')
    capture=c.get('capture',{});need(isinstance(capture,dict) and capture.get('mode') in ['none','local'],'base supports capture none/local only')
    if isinstance(capture,dict) and capture.get('mode')=='local':
        for k in ['title','purpose','label','consent']:need(bool(capture.get(k)),f'capture {k} required')
        need(capture.get('field') in ['email','phone'],'capture field must be email/phone')
    rules=c.get('eligibility',{}).get('all',[])
    need(isinstance(rules,list),'eligibility.all must be array')
    if isinstance(rules,list):
        for rule in rules:cond(rule,questions,'eligibility')
    if c.get('route')=='meeting':need(bool(rules),'meeting requires explicit eligibility')
    if rules:
        need(isinstance(c.get('ineligible'),dict) and bool(c['ineligible'].get('message')),'ineligible message required')
        destination(c.get('ineligible',{}).get('destination'),'ineligible')
    return errors
if __name__=='__main__':
    try: c=json.load(open(sys.argv[1]));errors=validate(c)
    except (OSError,ValueError,IndexError,TypeError,KeyError,AttributeError) as e:errors=[str(e)]
    for e in errors:print('ERROR:',e)
    if not errors:print('OK: contract valid; browser and evidence review still required')
    sys.exit(bool(errors))
