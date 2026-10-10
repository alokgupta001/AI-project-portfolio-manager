from pathlib import Path
import ast
import hashlib
import importlib
import inspect
import json
import os
import re
import sys
from urllib.parse import unquote

R = Path(__file__).resolve().parents[2]
D = R / 'docs'
sys.dont_write_bytecode = True
sys.path.insert(0, str(R / 'services/api'))
BEFORE = json.loads((R/'artifacts/documentation-audit/before.json').read_text(encoding='utf-8'))
original = {p: (R/p).read_text(encoding='utf-8-sig') for p in BEFORE if p.endswith('.md') and (R/p).exists()}
moves = {}
changed = set()
def write(path, content):
    p=R/path; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(content.rstrip()+'\n',encoding='utf-8'); changed.add(path)
def rel(source, target):
    return os.path.relpath(R/target,(R/source).parent).replace('\\','/')
def link(source,target,label=None):
    return f'[{label or Path(target).stem}]({rel(source,target)})'
def move(old,new):
    moves[old]=new
def target(p): return moves.get(p,p)

learn = {
'00-start-here.md':'00-getting-started/README.md',
'01-project-overview.md':'01-project-foundations/PROJECT_OVERVIEW.md',
'02-how-the-application-works.md':'02-backend/REQUEST_LIFECYCLE.md',
'03-frontend-explained.md':'03-frontend/FRONTEND_GUIDE.md',
'04-backend-explained.md':'02-backend/BACKEND_GUIDE.md',
'05-database-explained.md':'04-database/DATABASE_GUIDE.md',
'06-login-and-permissions.md':'05-security/AUTHENTICATION_AND_AUTHORIZATION.md',
'07-main-features-explained.md':'01-project-foundations/FEATURE_WORKFLOWS.md',
'08-assessments-and-dashboards.md':'06-ai-and-analytics/SCORING_AND_DASHBOARDS.md',
'09-ai-features-explained.md':'06-ai-and-analytics/AI_AND_JOBS.md',
'10-sprint-history.md':'01-project-foundations/SPRINT_HISTORY.md',
'11-how-to-read-and-change-the-code.md':'07-testing-and-debugging/DEVELOPER_GUIDE.md',
'12-interview-preparation.md':'01-project-foundations/INTERVIEW_PREPARATION.md',
'13-current-status-and-limitations.md':'08-deployment-and-operations/OPERATIONS_AND_LIMITS.md',
}
for old,new in learn.items(): move('docs/'+old,'docs/02-learning/'+new)
for name,folder in {
'AI_PPM_FUTURE_PRODUCT_VISION_AND_USER_GUIDE.md':'00-overview',
'FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md':'00-overview',
'SPRINT_8_1_GAP_AUDIT.md':'09-planning', 'SPRINT_8_1_PLAN.md':'09-planning',
'FUTURE_SPRINT_ROADMAP.md':'09-planning','FEATURE_GAP_TRACEABILITY.md':'09-planning',
'LOCAL-DEVELOPMENT.md':'07-setup-and-deployment','IDENTITY-DEVELOPMENT.md':'07-setup-and-deployment',
'DEMO-DEVELOPMENT.md':'05-demos/sprint-based/sprint-04',
'SPRINT_VERIFICATION_REPORT.md':'04-testing',
'LEARNING-DOCUMENTATION-VERIFICATION.md':'10-reference/history',
'18-api-contracts.md':'01-architecture','DATABASE-DICTIONARY.md':'01-architecture',
'CODE-AND-TEST-INDEX.md':'10-reference',
'SPRINT_8_1_USER_GUIDE.md':'03-sprints/active/sprint-8.1',
}.items(): move('docs/'+name,'docs/'+folder+'/'+name)
for i in range(9):
    sprint=f'sprint-{i:02d}'; root=f'docs/03-sprints/completed/{sprint}'
    move(f'docs/sprints/SPRINT-{i:02d}-REPORT.md',root+'/SPRINT_REPORT.md')
    move(f'docs/handoffs/SPRINT-{i:02d}-HANDOFF.md',root+'/HANDOFF.md')
    move(f'docs/verification/SPRINT-{i:02d}-CHECKS.md',f'docs/04-testing/sprint-based/{sprint}/TESTING_REPORT.md')
for name in ['SPRINT-06-REVIEW.md','SPRINT-07-CI-FIX.md']:
    move('docs/verification/'+name,'docs/04-testing/sprint-based/sprint-'+name[7:9]+'/'+name)
move('docs/sprints/SPRINT-8.1-REPORT.md','docs/03-sprints/active/sprint-8.1/SPRINT_REPORT.md')
move('docs/handoffs/SPRINT-8.1-HANDOFF.md','docs/03-sprints/active/sprint-8.1/HANDOFF.md')
for i in range(1,11): move(f'docs/verification/PPM-81-{i:03d}.md',f'docs/04-testing/sprint-based/sprint-8.1/PPM-81-{i:03d}.md')

# Rebase actual Markdown links and repository-path references, preserving prose history.
pattern=re.compile(r'(!?\[[^\]\n]*\]\()([^\s)]+)([^)]*\))')
def rewrite(s, old, new):
    def sub(m):
        u=m[2]; bare=u.strip('<>'); path,sep,anchor=bare.partition('#')
        if not path or re.match(r'^[a-zA-Z][\w+.-]*:',path): return m[0]
        absolute=Path(os.path.normpath((R/old).parent/unquote(path)))
        try: rp=absolute.relative_to(R).as_posix()
        except ValueError: return m[0]
        rp=target(rp); dest=rel(new,rp)+(sep+anchor if sep else '')
        return m[1]+dest+m[3]
    s=pattern.sub(sub,s)
    for a,b in sorted(moves.items(),key=lambda kv:-len(kv[0])):
        s=s.replace('`'+a+'`','`'+b+'`')
    return s
for old in BEFORE:
    if old.endswith('.md') and old not in original and old in moves:
        original[old] = rewrite((R/moves[old]).read_text(encoding='utf-8'),moves[old],old)
for old,s in original.items():
    # Frozen specifications and original prompt copies remain byte-for-byte intact.
    if old.startswith('docs/source/') or (old.startswith('docs/prompts/') and not old.endswith('/MASTER.md')): continue
    new=target(old); updated=rewrite(s,old,new)
    if old in moves:
        write(new,updated)
        (R/old).unlink(missing_ok=True)
    elif updated!=s: write(old,updated)

STATUS='docs/00-overview/CURRENT_STATUS.md'
CAT='docs/00-overview/FEATURE_CATALOGUE.md'
GUIDE='docs/00-overview/DOCUMENTATION_GUIDE.md'
TRACK='docs/09-planning/DOCUMENTATION_UPDATE_TRACKER.md'
MAP='docs/09-planning/FEATURE_DOCUMENT_MAPPING.md'
ROAD=target('docs/FUTURE_SPRINT_ROADMAP.md')
AUDIT=target('docs/SPRINT_8_1_GAP_AUDIT.md')
TRACE=target('docs/FEATURE_GAP_TRACEABILITY.md')
REPORT='docs/03-sprints/active/sprint-8.1/SPRINT_REPORT.md'
USER='docs/06-user-guides/USER_GUIDE.md'
TEST='docs/04-testing/TESTING_STRATEGY.md'
DEMO='docs/05-demos/CURRENT_DEMO_GUIDE.md'
API=target('docs/18-api-contracts.md')
DB=target('docs/DATABASE-DICTIONARY.md')
ARCH='docs/01-architecture/SYSTEM_ARCHITECTURE.md'
MAINT='docs/09-planning/SPRINT_DOCUMENTATION_CHECKLIST.md'
L={k:target('docs/'+k) for k in learn}

write(STATUS,f'''# Current implementation and acceptance

Audited 9 October 2026 (Asia/Calcutta). Code checkpoint: base `9056440` plus the existing dirty working tree; not a committed Sprint 8.1 release. Schema source ends at `0008_pilot_completion`. No runtime/database mutation was performed by this documentation audit.

| Capability | Status | Evidence and limits |
| --- | --- | --- |
| Identity, scoped delivery, resource capacity, rubric assessments, deterministic dashboards | IMPLEMENTED AND VERIFIED | Current modules and retained local sprint checks; broader production claims excluded. |
| Durable jobs, CSV imports, labeled Jira/GitHub fixtures | IMPLEMENTED AND VERIFIED | Sprint 08 report and job tests; fixture success is not live-provider acceptance. |
| Signup, setup/profile, browser grants, scoped record search, paging/comparison, My work/notifications, optional metadata, authorized refresh | IMPLEMENTED AND VERIFIED | PPM-81-001 and 003–009 have current source and recorded local acceptance. |
| SMTP delivery to a real inbox | BLOCKED | Adapter exists and fixture tests were recorded; provider/sender/recipient acceptance remains absent. |
| Sprint 8.1 closure | PARTIALLY IMPLEMENTED | 8 of 10 tasks complete locally; 002 external mail gate and 010 CI/Word visual gates remain open. |
| Current hosted CI and regenerated Word layout | IMPLEMENTED BUT UNVERIFIED | Workflow/document artifacts exist; current revision CI and every-page visual acceptance are not established. |
| Live Jira/GitHub sync | BLOCKED | Explicit credentials/provider acceptance required; do not present fixtures as customer integration. |
| Versioned document library, OCR, retrieval, AI gateway/agents/copilot, predictive models | PLANNED | Sprints 09–14. Existing plain-text assessment evidence is a narrower implemented feature. |
| Approvals, transformation, simulations, graph, broad benchmarking, meetings, reports/alerts/passkeys, production release | PLANNED | Sprints 15–23; current departmental comparison is a narrow local capability. |
| Optional unadopted additions and alternative stacks | NOT IN SCOPE | Only adopted required scope counts toward release; see the release criteria. |

Verification means the named behavior has source plus **retained successful local evidence**, not a new full rerun or production certification. BROKEN requires demonstrated failure; an unrun check is not a defect. Read {link(STATUS,REPORT,'Sprint 8.1 evidence')} for exact commands, counts and blockers; {link(STATUS,CAT,'catalogue')} for feature-level scope.

## Current limits

Command snapshots bound inputs to 200 projects, 100 assigned resources and 5,000 rows per loaded source kind, with 1–366-day periods. Sprint 8.1 selectors page on the server; that does not remove snapshot limits. Department comparison uses a selected framework version and the full authorized UTC creation-period cohort, not only the displayed page. SSE polls authorized revisions each second; this has a per-connection query cost and is not a production scalability proof.

Assessment evidence remains bounded UTF-8 text with manual release. Notification receipts show 30 days; this is presentation retention, not physical purge. Registration creates organization/membership only after verification; local mode needs private operator mailbox access. Production environment is rejected by configuration. Real data, provider credentials and deployment proof remain external acceptance obligations.
''')

