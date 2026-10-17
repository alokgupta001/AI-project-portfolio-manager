"use client";
import { useCallback, useEffect, useState } from "react";
import type { components } from "@ppm/contracts/schema";
import { apiError } from "./api-error";
import { Button, Field, StatePanel } from "./ui";
import { RecordSelect } from "./record-select";

type S = components["schemas"];
type Analysis = S["AnalysisView"];
type Summary = S["AnalysisSummary"];
type Item = S["FindingView"] | S["SuggestionView"];
const terminal = new Set([
  "succeeded",
  "partially_succeeded",
  "failed",
  "cancelled",
]);

export function Agents({
  account,
  transport,
}: {
  account: S["AccountView"];
  transport: typeof fetch;
}) {
  const [runs, setRuns] = useState<Summary[]>([]);
  const [selected, setSelected] = useState<Analysis | null>(null);
  const [definitions, setDefinitions] = useState<S["AgentDefinition"][]>([]);
  const [project, setProject] = useState("");
  const [assessment, setAssessment] = useState("");
  const [assessments, setAssessments] = useState<S["AssessmentRecord"][]>([]);
  const [documents, setDocuments] = useState<S["DocumentView"][]>([]);
  const [versions, setVersions] = useState<string[]>([]);
  const [item, setItem] = useState<Item | null>(null);
  const [reason, setReason] = useState("");
  const [approved, setApproved] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [offset, setOffset] = useState(0);
  const admin = account.role === "Admin";
  const api = useCallback(
    async <T,>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const response = await transport(
        new Request(window.location.origin + "/api/v1" + path, {
          method,
          headers: {
            "content-type": "application/json",
            "idempotency-key": crypto.randomUUID(),
            ...(revision === undefined ? {} : { "if-match": String(revision) }),
          },
          body: body === undefined ? undefined : JSON.stringify(body),
        }),
      );
      if (!response.ok)
        throw new Error(
          apiError(await response.json().catch(() => null), response.status),
        );
      return response.json();
    },
    [transport],
  );
  const refresh = useCallback(async () => {
    const [values, defs] = await Promise.all([
      api<Summary[]>(`/agents/runs?offset=${offset}`),
      api<S["AgentDefinition"][]>("/agents/definitions"),
    ]);
    setRuns(values);
    setDefinitions(defs);
  }, [api, offset]);
  useEffect(() => {
    let live = true;
    void refresh()
      .catch((e) => {
        if (live) setError(e.message);
      })
      .finally(() => {
        if (live) setLoading(false);
      });
    return () => {
      live = false;
    };
  }, [refresh]);
  useEffect(() => {
    let live = true;
    if (admin)
      void api<S["AssessmentRecord"][]>("/assessment/assessments")
        .then((x) => {
          if (live) setAssessments(x.filter((a) => a.can_read_evidence));
        })
        .catch((e) => {
          if (live) setError(e.message);
        });
    return () => {
      live = false;
    };
  }, [api, admin]);
  useEffect(() => {
    let live = true;
    setVersions([]);
    setDocuments([]);
    if (project)
      void Promise.all([
        api<S["DocumentPage"]>(
          "/documents?" +
            new URLSearchParams({ project_id: project, limit: "100" }),
        ),
        api<S["DocumentPage"]>("/documents?limit=100"),
      ])
        .then(([projectSources, allSources]) => {
          if (live)
            setDocuments([
              ...projectSources.items,
              ...allSources.items.filter(
                (d) => d.project_id === null && d.category === "policy",
              ),
            ]);
        })
        .catch((e) => {
          if (live) setError(e.message);
        });
    return () => {
      live = false;
    };
  }, [api, project]);
  const activeId = selected?.run.id;
  useEffect(() => {
    if (!activeId) return;
    let live = true;
    // Revalidate completed evidence too; a saved result does not retain revoked source access.
    const timer = setInterval(() => {
      void api<Analysis>(`/agents/runs/${activeId}`)
        .then((x) => {
          if (live) {
            setSelected(x);
            setItem((old) =>
              old
                ? ([...x.findings, ...x.suggestions].find(
                    (v) => v.key === old.key,
                  ) ?? null)
                : null,
            );
          }
        })
        .catch((e) => {
          if (live) {
            setSelected(null);
            setItem(null);
            setError(e.message);
          }
        });
    }, 1500);
    return () => {
      live = false;
      clearInterval(timer);
    };
  }, [api, activeId]);
  async function act(fn: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await fn();
      await refresh();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  function choose(value: Item) {
    setItem(value);
    setReason("");
    setApproved("");
  }
  async function review(decision: "accepted" | "rejected") {
    if (!selected || !item) return;
    await act(async () => {
      const result = await api<Analysis>(
        `/agents/runs/${selected.run.id}/reviews/${encodeURIComponent(item.key)}`,
        "POST",
        {
          decision,
          reason,
          approved_score:
            decision === "accepted" && "dimension_id" in item && approved !== ""
              ? approved
              : null,
        },
        item.review_revision,
      );
      setSelected(result);
      setItem(
        [...result.findings, ...result.suggestions].find(
          (x) => x.key === item.key,
        ) ?? null,
      );
      setReason("");
    });
  }
  return (
    <div className="agent-workspace">
      <header className="panel">
        <p className="eyebrow">Evidence and intelligence · Sprint 11</p>
        <h1>Agents & recommendation center</h1>
        <p>
          Nine read-only specialists propose evidence-backed candidates.
          Acceptance records human review. Use normal project forms for any
          later change.
        </p>
        <p>
          Real-provider semantic quality: <strong>UNVERIFIED/BLOCKED</strong>.
          Confidence is separate from maturity.
        </p>
      </header>
      {loading && <p role="status">Loading specialist runs…</p>}
      {error && (
        <StatePanel kind="error" title="Analysis unavailable">
          {error}
        </StatePanel>
      )}
      <Button disabled={busy} onClick={() => void act(refresh)}>
        Refresh recommendations
      </Button>
      {admin ? (
        <form
          className="panel"
          onSubmit={(e) => {
            e.preventDefault();
            void act(async () => {
              const result = await api<Analysis>("/agents/runs", "POST", {
                project_id: project,
                version_ids: versions,
                assessment_id: assessment || null,
              });
              setSelected(result);
              setItem(null);
            });
          }}
        >
          <h2>Start a scoped analysis</h2>
          <RecordSelect
            label="Analysis project"
            kind="projects"
            value={project}
            onChange={setProject}
            transport={transport}
            required
          />
          <Field label="Assessment (optional)">
            <select
              value={assessment}
              onChange={(e) => setAssessment(e.target.value)}
            >
              <option value="">No private assessment</option>
              {assessments.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name}
                </option>
              ))}
            </select>
          </Field>
          <fieldset>
            <legend>Ready document evidence (up to five)</legend>
            <p>
              Shows the first 100 project sources and organization policies from
              the latest 100 permitted library entries.
            </p>
            {documents.length === 0 && (
              <p>No project sources loaded. Metrics remain available.</p>
            )}
            {documents.map((d) => {
              const v = d.versions[0];
              return v?.status === "ready" ? (
                <label key={d.id}>
                  <input
                    type="checkbox"
                    checked={versions.includes(v.id)}
                    disabled={!versions.includes(v.id) && versions.length >= 5}
                    onChange={(e) =>
                      setVersions((old) =>
                        e.target.checked
                          ? [...old, v.id]
                          : old.filter((x) => x !== v.id),
                      )
                    }
                  />{" "}
                  {d.title} · version {v.number}
                </label>
              ) : null;
            })}
          </fieldset>
          <Button type="submit" disabled={busy || !project}>
            Run nine specialists
          </Button>
          <p>
            Existing provider settings, request limits, budget, retries and
            cancellation apply. Missing providers produce explicit fallback.
          </p>
        </form>
      ) : (
        <StatePanel kind="empty" title="Read and review access">
          Starting analysis requires Admin. Independent project editors or
          assigned assessment reviewers can review permitted results.
        </StatePanel>
      )}
      <section className="panel">
        <h2>Analysis runs</h2>
        {!loading && runs.length === 0 && (
          <p>No permitted specialist runs on this page.</p>
        )}
        <div
          className="table-scroll"
          tabIndex={0}
          role="region"
          aria-label="Analysis runs table"
        >
          <table>
            <caption>Latest 25 permitted runs · offset {offset}</caption>
            <thead>
              <tr>
                <th>Run</th>
                <th>Status</th>
                <th>Semantic result</th>
                <th>Open</th>
              </tr>
            </thead>
            <tbody>
              {runs.map((r) => (
                <tr key={r.run.id}>
                  <td>
                    {r.run.id.slice(0, 8)} ·{" "}
                    {new Date(r.run.created_at).toLocaleString()}
                  </td>
                  <td>{r.run.status}</td>
                  <td>{r.semantic_status}</td>
                  <td>
                    <Button
                      disabled={busy}
                      onClick={() =>
                        void act(async () => {
                          setSelected(
                            await api<Analysis>(`/agents/runs/${r.run.id}`),
                          );
                          setItem(null);
                        })
                      }
                    >
                      Open run {r.run.id.slice(0, 8)}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Button
          disabled={offset === 0 || busy}
          onClick={() => setOffset((x) => Math.max(0, x - 25))}
        >
          Previous runs
        </Button>
        <Button
          disabled={runs.length < 25 || offset >= 10000 || busy}
          onClick={() => setOffset((x) => x + 25)}
        >
          Next runs
        </Button>
      </section>
      {selected && (
        <section className="panel">
          <h2>Run details</h2>
          <p role="status">
            Execution: {selected.run.status} · Semantic result:{" "}
            {selected.semantic_status}
          </p>
          <p>
            Provider: {selected.run.provider} · Model:{" "}
            {selected.run.model ?? "unavailable"} · Charge USD{" "}
            {selected.run.charged_usd}
          </p>
          <p>
            Prompt {selected.prompt_version} · Rule {selected.rule_version} ·
            Framework {selected.framework_version_id ?? "not selected"} ·
            Assessment revision {selected.assessment_revision ?? "not selected"}
          </p>
          <p>
            Source snapshot SHA-256:{" "}
            <code>{selected.source_snapshot_sha256}</code>
          </p>
          <ul>
            {selected.limitations.map((x, i) => (
              <li key={i}>{x}</li>
            ))}
          </ul>
          <h3>Specialist outcomes</h3>
          <div
            className="table-scroll"
            tabIndex={0}
            role="region"
            aria-label="Specialist outcomes table"
          >
            <table>
              <caption>
                Missing semantic agents:{" "}
                {selected.missing_agents.join(", ") || "none"}
              </caption>
              <thead>
                <tr>
                  <th>Agent</th>
                  <th>Outcome</th>
                  <th>Limitation</th>
                </tr>
              </thead>
              <tbody>
                {selected.agents.map((a) => (
                  <tr key={a.agent}>
                    <th>{a.agent}</th>
                    <td>{a.status}</td>
                    <td>{a.code ?? "Supported by cited sources"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <details>
            <summary>Live processing stages</summary>
            <ol aria-label="Processing stages">
              {selected.stages.map((s) => (
                <li key={s.sequence}>
                  {s.stage} · {new Date(s.occurred_at).toLocaleTimeString()}
                </li>
              ))}
            </ol>
          </details>
          {admin && !terminal.has(selected.run.status) && (
            <Button
              disabled={busy}
              onClick={() =>
                void act(async () => {
                  await api(
                    `/ai/runs/${selected.run.id}/cancel`,
                    "POST",
                    {},
                    selected.run.revision,
                  );
                  setSelected(
                    await api<Analysis>(`/agents/runs/${selected.run.id}`),
                  );
                })
              }
            >
              Cancel specialist run
            </Button>
          )}
          <h3>Recommendations and discrepancies</h3>
          {selected.findings.length === 0 && (
            <p>
              No supported candidate findings. Missing evidence is not a clean
              bill of health.
            </p>
          )}
          <div
            className="table-scroll"
            tabIndex={0}
            role="region"
            aria-label="Recommendations table"
          >
            <table>
              <caption>
                Review candidates; accepted does not mean applied
              </caption>
              <thead>
                <tr>
                  <th>Candidate</th>
                  <th>Severity</th>
                  <th>Support confidence</th>
                  <th>Discrepancy</th>
                  <th>Review</th>
                </tr>
              </thead>
              <tbody>
                {selected.findings.map((f) => (
                  <tr key={f.key}>
                    <td>
                      {f.title} · {f.kind} · {f.signal}
                      <br />
                      {f.agents.join(", ")}
                    </td>
                    <td>{f.severity}</td>
                    <td>{f.confidence} (0–1)</td>
                    <td>
                      {f.discrepancy
                        ? "Conflicting evidence / reported health"
                        : "None detected"}
                      {f.conflicts.length > 0 && (
                        <p>Conflicts: {f.conflicts.join(", ")}</p>
                      )}
                    </td>
                    <td>
                      <Button onClick={() => choose(f)}>
                        Review candidate {f.key.slice(0, 6)}
                      </Button>
                      <p>
                        {f.available
                          ? (f.reviews.at(-1)?.decision ?? "Pending")
                          : "Evidence stale or revoked"}
                      </p>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <h3>Suggested semantic maturity</h3>
          {!selected.assessment_id && (
            <p>No private assessment selected for this run.</p>
          )}
          <div
            className="table-scroll"
            tabIndex={0}
            role="region"
            aria-label="Maturity comparison table"
          >
            <table>
              <caption>
                Maturity scores 0–100 · confidence 0–1 shown separately
              </caption>
              <thead>
                <tr>
                  <th>Dimension</th>
                  <th>Original deterministic</th>
                  <th>AI suggestion</th>
                  <th>Reviewer approved</th>
                  <th>Confidence</th>
                  <th>Review</th>
                </tr>
              </thead>
              <tbody>
                {selected.suggestions.map((s) => (
                  <tr key={s.key}>
                    <th>{s.dimension_name}</th>
                    <td>{s.original_score ?? "Unknown"}</td>
                    <td>{s.suggested_score ?? "Unavailable"}</td>
                    <td>{s.approved_score ?? "No approved score"}</td>
                    <td>{s.confidence ?? "Unknown"}</td>
                    <td>
                      <Button onClick={() => choose(s)}>
                        Review dimension {s.dimension_name}
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
      {selected && item && (
        <section className="panel" aria-label="Evidence and review">
          <h2>Evidence and human review</h2>
          <p>{item.improvement}</p>
          {"gaps" in item && (
            <ul>
              {item.gaps.map((g) => (
                <li key={g}>{g}</li>
              ))}
            </ul>
          )}
          {!item.available && (
            <StatePanel kind="empty" title="Evidence unavailable">
              Sources changed, were revoked, or are missing. Acceptance is
              disabled.
            </StatePanel>
          )}
          {item.spans.map((span, i) => {
            const source = selected.evidence.find(
              (s) => s.source === span.source,
            );
            return source ? (
              <details key={i} open>
                <summary>
                  {source.location} · characters {span.start}–{span.end}
                </summary>
                <p>
                  Version {source.version} · SHA-256 {source.sha256}
                </p>
                <blockquote>
                  {Array.from(source.text).slice(span.start, span.end).join("")}
                </blockquote>
              </details>
            ) : null;
          })}
          <h3>Immutable review history</h3>
          {item.reviews.length === 0 && <p>No human decision yet.</p>}
          <ol>
            {item.reviews.map((r) => (
              <li key={r.id}>
                {r.decision} · revision {r.revision} ·{" "}
                {new Date(r.created_at).toLocaleString()} · {r.actor_id}
                <p>{r.reason}</p>
                {r.approved_score !== null && (
                  <p>Approved maturity score: {r.approved_score}</p>
                )}
              </li>
            ))}
          </ol>
          {selected.can_review ? (
            <>
              <Field label="Review reason">
                <textarea
                  value={reason}
                  maxLength={1000}
                  onChange={(e) => setReason(e.target.value)}
                />
              </Field>
              {"dimension_id" in item && (
                <Field label="Approved maturity score override (optional, 0–100)">
                  <input
                    type="number"
                    min="0"
                    max="100"
                    step="0.0001"
                    value={approved}
                    onChange={(e) => setApproved(e.target.value)}
                  />
                </Field>
              )}
              <Button
                disabled={
                  busy ||
                  !reason.trim() ||
                  !item.available ||
                  ("suggested_score" in item && item.suggested_score === null)
                }
                onClick={() => void review("accepted")}
              >
                Accept as reviewed
              </Button>
              <Button
                disabled={busy || !reason.trim()}
                onClick={() => void review("rejected")}
              >
                Reject suggestion
              </Button>
            </>
          ) : (
            <p>An independent authorized reviewer must record this decision.</p>
          )}
        </section>
      )}
      <section className="panel">
        <h2>Specialist contracts</h2>
        {definitions.map((d) => (
          <details key={d.agent}>
            <summary>{d.agent}</summary>
            <p>
              Inputs: {d.inputs.join(", ")} · Read-only tools:{" "}
              {d.tools.join(", ")}
            </p>
            <p>
              Timeout: {d.timeout_seconds}s within the shared run deadline.
              Fallback: {d.fallback}
            </p>
            <p>
              Output: {d.output_schema}. Evaluation cases:{" "}
              {d.evaluation_cases.join(", ")}
            </p>
          </details>
        ))}
      </section>
    </div>
  );
}
