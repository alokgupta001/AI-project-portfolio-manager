"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { apiError } from "./api-error";
import type { components } from "@ppm/contracts/schema";
import { Button, Field, Modal, ChartFrame } from "./ui";

type S = components["schemas"];
type Framework = S["FrameworkRecord"];
type Definition = S["FrameworkInput-Input"];
type Dimension = S["Dimension-Input"];
type Question = S["Question-Input"];
type Assessment = S["AssessmentRecord"];
type Detail = S["AssessmentDetail"];
type Answer = S["AnswerInput"];
type Version = S["VersionRecord"];
import { AssessmentAccess, DepartmentComparison } from "./pilot";
import { RecordSelect } from "./record-select";
const base = "/api/v1/assessment";
const number = (n: string | number | null) =>
  n == null ? "Unknown" : Number(n).toFixed(2);
const blankQuestion = (): Question => ({
  id: crypto.randomUUID(),
  name: "New question",
  text: "Describe the practice",
  answer_type: "boolean",
  weight: "1",
  required: true,
  rubric_levels: [],
});
const blankDimension = (): Dimension => ({
  id: crypto.randomUUID(),
  name: "New dimension",
  description: "",
  weight: "1",
  questions: [blankQuestion()],
});
const blank = (): Definition => ({
  name: "New framework",
  description: "",
  category: "custom",
  archived: false,
  dimensions: [blankDimension()],
});