write(GUIDE,'''# Documentation guide

Start at [the documentation index](../README.md). Current status is authoritative for today's availability; source and verified behavior outrank documentation. Retained test logs prove only their recorded checkpoint. Plans prove intended scope.

## Organization and canonical locations

| Location | Purpose |
| --- | --- |
| 00-overview | Current scope/status, catalogue, vision and release criteria |
| 01-architecture | Current component, API and database explanations |
| 02-learning | Practical cross-sprint code walkthroughs and learning entry points |
| 03-sprints/completed/sprint-NN | Original reports/handoffs for Sprints 00–08 |
| 03-sprints/active/sprint-8.1 | Implemented pilot with open parent acceptance; original plan lives in 09-planning |
| 03-sprints/planned/sprint-NN | Intended outcome, links to canonical roadmap and required documentation changes; no execution reports |
| 04-testing | Strategy, current instructions and original sprint-specific test reports |
| 05-demos | Current reproducible walkthroughs and clearly labeled future outlines |
| 06-user-guides | Current user steps; detailed 8.1 tester guide linked rather than duplicated |
| 07-setup-and-deployment | Local setup and identity operation |
| 08-quality-and-security | Current limitations and acceptance boundaries |
| 09-planning | Gap audit, plans, roadmap, tracker, feature mappings and sprint checklist |
| 10-reference | Source-derived inventories, changelog and historical generated snapshots |

Each sprint-specific folder has a README. Reports, testing evidence, demos and learning notes have one canonical home; topic/sprint indexes link to it. Zero-pad whole sprint numbers, retain `sprint-8.1`, and preserve Sprint 00. A later sprint extends history; it does not rewrite a past test outcome.

## Deliberate deviations

The established `architecture/adr`, `contracts`, `requirements`, `source` and `prompts` trees remain in place because they are referenced scope/decision/interface collections. Frozen source and original prompt copies remain unchanged. `verification` retains raw logs, screenshots and JSON with stable paths; human test reports moved to testing sprint folders. `learning` retains legacy generators and Word artifacts as historical/unverified outputs; do not run older generators over canonical guides. Existing short chapter redirects remain compatibility links, with no independent canonical claim.

Sprint 8.1 is **active**, because implementation and genuine evidence already exist while parent acceptance remains open. Calling those records wholly PLANNED would erase verified work. Its original requirements remain a labeled historical plan; Sprints 09–23 are PLANNED. No future test or implementation report was fabricated.

## Status vocabulary and maintenance

Use IMPLEMENTED AND VERIFIED, IMPLEMENTED BUT UNVERIFIED, PARTIALLY IMPLEMENTED, BROKEN, PLANNED, BLOCKED and NOT IN SCOPE in current documents. Historical labels (COMPLETE, PARTIAL, VERIFIED COMPLETE, NOT IMPLEMENTED, UNVERIFIED, NOT REQUIRED) retain their original meaning; the current catalogue translates them with scope. Demo labels are CURRENT DEMO, FUTURE DEMO PLAN or BLOCKED. Future test cases say PLANNED TEST — NOT YET EXECUTED.

When moving a guide, rebase its links and callers, preserve unique content, and update the tracker. Run link/source/preservation checks and record actual results. Follow [the sprint checklist](../09-planning/SPRINT_DOCUMENTATION_CHECKLIST.md) and [feature mapping](../09-planning/FEATURE_DOCUMENT_MAPPING.md). Do not edit unrelated guides for an unrelated small change.
''')

# Repair stale claims in the actual learning content, then append topic-specific walkthroughs.
fixes={
'00-start-here.md': [('Through Sprint 07,','Through Sprint 8.1,'),('It was checked against source at Git `9056440` on 9 October 2026.','It describes base `9056440` plus preserved uncommitted Sprint 08/8.1 code, source-reviewed on 9 October 2026.')],
'01-project-overview.md': [('Activation/reset links use a local private mailbox, not an external email service.','Local mode uses a private operator mailbox; an SMTP adapter exists, but real inbox acceptance is BLOCKED.'),('Run a database checkpoint task through Celery','Run durable imports and delivery work alongside a database checkpoint'),('There are no durable business jobs or scheduled reports yet.','Durable jobs/imports exist; scheduled business reports remain PLANNED for Sprint 21.')],
'09-ai-features-explained.md': [('Sprint 07 implementation','Sprint 8.1 implementation'),('General durable jobs, retry history and crash recovery remain Sprint 08 work.','General durable jobs, retry history and recovery were implemented in Sprint 08; see the current jobs contract and tests.'),('This app has no connected ingestion, embedding, vector search or model-answer path','This app has CSV/fixture record ingestion, but no connected document embedding, vector search or model-answer path')],
'13-current-status-and-limitations.md': [('with migration chain ending **`0007_durable_jobs`**. Sprint 08 is the latest implemented sprint.','with migration chain ending **`0008_pilot_completion`**. Sprint 8.1 is implemented locally with open parent acceptance.'),('plus preserved uncommitted Sprint 08 changes','plus preserved uncommitted Sprint 08/8.1 changes'),('local mailbox rather than external mail','local mailbox and SMTP adapter; real inbox acceptance remains BLOCKED'),('`assessment.set_access`; no complete admin UI for that grant workflow','`assessment.set_access` and browser Framework/Assessment Access panels now exist'),('Some selectors only load their first 100 candidates.','Sprint 8.1 selectors now page/search on the server; snapshot input limits remain.')],
}
adds={
'00-start-here.md': 'Start with the current-status page before following older evidence. The new reading path includes the pilot walkthrough, current demo, test strategy and feature mapping. A source example remains a code explanation unless its test evidence is explicitly linked.',
'01-project-overview.md': 'Signup and setup now let a verified user create their first organization. Workspace search discovers permitted projects, work, risks and assessments; My work provides permitted personal items. The benefits are easier entry and record discovery, not a claim that AI or production release exists.',
'02-how-the-application-works.md': 'The project-save lifecycle remains authoritative. Optional priority, industry, category, methodology and size travel through delivery form fields, `ppm_schemas.py`, `delivery.write`, and nullable project columns. Work priority/type follow the same route. Unknown is stored as missing metadata, not an invented classification. Inspect 0008 and `test_pilot.py` when a value is rejected; unrelated identity/notification changes do not alter dashboard formulas.',
'03-frontend-explained.md': 'Open `apps/web/components/pilot.tsx` for setup/My work, `pilot-api.ts` for transport, `shell.tsx` for the record palette, and `record-select.tsx` for paged selectors. Input changes request a server page; a result carries its authorized destination. Selection opens the owning page, which fetches the record again. Empty results mean no permitted matches; a 401 or changed organization must not reuse another scope’s records. Debug Network requests, active organization and component error state; reproduce two profiles with `tests/browser/pilot.spec.ts`.',
'04-backend-explained.md': 'In `services/api/ppm_api/pilot.py`, `search` validates query length, type, offset and limit, then calls `records`. It builds SELECTs for projects/work/risks/assessments, escapes SQL wildcard characters, counts under the current principal/RLS, sorts by due date/name/type/id and returns items with links. `my_work` uses the same function with personal filters. Debug the authenticated organization and owning-row access before blaming pagination. This is SQL record discovery, not semantic document search; the latter is PLANNED in Sprint 09.',
'05-database-explained.md': 'Migration `0008_pilot_completion` adds nullable delivery metadata and registration/profile support, plus `identity_deliveries`, `personal_notifications` and `notification_preferences`. `pilot_tables.py` defines their columns and membership/token relationships. The notification unique key `(organization_id,user_id,event_key)` prevents duplicate receipts; recipient RLS and live target checks prevent unauthorized names/counts. `account_mail.enqueue` creates private delivery work with the challenge; `deliver_due` processes it. Inspect recorded preservation/restore evidence before proposing any future migration; this audit applies none.',
'06-login-and-permissions.md': 'Trace `/signup` to `identity.register`, then the challenge completion branch in `identity.complete`. Email-scoped locking and one atomic transaction create the verified user, organization and first Admin only after verification. `account_mail.py` stores/dispatches local or SMTP delivery; a timeout may follow provider acceptance, so single-use/replaced challenges remain the authority. Organization profile editing requires Admin and If-Match; invitation resend/cancel rechecks live inviter authority. Framework/result Access panels reuse assessment guards. Debug private operator mailbox configuration and challenge expiry without exposing tokens; `test_pilot.py` covers replay, revoked authority and scope.',
'07-main-features-explained.md': 'My work uses `pilot.my_work` and `records` to select personal permitted records, including assigned/reviewer assessments not completed. Receipts are created transactionally by owning writes; `notify`, `feed`, `eligible_notification`, `mark_read` and `preference` implement deduplication, revalidation, read state and opt-out. A missing or revoked target is hidden before labels/counts. Thirty days is the presentation window, not purge. Scheduled reminders, approvals and external alerts are PLANNED for Sprints 15/21. Debug receipt kind, target access, enabled preference and timestamp before expecting a feed entry.',
'08-assessments-and-dashboards.md': '`pilot.comparison` selects completed departmental assessments for one framework version and an ordered UTC creation period of at most ten years. It computes count/scored_count/average from the full permitted cohort, independent of display pagination, and preserves null scores. `pilot.stream` polls committed RLS-visible revision aggregates; `apps/web/components/live-workspace.ts` coalesces notices/refetches. No names or values are broadcast. A refetch does not make old source data fresh, change formulas or reconstruct historical snapshots. Debug version, period, missing scores and scope; compare independently with `test_pilot.py` and retain snapshot bounds.',
'09-ai-features-explained.md': 'Current durable imports live in `jobs.py` and `ingestion.py`; job state/outbox is PostgreSQL authority and Redis/Celery transports work. `account_mail.deliver_due` handles account deliveries separately. Provider failure/retry/cancellation diagnostics are not model inference. See `tests/test_jobs.py` and the jobs contract for recovery. A checkpoint-only task’s limitations must not be generalized to the implemented durable import pipeline.',
'10-sprint-history.md': 'Sprint 08 implemented durable jobs/outbox, CSV mapping, labeled connector fixtures and progress streams. Sprint 8.1 subsequently added signup/setup, browser grants, record discovery/paging, personal receipts, nullable metadata and authorized workspace refresh. Original reports and checks are preserved in completed/active sprint folders. The latest 8.1 report records 74 backend and 12 browser tests plus focused closure checks; this documentation audit did not repeat those suites. Mail/CI/Word gates remain open, so 8.1 is not moved to completed.',
'11-how-to-read-and-change-the-code.md': 'Follow the feature-to-document map when changing code. Confirm the exact task/acceptance and owning contract; implement, test and record real results before changing availability labels. Search functions by name because generated older line numbers moved. Update affected learning, user/demo, API/database, sprint report, limitations, catalogue and tracker; unrelated guides need no edit. Existing legacy generators contain snapshots and must not overwrite reviewed canonical guides.',
'12-interview-preparation.md': 'Knowledge checks: Why is fixture connector success different from real-provider acceptance? Why must notification counts recheck target permission? Why does server pagination not remove command snapshot bounds? Why is SMTP acceptance different from inbox arrival? Why can the original 8.1 plan still be historical while local implementation is verified? Cite the owning functions/tests and current report; do not claim that a dirty tree has a hosted CI checkpoint or that deterministic scores are AI predictions.',
'13-current-status-and-limitations.md': 'Current local setup includes migration 0008, a mail adapter and pilot controls. Real external delivery, current hosted CI and regenerated Word visual QA are open acceptance gates. Read CURRENT_STATUS for current scope and the original sprint reports for what was verified at each date. Legacy Word files/generators are retained and are not automatically the current canonical guide.',
}
for old,path in L.items():
    s=(R/path).read_text(encoding='utf-8')
    for a,b in fixes.get(old,[]): s=s.replace(a,b)
    if old=='10-sprint-history.md':
        s=s.replace('## Beyond Sprint 07','## Historical future boundary after Sprint 07')
        s=s.replace('Sprint 08 durable jobs/integrations, Sprint 09 document retrieval, Sprint 10 model gateway, Sprint 11 agents/semantic features, and later ML/copilot/release work remain plans', 'At the Sprint 07 checkpoint, Sprint 08 durable jobs/integrations and later work were plans. Sprint 08 and local Sprint 8.1 are now implemented; Sprint 09 document retrieval, Sprint 10 model gateway, Sprint 11 agents/semantic features, and later ML/copilot/release work remain plans')
    s+='\n\n## Source-reviewed Sprint 8.1 update — 9 October 2026\n\n'+adds[old]+'\n\n'
    s+=f'Status: **IMPLEMENTED AND VERIFIED** within retained local evidence; external gates stay **BLOCKED** or **IMPLEMENTED BUT UNVERIFIED**. See {link(path,STATUS,"current status")}, {link(path,REPORT,"8.1 evidence")}, {link(path,MAP,"future concept and documentation map")} and {link(path,ROAD,"PLANNED work")}.\n'
    write(path,s)

