"use client";

import { useCallback, useEffect, useState } from "react";
import type { components } from "@ppm/contracts/schema";
import { apiError } from "./api-error";
import { Button, Field } from "./ui";

type Pilot = components["schemas"]["PilotView"];

export function SelectionPilot({
  project,
  transport,
}: {
  project: string;
  transport: typeof fetch;
}) {
  const [pilots, setPilots] = useState<Pilot[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const [checked, setChecked] = useState<string[]>([]);
  const [reason, setReason] = useState("");
  const [attested, setAttested] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [clock, setClock] = useState(() => Date.now());
  const selected = pilots.find((p) => p.id === selectedId) ?? null;
  const api = useCallback(
    async <T,>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const response = await transport(
        new Request(
          window.location.origin + "/api/v1/agents/selection-pilots" + path,
          {
            method,
            headers: {
              "content-type": "application/json",
              "idempotency-key": crypto.randomUUID(),
              ...(revision === undefined
                ? {}
                : { "if-match": String(revision) }),
            },
            body: body === undefined ? undefined : JSON.stringify(body),
          },
        ),
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
    const values = await api<Pilot[]>(
      `?project_id=${encodeURIComponent(project)}`,
    );
    setPilots(values);
    return values;
  }, [api, project]);

  useEffect(() => {
    let live = true;
    void api<Pilot[]>(`?project_id=${encodeURIComponent(project)}`)
      .then((values) => {
        if (live) {
          setPilots(values);
          setSelectedId(values[0]?.id ?? "");
        }
      })
      .catch((e) => {
        if (live) setError(e.message);
      })
      .finally(() => {
        if (live) setLoading(false);
      });
    return () => {
      live = false;
    };
  }, [api, project]);

  const pending = selected?.cases.some((c) => c.status === "pending") ?? false;
  useEffect(() => {
    const timer = setInterval(() => setClock(Date.now()), 1000);
    return () => clearInterval(timer);
  }, []);
  const cooling = selected?.next_case_at
    ? new Date(selected.next_case_at).getTime() > clock
    : false;
  useEffect(() => {
    if (!pending) return;
    let live = true;
    const timer = setInterval(() => {
      void api<Pilot[]>(`?project_id=${encodeURIComponent(project)}`)
        .then((values) => {
          if (live) setPilots(values);
        })
        .catch((e) => {
          if (live) setError(e.message);
        });
    }, 2000);
    return () => {
      live = false;
      clearInterval(timer);
    };
  }, [api, project, pending]);

  async function act(action: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await action();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Pilot unavailable");
    } finally {
      setBusy(false);
    }
  }
  function accept(value: Pilot) {
    setPilots((current) => [
      value,
      ...current.filter((p) => p.id !== value.id),
    ]);
    setSelectedId(value.id);
    setChecked([]);
    setAttested(false);
    setReason("");
  }
  const next = selected?.cases.find((c) => c.status === "not_started");
  const stopped =
    selected?.cases.some((c) => c.status === "unavailable") ?? false;
  return (
    <section className="panel stack" aria-label="Financial selection pilot">
      <p className="eyebrow">Sprint 12.1 · Current API experiment</p>
      <h2>Financial selection pilot</h2>
      <p>
        Synthetic numeric fixtures · Gemini · one request per case · shared
        provider limits. This tests checklist selection. AT17 semantic quality
        remains BLOCKED.
      </p>
      {loading && <p role="status">Loading selection pilots…</p>}
      {error && <p role="alert">{error}</p>}
      <div className="actions">
        <Button
          disabled={busy || loading}
          onClick={() =>
            void act(async () => {
              accept(await api<Pilot>("", "POST", { project_id: project }));
            })
          }
        >
          Prepare selection pilot
        </Button>
        <Button
          variant="secondary"
          disabled={busy || loading}
          onClick={() =>
            void act(async () => {
              await refresh();
            })
          }
        >
          Refresh pilot
        </Button>
      </div>
      <Field label="Saved selection pilot">
        <select
          value={selectedId}
          onChange={(e) => {
            setSelectedId(e.target.value);
            setChecked([]);
            setAttested(false);
            setReason("");
          }}
        >
          <option value="">Choose a pilot</option>
          {pilots.map((p) => (
            <option key={p.id} value={p.id}>
              {new Date(p.created_at).toLocaleString()} · {p.id.slice(0, 8)}
            </option>
          ))}
        </select>
      </Field>
      {selected && (
        <>
          <p role="status">
            Pilot status: <strong>{String(selected.summary.state)}</strong>
          </p>
          <p>
            {selected.protocol.rule} The deterministic rule already solves these
            fixtures; API selection adds no demonstrated interpretation.
          </p>
          <details>
            <summary>Protocol and model fingerprints</summary>
            <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>
              {JSON.stringify(selected.binding, null, 2)}
            </pre>
          </details>
          {!selected.review && (
            <p>
              {selected.can_automated_review
                ? "This pilot has owner-authorized automated arithmetic checking for its fixed synthetic labels. It records no personal human review."
                : "A different person with Admin access and an existing guided grant must review all 12 expected labels before any call."}{" "}
              Review both sets; do not use the six reserved cases for prompt
              tuning.
            </p>
          )}
          {selected.can_automated_review && (
            <Button
              disabled={busy}
              onClick={() =>
                void act(async () =>
                  accept(
                    await api<Pilot>(
                      `/${selected.id}/automated-review`,
                      "POST",
                      {
                        corpus_sha256: selected.protocol.corpus_sha256,
                        strategy_sha256: selected.protocol.strategy_sha256,
                        synthetic_only: true,
                      },
                      selected.revision,
                    ),
                  ),
                )
              }
            >
              Run approved automated check
            </Button>
          )}
          <div
            className="table-scroll"
            role="region"
            aria-label="Pilot fixture labels and measurements"
            tabIndex={0}
          >
            <table>
              <thead>
                <tr>
                  <th>Case</th>
                  <th>Fixture observations</th>
                  <th>Expected IDs</th>
                  <th>API result</th>
                  {selected.can_review && <th>Label review</th>}
                </tr>
              </thead>
              <tbody>
                {selected.protocol.cases.map((c) => {
                  const result = selected.cases.find((r) => r.id === c.id)!;
                  return (
                    <tr key={c.id}>
                      <th scope="row">
                        {c.id} · {c.split}
                      </th>
                      <td>
                        {c.observations.map((o) => (
                          <p key={o.id}>
                            {o.id}: {o.fact}
                          </p>
                        ))}
                      </td>
                      <td>{c.expected.join(", ") || "Abstain"}</td>
                      <td>
                        <div
                          style={{
                            maxWidth: "12rem",
                            overflowWrap: "anywhere",
                          }}
                        >
                          {result.status}
                          {result.status === "measured" &&
                            ` · ${result.selected.join(", ") || "Abstain"} · ${result.correct ? "matches" : "differs"}`}
                          {result.diagnostic && ` · ${result.diagnostic}`}
                          {result.timing_kind === "accepted_response" &&
                            ` · Response latency: ${result.elapsed_ms} ms`}
                          {result.timing_kind === "unavailable_attempt" &&
                            ` · Unavailable attempt elapsed: ${result.elapsed_ms} ms (excluded from p95)`}
                          {result.status === "unavailable" &&
                            result.timing_kind === "not_recorded" &&
                            " · Elapsed time not recorded"}
                        </div>
                      </td>
                      {selected.can_review && (
                        <td>
                          <label>
                            <input
                              type="checkbox"
                              checked={checked.includes(c.id)}
                              onChange={(e) =>
                                setChecked((values) =>
                                  e.target.checked
                                    ? [...values, c.id]
                                    : values.filter((v) => v !== c.id),
                                )
                              }
                            />
                            Reviewed label {c.id}
                          </label>
                        </td>
                      )}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          {selected.can_review && (
            <form
              className="stack"
              onSubmit={(e) => {
                e.preventDefault();
                void act(async () =>
                  accept(
                    await api<Pilot>(
                      `/${selected.id}/label-review`,
                      "POST",
                      {
                        corpus_sha256: selected.protocol.corpus_sha256,
                        strategy_sha256: selected.protocol.strategy_sha256,
                        reviewed_case_ids: checked,
                        human_reviewed: attested,
                        reason,
                      },
                      selected.revision,
                    ),
                  ),
                );
              }}
            >
              <Field label="Label review reason">
                <textarea
                  required
                  minLength={12}
                  maxLength={1000}
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                />
              </Field>
              <label>
                <input
                  type="checkbox"
                  checked={attested}
                  onChange={(e) => setAttested(e.target.checked)}
                />
                I personally reviewed the rule and every expected label; these
                are synthetic fixtures, not genuine outcomes.
              </label>
              <Button
                disabled={
                  busy ||
                  checked.length !== 12 ||
                  !attested ||
                  reason.trim().length < 12
                }
              >
                Freeze reviewed labels
              </Button>
            </form>
          )}
          {selected.review && (
            <p>
              {selected.review_kind === "automated_rule_audit"
                ? "Automated arithmetic check recorded. Human review: false."
                : "Independent human label review recorded."}{" "}
              Changed policy, prompt or corpus requires a new pilot. All
              attempts remain in the normal usage history.
            </p>
          )}
          {next && (
            <Button
              disabled={
                busy ||
                pending ||
                cooling ||
                stopped ||
                !selected.binding_current
              }
              onClick={() =>
                void act(async () =>
                  accept(
                    await api<Pilot>(
                      `/${selected.id}/cases/${next.id}`,
                      "POST",
                      {},
                      selected.revision,
                    ),
                  ),
                )
              }
            >
              Measure case {next.id}
            </Button>
          )}
          {cooling && !pending && (
            <p role="status">
              One-minute provider pacing: the next case becomes available at{" "}
              {new Date(selected.next_case_at!).toLocaleTimeString()}.
            </p>
          )}
          {pending && (
            <p role="status">
              Waiting for the existing job. Refreshing makes no additional API
              call.
            </p>
          )}
          {stopped && (
            <p>
              This pilot stopped after an unavailable attempt. Diagnose the
              provider or quota before preparing a new reviewed pilot; do not
              reset usage.
            </p>
          )}
          <details>
            <summary>Measured counts and limitations</summary>
            <pre style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>
              {JSON.stringify(selected.summary, null, 2)}
            </pre>
          </details>
          <Button
            variant="secondary"
            disabled={busy}
            onClick={() =>
              void act(async () => {
                const report = await api<Pilot>(`/${selected.id}`);
                const url = URL.createObjectURL(
                  new Blob([JSON.stringify(report, null, 2)], {
                    type: "application/json",
                  }),
                );
                const link = document.createElement("a");
                link.href = url;
                link.download = `selection-pilot-${selected.id}.json`;
                link.click();
                URL.revokeObjectURL(url);
              })
            }
          >
            Download pilot report
          </Button>
        </>
      )}
    </section>
  );
}
