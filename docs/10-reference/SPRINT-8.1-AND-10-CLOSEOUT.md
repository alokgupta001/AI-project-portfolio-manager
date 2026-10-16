# Sprint 8.1 and Sprint 10 development closeout

16 October 2026. **Both sprints are COMPLETED for their implemented development
scope.** Their canonical homes and ordinary-language reports now live under
`completed`. This resolves stale active-folder and hosted-CI statements without
claiming production certification or future agent/model accuracy.

## Acceptance disposition

| Work | Current disposition | Evidence |
| --- | --- | --- |
| PPM-81-001 and 003–009 | Completed locally; original test/preservation results retained | [Pilot report](../03-sprints/completed/sprint-8.1/SPRINT_REPORT.md) and [task records](../04-testing/sprint-based/sprint-8.1/README.md) |
| PPM-81-002 development email journeys | Completed for signup, existing-account Viewer invitation acceptance and recovery in the configured development environment | [Actual Gmail/recipient/website verification](../04-testing/ACCOUNT_EMAIL_VERIFICATION.md); this is not a claim about every production template or deliverability target |
| PPM-81-010 guide, regression and reviewed checkpoint | Completed for the development pilot | [Successful hosted CI](https://github.com/alokgupta001/AI-project-portfolio-manager/actions/runs/38885041673) at application commit `631c149`; retained scratch restore/preservation results; [current Word guide](../03-sprints/completed/sprint-8.1/SPRINT_8_1_USER_GUIDE.docx) and [Markdown guide](../03-sprints/completed/sprint-8.1/SPRINT_8_1_USER_GUIDE.md) |
| PPM-10-001 provider, embeddings and limits | Completed for the bounded gateway | [Real Gemini completion and 256-dimension embedding smoke](../verification/gemini-free-tier-smoke.json), [provider/fallback regression](../04-testing/sprint-based/sprint-10/GEMINI-FOLLOWUP.md), zero-dollar/key-bound/model/request controls |
| PPM-10-002 typed orchestration and protected tools | Completed for fixed read-only branches | [201-test review-fix evidence](../verification/coderabbit-review-fixes.json), including cancellation/lease accounting, replay, tenant/role denial and source revocation coverage |
| PPM-10-003 operations and evaluation gates | Completed for Admin operations and the versioned evaluation harness | [Original scope and executed tests](../04-testing/sprint-based/sprint-10/TESTING_REPORT.md); twelve predeclared deterministic support/citation/completion/leakage/unsupported-number cases are rerun in [closeout evidence](../verification/sprint-8.1-10-closeout.json) |

Sprint 10's source prompt requires a common provider/runtime, failure/authorization
tests, versioned evaluation fixtures and thresholds before evaluating production
agents. Its bounded configured-provider smoke is already verified. Nine-agent
quality evaluation and production-scale retrieval are successor/release obligations,
not capabilities supplied by the extractive gateway. The original requirement rows
for semantic findings remain partial; no acceptance threshold or planned feature
was silently changed to completed.

## Word guide correction and visual verification

The packaged renderer could not run on Windows because `soffice.exe` is absent.
The same renderer was run in a temporary local Linux QA image using free
LibreOffice. Rendering ran with networking disabled and mounted only the input
guide and private QA output directory; no credentials, database or application
volumes were mounted.

The historical website-testing Word snapshot has stale setup instructions and a
pagination defect. Its bytes are preserved. A current pilot edition was generated
from the reviewed Markdown guide with nine clearly separated workflow sections,
current development email guidance and corrected links. Both final pages were
visually inspected: text, headings, links and page numbers are readable, with no
clipping, overlap, title border or footer collision. The current edition supersedes
that old snapshot for the pilot guide acceptance. Other archived learning books
remain historical artifacts rather than newly validated current instructions.

## GitHub and local verification boundaries

The successful hosted workflow is tied to **application commit `631c149`**, not
to these later uncommitted documentation edits. Its reviewed application source is
preserved by this closeout. The six original CodeRabbit findings were verified,
fixed and resolved; their local full backend run passed 201 tests and the affected
document browser scenario passed. Those runs are retained evidence, not reruns by
this documentation task.

New closeout checks cover folder uniqueness, required artifacts, local links and
anchors, generated documentation inventories, frozen source hashes, whitespace,
Word structure/render/visual QA, deterministic evaluation and protected-file hashes.
Actual results and normalized hashes are recorded in
[machine-readable evidence](../verification/sprint-8.1-10-closeout.json).

No real AI provider request, new email delivery, deployment, normal data mutation
or paid service was used in this closeout. Gemini authorization remains maximum
spend **$0**; confirmation does not expire daily. Stop before 11.

## Retained release and successor gates

[The acceptance register](../09-planning/RELEASE-ACCEPTANCE-REGISTER.md) keeps broad
agent/model quality, real-world retrieval scale, production identity/email,
storage/erasure/recovery, accessibility/performance and deployment requirements
explicitly OPEN. Moving a development sprint into completed does not pass those
release gates or authorize Sprint 11 implementation.