# Fix the wider worker explanation rather than simply adding an overriding disclaimer.
p=L['09-ai-features-explained.md']; s=(R/p).read_text(encoding='utf-8')
s=s.replace('Redis/Celery also demonstrate a real worker-to-database task round trip.','Redis/Celery transport durable ingestion jobs and also demonstrate a real worker-to-database checkpoint round trip.')
s=s.replace('The current task has no application-level retry/recovery workflow. Broker reconnect settings do not implement durable business retries.','The checkpoint task has no application-level retry/recovery workflow. Durable imports use the separate PostgreSQL outbox/job protocol, which does implement bounded retries and recovery; broker reconnect alone is insufficient.')
write(p,s)

write('docs/02-learning/README.md',f'''# Learn the current application

Follow {link('docs/02-learning/README.md',L['00-start-here.md'],'the practical reading order')}. Fourteen existing cross-sprint chapters were retained and corrected for Sprint 8.1; they trace the real UI, API, data, authorization, formulas, failures and debugging path.

General concepts belong in topic folders; [sprint-based links](sprint-based/README.md) explain which sprint introduced or extended them. {link('docs/02-learning/README.md',MAP,'The feature map')} supplies PLANNED concepts, business purpose, task ownership and future documentation changes without fake code walkthroughs.
''')

# Normalize present planning tables without rewriting original acceptance obligations/history.
historical='**Historical planning baseline (before Sprint 8.1 execution):**'
for p in [AUDIT,ROAD,TRACE,target('docs/SPRINT_8_1_PLAN.md'),target('docs/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md')]:
    s=(R/p).read_text(encoding='utf-8'); s=s.replace('**Planning baseline: 9 October 2026.',historical+' 9 October 2026.')
    s=s.replace('**Current evidence for PPM-81-', '**Historical pre-execution evidence for PPM-81-')
    s=s.replace('## Baseline and evidence limits','## Historical pre-execution baseline and evidence limits')
    s=s.replace('No sprint closes solely because code exists.',f'Documentation acceptance follows {link(p,MAINT,"the shared sprint checklist")}. No sprint closes solely because code exists.')
    write(p,s)

trace=(R/TRACE).read_text(encoding='utf-8')
gap_rows=[]; req_rows=[]
for line in trace.splitlines():
    cells=[x.strip() for x in line.strip('|').split('|')]
    if cells and re.match(r'G-\d{3} ',cells[0]): gap_rows.append(cells)
    if cells and re.fullmatch(r'[FNETP]-\d{3}',cells[0]): req_rows.append(cells)
statusmap={'VERIFIED COMPLETE':'IMPLEMENTED AND VERIFIED','PARTIAL':'PARTIALLY IMPLEMENTED','NOT IMPLEMENTED':'PLANNED','NOT REQUIRED':'NOT IN SCOPE','UNVERIFIED':'IMPLEMENTED BUT UNVERIFIED'}
def current_status(raw):
    if raw.startswith('IMPLEMENTED locally') or raw.startswith('VERIFIED locally'): return 'IMPLEMENTED AND VERIFIED'
    if raw.startswith('BLOCKED'): return 'BLOCKED'
    if raw.startswith('PARTIAL'): return 'PARTIALLY IMPLEMENTED'
    return statusmap.get(raw,raw)
cat=f'''# Feature catalogue

Code and retained local evidence establish current capability; original acceptance obligations are unchanged. Read {link(CAT,STATUS,'current scope and evidence limits')}. Current status labels below translate the existing traceability vocabulary; a multi-stage parent remains partial until all stages pass. Future sprints describe intended user outcomes, not available buttons.

## Gap-level user outcomes

| Feature / gap | Current status | User benefit / intended result | Task / sprint |
| --- | --- | --- | --- |
'''
for c in gap_rows: cat+=f'| {c[0]} | {current_status(c[1])} | {c[4]} | {c[3]} |\n'
cat+='\n## Requirement-level catalogue\n\nThese are the complete 156 approved crosswalk rows, including scope exclusions and technical controls. Acceptance wording is retained in the canonical traceability matrix.\n\n| ID | Feature | Current scope status | Owning task / scope decision |\n| --- | --- | --- | --- |\n'
for c in req_rows: cat+=f'| {c[0]} | {c[1]} | {current_status(c[2])} | {c[3]} |\n'
cat+=f'\nUser steps: {link(CAT,USER,"current guide")}; future outcomes/acceptance: {link(CAT,ROAD,"roadmap")}; obligations: {link(CAT,TRACE,"traceability")}.\n'
write(CAT,cat)

topics={'8.1':'Operational onboarding and record discovery','09':'Versioned evidence, keyword retrieval and governance','10':'AI gateway, embeddings, orchestration and evaluation','11':'Nine agents, semantic assessment and reviewed recommendations','12':'Connector authority, historical labels and baseline models','13':'Eligible forecast serving with uncertainty','14':'Scoped copilot context and natural-language analytics','15':'Approvals, due-event reminders and assessment follow-through','16':'Transformation plans and decision records','17':'Resource/budget scenarios that preserve the live plan','18':'Derived knowledge graph and bounded impact paths','19':'Compatible benchmarks and privacy safeguards','20':'Meeting intake, cited minutes and approved actions','21':'Reports, authorized alerts and daily briefings','22':'Passkeys, account lifecycle and revocation','23':'Integrated release, performance, recovery and deployment'}
def learning_for(owner):
    if any(x in owner for x in ('09-','10-','11-','12-','13-','14-','18-','19-','20-','21-')): return L['09-ai-features-explained.md']
    if '22-' in owner or '81-001' in owner or '81-002' in owner or '81-004' in owner: return L['06-login-and-permissions.md']
    if '23-' in owner: return L['13-current-status-and-limitations.md']
    return L['07-main-features-explained.md']
mapping=f'''# Feature-to-document mapping and planned concepts

Every original crosswalk requirement and confirmed gap is listed below. The roadmap is the canonical detailed plan; update documents by impact. Named future files/functions in that plan are proposals. Current general guides explain foundations and link here for missing capabilities.

## Planned concepts and business purpose

| Sprint | PLANNED concept / purpose | Current foundation and boundary | Required learning home |
| --- | --- | --- | --- |
'''
for n,t in topics.items():
    if n=='8.1': continue
    plan=f'docs/03-sprints/planned/sprint-{n}/README.md'
    mapping+=f'| {link(MAP,plan,n)} | {t} | Reuse current identity, domain facts, jobs and typed contracts; implementation and acceptance are not yet executed. | {link(MAP,learning_for("PPM-"+n+"-001"),"topic guide")} |\n'
mapping+='\n## All required features and gaps\n\n| Feature / ID | Learning guide | User guide | Demo guide | Tests | Architecture/API docs | Sprint plan / acceptance |\n| --- | --- | --- | --- | --- | --- | --- |\n'
for c in req_rows+gap_rows:
    gap=c[0].startswith('G-'); owner=c[3]; feature=c[0] if gap else c[0]+' '+c[1]
    m=re.search(r'PPM-(81|\d{2})-',owner); num='8.1' if m and m[1]=='81' else m[1] if m else None
    plan='docs/03-sprints/active/sprint-8.1/README.md' if num=='8.1' else f'docs/03-sprints/planned/sprint-{num}/README.md' if num else TRACE
    mapping+='| '+feature+' | '+link(MAP,learning_for(owner),'learning')+' | '+link(MAP,USER,'current steps')+' | '+link(MAP,'docs/05-demos/FUTURE_DEMO_PLANS.md' if current_status(c[1] if gap else c[2]) in ('PLANNED','BLOCKED','PARTIALLY IMPLEMENTED') else DEMO,'demo / limits')+' | '+link(MAP,'docs/04-testing/GAP_ACCEPTANCE_TEST_PLAN.md','acceptance')+' | '+link(MAP,ARCH,'architecture')+' / '+link(MAP,API,'API')+' | '+link(MAP,plan,owner)+' |\n'
