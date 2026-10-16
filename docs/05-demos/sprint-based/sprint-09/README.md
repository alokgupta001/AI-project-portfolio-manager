# Sprint 09 current document demo

**CURRENT DEMO**, backed by the isolated browser acceptance in
[the testing report](../../../04-testing/sprint-based/sprint-09/TESTING_REPORT.md).
Do not seed or purge established normal data to run this exercise. Use the existing
isolated demo/test organization and separate Admin/PM/Viewer profiles. Operators
start the [scanner/runtime](../../../07-setup-and-deployment/DOCUMENT-PROCESSING.md);
members follow [the full user steps](../../../03-sprints/completed/sprint-09/USER_GUIDE.md).
No default accounts/passwords or new normal demo records are supplied.

1. Admin gives the PM project edit/manage and Viewer project read on a fictional
   project. PM opens **Document library**, selects that project and `charter`, and
   uploads UTF-8 `charter.txt` containing `Cedar launch evidence. Sponsor reviews scope.`
   Store and process; wait for Ready. Missing scanner must show quarantine, not success.
2. Open preview, inspect paragraph/location and download. Compare the original bytes.
   Search `Cedar`, open the cited location and verify its version. Viewer can read the
   permitted source and has no upload/edit action. An unrelated organization cannot read it.
3. PM appends changed bytes containing `Cedar revised scope`. Confirm the new version
   and latest-version search. Original history stays distinct. Repeat identical bytes
   and confirm no duplicate version. Source text is escaped, never a tool instruction.
4. For the evidence bridge, use an independently released assessment TXT attachment
   with identical bytes, copy its reference from Assessments and link its ready library
   version with both required authorities. Saved scores/coverage stay unchanged. Viewer
   must not gain private attachment access from a public document reference.
5. Admin uploads a fictional organization-wide `policy`, selects a ready version,
   active owner, applicability, dates and state. Show UTC review/effective labels;
   approval workflow is unavailable until Sprint 15.
6. In synthetic fixtures only, show hold/retention refusal, then eligible logical
   delete and explicit purge. Confirm preview/search/tickets fail after deletion.
   Orphan preview/purge must preserve referenced/held versions, including archived
   projects. The automated fixture controls eligibility dates; never shorten a real
   hold to make this demonstration succeed.

The accepted Playwright flow also exercises 1440/768/360 widths and automated WCAG-tag
checks; [screenshots](../../../verification/sprint09-documents-360.png) show the
focusable horizontally scrollable table at small width. Eight synthetic keyword
queries returned their expected source/location; no semantic or production relevance
claim follows. Freshly performed demos should record actual results separately.
Embeddings/hybrid retrieval, agents and semantic findings remain FUTURE DEMO PLAN
for Sprints 10/11; policy approvals remain 15.
