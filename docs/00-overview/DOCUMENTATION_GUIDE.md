# Documentation guide

Start at [the documentation index](../README.md). Current status is authoritative for today's availability; source and verified behavior outrank documentation. Retained test logs prove only their recorded checkpoint. Plans prove intended scope.

## Organization and canonical locations

| Location | Purpose |
| --- | --- |
| 00-overview | Current scope/status, catalogue, vision and release criteria |
| 01-architecture | Current component, API and database explanations |
| 02-learning | Practical cross-sprint code walkthroughs and learning entry points |
| 03-sprints/completed/sprint-NN | Reports/handoffs for Sprints 00–09, with each sprint’s actual local acceptance limits |
| 03-sprints/active/sprint-8.1 and sprint-10 | Open parent/model-quality acceptance with local and bounded provider evidence recorded |
| 03-sprints/planned/sprint-NN | Intended outcome, links to canonical roadmap and required documentation changes; no execution reports |
| 04-testing | Strategy, current instructions and original sprint-specific test reports |
| 05-demos | Current reproducible walkthroughs and clearly labeled future outlines |
| 06-user-guides | Current user steps; detailed 8.1 tester guide linked rather than duplicated |
| 07-setup-and-deployment | Local setup and identity operation |
| 08-quality-and-security | Current limitations and acceptance boundaries |
| 09-planning | Gap audit, plans, roadmap, tracker, feature mappings and sprint checklist |
| 10-reference | Source-derived inventories, changelog and historical generated snapshots |
| 11-plain-language-sprint-reports | Business explanations and user-check steps for completed/local prior sprint scope |

Each sprint-specific folder has a README. Reports, testing evidence, demos and learning notes have one canonical home; topic/sprint indexes link to it. Zero-pad whole sprint numbers, retain `sprint-8.1`, and preserve Sprint 00. A later sprint extends history; it does not rewrite a past test outcome.

## Deliberate deviations

The established `architecture/adr`, `contracts`, `requirements`, `source` and `prompts` trees remain in place because they are referenced scope/decision/interface collections. Frozen source and original prompt copies remain unchanged. `verification` retains raw logs, screenshots and JSON with stable paths; human test reports moved to testing sprint folders. `learning` retains legacy generators and Word artifacts as historical/unverified outputs; do not run older generators over canonical guides. Existing short chapter redirects remain compatibility links, with no independent canonical claim.

Sprint 8.1 is **active**, because implementation and genuine evidence already exist while parent acceptance remains open. Calling those records wholly PLANNED would erase verified work. Its original requirements remain a labeled historical plan; Sprint 09 is locally implemented under `03-sprints/completed/sprint-09`; its former planned compatibility entry has been removed after updating internal links. Sprint 10 is implemented with bounded Gemini smoke acceptance and open broader quality gates; Sprints 11–23 are PLANNED. No future test or implementation report was fabricated.

## Status vocabulary and maintenance

Use IMPLEMENTED AND VERIFIED, IMPLEMENTED BUT UNVERIFIED, PARTIALLY IMPLEMENTED, BROKEN, PLANNED, BLOCKED and NOT IN SCOPE in current documents. Historical labels (COMPLETE, PARTIAL, VERIFIED COMPLETE, NOT IMPLEMENTED, UNVERIFIED, NOT REQUIRED) retain their original meaning; the current catalogue translates them with scope. Demo labels are CURRENT DEMO, FUTURE DEMO PLAN or BLOCKED. Future test cases say PLANNED TEST — NOT YET EXECUTED.

When moving a guide, rebase its links and callers, preserve unique content, and update the tracker. Run link/source/preservation checks and record actual results. Follow [the sprint checklist](../09-planning/SPRINT_DOCUMENTATION_CHECKLIST.md) and [feature mapping](../09-planning/FEATURE_DOCUMENT_MAPPING.md). Do not edit unrelated guides for an unrelated small change.