write(MAP,mapping)

write(MAINT,'''# Shared sprint documentation acceptance checklist

Use this for every future task, scoped to the feature's actual impact. A sprint is not fully documented while a required guide is inaccurate or missing.

1. Confirm canonical task requirement, feature/gap IDs and acceptance criteria.
2. Implement the authorized feature and record the actual code revision.
3. Add/update meaningful automated and negative-case tests.
4. Run appropriate tests; record real command, environment, fixtures and results. Separate external blockers.
5. Update the owning technical explanation and practical learning guide with real symbols/data/failures/debugging.
6. Update current user steps and executable demo; keep unavailable scenarios labeled FUTURE DEMO PLAN or BLOCKED.
7. Update affected API/database/architecture/security/setup documents and generated inventories, after checking real source.
8. Update sprint report/handoff, test evidence, bugs/fixes and known limitations without rewriting old outcomes.
9. Update feature catalogue and current status within the scope actually verified.
10. Update tracker, feature mapping and links; choose one canonical document.
11. Confirm planned/current distinction, source references, links and application/document preservation.

Completion record: list affected canonical paths, checks run, unresolved documentation/provider gates and next owner action. Do not report a test pass before execution. Do not make unrelated edits for a minor feature change. Use [the feature map](FEATURE_DOCUMENT_MAPPING.md) to select documents.
''')

# Sprint indexes preserve original reports, test evidence and plans in one canonical location.
purposes=['Scope reconciliation and architecture contracts','Reproducible runtime foundation','Identity and tenant authorization','Enterprise UI shell','Delivery system of record','Resource capacity','Versioned maturity assessments','Deterministic command center','Durable jobs and ingestion']
for i,purpose in enumerate(purposes):
    sn=f'sprint-{i:02d}'; p=f'docs/03-sprints/completed/{sn}/README.md'; test=f'docs/04-testing/sprint-based/{sn}/TESTING_REPORT.md'
    learning=L['09-ai-features-explained.md'] if i==8 else L['06-login-and-permissions.md'] if i==2 else L['07-main-features-explained.md']
    write(p,f'''# Sprint {i:02d} — {purpose}

Historical completed sprint; availability is limited to the original report's acceptance. Its plan and actual outcome are distinguished in [SPRINT_REPORT](SPRINT_REPORT.md); do not infer current release status from an old report.

| Question | Canonical evidence |
| --- | --- |
| Purpose and original planned scope | {purpose}; original report Status/scope and preserved ordered prompt pack |
| Actual implementation and changes | [Original report](SPRINT_REPORT.md) and [handoff](HANDOFF.md) |
| Tests actually executed | {link(p,test,'Historical testing report')}; retains failures, limits and recorded commands |
| Incomplete or blocked work | Original report/handoff limitations; {link(p,STATUS,'current status')} separates later changes |
| Learning guide | {link(p,learning,'General code walkthrough')} (cross-sprint; no invented historical tutorial) |
| Demo | Original report's use/demo sections; {link(p,DEMO,'current walkthrough')} covers today's experience |
| Later extension | Sprints {', '.join(f'{n:02d}' for n in range(i+1,9))+' and ' if i<8 else ''}8.1 extended foundations; trace exact changes in their reports |
| Do not assume | AI, full document intelligence, production deployment or future roadmap acceptance |

No separate learning/demo/test document is invented where the original report already contains that evidence.
''')
    tp=f'docs/04-testing/sprint-based/{sn}/README.md'
    write(tp,f'# Sprint {i:02d} test evidence\n\n[Original executed checks](TESTING_REPORT.md) retain their historical outcome. {link(tp,p,"Sprint purpose, plan, outcome and limits")}. Current rerun instructions are in {link(tp,TEST,"the testing strategy")}; no rerun is inferred from moving a file.')
    for section in ['02-learning','05-demos']:
        q=f'docs/{section}/sprint-based/{sn}/README.md'
        write(q,f'# Sprint {i:02d} — {purpose}\n\n{link(q,p,"Sprint record")} identifies original scope, actual outcome, tests, limitations and later changes. {link(q,learning if section=="02-learning" else DEMO,"Current topic guide")} explains the current application; historical demo/learning details remain in the report, without duplicated copies.')
p='docs/03-sprints/active/sprint-8.1/README.md'
write(p,f'''# Sprint 8.1 — local pilot implementation, acceptance open

Status: **PARTIALLY IMPLEMENTED** at parent level; 8 of 10 tasks complete locally. This folder is active rather than planned/completed because real implementation evidence exists and closure gates remain.

Original intended scope: {link(p,target('docs/SPRINT_8_1_PLAN.md'),'historical plan')}. Actual outcome/tests: [report](SPRINT_REPORT.md), [handoff](HANDOFF.md), and {link(p,'docs/04-testing/sprint-based/sprint-8.1/README.md','task evidence')}. Source walkthroughs: {link(p,L['04-backend-explained.md'],'backend')} and {link(p,L['06-login-and-permissions.md'],'identity')}. Demo/testing steps: [pilot tester guide](SPRINT_8_1_USER_GUIDE.md), {link(p,DEMO,'current demo')}.

Signup/setup, grants, search/paging/cohorts, My work/receipts, metadata and revision refresh are locally accepted. Real account mail is BLOCKED; current hosted CI and regenerated Word visual QA are open. Sprint 09 has not begun and extends document evidence only after its stated entry gates. Do not infer AI, scheduled alerts, unlimited dashboards or production readiness from these records. The current guide is Markdown; unrendered Word is not acceptance evidence.
''')
p='docs/04-testing/sprint-based/sprint-8.1/README.md'
write(p,'# Sprint 8.1 recorded acceptance\n\n'+ '\n'.join(f'- [PPM-81-{i:03d}](PPM-81-{i:03d}.md)' for i in range(1,11))+f'\n\n{link(p,REPORT,"Original execution report")} records actual totals and open gates. These are retained results, not reruns in the documentation audit.')
for section in ['02-learning','05-demos']:
    p=f'docs/{section}/sprint-based/sprint-8.1/README.md'
    write(p,f'# Sprint 8.1\n\n{link(p,"docs/03-sprints/active/sprint-8.1/README.md","Purpose, plan, actual implementation, checks and open gates")}. {link(p,L["04-backend-explained.md"] if section=="02-learning" else DEMO,"Current guide")}. No duplicate pilot report is maintained here.')
for n,t in topics.items():
    if n=='8.1': continue
    p=f'docs/03-sprints/planned/sprint-{n}/README.md'
    match=re.search(rf'## Sprint {n}[^\n]*\n(.*?)(?=\n## Sprint |\Z)',(R/ROAD).read_text(encoding='utf-8'),re.S)
    summary=match[1] if match else ''
    tasks=re.findall(r'^### (PPM-[^\n]+)',summary,re.M)
    acceptance=re.findall(r'^\*\*Acceptance:\*\* (.*)',summary,re.M)
    write(p,f'''# Sprint {n} — {t}

**PLANNED**. No implementation, executed tests or completed report is claimed. Purpose and intended work: {t}. Actual implementation/test result: none for this sprint in the audited tree. Incomplete: all planned packages and their external acceptance. Dependencies, exact tasks and acceptance remain in {link(p,ROAD,'the canonical roadmap')} (Sprint {n} section). Later extensions/dependencies are listed in its sequence.

## Planned work packages

'''+ '\n'.join('- '+x for x in tasks)+f'''

## Planned testing and demo

**PLANNED TEST — NOT YET EXECUTED**. {link(p,'docs/04-testing/GAP_ACCEPTANCE_TEST_PLAN.md','Acceptance plan')} links every gap to its actual roadmap acceptance. {link(p,'docs/05-demos/FUTURE_DEMO_PLANS.md','Future demo outline')} describes intended outcomes only. No standalone historical learning/test/demo/report exists yet for this sprint.

## Required documentation at implementation

Update {link(p,learning_for('PPM-'+n+'-001'),'the relevant learning guide')}, {link(p,USER,'user steps')}, {link(p,DEMO,'current demo')}, {link(p,TEST,'testing instructions')}, {link(p,API,'API')}, {link(p,DB,'database')}, {link(p,ARCH,'architecture')} according to actual impact; report/handoff/evidence, {link(p,CAT,'catalogue')}, {link(p,STATUS,'status')}, {link(p,TRACK,'tracker')} and {link(p,MAP,'feature mapping')} are completion obligations. Follow {link(p,MAINT,'the shared checklist')}.

Do not assume proposed endpoints, pages, models, migrations, providers or test passes exist before implementation. Original required scope and release gates are not changed by this folder.
''')
for section in ['02-learning','04-testing','05-demos']:
    p=f'docs/{section}/sprint-based/README.md'
    write(p,'# Sprint-based documentation\n\nOne canonical report/test/demo location per artifact. Topic indexes link to it rather than copy historical records.\n\n'+ '\n'.join(f'- [Sprint {n:02d}](sprint-{n:02d}/README.md)' for n in range(9))+ '\n- [Sprint 8.1](sprint-8.1/README.md)\n\n'+link(p,'docs/03-sprints/README.md','Future sprint plans')+' are PLANNED, with no fabricated execution evidence.')
p='docs/03-sprints/README.md'
write(p,'# Sprint history and future work\n\n'+ '\n'.join(f'- [Completed Sprint {i:02d}: {t}](completed/sprint-{i:02d}/README.md)' for i,t in enumerate(purposes))+'\n- [Active Sprint 8.1: local implementation, parent acceptance open](active/sprint-8.1/README.md)\n'+ '\n'.join(f'- [PLANNED Sprint {n}: {t}](planned/sprint-{n}/README.md)' for n,t in topics.items() if n!='8.1')+f'\n\n{link(p,MAINT,"Documentation acceptance applies to every future sprint")}. Dates/numbers are execution order, not delivery promises.')

