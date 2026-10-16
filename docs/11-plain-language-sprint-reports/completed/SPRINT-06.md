# Sprint 06 — Assessing how well teams work

**Status:** Completed locally for the questionnaire, scoring and review process.

## What was built and why it matters

An Admin can define a maturity questionnaire, give different topics different importance, and ask one person to answer it and another to review it. Scores keep the questionnaire version that produced them, so editing next year's questions does not rewrite last year's result.

Open **Maturity assessments** at [Assessments](http://localhost:3000/assessments).

| Delivered function | Where to find it | How to check / expected result |
| --- | --- | --- |
| Build a questionnaire/framework | **Framework library → Create framework**. | Add dimensions (topics), weights and questions. A valid draft saves; invalid weights or incomplete required fields are rejected. |
| Editable starting examples | Framework library examples for PMO, Agile, governance and delivery. | Load an example and inspect/edit its questions before publishing. Examples are guidance, not completed organizational assessments. |
| Yes/no, rubric and text answers | Question **Answer type** in the framework editor. | Create suitable questions and inspect the corresponding respondent controls. Text does not pretend to be a numeric score. |
| Publish a preserved version | Framework **Publish** control, Admin only. | Publish a valid framework. Later draft edits do not modify the published version. |
| Assign an assessment | **Assign assessment**, then **Create assignment**. | Select a published version and two different active eligible Admin/PM members. Self-review and Viewer participant assignments are rejected. |
| Answer, attach evidence notes and save a draft | Open the assigned assessment as respondent. | Enter answers and notes; wait for **Draft saved** or use **Save answers**. Reload and check the saved draft. |
| Submit and independently review | Assessment workflow controls. | Respondent submits; assigned reviewer starts review and can return it with reasons or complete it after requirements are met. |
| Explain score adjustments | Reviewer answer controls: adjusted score and reason. | Enter a permitted adjustment with a reason. The score/history records the change; a reason is required. |
| Attach and release private evidence | Question attachment control, then reviewer preview/release. | Upload a small UTF-8 TXT, have the reviewer preview/release it with a reason, and then complete review. Unreleased attachments block completion. |
| Read scores, coverage and history | Open the assessment result. | Inspect dimension/overall scores, answer coverage, evidence coverage and history. Coverage of evidence presence is not a judgement of its quality. |
| Compare departments fairly | **Department comparison**. | Compare completed permitted assessments using the same published version. A different framework version is not mixed into the comparison. |

## A simple end-to-end check

**You need:** An Admin, a respondent and a different reviewer with eligible active roles. The Admin can also be one participant where allowed, but no person reviews their own response. See [Getting access](../START_HERE.md).

1. As Admin, create or load an example, finish its required fields and publish it.
2. Assign that version to the practice respondent and reviewer.
3. As respondent, answer all required questions, add evidence notes and wait for the saved indicator.
4. Submit with a note.
5. As reviewer, start review. Return it with a specific correction, then have the respondent correct and resubmit.
6. Complete review with a note after any attached files are released.
7. Edit and republish the framework draft; reopen the completed assessment.

**Expected result:** The status follows the answer/review process, the completed result shows scores and history, and the old result still refers to its original published version.

For a full worked example with framework fields and people, follow the assessment sections of the [website walkthrough](../../06-user-guides/WEBSITE_WALKTHROUGH.md).

## Where it was implemented

| Part | Implementation files |
| --- | --- |
| Framework editor, answers, review and score screens | [Assessment screen](../../../apps/web/components/assessments.tsx) |
| Assignment, scoring, permissions and workflow | [Assessment service](../../../services/api/ppm_api/assessment.py) |
| Preserved versions and assessment history | [Assessment tables](../../../services/api/ppm_api/assessment_tables.py), [assessment migration](../../../services/api/migrations/versions/0005_assessment.py) |
| Browser check | [Assessment scenario](../../../tests/browser/assessment.spec.ts) |

## Recorded checks, later changes and limits

The sprint recorded 49 backend tests and a final targeted browser pass for the completed workflow. Original evidence attachments are TXT only, up to 512 KiB, with at most 50 per assessment. Reviewer release is a human review step, not an antivirus scan.

Access-sharing controls and broader paging arrived in [Sprint 8.1](../completed/SPRINT-8.1.md). The separate multi-format library and same-file assessment links arrived in [Sprint 09](SPRINT-09.md). Neither replaces this private assessment workflow. AI scoring and automatic semantic findings were not delivered here.

[Original report](../../03-sprints/completed/sprint-06/SPRINT_REPORT.md) · [Recorded testing](../../04-testing/sprint-based/sprint-06/TESTING_REPORT.md) · [Report index](../README.md)
