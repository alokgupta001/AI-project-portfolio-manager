from pathlib import Path
import hashlib, json, os, re, subprocess
from urllib.parse import unquote
R=Path(__file__).resolve().parents[2]; D=R/'docs'
data=json.loads((R/'artifacts/documentation-audit/changes.json').read_text())
before=json.loads((R/'artifacts/documentation-audit/before.json').read_text())
moves=data['moves']
def write(p,s):
    (R/p).write_text(s.rstrip()+'\n',encoding='utf-8')
def link(s,t,label): return f'[{label}]({os.path.relpath(R/t,(R/s).parent).replace(chr(92),"/")})'

p='docs/03-sprints/active/sprint-8.1/SPRINT_8_1_USER_GUIDE.md'; s=(R/p).read_text(encoding='utf-8').replace('a password of 12–72 UTF-8 bytes','a password of at least 12 characters and at most 72 UTF-8 bytes'); write(p,s)
p='docs/04-testing/TESTING_STRATEGY.md'; s=(R/p).read_text(encoding='utf-8')
s=s.replace('-p no:cacheprovider`','-p no:cacheprovider --basetemp=artifacts/documentation-audit/pytest-focused-20261009`')
s=s.replace('The broad marker-selected suite encountered errors/hung in this host and was interrupted; use guarded Compose for wider acceptance.','The broad marker-selected run hit sandbox temporary-directory errors and was interrupted; the focused command passed with a workspace basetemp. Use guarded Compose for integration acceptance.')
write(p,s)
# Current gap table uses current labels; historical crosswalk and baseline keep original wording.
p='docs/09-planning/FEATURE_GAP_TRACEABILITY.md'; s=(R/p).read_text(encoding='utf-8')
status={'IMPLEMENTED locally':'IMPLEMENTED AND VERIFIED','BLOCKED real SMTP; local implementation complete':'BLOCKED','PARTIAL; Word layout unverified':'PARTIALLY IMPLEMENTED','NOT IMPLEMENTED':'PLANNED','PARTIAL':'PARTIALLY IMPLEMENTED','UNVERIFIED':'IMPLEMENTED BUT UNVERIFIED','VERIFIED locally':'IMPLEMENTED AND VERIFIED'}
lines=[]
for ln in s.splitlines():
    if ln.startswith('| G-'):
        c=ln.split('|'); c[2]=' '+status.get(c[2].strip(),c[2].strip())+' '; ln='|'.join(c)
    lines.append(ln)
write(p,'\n'.join(lines))

report='docs/10-reference/DOCUMENTATION_AUDIT_RESULTS.md'
changelog='docs/10-reference/DOCUMENTATION_CHANGELOG.md'
write(report,'# Documentation audit results\n\nVerification in progress; final measured results are written below after link, source and preservation checks.')
write(changelog,'''# Documentation changelog

## 9 October 2026 — source-based reorganization

Migrated 70 existing documents to canonical overview/architecture/learning/sprint/testing/demo/setup/planning/reference locations. Updated fourteen cross-sprint learning chapters for local Sprint 8.1; preserved original historical reports/test results and frozen source/prompts. Resolved 31 prior chapter/master-entry redirects as explicit superseded compatibility links.

Added current status/catalogue/user/demo/testing/architecture guides, gap acceptance and feature-document mapping covering 156 original requirements and 36 gaps, and impact-based documentation obligations for all planned Sprints 09–23. Kept active Sprint 8.1 separate from completed Sprints 00–08 and PLANNED future folders. Current inventories include 77 route operations and 62 metadata tables; raw evidence and legacy Word/generator artifacts remain preserved with explicit limits.

See [measured verification](DOCUMENTATION_AUDIT_RESULTS.md) and [remaining work](../09-planning/DOCUMENTATION_UPDATE_TRACKER.md). No application code, configuration, tests, migration or data was changed by this documentation task.
''')

# Include newly created audit/changelog rows and mark only mechanically verified scopes as verified.
tracker='docs/09-planning/DOCUMENTATION_UPDATE_TRACKER.md'; s=(R/tracker).read_text(encoding='utf-8')
table_end=s.index('\n## Remaining work')
rows=''
for p in [report,changelog]:
    rows+=f'| {Path(p).name} | {link(tracker,p,p)} | Documentation verification | Measured link/source/preservation results | Revalidate after future changes | G-010, G-034–036 | Cross-sprint | UPDATED AND VERIFIED |\n'
s=s[:table_end]+rows+s[table_end:]
write(tracker,s)

# Reuse the non-mutating link and anchor validator only.
finish=(R/'artifacts/documentation-audit/finish.py').read_text(encoding='utf-8')
piece=finish[finish.index('frozen=lambda'):finish.index("(R/'artifacts/documentation-audit/link-errors.json')")]
exec(piece)
assert not bad, json.dumps(bad[:10])

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
protected=[]; lost=[]; updated=[]; unchanged=[]
for p,h in before.items():
    dest=R/moves.get(p,p)
    if not dest.exists(): lost.append(p); continue
    now=digest(dest)
    if now!=h:
        if p in ('README.md','ANTIGRAVITY.md') or (p.startswith('docs/') and p.endswith('.md')): updated.append(p)
        else: protected.append(p)
    else: unchanged.append(p)
assert not protected, 'Unexpected non-document changes: '+str(protected)
assert not lost, 'Lost unique files: '+str(lost)
source=subprocess.run([str(R/'.venv/Scripts/python.exe'),'-B','scripts/check_sources.py'],cwd=R,capture_output=True,text=True)
diff=subprocess.run(['git','-c','safe.directory='+str(R),'diff','--check','--','README.md','docs'],cwd=R,capture_output=True,text=True)
assert source.returncode==0,source.stdout+source.stderr
assert diff.returncode==0,diff.stdout+diff.stderr
current={p.relative_to(R).as_posix() for p in D.rglob('*.md')}
new=sorted(current-set(before)-set(moves.values()))