# Current user and demo flows are grounded in real screens; no fake assistant page.
write(USER,f'''# Current user guide

Availability: **IMPLEMENTED AND VERIFIED** within retained local checks. Production acceptance remains open. Use {link(USER,STATUS,'current status')} and {link(USER,CAT,'the catalogue')} for exact scope. For complete Sprint 8.1 steps and recovery limits, use {link(USER,target('docs/SPRINT_8_1_USER_GUIDE.md'),'the pilot tester guide')}.

| User / purpose | What to do | Needed information | Expected result and limitation |
| --- | --- | --- | --- |
| New user: join/create organization | Open `/signup`, request verification, privately open the message, choose name/password, sign in | Your email, organization name; local operator mailbox assistance or accepted mail provider | Organization created only after verification; real inbox delivery BLOCKED until accepted |
| Admin: configure access | Open `/account`, edit organization profile; invite/manage members; use project Grants/resource access/framework or completed-result Access | Correct organization and grant scope | Saved membership/grants; ownership alone never grants access; private effort remains separately scoped |
| PM: plan delivery | Open `/portfolios`, create allowed portfolio/project; open `/projects/{id}` and its tabs | Name, portfolio, valid dates/currency, optional metadata | Stored project/work/milestones/risks; archive checks active dependents; stale revision must be reloaded |
| PM: manage staffing | Open `/resources`, create permitted resource/calendar/allocation | Resource profile, working dates/hours and project | Deterministic capacity or Unknown for missing schedule/scope; login account and workforce profile differ |
| Assessor/reviewer: evaluate maturity | Open `/assessments`, create/publish framework, assign distinct respondent/reviewer, save answers, submit/review/complete | Published version, assignment, required answers/evidence | Saved rubric-based result/history; numeric reviewer changes require reasons; no AI scoring |
| Executive/Viewer: inspect portfolio | Open `/command-center`, choose permitted scope/period/view and inspect source drawer | Authorized records and compatible currency/period | Explainable deterministic measures with coverage/Unknown; not a predictive probability or complete historical reconstruction |
| All permitted users: find work | Ctrl K / search button → Find a record → type/query → page → open | Active organization, record query/type | Older permitted records discoverable; owning page rechecks access |
| Assigned user: follow up | Workspace My work; Notifications → mark read/preferences | Assignment and permitted target | Persistent in-app receipts shown for 30 days; scheduled/external notifications PLANNED |
| Import operator: load supported data | Open `/integrations`; choose configured fixture/CSV destination and mapping, preview/run/check job | Authorized project, supported columns, file and adapter mode | Durable job outcomes/rejected rows; real Jira/GitHub credentials are BLOCKED external acceptance |

## Recovery and unavailable experiences

Wrong organization or absent grant can hide a row; recheck Account and access rather than changing IDs. Keep separate browser profiles for different users. On 401 sign in/refresh; on stale revision reload before editing. Unknown metrics need source/calendar/coverage corrections, not invented zeros. Failed imports expose bounded diagnostics through their job surface. Local challenge links are private, expire and cannot be replayed.

**PLANNED:** reusable documents/retrieval (09), AI/agents (10–11), predictive models (12–13), project/multi-project copilot (14), approvals/reminders (15), transformation/scenarios/graph/benchmarks/meetings (16–20), reports/exports/alerts/audio (21), passkeys/lifecycle (22), production recovery/deployment (23). There is no executable AI assistant or report-export demo at this checkpoint. Follow {link(USER,ROAD,'approved future scope')}; optional additions are not guaranteed.
''')
write(DEMO,f'''# Current demo guide

**CURRENT DEMO**, source-reviewed against the local pilot and retained browser checks; not freshly executed by this documentation audit. Use fictional data and separate browser profiles. Real SMTP/Jira/GitHub and production demonstration are **BLOCKED** for their external gates. {link(DEMO,target('docs/DEMO-DEVELOPMENT.md'),'Sprint 04 sample setup')} is the canonical guarded seed guide; {link(DEMO,target('docs/LOCAL-DEVELOPMENT.md'),'local setup')} lists start commands/services. Required: Docker Linux engine, configured private `.env`, PostgreSQL/Redis/API/web/worker/dispatcher, active organization and suitable role/grants. No default password exists.

| Scenario | Exact page/actions | Expected result | Recovery / limitation |
| --- | --- | --- | --- |
| Signup and onboarding | Open `/signup`; request message; operator privately retrieves register link; complete verification; sign in; follow Workspace Getting started | Saved organization/first Admin; checklist reflects stored records | Expired/replaced links fail; local message requires operator; real inbox acceptance BLOCKED |
| PM delivery | Open `/projects`; create in an allowed portfolio; open the resulting `/projects/{id}`; add permitted milestone/work/risk; save and reload | Records persist and belong to that project; optional classification may be Unknown | Missing portfolio/grant/invalid date yields denial/validation; re-read revision on conflict |
| Project detail and discovery | Ctrl K → Find a record; query permitted project/work/risk; choose result; page to older records | Project detail opens; child deep link filters target | Wrong scope/revocation hides results; no semantic document retrieval |
| Assessment | `/assessments`: create/publish allowed framework, assign separate respondent/reviewer; respondent answers/submits; reviewer reviews/completes | Deterministic score, coverage and immutable completed history; published version retained | Required answer, self-review and missing scope block transition; evidence is UTF-8 text/manual release |
| Executive overview | `/command-center`: choose available view/scope/date; open source/evidence drawer; compare project facts | Deterministic measures and explicit missing/stale inputs; currency remains separate | Missing inputs stay Unknown; snapshot limits remain; no AI prediction |
| Resource planning | `/resources`: open permitted profile, schedule/leave/allocation; inspect capacity for period | Hours, overload and coverage reflect actual scope | Full workload/effort requires separate grants; missing calendar is not zero capacity |
| Pilot receipts and refresh | Workspace My work; Notifications; mark read; change preference. Keep Command center in second signed-in profile while saving permitted milestone in first | Persistent read/preferences and authorized saved-change refetch | Receipt needs qualifying assignment/review/import event; 30-day window; revoked target hidden |
| Imports | `/integrations`: use labeled supported fixture or CSV mapping; inspect progress/rejected rows | Durable persisted job outcome and errors | Fixture is not live-provider proof; retry only owning supported action |

## Safe reset and failure handling

Use the isolated demo project/database and documented deterministic seed; repeated seeding preserves subsequent edits and does not reset everything. Archive fictional records through authorized forms only after dependent checks. A fresh scenario can use another fictional organization. Do not reset/delete databases or use `down --volumes`. Stop the demo with its identical compose file arguments; preserve volumes. No cleanup/reset command was run by this audit.

Record expected/actual result and Pass/Fail/Blocked when you actually execute. Do not reuse old screenshots as proof of a new run. {link(DEMO,'docs/05-demos/FUTURE_DEMO_PLANS.md','Future outlines')} contain unavailable assistant/report experiences.
''')
p='docs/05-demos/FUTURE_DEMO_PLANS.md'
write(p,'# Future demo plans\n\n**FUTURE DEMO PLAN** throughout; none is executable evidence. Activate only after the owning sprint’s real UI and acceptance exist.\n\n| Sprint | Intended demonstration | Acceptance authority |\n| --- | --- | --- |\n'+ '\n'.join(f'| {n} | {t}; show only actual implemented screens/results after verification | {link(p,f"docs/03-sprints/planned/sprint-{n}/README.md","plan and gates")} |' for n,t in topics.items() if n!='8.1')+'\n\nAI assistant (14) must demonstrate selected/multi-project permission-filtered context, factual/cited answers and follow-ups; report exports (21) must match source totals and render readable layouts. No imaginary button/navigation step or fabricated screenshot is specified. Mail/provider/deployment flows remain BLOCKED until their prerequisites are supplied and accepted.')
write(TEST,f'''# Testing strategy and current commands

This is strategy/run guidance, not an executed full application report. Historical evidence: {link(TEST,'docs/04-testing/sprint-based/README.md','sprint checks')} and {link(TEST,REPORT,'8.1 report')}. Future acceptance: {link(TEST,'docs/04-testing/GAP_ACCEPTANCE_TEST_PLAN.md','gap plan')}.

| Category / purpose | Real infrastructure and run command | Scope / limits |
| --- | --- | --- |
| Backend unit tests: deterministic input/arithmetic/config | Windows `.\\.venv\\Scripts\\python.exe -B -m pytest -q -m "not integration" -p no:cacheprovider` | `pyproject.toml` config; `tests/test_config_storage.py`, mapping and pure domain cases; no normal DB |
| API/database integration: stored behavior and transaction boundaries | `docker compose --profile test run --build --rm test` | `scripts/test_backend.py` guards `ppm_test`; identity/delivery/capacity/assessment/command/jobs/pilot/transaction tests; lifecycle/drift on disposable test DB only |
| Frontend/end-to-end: real role-specific browser journeys | `npx playwright install chromium`; `node scripts/check-identity-browser.mjs` | Playwright `tests/browser`; isolated identity-test project, independent volumes/origins; fixture scripts can mutate only that disposable environment |
| API/schema contract drift | `npm run contracts:check` | Compares generated OpenAPI/TypeScript; no planned endpoint may be listed as current |
| UI static checks | `npm run typecheck`; `npm run lint`; `npm run format:check` | Type/error/format checks are not interactive user acceptance |
| Security/tenant isolation | Full guarded backend and browser suites; focus `test_identity.py`, `test_pilot.py`, assessment/capacity cases | Two tenants, ID substitution, revocation, CSRF, changed scope and sensitive effort; check negative cases rather than relying on UI hiding |
| Worker/persistence | `docker compose exec -T api python scripts/smoke_worker.py`; `node scripts/check-persistence.mjs` | Specific worker round trip/restart fixture; writes/restarts require intended local acceptance scope and are not run during a docs-only audit |
| Source preservation | `.\\.venv\\Scripts\\python.exe scripts/check_sources.py` | Frozen source hashes; separate from application regression |
| AI grounding/quality | PLANNED TEST — NOT YET EXECUTED | Sprints 09–14: scoped retrieval/citations, provider failure/invalid output/adversarial text, evaluation and genuine-label model suitability |
| Performance/recovery/release smoke | PLANNED TEST — NOT YET EXECUTED | 22/23 documented workload/device/profile and restore/rollback exercises; historical tiny-fixture timings do not prove targets |

## Test environment and interpreting results

Follow {link(TEST,target('docs/LOCAL-DEVELOPMENT.md'),'local environment instructions')} for locked tools/services and {link(TEST,target('docs/IDENTITY-DEVELOPMENT.md'),'identity tests')}. Keep `ppm_local`, `ppm_demo` and guarded `ppm_test` distinct. Do not run lifecycle/reset/seed against the normal database. Existing tests contain integration/worker markers; a collected definition is not a pass. Static checks and fixture success cannot close live provider gates.

For a regression, record expected/actual, command, environment, fixtures, code revision and retained output. Preserve old successful reports even when a current run fails; add the current defect separately. Cover empty/invalid/stale/network/unavailable-provider cases, totals/relationships/periods and permissions. Run only checks relevant to changed behavior; documentation-only link/source checks do not require resetting application data.

Final release acceptance remains {link(TEST,target('docs/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md'),'the existing release criteria')}; no gate is weakened by this strategy.
''')
p='docs/04-testing/GAP_ACCEPTANCE_TEST_PLAN.md'
s=f'''# Gap acceptance test plan

This table covers all 36 confirmed/blocked findings. The exact task's acceptance and negative cases remain in {link(p,ROAD,'the roadmap')} or {link(p,target('docs/SPRINT_8_1_PLAN.md'),'historical 8.1 plan')}; acceptance obligations are not reduced to a generic test. Existing results remain in the linked evidence. Planned tests are **PLANNED TEST — NOT YET EXECUTED** until real execution.

| Gap / feature | Owning acceptance | Test disposition | Cases to retain / add |
| --- | --- | --- | --- |
'''
for c in gap_rows:
    own=re.search(r'PPM-81-\d{3}',c[3]); state=current_status(c[1])
    evidence=f'docs/04-testing/sprint-based/sprint-8.1/{own[0]}.md' if own else ROAD
    disp='Recorded local acceptance; rerun NOT performed by docs audit' if state=='IMPLEMENTED AND VERIFIED' else 'BLOCKED external gate; retain fixture checks' if state=='BLOCKED' else 'PLANNED TEST — NOT YET EXECUTED for remaining scope'
    s+=f'| {c[0]} | {link(p,evidence,c[3])} | {disp} | {c[4]} Include permitted/denied roles, two tenants, empty/invalid/stale input, failure and repeat/revocation behavior as applicable. |\n'
