# Sprint 12.1 ordinary guided-review timeout follow-up

30 October 2026. The owner explicitly approved up to 60 seconds for ordinary
guided reviews after the earlier experiment reached its fixed 22-second deadline.
This is a local runtime change, not another accuracy experiment or Sprint 13.

## Behavior and scope

New ordinary cloud guided runs record `guided_cloud_timeout_seconds` in immutable
run versions. The default is 60, configurable within 1–60 through
`PPM_AI_GUIDED_CLOUD_TIMEOUT_SECONDS`. A worker may reduce the recorded limit when
the current setting is lower; it cannot silently extend the recorded policy.
Legacy runs without this field retain 22 seconds. Fixture pilots and other analysis
modes retain the existing local completion setting, capped at 22 seconds.

The runtime issues an internal permit with the admitted timeout. The adapter checks
the task and ordinary guided prompt before allowing more than 22 seconds, checks
the permit bound, and limits execution to the earlier of the request timeout and
permit expiry. An unavailable response still produces the usable rules-only
checklist. Elapsed failure time and unknown usage remain honestly recorded.

Forward migration **0020_guided_cloud_timeout** changes the admission function only.
Longer admission requires an ordinary guided run with a recorded numeric policy,
no pilot ID, a cloud provider, and at least the request duration plus five seconds
remaining in the existing 90-second run deadline. It retains the grant/session/RLS
checks, ten-second heartbeat, one generation slot, one/minute pacing, shared
50/day/provider ceiling and $0 policy. A 60-second admission reserves its slot for
65 seconds; successful settlement releases the slot immediately. There is still
only one optional request per guided run. No automatic retry or provider switch.

The two stopped fixture pilots and their 22-second deadline/20-second acceptance
gate are unchanged. Their results are not pooled or relabeled. **AT17 remains
BLOCKED**. Waiting longer can accept a slower response; it does not establish that
Gemini is faster, reliably available or accurate.

## Evidence and validation

The controlled offline adapter test accepts a response after an actual 23-second
wait. Other tests check permit expiry/unknown outcome, rejected over-limit requests,
legacy/local/fixture boundaries, frozen configuration and reduced operator limits.
Integration checks cover app-role guided admission, a 65-second in-flight quota
slot, immediate release on completion, rejected 61-second admission, denied
60-second fixture admission and existing access/revocation controls.

The full guarded run completed **580 passed, 2 failed, 1 skipped**, with one
inherited Starlette warning in 782.10 seconds. Both failures were in the new test:
it inspected slot expiry after successful settlement had already released the
slot. The assertion was moved to the in-flight callback and settlement is now
checked separately. This test correction did not change runtime behavior.
The disposable migration lifecycle 0020 → 0006 → 0020 → base → 0020 → 0020 and
schema-drift check passed. Static/contracts and local image builds passed.

Windows unit execution encountered sandbox temporary-directory problems and was
aborted; the same tests ran in the guarded Linux suite. Interrupted test containers
are not counted as passes. The corrected focused run passed **28 tests in 189.43
seconds**, including both previously failing cases; it overlaps the full suite.
The other 580 passes remain applicable because only the test assertions changed.
This is not reported as a second all-green full-suite run. Two isolated browser
journeys passed in **46.0 seconds**, including visible 60-second guidance and
unchanged pilot review/stop/report behavior. No provider inference was used.

## Use and limitations

In Agents, choose an approved project, use **Guided review · limited, one API call**
and select a role. Start a new ordinary run to use the new policy; opening a saved
run does not change its policy or make another call. The page explains the longer
wait and the separate fixture deadline. The shared run deadline includes queue and
preparation time, so a late job can be rejected before contacting a provider.

No new provider inference is used to validate this change. Live completion within
60 seconds remains unverified; the exact cause of the previous Gemini delay is
still unresolved. Previous diagnostic logs covered only two of six repair calls.
No keys, approved egress scope, model/prompt, label, access or usage history changed.
No commit, PR, push, production deployment or Sprint 13 work is included.

## Local activation and preservation

Normal 0019 → **0020** completed on 30 October. All **83 table hashes** matched
before and after migration; **24 configuration/applied-migration hashes** and
**134 prior evidence/tooling file hashes** matched. The migration alters only the
admission function. The running API and worker both report guided cloud 60 seconds,
other completion 22 seconds and total run 90 seconds. Calls and quota reservations
remain at twelve each: no additional inference occurred.

The normal signed-in Agents page displays the new guidance and retained history;
no browser warnings/errors were observed. The two isolated browser journeys used
the repository Playwright runner because the Browser plugin was unavailable.
The normal page was inspected with the available in-app browser tooling.
The documentation inventory and link checks passed, including 13 prior sprint
packages/115 artifacts. The tracker, handoff, guides, contracts, coverage and
limitations now point to this follow-up; older dated results remain historical.

[Validation and preservation receipt](../../../verification/sprint12_1/timeout-followup/validation.json) ·
[Running UI screenshot](../../../verification/sprint12_1/timeout-followup/ordinary-guided.png).

[Approved scope](../../../09-planning/sprint-12.1/TIMEOUT_FOLLOWUP_PROPOSAL.md) ·
[Earlier timing repair and stopped experiment](REPAIR_FOLLOWUP.md).
