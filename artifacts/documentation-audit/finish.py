from pathlib import Path
import ast, hashlib, inspect, json, os, re, sys
from urllib.parse import unquote
R=Path(__file__).resolve().parents[2]; D=R/'docs'
sys.dont_write_bytecode=True; sys.path.insert(0,str(R/'services/api'))
changes=json.loads((R/'artifacts/documentation-audit/changes.json').read_text())
moves=changes['moves']; changed=set(changes['changed_paths'])
def rel(s,t): return os.path.relpath(R/t,(R/s).parent).replace('\\','/')
def link(s,t,label=None): return f'[{label or Path(t).stem}]({rel(s,t)})'
def write(p,s):
    (R/p).parent.mkdir(parents=True,exist_ok=True); (R/p).write_text(s.rstrip()+'\n',encoding='utf-8'); changed.add(p)
API='docs/01-architecture/18-api-contracts.md'; ROAD='docs/09-planning/FUTURE_SPRINT_ROADMAP.md'
def flatten(routes):
    for rt in routes:
        if hasattr(rt,'original_router'): yield from flatten(rt.original_router.routes)
        else: yield rt
script=(R/'artifacts/documentation-audit/reorganize.py').read_text(encoding='utf-8')
piece=script[script.index('from ppm_api.main import create_app'):script.index("for module in ['identity_tables'")]
piece=piece.replace("write('docs/10-reference/history/API_INVENTORY_PRE_AUDIT.md',rewrite(original['docs/18-api-contracts.md'],'docs/18-api-contracts.md','docs/10-reference/history/API_INVENTORY_PRE_AUDIT.md'))",'')
piece=piece.replace('for rt in app.routes:', 'for rt in flatten(app.routes):')
exec(piece)
changes['routes']=route_count
assert route_count==sum(len([m for m in op if m in {'get','post','patch','put','delete','options','head'}]) for op in schema['paths'].values())

# Remove repeated identical checkpoint addenda from an interrupted/resumed write.
for p in (D/'02-learning').rglob('*.md'):
    s=p.read_text(encoding='utf-8'); marker='\n\n## Source-reviewed Sprint 8.1 update — 9 October 2026'
    chunks=s.split(marker)
    if len(chunks)>2: write(p.relative_to(R).as_posix(),chunks[0]+marker+chunks[-1])
for name in ['API_INVENTORY_PRE_AUDIT.md','DATABASE_DICTIONARY_PRE_AUDIT.md','CODE_INDEX_PRE_AUDIT.md']:
    p='docs/10-reference/history/'+name; s=(R/p).read_text(encoding='utf-8'); pos=s.find('\n')
    write(p,s[:pos]+'\n\n**ARCHIVED pre-audit snapshot.** Use the current architecture/reference inventory; this retained snapshot is not a competing canonical guide.\n'+s[pos:])

# Replace noisy SQLAlchemy reprs with actual check expressions for useful schema lookup.
from ppm_api.database import Base
p='docs/01-architecture/DATABASE-DICTIONARY.md'; s=(R/p).read_text(encoding='utf-8')
for t in Base.metadata.tables.values():
    start=s.find('## '+t.name+'\n'); end=s.find('\n## ',start+1)
    if start<0: continue
    segment=s[start:end if end>=0 else len(s)]
    expressions='; '.join(str(c.sqltext) for c in t.constraints if c.__class__.__name__=='CheckConstraint') or 'See referential/primary/unique definitions and migrations'
    segment=re.sub(r'Metadata constraints: .*',lambda _: 'Metadata check expressions: '+expressions,segment)
    s=s[:start]+segment+s[end if end>=0 else len(s):]
write(p,s)

# Narrow the advertised host-safe command based on the observed host test limitation.
p='docs/04-testing/TESTING_STRATEGY.md'; s=(R/p).read_text(encoding='utf-8')
s=s.replace('pytest -q -m "not integration"','pytest tests/test_ingestion_mapping.py tests/test_config_storage.py -q')
s=s.replace('`pyproject.toml` config; `tests/test_config_storage.py`, mapping and pure domain cases; no normal DB','Explicit pure mapping/config/storage tests; no normal DB. The broad marker-selected suite encountered errors/hung in this host and was interrupted; use guarded Compose for wider acceptance.')
write(p,s)

# Collect Markdown path/anchor errors, excluding frozen reference copies from mutation.
frozen=lambda p: p.startswith('docs/source/') or (p.startswith('docs/prompts/') and not p.endswith('/MASTER.md'))
def links(s):
    s=re.sub(r'```[^\n]*\n.*?```','',s,flags=re.S)
    return re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)',s)
def slug(s):
    s=s.lower(); s=re.sub(r'[`*_~]','',s); s=re.sub(r'[^\w\- ]','',s); return s.replace(' ','-')
def anchors(path):
    seen={}; result=set()
    for h in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',path.read_text(encoding='utf-8-sig'),re.M):
        a=slug(h); num=seen.get(a,0); seen[a]=num+1; result.add(a if not num else a+'-'+str(num))
    return result
def check():
    bad=[]; skipped=[]; count=0
    for p in [R/'README.md']+list(D.rglob('*.md')):
        rp=p.relative_to(R).as_posix()
        for u in links(p.read_text(encoding='utf-8-sig')):
            u=u.split(' "',1)[0].strip('<>'); path,sep,anchor=u.partition('#')
            if re.match(r'^[a-zA-Z][\w+.-]*:',path): continue
            count+=1; dest=p.parent/unquote(path) if path else p
            reason=None
            if not dest.exists(): reason='missing target'
            elif sep and anchor and dest.suffix=='.md' and unquote(anchor) not in anchors(dest): reason='missing anchor'
            if reason:
                record={'document':rp,'link':u,'reason':reason}
                (skipped if frozen(rp) else bad).append(record)
    return count,bad,skipped
count,bad,skipped=check()
(R/'artifacts/documentation-audit/link-errors.json').write_text(json.dumps({'checked':count,'errors':bad,'frozen_reference_errors':skipped},indent=2),encoding='utf-8')
changes['changed_paths']=sorted(changed)
(R/'artifacts/documentation-audit/changes.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print(json.dumps({'current_routes':route_count,'links_checked':count,'errors':len(bad),'frozen_reference_errors':len(skipped),'first_errors':bad[:20]},indent=2))