write(p,s)

# Current architecture plus source-derived API/database/function inventories.
write(ARCH,f'''# Current system architecture

Status: **IMPLEMENTED AND VERIFIED** within retained local checks; future design is separately labeled in the preserved proposed architecture. Current source uses a modular monolith, not a separate microservice for each business feature.

```mermaid
flowchart LR
    Browser --> Next[Next.js pages and proxy]
    Next --> API[FastAPI routes and principal]
    API --> DB[PostgreSQL domain facts and RLS]
    API --> Store[Private local object storage]
    API --> Redis[Redis rate limits and task transport]
    DB --> Dispatch[Outbox dispatcher]
    Dispatch --> Redis
    Redis --> Worker[Linux Celery worker]
    Worker --> DB
    Worker --> Mail[Local mailbox or SMTP adapter]
```

| Component / real files | Responsibility / flow |
| --- | --- |
| `apps/web/app` and `components` | Routes/forms/selectors; delivery, resources, assessment, command center, integrations and pilot controls |
| `apps/web/app/api/v1/[...path]/route.ts` | Same-origin proxy forwards to API_ORIGIN and preserves transport/identity behavior |
| `packages/contracts/src/client.ts` | Typed openapi-fetch client; generated schema is derived from actual API |
| `main.py`, `identity.py` | Lifespan/config/health, CSRF/request IDs/errors, sessions and function-scoped principal transaction/tenant context |
| `delivery.py`, `capacity.py`, `assessment.py`, `command.py` | Domain rules with SQLAlchemy statements directly; no universal repository abstraction; deterministic scoring/metrics |
| `jobs.py`, `ingestion.py`, `job_tables.py`, worker | Durable PostgreSQL state/outbox with Redis/Celery transport; CSV/fixture adapters and progress; live connector acceptance open |
| `pilot.py`, `pilot_tables.py`, `account_mail.py` | Scoped search/setup/My work/cohorts/receipts/revision SSE, private account deliveries |
| `database.py`, `*tables.py`, migrations 0001–0008 | Metadata, constraints, tenant/reference keys, app-role RLS, migration-owner/application-role separation |

## Request, authorization and failure flow

Form → typed same-origin request → proxy → CSRF and identity → function-scoped transaction/principal → validation and owning domain rule → transaction-local user/organization/role → RLS/constraints → commit → response → component refetch. Permission is checked at the backend/database, not only by hiding a button. Ownership, role, grants and private effort are distinct.

File bytes and database metadata are not one atomic transaction. Import/outbox authority is PostgreSQL; Redis is transport, not durable business truth. Workspace SSE polls committed authorized revisions and broadcasts opaque change notices; it rechecks sessions and scope, closes on revocation, and clients coalesce refetch. SMTP delivery ambiguity requires honest status; accepted transport is not inbox proof.

Validation returns 422; CSRF/authority denial 403; absent/hidden records and authentication errors follow owning routes; stale revisions conflict; dependency readiness is 503. `main.error_response` provides sanitized errors/request IDs and avoids exposing driver credentials. Debug request ID, route, active organization, revision and source completeness.

## Explicit future boundaries

**PLANNED:** reusable documents/keyword retrieval/OCR (09), embeddings/gateway/orchestration (10), agents/semantic extraction (11), labeled models/forecasting (12–13), copilot (14), later enterprise/release modules (15–23). Existing assessment evidence and fixture ingestion are not a working RAG pipeline. Future vector/graph stores are derived views; no invented endpoint or table appears in current inventories.

See {link(ARCH,API,'API details')}, {link(ARCH,DB,'schema')}, {link(ARCH,L['06-login-and-permissions.md'],'authentication walkthrough')}, {link(ARCH,L['08-assessments-and-dashboards.md'],'formula/data flow')}, {link(ARCH,'docs/contracts/pilot.md','pilot guarantees')} and {link(ARCH,ROAD,'future design')}. The established contracts/ADRs retain their canonical locations.
''')

from ppm_api.main import create_app
app=create_app(); schema=app.openapi()
schema_old=json.loads((R/'packages/contracts/openapi.json').read_text(encoding='utf-8'))
write('docs/10-reference/history/API_INVENTORY_PRE_AUDIT.md',rewrite(original['docs/18-api-contracts.md'],'docs/18-api-contracts.md','docs/10-reference/history/API_INVENTORY_PRE_AUDIT.md'))
api=f'''# API reference — actual current routes

Source-reviewed 9 October 2026. Generated from `main.create_app().openapi()` and actual route endpoints **without running lifespan, accessing settings secrets or contacting databases/providers**. {'Committed OpenAPI matches the constructed schema.' if schema==schema_old else 'Committed OpenAPI differs from the constructed schema; drift needs a separate implementation review.'} HTTP methods/paths and parameters below are current, not future proposals.

## Authentication, validation and errors

Authenticated routes depend on `identity.principal`/Auth and current organization membership/RLS. Browser cookies are `ppm_access`/`ppm_refresh`; state-changing requests require configured Origin plus CSRF cookie/header except the specifically signed GitHub hook. Public challenge/auth routes still follow their own CSRF/rate-limit rules. Read each linked handler and {link(API,'docs/contracts/permissions.md','permission contract')} for exact role/grant/assignment requirements: OpenAPI alone does not enumerate all authorization rules. Ownership never bypasses grants; private effort/assessment answers need their own access.

`main.error_response` emits `error` with code, message, request_id and details. Pydantic validation returns 422; identity, denial, not-found, revision conflict and 503 dependency cases depend on the route. Error messages are sanitized; no credentials/challenge payload is a public response. Generic reset/registration requests resist enumeration. Nullable/missing values and decimal serialization follow actual schemas.

## Route inventory

| Method and path | Actual handler | Parameters / validation | Request body | Success / documented responses |
| --- | --- | --- | --- | --- |
'''
route_count=0
for rt in app.routes:
    if not hasattr(rt,'endpoint') or rt.path not in schema['paths']: continue
    src=inspect.getsourcefile(rt.endpoint)
    try: src=Path(src).relative_to(R).as_posix()
    except (ValueError,TypeError): src='services/api/ppm_api/main.py'
    for method in sorted(rt.methods or []):
        operation=schema['paths'][rt.path].get(method.lower())
        if not operation: continue
        route_count+=1
        pars=[]
        for q in operation.get('parameters',[]):
            ss=q.get('schema',{}); bounds={k:v for k,v in ss.items() if k in ['minimum','maximum','minLength','maxLength','enum','default']}
            pars.append(q['name']+' ('+q['in']+(', required' if q.get('required') else '')+'): '+json.dumps(bounds,ensure_ascii=False))
        body=operation.get('requestBody',{}).get('content',{})
        bodytext='; '.join(k+': '+json.dumps(v.get('schema',{}),ensure_ascii=False) for k,v in body.items()) or '—'
        resp='; '.join(k+': '+', '.join(json.dumps(v.get('schema',{})) for v in val.get('content',{}).values()) for k,val in operation.get('responses',{}).items())
        api+=f'| `{method} {rt.path}` | {link(API,src,rt.endpoint.__name__)} | '+('; '.join(pars) or '—')+' | '+bodytext.replace('|','\\|')+' | '+resp.replace('|','\\|')+' |\n'
api+=f'\n## Full request/response schemas\n\nNested properties, required fields and validation are defined in {link(API,"packages/contracts/openapi.json","committed OpenAPI")} (`components.schemas`) and linked route Pydantic models. Current generated TypeScript is {link(API,"packages/contracts/src/schema.d.ts","schema.d.ts")}. Use `npm run contracts:check` to detect drift; this audit does not regenerate application contracts. Planned API work belongs to {link(API,ROAD,"the roadmap")}, never this inventory.\n'
write(API,api)