export function Assessments({
  account,
  transport,
}: {
  account: S["AccountView"];
  transport: typeof fetch;
}) {
  const [frameworks, setFrameworks] = useState<Framework[]>([]);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [, setPeople] = useState<S["PersonView"][]>([]);
  const [departments, setDepartments] = useState<S["RecordView"][]>([]);
  const [, setTeams] = useState<S["RecordView"][]>([]);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [editor, setEditor] = useState<Definition | null>(null);
  const [editing, setEditing] = useState<Framework | null>(null);
  const [versions, setVersions] = useState<Version[]>([]);
  const listRequest = useRef(0);
  const [assessmentOffset, setAssessmentOffset] = useState(0);
  const [assessmentQuery, setAssessmentQuery] = useState("");
  const [frameworkOffset, setFrameworkOffset] = useState(0);
  const [assignVersion, setAssignVersion] = useState("");
  const [detail, setDetail] = useState<Detail | null>(null);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [dirty, setDirty] = useState(false);
  const [events, setEvents] = useState<S["EventRecord"][]>([]);
  const [evidence, setEvidence] = useState<S["EvidenceRecord"][]>([]);
  const [reviewNote, setReviewNote] = useState("");
  const [adjustments, setAdjustments] = useState<
    Record<string, { score: string; note: string }>
  >({});
  const [previews, setPreviews] = useState<Record<string, string>>({});
  const saving = useRef(false);
  const admin = account.role === "Admin";

  const api = useCallback(
    async <T,>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const headers: Record<string, string> = {};
      if (method !== "GET") {
        headers["content-type"] = "application/json";
        headers["idempotency-key"] = crypto.randomUUID();
      }
      if (revision != null) headers["if-match"] = String(revision);
      const r = await transport(
        new Request(window.location.origin + path, {
          method,
          headers,
          body: body === undefined ? undefined : JSON.stringify(body),
        }),
      );
      if (!r.ok) {
        const e = await r.json().catch(() => null);
        throw new Error(apiError(e, r.status));
      }
      return r.json();
    },
    [transport],
  );

  const load = useCallback(async () => {
    const request = ++listRequest.current;
    const [f, a, p, d, t] = await Promise.all([
      api<Framework[]>(base + `/frameworks?offset=${frameworkOffset}`),
      api<Assessment[]>(
        base +
          `/assessments?limit=25&offset=${assessmentOffset}&q=${encodeURIComponent(assessmentQuery)}`,
      ),
      api<S["PersonView"][]>("/api/v1/delivery/people"),
      api<S["PageView"]>("/api/v1/delivery/departments"),
      api<S["PageView"]>("/api/v1/delivery/teams"),
    ]);
    if (request !== listRequest.current) return;
    setFrameworks(f);
    setAssessments(a);
    setPeople(p);
    setDepartments(d.items);
    setTeams(t.items);
  }, [api, assessmentOffset, assessmentQuery, frameworkOffset]);
  useEffect(() => {
    let active = true;
    load()
      .then(async () => {
        const id = new URLSearchParams(window.location.search).get(
          "assessment",
        );
        if (id) {
          const a = await api<Detail>(`${base}/assessments/${id}`);
          if (active) await open(a.assessment);
        }
      })
      .catch((e) => {
        if (active) setError(String(e.message));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [load]);

  async function act(fn: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await fn();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }
  async function open(a: Assessment) {
    const d = await api<Detail>(`${base}/assessments/${a.id}`);
    setDetail(d);
    setAnswers(
      d.answers.map((r) => ({
        question_id: r.question_id,
        value: r.value,
        evidence_text: r.evidence_text,
      })),
    );
    setDirty(false);
    setReviewNote("");
    setAdjustments({});
    if (d.assessment.can_read_evidence) {
      const [h, e] = await Promise.all([
        api<S["EventRecord"][]>(`${base}/assessments/${a.id}/events`),
        api<S["EvidenceRecord"][]>(`${base}/assessments/${a.id}/evidence`),
      ]);
      setEvents(h);
      setEvidence(e);
    } else {
      setEvents([]);
      setEvidence([]);
    }
  }
  const save = useCallback(async () => {
    if (!detail || !dirty || saving.current) return;
    saving.current = true;
    setBusy(true);
    setError("");
    try {
      const updated = await api<Detail>(
        `${base}/assessments/${detail.assessment.id}/answers`,
        "PUT",
        { items: answers },
        detail.assessment.revision,
      );
      setDetail(updated);
      setDirty(false);
      setNotice("Draft saved.");
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      setDirty(true);
      setNotice(
        "Draft was not saved. Your answers remain here; reload before retrying a conflict.",
      );
    } finally {
      saving.current = false;
      setBusy(false);
    }
  }, [detail, dirty, answers, api, load]);
  useEffect(() => {
    if (!dirty || error) return;
    const timer = setTimeout(() => {
      void save();
    }, 900);
    return () => clearTimeout(timer);
  }, [dirty, error, save]);

  function changeAnswer(
    q: Question | S["Question-Output"],
    value: string,
    evidenceText?: string,
  ) {
    const old = answers.find((a) => a.question_id === q.id);
    setAnswers((a) => [
      ...a.filter((r) => r.question_id !== q.id),
      {
        question_id: q.id!,
        value,
        evidence_text: evidenceText ?? old?.evidence_text ?? "",
      },
    ]);
    setDirty(true);
    setNotice("Unsaved changes…");
  }
  function updateDimension(i: number, change: Partial<Dimension>) {
    setEditor(
      (e) =>
        e && {
          ...e,
          dimensions: (e.dimensions || []).map((d, j) =>
            i === j ? { ...d, ...change } : d,
          ),
        },
    );
  }
  function updateQuestion(i: number, j: number, change: Partial<Question>) {
    const d = editor!.dimensions![i];
    updateDimension(i, {
      questions: (d.questions || []).map((q, k) =>
        k === j ? { ...q, ...change } : q,
      ),
    });
  }
  async function upload(qid: string, file?: File) {
    if (!file || !detail) return;
    if (file.size > 524288 || !file.name.endsWith(".txt"))
      throw new Error("Choose a UTF-8 .txt file up to 512 KiB.");
    const bytes = new Uint8Array(await file.arrayBuffer());
    let binary = "";
    bytes.forEach((b) => {
      binary += String.fromCharCode(b);
    });
    await api(
      `${base}/assessments/${detail.assessment.id}/evidence`,
      "POST",
      { question_id: qid, file_name: file.name, content_base64: btoa(binary) },
      detail.assessment.revision,
    );
    await open(detail.assessment);
    await load();
  }
  async function transition(action: string) {
    if (!detail) return;
    const a = detail.assessment;
    const payload =
      action === "submit"
        ? { note: reviewNote }
        : {
            action,
            note: reviewNote,
            adjustments: Object.entries(adjustments)
              .filter(([, v]) => v.score !== "")
              .map(([id, v]) => ({
                answer_id: id,
                reviewer_score: v.score,
                reviewer_note: v.note,
              })),
          };
    const updated = await api<Assessment>(
      `${base}/assessments/${a.id}/${action === "submit" ? "submit" : "review"}`,
      "POST",
      payload,
      a.revision,
    );
    await open(updated);
    await load();
    setNotice(`Assessment ${updated.status.replaceAll("_", " ")}.`);
  }
  const current = detail?.assessment;
  const deptName = (id: string | null | undefined) =>
    departments.find((d) => d.id === id)?.data.name ||
    (id ? "Department" : "Organization");

  return (
    <section className="assessment-workspace">
      <header className="page-heading">
        <p className="eyebrow">CAPABILITY & GOVERNANCE</p>
        <h1>Maturity assessments</h1>
        <p>
          Assess practices against a published framework. Review evidence and
          agree on improvements.
        </p>
      </header>
      {error && (
        <div className="panel" role="alert">
          <strong>Action could not be completed</strong>
          <p>{error}</p>
          <Button
            onClick={() =>
              void act(async () => {
                await load();
                if (current) await open(current);
              })
            }
          >
            Reload current data
          </Button>
        </div>
      )}
      <p role="status" aria-live="polite">
        {loading ? "Loading assessments…" : notice}
      </p>
      <div className="assessment-columns">
        <section className="panel">
          <h2>Framework library</h2>
          <button
            disabled={!frameworkOffset}
            onClick={() => setFrameworkOffset(frameworkOffset - 100)}
          >
            Previous frameworks
          </button>
          <button
            disabled={frameworks.length < 100}
            onClick={() => setFrameworkOffset(frameworkOffset + 100)}
          >
            Next frameworks
          </button>
          <p>
            Current page of frameworks. Examples are editable product guidance,
            not certified models.
          </p>
          {admin && (
            <div className="button-row">
              <Button
                disabled={busy}
                onClick={() => {
                  setEditing(null);
                  setEditor(blank());
                }}
              >
                Create framework
              </Button>
              <Button
                variant="secondary"
                disabled={busy}
                onClick={() =>
                  void act(async () => {
                    await api(base + "/seed-examples", "POST", {});
                    await load();
                    setNotice("Four example frameworks are available.");
                  })
                }
              >
                Add example frameworks
              </Button>
            </div>
          )}
          {!loading && !frameworks.length && (
            <p>
              No frameworks yet. An administrator can create one or add
              examples.
            </p>
          )}
          {frameworks.map((f) => (
            <article className="assessment-card" key={f.id}>
              <h3>{f.name}</h3>
              <p>{f.description}</p>
              <p>
                {f.archived
                  ? "Archived"
                  : f.published_version
                    ? `Published version ${f.published_version}`
                    : "Draft — not published"}
              </p>
              <div className="button-row">
                {f.can_edit && (
                  <Button
                    variant="secondary"
                    disabled={busy}
                    onClick={() => {
                      setEditing(f);
                      setEditor({
                        name: f.name,
                        description: f.description,
                        category: f.category,
                        archived: f.archived,
                        dimensions: f.dimensions,
                      });
                    }}
                  >
                    Edit draft
                  </Button>
                )}
                {admin && !f.archived && (
                  <Button
                    disabled={busy}
                    onClick={() =>
                      void act(async () => {
                        await api(
                          `${base}/frameworks/${f.id}/publish`,
                          "POST",
                          {},
                          f.revision,
                        );
                        await load();
                        setNotice(
                          "Published a new immutable version. Existing assessments retain their original version.",
                        );
                      })
                    }
                  >
                    Publish version
                  </Button>
                )}
                {admin && f.published_version && !f.archived && (
                  <Button
                    variant="secondary"
                    disabled={busy}
                    onClick={() =>
                      void act(async () => {
                        const v = await api<Version[]>(
                          `${base}/frameworks/${f.id}/versions`,
                        );
                        setVersions(v);
                        setAssignVersion(v[0].id);
                      })
                    }
                  >
                    Assign assessment
                  </Button>
                )}
              </div>
              <AssessmentAccess
                transport={transport}
                account={account}
                frameworkId={f.id}
              />
            </article>
          ))}
        </section>
        <section className="panel">
          <h2>Assessments</h2>
          <p>
            Current page of permitted records. Completed results use their
            original published version.
          </p>
          <label>
            Find assessments
            <input
              type="search"
              maxLength={160}
              value={assessmentQuery}
              onChange={(e) => {
                setAssessmentQuery(e.target.value);
                setAssessmentOffset(0);
              }}
            />
          </label>
          <button
            disabled={!assessmentOffset}
            onClick={() => setAssessmentOffset(assessmentOffset - 25)}
          >
            Previous assessments
          </button>
          <button
            disabled={assessments.length < 25}
            onClick={() => setAssessmentOffset(assessmentOffset + 25)}
          >
            Next assessments
          </button>
          {!loading && !assessments.length && (
            <p>No assigned assessments yet.</p>
          )}
          {assessments.map((a) => (
            <article className="assessment-card" key={a.id}>
              <h3>{a.name}</h3>
              <p>
                {deptName(a.department_id)} · {a.framework_name} v
                {a.framework_version}
              </p>
              <p>
                {a.status.replaceAll("_", " ")} ·{" "}
                {a.provisional ? "Provisional" : "Approved"} score:{" "}
                {number(a.overall_score)} / 100
              </p>
              <Button
                variant="secondary"
                disabled={busy || dirty}
                onClick={() => void act(() => open(a))}
              >
                Open {a.name}
              </Button>
            </article>
          ))}
        </section>
      </div>
      {detail && current && (
        <section className="panel">
          <h2>{current.name}</h2>
          <p>
            {current.framework_name}, version {current.framework_version} ·{" "}
            {current.status.replaceAll("_", " ")} ·{" "}
            {current.provisional
              ? "Provisional until independent review"
              : "Completed and preserved"}
          </p>
          <ChartFrame
            title="Dimension scores"
            description="Scores range from 0 to 100; higher means stronger capability. Weight coverage measures valid answers. Evidence coverage counts questions with notes or attachments."
            table={
              <div
                className="table-scroll"
                tabIndex={0}
                role="region"
                aria-label="Scrollable dimension score table"
              >
                <table>
                  <caption>Assessment scores and coverage</caption>
                  <thead>
                    <tr>
                      <th>Dimension</th>
                      <th>Score / 100</th>
                      <th>Weight</th>
                      <th>Answer weight coverage %</th>
                      <th>Evidence coverage %</th>
                    </tr>
                  </thead>
                  <tbody>
                    {current.dimension_scores.map((d) => (
                      <tr key={d.dimension_id}>
                        <th>{d.dimension_name}</th>
                        <td>{number(d.score)}</td>
                        <td>{d.weight}</td>
                        <td>{number(d.coverage_percent)}</td>
                        <td>{number(d.evidence_coverage_percent)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            }
          >
            {current.dimension_scores.map((d) => (
              <div className="assessment-score" key={d.dimension_id}>
                <span>
                  {d.dimension_name}: {number(d.score)}
                </span>
                <div className="assessment-track">
                  <div
                    style={{
                      width: `${Math.max(0, Math.min(100, Number(d.score || 0)))}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </ChartFrame>
          {detail.notes.length > 0 && (
            <p role="status">Incomplete: {detail.notes.join("; ")}</p>
          )}
          <p>
            Overall score:{" "}
            <strong>{number(current.overall_score)} / 100</strong>. Each numeric
            answer is normalized to 0–100, weighted within its dimension, then
            multiplied by the dimension weight. Missing answers remain
            provisional; text answers require human review and receive no
            numeric score.
          </p>
          {current.can_read_evidence && (
            <fieldset disabled={busy}>
              <legend>Answers and supporting evidence</legend>
              {detail.snapshot.dimensions?.map((d) => (
                <section key={d.id}>
                  <h3>{d.name}</h3>
                  {d.questions?.map((q) => {
                    const a = answers.find((v) => v.question_id === q.id);
                    const stored = detail.answers.find(
                      (v) => v.question_id === q.id,
                    );
                    return (
                      <article className="assessment-card" key={q.id}>
                        <Field
                          label={`${q.name}${q.required ? " (required)" : ""}`}
                          hint={q.text}
                        >
                          {q.answer_type === "text" ? (
                            <textarea
                              value={a?.value || ""}
                              disabled={!current.can_answer}
                              onChange={(e) => changeAnswer(q, e.target.value)}
                            />
                          ) : (
                            <select
                              value={a?.value || ""}
                              disabled={!current.can_answer}
                              onChange={(e) => changeAnswer(q, e.target.value)}
                            >
                              <option value="">Not answered</option>
                              {q.answer_type === "boolean" ? (
                                <>
                                  <option value="true">Yes</option>
                                  <option value="false">No</option>
                                </>
                              ) : (
                                q.rubric_levels?.map((l) => (
                                  <option key={l.level} value={l.level}>
                                    {l.level} — {l.label}
                                  </option>
                                ))
                              )}
                            </select>
                          )}
                        </Field>
                        <Field label={`Evidence notes for ${q.name}`}>
                          <textarea
                            value={a?.evidence_text || ""}
                            disabled={!current.can_answer}
                            onChange={(e) =>
                              changeAnswer(q, a?.value || "", e.target.value)
                            }
                          />
                        </Field>
                        {stored?.reviewer_score != null && (
                          <p>
                            Reviewer score: {stored.reviewer_score}. Reason:{" "}
                            {stored.reviewer_note}
                          </p>
                        )}
                        {current.can_review &&
                          stored &&
                          q.answer_type !== "text" && (
                            <div className="form-grid">
                              <Field label={`Adjusted score for ${q.name}`}>
                                <input
                                  type="number"
                                  min="0"
                                  max="100"
                                  step="0.0001"
                                  value={adjustments[stored.id]?.score || ""}
                                  onChange={(e) =>
                                    setAdjustments((s) => ({
                                      ...s,
                                      [stored.id]: {
                                        score: e.target.value,
                                        note: s[stored.id]?.note || "",
                                      },
                                    }))
                                  }
                                />
                              </Field>
                              <Field label={`Adjustment reason for ${q.name}`}>
                                <input
                                  value={adjustments[stored.id]?.note || ""}
                                  onChange={(e) =>
                                    setAdjustments((s) => ({
                                      ...s,
                                      [stored.id]: {
                                        score: s[stored.id]?.score || "",
                                        note: e.target.value,
                                      },
                                    }))
                                  }
                                />
                              </Field>
                            </div>
                          )}
                        {evidence
                          .filter((e) => e.question_id === q.id)
                          .map((e) => (
                            <div key={e.id}>
                              <p>
                                {e.released ? (
                                  <a
                                    href={`${base}/assessments/${current.id}/evidence/${e.id}`}
                                    download
                                  >
                                    {e.file_name}
                                  </a>
                                ) : (
                                  <strong>{e.file_name} — quarantined</strong>
                                )}{" "}
                                · {e.file_size} bytes
                              </p>
                              {e.released && (
                                <p
                                  className="muted"
                                  style={{ overflowWrap: "anywhere" }}
                                >
                                  Reusable document attachment reference: {e.id}
                                </p>
                              )}
                              <div className="button-row">
                                <Button
                                  variant="secondary"
                                  onClick={() =>
                                    void act(async () => {
                                      const text = await api<{ note: string }>(
                                        `${base}/assessments/${current.id}/evidence/${e.id}/preview`,
                                      );
                                      setPreviews((p) => ({
                                        ...p,
                                        [e.id]: text.note,
                                      }));
                                    })
                                  }
                                >
                                  Preview {e.file_name}
                                </Button>
                                {current.can_review && !e.released && (
                                  <Button
                                    disabled={!reviewNote || !previews[e.id]}
                                    onClick={() =>
                                      void act(async () => {
                                        await api(
                                          `${base}/assessments/${current.id}/evidence/${e.id}/release`,
                                          "POST",
                                          { note: reviewNote },
                                          current.revision,
                                        );
                                        await open(current);
                                        setNotice(
                                          "Text evidence released after independent review.",
                                        );
                                      })
                                    }
                                  >
                                    Release {e.file_name}
                                  </Button>
                                )}
                                {current.can_answer && (
                                  <Button
                                    variant="secondary"
                                    disabled={dirty}
                                    onClick={() =>
                                      void act(async () => {
                                        await api(
                                          `${base}/assessments/${current.id}/evidence/${e.id}`,
                                          "DELETE",
                                          undefined,
                                          current.revision,
                                        );
                                        await open(current);
                                      })
                                    }
                                  >
                                    Remove {e.file_name}
                                  </Button>
                                )}
                              </div>
                              {previews[e.id] && (
                                <pre className="evidence-preview">
                                  {previews[e.id]}
                                </pre>
                              )}
                            </div>
                          ))}
                        {current.can_answer && (
                          <Field
                            label={`Attach evidence for ${q.name}`}
                            hint="UTF-8 plain text (.txt), up to 512 KiB. Uploads are quarantined. An independent reviewer must preview and release the text before download."
                          >
                            <input
                              type="file"
                              accept=".txt,text/plain"
                              disabled={dirty}
                              onChange={(e) => {
                                const file = e.target.files?.[0];
                                void act(() => upload(q.id!, file));
                                e.target.value = "";
                              }}
                            />
                          </Field>
                        )}
                      </article>
                    );
                  })}
                </section>
              ))}
            </fieldset>
          )}
          {(current.can_answer || current.can_review) && (
            <>
              <Field label="Review or submission note">
                <textarea
                  value={reviewNote}
                  onChange={(e) => setReviewNote(e.target.value)}
                  disabled={busy}
                />
              </Field>
              <div className="button-row">
                {current.can_answer && (
                  <>
                    <Button
                      disabled={busy || !dirty}
                      onClick={() => void save()}
                    >
                      Save answers
                    </Button>
                    <Button
                      disabled={busy || dirty}
                      onClick={() => void act(() => transition("submit"))}
                    >
                      Submit for review
                    </Button>
                  </>
                )}
                {current.can_review && (
                  <>
                    {current.status === "submitted" && (
                      <Button
                        disabled={busy || !reviewNote}
                        onClick={() => void act(() => transition("start"))}
                      >
                        Start review
                      </Button>
                    )}
                    <Button
                      variant="secondary"
                      disabled={busy || !reviewNote}
                      onClick={() => void act(() => transition("return"))}
                    >
                      Return for changes
                    </Button>
                    <Button
                      disabled={busy || !reviewNote}
                      onClick={() => void act(() => transition("complete"))}
                    >
                      Complete review
                    </Button>
                  </>
                )}
              </div>
            </>
          )}
          {current.status === "completed" && (
            <AssessmentAccess
              transport={transport}
              account={account}
              assessmentId={current.id}
            />
          )}
          <DepartmentComparison
            transport={transport}
            version={current.framework_version_id}
          />
          {current.can_read_evidence && (
            <>
              <h3>History</h3>
              {events.map((e) => (
                <details key={e.id}>
                  <summary>
                    {e.event.replaceAll("_", " ")} ·{" "}
                    {new Date(e.created_at).toLocaleString()}
                  </summary>
                  <p>{e.note || "Assessment record updated."}</p>
                </details>
              ))}
            </>
          )}
        </section>
      )}
      <Modal
        open={!!editor}
        onClose={() => {
          if (!busy) setEditor(null);
        }}
        title={editing ? "Edit framework draft" : "Create framework"}
      >
        {editor && (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void act(async () => {
                await api(
                  editing
                    ? `${base}/frameworks/${editing.id}`
                    : `${base}/frameworks`,
                  editing ? "PUT" : "POST",
                  editor,
                  editing?.revision,
                );
                setEditor(null);
                await load();
                setNotice("Framework draft saved. Publish when ready.");
              });
            }}
          >
            <fieldset disabled={busy}>
              {error && <p role="alert">{error}</p>}
              <Field label="Framework name">
                <input
                  required
                  value={editor.name}
                  onChange={(e) =>
                    setEditor({ ...editor, name: e.target.value })
                  }
                />
              </Field>
              <Field label="Description">
                <textarea
                  value={editor.description}
                  onChange={(e) =>
                    setEditor({ ...editor, description: e.target.value })
                  }
                />
              </Field>
              <Field label="Category">
                <select
                  value={editor.category}
                  onChange={(e) =>
                    setEditor({
                      ...editor,
                      category: e.target.value as Definition["category"],
                    })
                  }
                >
                  {["custom", "pmo", "agile", "governance", "delivery"].map(
                    (c) => (
                      <option key={c}>{c}</option>
                    ),
                  )}
                </select>
              </Field>
              <p>
                Dimension weights must total 1 before publishing. Each dimension
                needs a numeric question; rubric questions need at least two
                distinct levels.
              </p>
              {editor.dimensions?.map((d, i) => (
                <fieldset key={d.id}>
                  <legend>Dimension {i + 1}</legend>
                  <Field label={`Dimension ${i + 1} name`}>
                    <input
                      required
                      value={d.name}
                      onChange={(e) =>
                        updateDimension(i, { name: e.target.value })
                      }
                    />
                  </Field>
                  <Field label={`Dimension ${i + 1} weight`}>
                    <input
                      type="number"
                      min="0.00001"
                      max="1"
                      step="0.00001"
                      required
                      value={d.weight}
                      onChange={(e) =>
                        updateDimension(i, { weight: e.target.value })
                      }
                    />
                  </Field>
                  {d.questions?.map((q, j) => (
                    <fieldset key={q.id}>
                      <legend>Question {j + 1}</legend>
                      <Field label={`Question ${i + 1}.${j + 1} name`}>
                        <input
                          required
                          value={q.name}
                          onChange={(e) =>
                            updateQuestion(i, j, { name: e.target.value })
                          }
                        />
                      </Field>
                      <Field label="Question prompt">
                        <textarea
                          required
                          value={q.text}
                          onChange={(e) =>
                            updateQuestion(i, j, { text: e.target.value })
                          }
                        />
                      </Field>
                      <Field label="Answer type">
                        <select
                          value={q.answer_type}
                          onChange={(e) =>
                            updateQuestion(i, j, {
                              answer_type: e.target
                                .value as Question["answer_type"],
                              rubric_levels:
                                e.target.value === "rubric"
                                  ? [
                                      {
                                        level: 0,
                                        label: "Not demonstrated",
                                        description: "",
                                      },
                                      {
                                        level: 1,
                                        label: "Demonstrated",
                                        description: "",
                                      },
                                    ]
                                  : [],
                            })
                          }
                        >
                          <option value="boolean">Yes / no</option>
                          <option value="rubric">Rubric level</option>
                          <option value="text">Text (not scored)</option>
                        </select>
                      </Field>
                      <Field label="Question weight">
                        <input
                          type="number"
                          min="0.00001"
                          max="1000"
                          step="0.00001"
                          required
                          value={q.weight}
                          onChange={(e) =>
                            updateQuestion(i, j, { weight: e.target.value })
                          }
                        />
                      </Field>
                      <label>
                        <input
                          type="checkbox"
                          checked={q.required}
                          onChange={(e) =>
                            updateQuestion(i, j, { required: e.target.checked })
                          }
                        />{" "}
                        Required answer
                      </label>
                      {q.answer_type === "rubric" && (
                        <>
                          {q.rubric_levels?.map((l, k) => (
                            <div className="form-grid" key={k}>
                              <Field label={`Level ${k + 1} value`}>
                                <input
                                  type="number"
                                  min="0"
                                  max="1000"
                                  required
                                  value={l.level}
                                  onChange={(e) =>
                                    updateQuestion(i, j, {
                                      rubric_levels: q.rubric_levels!.map(
                                        (v, n) =>
                                          n === k
                                            ? {
                                                ...v,
                                                level: Number(e.target.value),
                                              }
                                            : v,
                                      ),
                                    })
                                  }
                                />
                              </Field>
                              <Field label={`Level ${k + 1} label`}>
                                <input
                                  required
                                  value={l.label}
                                  onChange={(e) =>
                                    updateQuestion(i, j, {
                                      rubric_levels: q.rubric_levels!.map(
                                        (v, n) =>
                                          n === k
                                            ? { ...v, label: e.target.value }
                                            : v,
                                      ),
                                    })
                                  }
                                />
                              </Field>
                              <Button
                                type="button"
                                variant="secondary"
                                onClick={() =>
                                  updateQuestion(i, j, {
                                    rubric_levels: q.rubric_levels!.filter(
                                      (_, n) => n !== k,
                                    ),
                                  })
                                }
                              >
                                Remove level {k + 1}
                              </Button>
                            </div>
                          ))}
                          <Button
                            type="button"
                            variant="secondary"
                            onClick={() =>
                              updateQuestion(i, j, {
                                rubric_levels: [
                                  ...(q.rubric_levels || []),
                                  {
                                    level: q.rubric_levels?.length || 0,
                                    label: "New level",
                                    description: "",
                                  },
                                ],
                              })
                            }
                          >
                            Add rubric level
                          </Button>
                        </>
                      )}
                      <Button
                        type="button"
                        variant="secondary"
                        onClick={() =>
                          updateDimension(i, {
                            questions: d.questions!.filter((_, k) => k !== j),
                          })
                        }
                      >
                        Remove question {j + 1}
                      </Button>
                    </fieldset>
                  ))}
                  <div className="button-row">
                    <Button
                      type="button"
                      onClick={() =>
                        updateDimension(i, {
                          questions: [...(d.questions || []), blankQuestion()],
                        })
                      }
                    >
                      Add question
                    </Button>
                    <Button
                      type="button"
                      variant="secondary"
                      onClick={() =>
                        setEditor({
                          ...editor,
                          dimensions: editor.dimensions!.filter(
                            (_, j) => j !== i,
                          ),
                        })
                      }
                    >
                      Remove dimension {i + 1}
                    </Button>
                  </div>
                </fieldset>
              ))}
              <div className="button-row">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() =>
                    setEditor({
                      ...editor,
                      dimensions: [
                        ...(editor.dimensions || []),
                        blankDimension(),
                      ],
                    })
                  }
                >
                  Add dimension
                </Button>
                <Button type="submit">Save framework draft</Button>
              </div>
            </fieldset>
          </form>
        )}
      </Modal>
      <Modal
        open={versions.length > 0}
        onClose={() => {
          if (!busy) setVersions([]);
        }}
        title="Assign assessment"
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            const f = new FormData(e.currentTarget);
            void act(async () => {
              await api(base + "/assessments", "POST", {
                name: f.get("name"),
                framework_version_id: assignVersion,
                department_id: f.get("department") || null,
                team_id: f.get("team") || null,
                assigned_to: f.get("respondent"),
                reviewer_id: f.get("reviewer"),
              });
              setVersions([]);
              await load();
              setNotice("Assessment assigned.");
            });
          }}
        >
          <fieldset disabled={busy}>
            {error && <p role="alert">{error}</p>}
            <Field label="Assessment name">
              <input name="name" required />
            </Field>
            <Field label="Published version">
              <select
                value={assignVersion}
                onChange={(e) => setAssignVersion(e.target.value)}
              >
                {versions.map((v) => (
                  <option key={v.id} value={v.id}>
                    Version {v.version}
                  </option>
                ))}
              </select>
            </Field>
            <RecordSelect
              transport={transport}
              kind="departments"
              label="Department"
              name="department"
            />
            <RecordSelect
              transport={transport}
              kind="teams"
              label="Team"
              name="team"
            />
            <p>Choose different active Admin or Project Manager members.</p>
            <RecordSelect
              transport={transport}
              kind="people"
              label="Respondent"
              name="respondent"
              required
            />
            <RecordSelect
              transport={transport}
              kind="people"
              label="Independent reviewer"
              name="reviewer"
              required
            />
            <Button type="submit">Create assignment</Button>
          </fieldset>
        </form>
      </Modal>
    </section>
  );
}