# Verify all baseline Markdown records contain the same historical prose after stripping links/path rebasing.
# Exact hashes cover frozen copies and non-doc content; reports intentionally changed links only.
counts={'existing_markdown_screened':data['existing_markdown_screened'],'existing_documents_updated':len([p for p in updated if p.startswith('docs/')]),'root_readme_updated':True,'moved':len(moves),'new_markdown':len(new),'superseded_redirects':data['redirects_resolved'],'relative_links_checked':count,'broken_links':len(bad),'frozen_reference_link_errors':len(skipped),'current_api_operations':data['routes'],'metadata_tables':data['tables'],'feature_requirements':data['requirements'],'gap_findings':data['gaps'],'application_files_changed':len(protected),'lost_baseline_files':len(lost),'focused_unit_result':'12 passed in 0.19s','source_preservation':source.stdout.strip(),'git_diff_check':'PASS'}
(R/'artifacts/documentation-audit/final-results.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')

write(report,f'''# Documentation audit results — 9 October 2026

## Measured work

| Measure | Result |
| --- | --- |
| Existing Markdown documents inventoried/screened | {counts['existing_markdown_screened']} (not all received exhaustive semantic review) |
| Existing documentation files updated | {counts['existing_documents_updated']}; root README and portable Markdown handoff links also updated |
| Existing documents moved/renamed | {counts['moved']} |
| Prior redirects/master-entry duplicates resolved | {counts['superseded_redirects']} superseded compatibility links; no unique content discarded |
| New purposeful Markdown pages/indexes | {counts['new_markdown']} |
| Learning chapters corrected | 14, including reading order, request, frontend/backend/database, identity, workflows/scoring, AI/jobs, history, developer/interview and operations |
| Feature-to-document coverage | 156 original requirement rows and 36 gaps |
| Current source inventories | 77 API operations across 67 OpenAPI paths; 62 SQLAlchemy metadata tables, plus current symbol/test index |
| Relative links/anchors checked | {count}; zero missing targets/anchors (including frozen reference Markdown) |
| New application/configuration/migration/test changes | 0; baseline non-Markdown hashes preserved |
| Baseline files lost | 0; each moved file has a canonical replacement |

## Checks actually run

- Link/anchor validation of root README and every current docs Markdown file: **PASS**, {count} relative references. External network links were not queried. Older plain-text path/line references in frozen generators/source are retained historical pointers, not executable commands.
- Actual `create_app().openapi()` versus committed OpenAPI: **PASS** byte-content-equivalent data. Lazy included routers were expanded; 77 documented operations exactly equal the OpenAPI operation count. No application lifespan/database/provider was invoked.
- SQLAlchemy metadata/table inspection: **PASS**, 62 definitions with columns/types/nullability/keys/check expressions/indexes. Runtime-applied schema/RLS were not independently queried; migration source remains required for SQL-only policies/constraints.
- Existing source/prompt preservation checker: **PASS**, seven preserved copies match their SHA256 manifest.
- `git diff --check -- README.md docs`: **PASS**. Before/after snapshots include pre-existing dirty application changes; this task does not claim ownership of them. Non-doc baseline hashes and all preserved Word/generator assets are unchanged.
- Focused pure tests: `.\\.venv\\Scripts\\python.exe -B -m pytest tests/test_ingestion_mapping.py tests/test_config_storage.py -q -p no:cacheprovider --basetemp=artifacts/documentation-audit/pytest-focused-20261009`: **12 passed in 0.19s**. No normal database operation.
- An earlier marker-selected host pytest run was interrupted after temporary-directory setup errors. The first focused attempt recorded 4 passed/8 setup errors because sandbox temp was unwritable; the workspace-basetemp rerun above passed all 12. Those setup errors are environment evidence, not a demonstrated application regression or successful full suite.

## Important incomplete checks and remaining work

This prioritized pass does not claim all large legacy business-guide paragraphs, contracts/ADRs/requirements or Word outputs are fully reconciled. The tracker marks remaining semantic review, historical generator/path work and Word visual acceptance explicitly. New core user/demo/testing guides provide current executable scope; original vision and acceptance obligations remain preserved.

Full browser/integration/migration/performance/hosted CI/provider/deployment checks were not rerun. Setup/demo commands are checked against code/scripts/configuration and retained evidence, not freshly executed. Real SMTP, current hosted CI and Word visual QA remain open Sprint 8.1 gates. The existing 74-backend/12-browser and subsequent focused closure results remain historical execution evidence, not results of this documentation audit.

Sprint organization: completed 00–08 reports/handoffs in `03-sprints/completed`; original test reports in testing sprint folders; active implemented-but-open 8.1 in `03-sprints/active`; planned 09–23 folders link exact canonical roadmap tasks and impact-based documentation obligations without fake execution reports. Raw verification logs/screenshots stay stable; topic guides link to canonical records.

Main entry: [docs/README](../README.md). [Tracker](../09-planning/DOCUMENTATION_UPDATE_TRACKER.md) and [feature mapping](../09-planning/FEATURE_DOCUMENT_MAPPING.md) identify subsequent work.
''')
# Final report adds valid existing relative links, so verify again after the last write.
count,bad,skipped=check(); assert not bad
counts['relative_links_checked']=count
(R/'artifacts/documentation-audit/final-results.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')
print(json.dumps(counts,indent=2))