for module in ['identity_tables','ppm_tables','assessment_tables','command_tables','job_tables','pilot_tables']: importlib.import_module('ppm_api.'+module)
from ppm_api.database import Base
old_db='docs/10-reference/history/DATABASE_DICTIONARY_PRE_AUDIT.md'
write(old_db,rewrite(original['docs/DATABASE-DICTIONARY.md'],'docs/DATABASE-DICTIONARY.md',old_db))
db=f'''# Current source-derived database dictionary

Derived from current SQLAlchemy `Base.metadata` definitions, including pilot tables, without opening a connection. Schema source has migrations 0001–0008. This does not independently inspect the applied runtime schema. Constraints/indexes/RLS installed by migration SQL must also be read in {link(DB,'services/api/migrations/versions','the migration directory')}; metadata alone is not the complete database-policy definition. No migration/schema/data was changed by this audit.

## Important data flows

Organization → membership → transaction-local principal/RLS → domain records. Portfolio/project links constrain work/risks/milestones/allocations; resource profiles differ from login identities. Published framework versions preserve assessment scoring history. Jobs/outbox persist ingestion state. Identity deliveries reference challenge hashes privately. Notification membership references and unique event keys isolate recipients and deduplicate receipts. Optional project/work metadata remains null for unknown historical classification.

For transactional query/debugging steps use {link(DB,L['05-database-explained.md'],'database learning')}; for planned schema changes use {link(DB,ROAD,'roadmap')} marked PLANNED. Historical pre-audit dictionary remains {link(DB,old_db,'an archived snapshot')}.
'''
for t in sorted(Base.metadata.tables.values(),key=lambda t:t.name):
    db+=f'\n## {t.name}\n\n| Column | SQL type | Nullable | Primary key | Foreign reference |\n| --- | --- | --- | --- | --- |\n'
    for c in t.columns: db+=f'| `{c.name}` | `{c.type}` | {c.nullable} | {c.primary_key} | '+(', '.join(f.target_fullname for f in c.foreign_keys) or '—')+' |\n'
    db+='\nMetadata constraints: '+('; '.join(str(c) for c in t.constraints if c.__class__.__name__=='CheckConstraint') or 'Referential/primary/unique definitions below and migrations')+'\n'
    for c in sorted(t.constraints,key=lambda c:str(c.name)):
        if c.__class__.__name__=='CheckConstraint': continue
        db+='\n- '+c.__class__.__name__+' '+str(c.name or '(unnamed)')+': '+', '.join(x.name for x in c.columns)+'\n'
    for idx in sorted(t.indexes,key=lambda i:i.name): db+='\n- Index '+idx.name+': '+', '.join(str(e) for e in idx.expressions)+ (' (unique)' if idx.unique else '')+'\n'
write(DB,db)
p=target('docs/CODE-AND-TEST-INDEX.md')
old_idx='docs/10-reference/history/CODE_INDEX_PRE_AUDIT.md'
write(old_idx,rewrite(original['docs/CODE-AND-TEST-INDEX.md'],'docs/CODE-AND-TEST-INDEX.md',old_idx))
idx='# Current code and test navigation\n\nSource-derived AST inventory, 9 October 2026. Search symbols instead of relying on line numbers; a test definition is not an executed result. Includes current pilot/mail modules and all migrations.\n'
for root in ['services/api','services/worker','tests','scripts']:
    for f in sorted((R/root).rglob('*.py')):
        if '__pycache__' in f.parts: continue
        tree=ast.parse(f.read_text(encoding='utf-8-sig')); symbols=[(n.name,n.lineno) for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
        if not symbols: continue
        rp=f.relative_to(R).as_posix(); idx+=f'\n## {rp}\n\n'+link(p,rp,'Source')+'\n\n'+ '\n'.join(f'- `{name}` — line {ln}' for name,ln in symbols)+'\n'
write(p,idx)

p=target('docs/LOCAL-DEVELOPMENT.md'); s=(R/p).read_text(encoding='utf-8').replace('Migrations `0001_foundation` through `0007_durable_jobs`','Migrations `0001_foundation` through `0008_pilot_completion`').replace('current Sprint 08 local verification does not establish a new hosted run','current Sprint 8.1 local verification does not establish a new hosted run'); write(p,s)
p='docs/07-setup-and-deployment/ENVIRONMENT_VARIABLES.md'
env='# Configuration field reference\n\nVerified against `config.Settings`, Compose and `.env.example` by field name only. No real secret values were read/copied. Local/test/demo are allowed; production is rejected. Setup commands are source-reviewed, not freshly run.\n\n| Variable | Purpose / definition |\n| --- | --- |\n'
tree=ast.parse((R/'services/api/ppm_api/config.py').read_text(encoding='utf-8'))
for n in ast.walk(tree):
    if isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name):
        name=n.target.id; definition=ast.unparse(n.annotation)
        env+=f'| `PPM_{name.upper()}` | {definition}; '+('required' if n.value is None else 'default/validation: `'+ast.unparse(n.value)+'`')+' |\n'
env+='\nAdditional Compose/bootstrap-only configuration keys: '+', '.join('`'+k+'`' for k in sorted(set(re.findall(r'\$\{([A-Z_0-9]+)',(R/'compose.yaml').read_text(encoding='utf-8')))))+'\n\n`API_ORIGIN` is the Next.js server proxy destination. Loopback origins/ports must match CSRF/cookies. Migration credentials belong only to migration tooling; ordinary requests use the app role. SMTP uses STARTTLS and private secrets; real inbox acceptance remains BLOCKED. See [local setup](LOCAL-DEVELOPMENT.md) and [identity operations](IDENTITY-DEVELOPMENT.md).'
write(p,env)
write('docs/08-quality-and-security/KNOWN_LIMITATIONS.md',f'# Quality, security and operational limitations\n\n{link("docs/08-quality-and-security/KNOWN_LIMITATIONS.md",STATUS,"Current limitations")} identifies snapshot bounds, evidence/file transaction limits, notification presentation retention, SSE polling cost and open external/release gates. {link("docs/08-quality-and-security/KNOWN_LIMITATIONS.md",L["06-login-and-permissions.md"],"Security walkthrough")} explains live membership, RLS, roles/grants/ownership and private effort. {link("docs/08-quality-and-security/KNOWN_LIMITATIONS.md",TEST,"Test strategy")} maps negative cases; {link("docs/08-quality-and-security/KNOWN_LIMITATIONS.md",target("docs/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md"),"Release criteria")} retains performance/recovery/accessibility obligations. Existing local checks do not imply independent security certification, production throughput or full recovery acceptance.')

# Large business-facing guide: correct current checkpoint and competing status vocabulary,
# retain unique future explanations, explicitly track remaining section-by-section reconciliation.
p=target('docs/AI_PPM_FUTURE_PRODUCT_VISION_AND_USER_GUIDE.md'); s=(R/p).read_text(encoding='utf-8')
s=s.replace('**Implemented and Verified Today**','**IMPLEMENTED AND VERIFIED**').replace('**Planned for the Complete Product**','**PLANNED**').replace('**Completion Still Needs Confirmation**','**IMPLEMENTED BUT UNVERIFIED**')
pos=s.find('\n'); s=s[:pos]+f'\n\n**Current canonical availability (9 October 2026):** {link(p,STATUS,"current status")}, {link(p,CAT,"feature catalogue")} and {link(p,USER,"executable user steps")}. This long-form product vision retains future business explanations and its dated baseline; Sprint 8.1 is locally implemented with open mail/CI/Word gates. Any older planned statement about core pilot controls is historical, not current availability. Detailed section-by-section reconciliation remains tracked; do not use a future journey as an executable demo.\n'+s[pos:]; write(p,s)

# Compatibility redirects are short and explicitly non-canonical, so no unique content is lost.
resolved=[]
for old,s in original.items():
    if old.startswith('docs/') and len(s)<900 and old not in moves and 'This topic is now taught' in s:
        p=old; write(p,rewrite(s,old,old)+'\n\n**SUPERSEDED compatibility link.** Current availability is in '+link(p,STATUS,'current status')+'.'); resolved.append(p)
p='docs/AI-PPM-MASTER-LEARNING-GUIDE.md'
write(p,f'# AI-PPM learning guide\n\n**SUPERSEDED entry point; no independent canonical content.** Follow {link(p,"docs/02-learning/README.md","the canonical learning index")} and {link(p,"docs/README.md","main documentation index")}. Historical Word/generator assets remain under `docs/learning`; their old snapshots and unverified layout are not current acceptance.'); resolved.append(p)
for folder,body in {
'00-overview':f'Current product: {link("docs/00-overview/README.md",STATUS,"status")}, {link("docs/00-overview/README.md",CAT,"catalogue")}, [documentation guide](DOCUMENTATION_GUIDE.md), [release criteria](FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md).',
'01-architecture':'[Current system](SYSTEM_ARCHITECTURE.md), [actual API](18-api-contracts.md), [current schema](DATABASE-DICTIONARY.md). Established ADRs/contracts remain separately canonical.',
'04-testing':'[Strategy and real commands](TESTING_STRATEGY.md), [gap acceptance plan](GAP_ACCEPTANCE_TEST_PLAN.md), [historical sprint results](sprint-based/README.md), [verification history](SPRINT_VERIFICATION_REPORT.md).',
'05-demos':'[Current walkthrough](CURRENT_DEMO_GUIDE.md), [future outlines](FUTURE_DEMO_PLANS.md), [sprint scenarios](sprint-based/README.md).',
'06-user-guides':'[Current user steps and recovery](USER_GUIDE.md). Future product scenarios belong to the roadmap/vision and are PLANNED.',
'07-setup-and-deployment':'[Local setup](LOCAL-DEVELOPMENT.md), [identity operation](IDENTITY-DEVELOPMENT.md), [configuration fields](ENVIRONMENT_VARIABLES.md). Production deployment is PLANNED; no successful deployment is claimed.',
'09-planning':'[Gap audit](SPRINT_8_1_GAP_AUDIT.md), [historical 8.1 plan](SPRINT_8_1_PLAN.md), [roadmap](FUTURE_SPRINT_ROADMAP.md), [traceability](FEATURE_GAP_TRACEABILITY.md), [tracker](DOCUMENTATION_UPDATE_TRACKER.md), [feature map](FEATURE_DOCUMENT_MAPPING.md), [sprint checklist](SPRINT_DOCUMENTATION_CHECKLIST.md).',
'10-reference':'[Code/test index](CODE-AND-TEST-INDEX.md), [documentation changelog](DOCUMENTATION_CHANGELOG.md), [audit results](DOCUMENTATION_AUDIT_RESULTS.md). `history` holds labeled older snapshots; current inventories are canonical in architecture/reference.',
}.items(): write('docs/'+folder+'/README.md','# '+folder.split('-',1)[1].replace('-',' ').title()+'\n\n'+body)

write('docs/README.md','''# AI-PPM documentation

Audited 9 October 2026. Current source includes local Sprint 8.1 implementation with open parent acceptance; Sprints 09–23 remain PLANNED. Historical reports retain the results they actually recorded. No application behavior was changed by this audit.

1. [What the product does and what exists today](00-overview/CURRENT_STATUS.md); [feature catalogue](00-overview/FEATURE_CATALOGUE.md).
2. [Run it locally](07-setup-and-deployment/LOCAL-DEVELOPMENT.md); [account setup](07-setup-and-deployment/IDENTITY-DEVELOPMENT.md); [configuration](07-setup-and-deployment/ENVIRONMENT_VARIABLES.md).
3. [Understand the architecture](01-architecture/SYSTEM_ARCHITECTURE.md), [actual API](01-architecture/18-api-contracts.md) and [schema](01-architecture/DATABASE-DICTIONARY.md).
4. [Learn the code step by step](02-learning/README.md).
5. [Run meaningful tests](04-testing/TESTING_STRATEGY.md); [original sprint evidence](04-testing/sprint-based/README.md).
6. [Demonstrate current features](05-demos/CURRENT_DEMO_GUIDE.md); [use the application](06-user-guides/USER_GUIDE.md).
7. [Find each sprint’s plan, actual outcome and limitations](03-sprints/README.md).
8. [Understand gaps and remaining product work](09-planning/SPRINT_8_1_GAP_AUDIT.md), [future roadmap](09-planning/FUTURE_SPRINT_ROADMAP.md) and [release criteria](00-overview/FINAL_PRODUCT_SCOPE_AND_RELEASE_CRITERIA.md).
9. [Close active Sprint 8.1 gates](03-sprints/active/sprint-8.1/README.md); [planned Sprint 09](03-sprints/planned/sprint-09/README.md).

[Documentation organization/status rules](00-overview/DOCUMENTATION_GUIDE.md) · [Update tracker and remaining work](09-planning/DOCUMENTATION_UPDATE_TRACKER.md) · [Feature-to-document map](09-planning/FEATURE_DOCUMENT_MAPPING.md) · [Maintenance checklist](09-planning/SPRINT_DOCUMENTATION_CHECKLIST.md) · [Audit checks](10-reference/DOCUMENTATION_AUDIT_RESULTS.md).
''')

# Preserve historical verification wording by labeling its date, not changing executed results.
p=target('docs/SPRINT_VERIFICATION_REPORT.md'); s=(R/p).read_text(encoding='utf-8').replace('## Current state and evidence','## Historical Sprint 08 state and evidence').replace('Latest implemented sprint: **08**','Historical checkpoint latest implemented sprint: **08**'); write(p,s)
for p in ['docs/architecture/overview.md','docs/architecture/data-model.md','docs/planning/PRODUCT-REUSE-AND-SCREEN-PLAN.md','docs/planning/SPRINT-PLAN-GAP-REVIEW.md','docs/requirements/roadmap.md']:
    s=(R/p).read_text(encoding='utf-8'); loc=s.find('\n'); s=s[:loc]+f'\n\n**Historical/proposed reference:** Current availability is {link(p,STATUS,"CURRENT_STATUS")}; current architecture is {link(p,ARCH,"SYSTEM_ARCHITECTURE")}; future execution order is {link(p,ROAD,"the revised roadmap")}. Preserve dated decisions/scope below; proposed components are not implementation claims.\n'+s[loc:]; write(p,s)
p='README.md'; s=(R/p).read_text(encoding='utf-8'); pos=s.find('\n'); s=s[:pos]+'\n\n[Canonical documentation index](docs/README.md) · [Current scope and open gates](docs/00-overview/CURRENT_STATUS.md) · [Documentation tracker](docs/09-planning/DOCUMENTATION_UPDATE_TRACKER.md)\n'+s[pos:]; write(p,s)

# Legacy generated artifacts are preserved and blocked/archived explicitly rather than silently regenerated.
write('docs/learning/README.md','''# Legacy learning artifacts and generators

**ARCHIVED / not current canonical guides.** These generators, manifests and Word outputs were retained byte-for-byte. Their snapshots may contain earlier paths/status/line numbers; do not rerun them over reviewed Markdown guides. The generated website testing Word guide has an open visual QA gate (missing renderer in prior execution). No Word content/layout was inspected or revalidated in this Markdown audit.

Use [canonical learning](../02-learning/README.md), [current user steps](../06-user-guides/USER_GUIDE.md) and [tracker](../09-planning/DOCUMENTATION_UPDATE_TRACKER.md). Generator migration and every-page Word reconciliation/rendering remain BLOCKED/PLANNED work, not a completed guide update.
''')

deep=set(moves)|set('docs/'+k for k in learn)|{'README.md','docs/contracts/pilot.md','docs/contracts/jobs-integrations.md','docs/contracts/permissions.md'}
tracker=f'''# Documentation update tracker

Audit date: 9 October 2026. Every existing Markdown file was inventoried and screened for links/status/sprint headings; rows distinguish detailed correction from retained historical/reference content and incomplete exhaustive review. This is a prioritized safe pass, not a claim that every paragraph of large legacy documents or Word output has been validated. Current checks are in {link(TRACK,'docs/10-reference/DOCUMENTATION_AUDIT_RESULTS.md','audit results')}.

| Document | Canonical path | Type | Current accuracy | Required changes | Related feature/gap IDs | Sprint association | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
'''
allpaths=sorted(set(original)|set(p.relative_to(R).as_posix() for p in D.rglob('*.md')))
for old in allpaths:
    new=target(old)
    if old!=new and new in original: continue
    if old not in original and old in moves.values(): continue
    if old in moves: state='UPDATED BUT UNVERIFIED'; accuracy='Content retained; paths/current annotations corrected'; action='Read historical scope separately; runtime claims rely on retained evidence'
    elif old in resolved: state='SUPERSEDED'; accuracy='Compatibility link only'; action='Use linked canonical guide'
    elif old.startswith('docs/source/') or (old.startswith('docs/prompts/') and not old.endswith('/MASTER.md')): state='REVIEWED — NO CHANGE NEEDED'; accuracy='Frozen scope/prompt reference; not runtime authority'; action='Preserve byte-for-byte; revised plan owns future order'
    elif old in changed: state='UPDATED BUT UNVERIFIED'; accuracy='Source-reviewed content; local evidence linked'; action='Complete runtime/visual acceptance only where required'
    else: state='REVIEWED — NO CHANGE NEEDED'; accuracy='Structural/link screening; retained historical/reference purpose'; action='Detailed semantic review when owning feature changes'
    if old== 'docs/AI_PPM_FUTURE_PRODUCT_VISION_AND_USER_GUIDE.md': state='PLANNED'; accuracy='Current header/status corrected; large baseline still partly stale'; action='Reconcile all detailed journeys/catalogue paragraphs against current code and map'
    if '/history/' in new: state='ARCHIVED'; accuracy='Historical snapshot'; action='Do not use as current inventory'
    if old.startswith('docs/contracts/') or old.startswith('docs/architecture/adr/'):
        accuracy='Existing interface/design decision, links reviewed; full clause audit pending'; action='Check every current/proposed clause against owning source on next feature change'; state='UPDATED BUT UNVERIFIED' if old in changed else 'PLANNED'
    if old in ['docs/requirements/coverage.md','docs/requirements/quality-plan.md','docs/requirements/product-scope.md']: state='PLANNED'; action='Full requirement-by-requirement semantic reconciliation beyond path/status screening'
    assoc=re.search(r'sprint-(\d{2}|8\.1)',new,re.I); assoc=assoc[1] if assoc else 'cross-sprint / unverified association'
    typ='history/evidence' if any(x in new for x in ('completed/','TESTING_REPORT','verification/','HANDOFF','history/')) else 'planning' if 'planning/' in new or 'planned/' in new else 'guide/reference'
    refs='G-001–010, G-034–036' if '8.1' in new or '/02-learning/' in new else 'See FEATURE_DOCUMENT_MAPPING (all 156 requirements / 36 gaps)'
    tracker+=f'| {Path(old).name} | {link(TRACK,new,new)} | {typ} | {accuracy} | {action} | {refs} | {assoc} | {state} |\n'
for f in sorted((D/'learning').iterdir()):
    if not f.is_file() or f.suffix=='.md': continue
    p=f.relative_to(R).as_posix(); state='BLOCKED' if f.suffix=='.docx' else 'ARCHIVED'
    tracker+=f'| {f.name} | {link(TRACK,p,p)} | Legacy Word/generator/manifest | Not content/layout verified in this audit | Preserve; reconcile output/generator paths then render and inspect every Word page | G-010 | Association unverified; not current authority | {state} |\n'
tracker+='''
## Remaining work and exact boundaries

- Long-form future product vision: current status override and vocabulary were corrected, but every business journey/table paragraph still needs a full semantic pass; canonical current user steps/catalogue cover the safe executable scope.
- Existing contracts, ADRs and requirement collections: screened and linked, preserved unique content; exhaustive current-versus-proposed clause reconciliation remains a distinct tracked task. Original acceptance obligations were not weakened.
- Legacy Word/generator assets: preserved; outputs not rendered/inspected here, older path manifests may remain stale. Update generators only in a separate reviewed documentation pass, then render all pages before accepting Word guides.
- Full browser/integration/migration/provider/hosted CI/load/deployment acceptance was not rerun. This audit runs only documentation checks and safe unit/source checks. SMTP, current hosted CI and Word layout remain open Sprint 8.1 gates.
- Frozen original prompt/source links remain historical; source paths in them are not automatically rewritten. Raw verification logs/screenshots/JSON retain original locations/checkpoints and do not become current documentation just because they exist.

Every planned Sprint 09–23 README lists affected documentation and links the shared checklist. The feature map contains all original crosswalk rows plus all gaps. No planned feature is claimed executed by that map.
'''
write(TRACK,tracker)

summary={'existing_markdown_screened':len([p for p in original if p.startswith('docs/')]),'moved':len(moves),'redirects_resolved':len(resolved),'routes':route_count,'tables':len(Base.metadata.tables),'requirements':len(req_rows),'gaps':len(gap_rows),'moves':moves,'changed_paths':sorted(changed)}
(R/'artifacts/documentation-audit/changes.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k not in ('moves','changed_paths')},indent=2))
