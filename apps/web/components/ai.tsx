"use client";
import { useCallback, useEffect, useState } from "react";
import type { components } from "@ppm/contracts/schema";
import { apiError } from "./api-error";
import { Button, Field, StatePanel } from "./ui";
import { RecordSelect } from "./record-select";

type S = components["schemas"];
type Run = S["AIRunView"];
const terminal = new Set([
  "succeeded",
  "partially_succeeded",
  "failed",
  "cancelled",
]);

export function AI({
  account,
  transport,
}: {
  account: S["AccountView"];
  transport: typeof fetch;
}) {
  const [status, setStatus] = useState<S["AIProviderStatus"] | null>(null);
  const [evaluation, setEvaluation] = useState<S["AIEvaluation"] | null>(null);
  const [ops, setOps] = useState<S["AIOperations"] | null>(null);
  const [runs, setRuns] = useState<Run[]>([]);
  const [stages, setStages] = useState<S["StageView"][]>([]);
  const [selected, setSelected] = useState<Run | null>(null);
  const [diagnostics, setDiagnostics] = useState<S["AIDiagnostics"] | null>(
    null,
  );
  const [project, setProject] = useState("");
  const [query, setQuery] = useState("");
  const [version, setVersion] = useState("");
  const [sources, setSources] = useState<S["DocumentView"][]>([]);
  const [sourceRevision, setSourceRevision] = useState(0);
  const [limit, setLimit] = useState("0");
  const [concurrency, setConcurrency] = useState(1);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const admin = account.role === "Admin";
  const api = useCallback(
    async <T,>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const response = await transport(
        new Request(window.location.origin + "/api/v1/ai" + path, {
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
    setSourceRevision((value) => value + 1);
    const [provider, items] = await Promise.all([
      api<S["AIProviderStatus"]>("/status"),
      api<Run[]>("/runs"),
    ]);
    setStatus(provider);
    setRuns(items);
    if (admin) {
      const value = await api<S["AIOperations"]>("/operations");
      setOps(value);
      setEvaluation(await api<S["AIEvaluation"]>("/evaluation"));
      setLimit(String(value.limit_usd));
      setConcurrency(value.concurrency);
    }
  }, [api, admin]);
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
    setSources([]);
    setVersion("");
    if (project)
      void transport(
        new Request(
          window.location.origin +
            "/api/v1/documents?" +
            new URLSearchParams({ project_id: project, limit: "100" }),
        ),
      )
        .then(async (response) => {
          if (!response.ok)
            throw new Error(
              apiError(
                await response.json().catch(() => null),
                response.status,
              ),
            );
          const page: S["DocumentPage"] = await response.json();
          if (live) setSources(page.items);
        })
        .catch((e) => {
          if (live) setError(e.message);
        });
    return () => {
      live = false;
    };
  }, [project, transport, sourceRevision]);
  useEffect(() => {
    if (!selected || terminal.has(selected.status)) return;
    let live = true;
    const timer = setInterval(() => {
      void api<Run>(`/runs/${selected.id}`)
        .then((value) => {
          if (live) {
            setSelected(value);
            if (terminal.has(value.status))
              void refresh().catch((e) => setError(e.message));
          }
        })
        .catch((e) => {
          if (live) {
            setSelected(null);
            setDiagnostics(null);
            setError(e.message);
          }
        });
    }, 1000);
    return () => {
      live = false;
      clearInterval(timer);
    };
  }, [api, selected, refresh]);
  const activeId = selected?.id;
  const activeStatus = selected?.status;
  useEffect(() => {
    if (!activeId) {
      setStages([]);
      return;
    }
    let live = true;
    void api<S["StageView"][]>(`/runs/${activeId}/stages`)
      .then((value) => {
        if (live) setStages(value);
      })
      .catch((e) => {
        if (live) {
          setStages([]);
          setError(e.message);
        }
      });
    return () => {
      live = false;
    };
  }, [api, activeId, activeStatus]);
  async function action(work: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await work();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function start(operation: "query" | "index") {
    await action(async () => {
      const run = await api<Run>("/runs", "POST", {
        project_id: project,
        operation,
        query: operation === "query" ? query : "",
        version_id: operation === "index" ? version : null,
      });
      setSelected(run);
      setDiagnostics(null);
      await refresh();
    });
  }
  return (
    <div className="module-page">
      <header>
        <p className="eyebrow">CONTROLLED EVIDENCE RUNTIME</p>
        <h1>AI operations & evidence</h1>
        <p>
          Read-only source previews with current citations. Agent findings and
          plan edits are unavailable.
        </p>
      </header>
      {loading && <p role="status">Loading AI configuration…</p>}
      {error && (
        <StatePanel kind="error" title="AI request unavailable">
          {error}
          <p>Refresh the view or correct the input, then retry.</p>
        </StatePanel>
      )}
      <Button
        variant="secondary"
        disabled={busy}
        onClick={() => action(refresh)}
      >
        Refresh AI view
      </Button>
      {status && (
        <section className="panel">
          <h2>Provider status</h2>
          <p>
            {status.enabled
              ? status.provider === "gemini"
                ? "Gemini free tier — $0 spending limit"
                : "Configured provider — real acceptance not verified"
              : "AI provider disabled — no model calls"}
          </p>
          {status.provider === "gemini" && (
            <p>
              {status.enabled
                ? "Free quota only. Quota exhaustion returns source excerpts. Your Google project must have no billing account attached; billing status is confirmed by the operator."
                : "Gemini is paused. Check the key, authorization and confirmed free-tier project configuration. Source keyword search remains available."}
            </p>
          )}
          {status.provider === "gemini" && status.enabled && (
            <p>
              Selected source excerpts are sent to Google. Free-tier content may
              be used to improve Google products; use synthetic test sources.
            </p>
          )}
          <p>
            {status.enabled
              ? `${status.provider}: ${status.completion_model}`
              : "Missing keys or authorization keeps paid operations disabled. Source keyword previews remain usable."}
          </p>
          <p>
            {status.provider === "gemini" && status.enabled
              ? "Free-tier use is authorized. General model quality has not yet been evaluated."
              : "Real-provider acceptance: BLOCKED until explicitly authorized and verified."}
          </p>
        </section>
      )}
      {!admin && (
        <StatePanel kind="forbidden" title="Admin operations restricted">
          Usage, errors, budgets, diagnostics and starting analyses require
          Admin. Use the document library for permitted keyword searches.
        </StatePanel>
      )}
      {admin && (
        <>
          <section className="panel">
            <h2>Evidence preview</h2>
            <RecordSelect
              transport={transport}
              kind="projects"
              label="AI project"
              value={project}
              onChange={setProject}
              required
            />
            <Field label="Evidence keywords">
              <input
                value={query}
                maxLength={160}
                onChange={(e) => setQuery(e.target.value)}
              />
            </Field>
            <Button
              disabled={busy || !project || !query.trim()}
              onClick={() => start("query")}
            >
              Retrieve evidence preview
            </Button>
            <Field label="Ready source version">
              <select
                value={version}
                onChange={(e) => setVersion(e.target.value)}
              >
                <option value="">
                  Choose one of the first 100 permitted sources
                </option>
                {sources.flatMap((d) =>
                  d.versions
                    .slice(0, 1)
                    .filter((v) => v.status === "ready")
                    .map((v) => (
                      <option key={v.id} value={v.id}>
                        {d.title} — version {v.number}
                      </option>
                    )),
                )}
              </select>
            </Field>
            <Button
              disabled={
                busy ||
                !project ||
                !version ||
                !status?.enabled ||
                !status?.embedding_model
              }
              onClick={() => start("index")}
            >
              Index source embeddings
            </Button>
            {(!status?.enabled || !status?.embedding_model) && (
              <p>
                Embeddings are disabled. Existing source keyword search remains
                available.
              </p>
            )}
          </section>
          {ops && (
            <section className="panel">
              <h2>Tenant budget and circuit</h2>
              {evaluation && (
                <p>
                  Evaluation {evaluation.version}: {evaluation.passed}/
                  {evaluation.count} deterministic gates passed.
                  Support/citation/completion thresholds 100%; leakage and
                  unsupported numbers 0. Real-provider acceptance:{" "}
                  {evaluation.real_provider_acceptance}.
                </p>
              )}
              <p>
                USD spent (conservative): {ops.spent_usd}; reserved:{" "}
                {ops.reserved_usd}. Operator ceiling: {ops.deployment_limit_usd}{" "}
                USD.
              </p>
              <p>
                Recent consecutive provider failures: {ops.failures}. Circuit:{" "}
                {ops.circuit_until
                  ? `open until ${ops.circuit_until}`
                  : "closed"}
                .
              </p>
              <Field label="Tenant spending limit (USD)">
                <input
                  type="number"
                  min="0"
                  max={Number(ops.deployment_limit_usd)}
                  step="0.000001"
                  value={limit}
                  onChange={(e) => setLimit(e.target.value)}
                />
              </Field>
              <Field label="Concurrent AI runs">
                <input
                  type="number"
                  min="1"
                  max="4"
                  value={concurrency}
                  onChange={(e) => setConcurrency(Number(e.target.value))}
                />
              </Field>
              <Button
                disabled={busy || limit === ""}
                onClick={() =>
                  action(async () => {
                    const value = await api<S["AIOperations"]>(
                      "/budget",
                      "PATCH",
                      { limit_usd: limit, concurrency },
                      ops.revision,
                    );
                    setOps(value);
                  })
                }
              >
                Save tenant budget
              </Button>
              <p>
                {status?.provider === "gemini"
                  ? "Gemini spending stays at $0. Failed attempts count toward the request limit; quota exhaustion returns source excerpts."
                  : "Budget changes cannot raise the operator-authorized ceiling. Timeouts retain the reserved attempt charge."}
              </p>
            </section>
          )}
        </>
      )}
      <section className="panel">
        <h2>Recent permitted runs</h2>
        <p>Latest 25 permitted runs. Refresh to reauthorize citations.</p>
        {!loading && runs.length === 0 && <p>No permitted AI runs yet.</p>}
        <ul>
          {runs.map((run) => (
            <li key={run.id}>
              <Button
                variant="secondary"
                disabled={busy}
                onClick={() =>
                  action(async () => {
                    setSelected(await api<Run>(`/runs/${run.id}`));
                    setDiagnostics(null);
                  })
                }
              >
                Open {run.operation} run {run.id.slice(0, 8)}
              </Button>{" "}
              — {run.status}
            </li>
          ))}
        </ul>
      </section>
      {selected && (
        <section className="panel" aria-live="polite">
          <h2>Run details</h2>
          <ol aria-label="Authorized processing stages">
            {stages.map((stage) => (
              <li key={stage.sequence}>
                {stage.stage.replaceAll("_", " ")} ·{" "}
                {new Date(stage.occurred_at).toLocaleTimeString()}
              </li>
            ))}
          </ol>
          <p>
            Run status: {selected.status}; answer: {selected.answer_status};
            retrieval: {selected.retrieval}; progress sequence:{" "}
            {selected.sequence}.
          </p>
          <p>
            Provider: {selected.provider}; prompt: {selected.prompt_version};
            schema: {selected.schema_version}; tools: {selected.tool_version}.
          </p>
          <p>
            USD charged (conservative): {selected.charged_usd}; input tokens:{" "}
            {selected.input_tokens ?? "unavailable"}; output tokens:{" "}
            {selected.output_tokens ?? "unavailable"}; provider latency:{" "}
            {selected.latency_ms} ms.
          </p>
          {selected.diagnostic && <p>Diagnostic: {selected.diagnostic}</p>}
          <ul>
            {selected.limitations.map((text, index) => (
              <li key={index}>{text}</li>
            ))}
          </ul>
          {selected.evidence.length === 0 && (
            <p>No current permitted excerpts are available.</p>
          )}
          {selected.evidence.map((ref) => (
            <article key={ref.chunk_id}>
              <h3>{ref.location}</h3>
              <blockquote>{ref.quote}</blockquote>
              <p>Source version: {ref.version_id}</p>
              <Button
                variant="secondary"
                disabled={busy}
                onClick={() =>
                  action(async () => {
                    const response = await transport(
                      new Request(
                        window.location.origin +
                          "/api/v1/documents/citations/" +
                          ref.chunk_id,
                      ),
                    );
                    if (!response.ok) {
                      setSelected(await api<Run>(`/runs/${selected.id}`));
                      throw new Error(
                        "Citation is no longer available. Retrieve current sources.",
                      );
                    }
                    const current: S["ChunkView"] = await response.json();
                    if (current.text !== ref.quote)
                      throw new Error("Source changed. Refresh evidence.");
                    setSelected(await api<Run>(`/runs/${selected.id}`));
                  })
                }
              >
                Revalidate citation
              </Button>
            </article>
          ))}
          {admin && (
            <>
              {!terminal.has(selected.status) && (
                <Button
                  variant="danger"
                  disabled={busy}
                  onClick={() =>
                    action(async () => {
                      setSelected(
                        await api<Run>(
                          `/runs/${selected.id}/cancel`,
                          "POST",
                          {},
                          selected.revision,
                        ),
                      );
                      await refresh();
                    })
                  }
                >
                  Cancel AI run
                </Button>
              )}
              <Button
                variant="secondary"
                disabled={busy}
                onClick={() =>
                  action(async () =>
                    setDiagnostics(
                      await api<S["AIDiagnostics"]>(
                        `/runs/${selected.id}/diagnostics`,
                      ),
                    ),
                  )
                }
              >
                Inspect redacted diagnostics
              </Button>
            </>
          )}
        </section>
      )}
      {diagnostics && (
        <section className="panel">
          <h2>Redacted diagnostics</h2>
          <p>
            Input SHA-256:{" "}
            <span className="ai-digest">{diagnostics.input_sha256}</span>
          </p>
          <p>
            No raw provider output, source snapshots, secrets or private
            reasoning are displayed.
          </p>
          <div
            className="ai-accounting"
            role="region"
            aria-label="AI call accounting"
            tabIndex={0}
          >
            <table>
              <thead>
                <tr>
                  <th>Operation</th>
                  <th>Attempt</th>
                  <th>Status</th>
                  <th>Code</th>
                  <th>USD charge</th>
                  <th>Latency (ms)</th>
                </tr>
              </thead>
              <tbody>
                {diagnostics.calls.map((call) => (
                  <tr key={call.id}>
                    <td>{call.operation}</td>
                    <td>{call.attempt}</td>
                    <td>{call.status}</td>
                    <td>{call.code ?? "None"}</td>
                    <td>{call.charged_usd}</td>
                    <td>{call.latency_ms}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {diagnostics.calls.length === 0 && (
            <p>No provider calls were made.</p>
          )}
        </section>
      )}
    </div>
  );
}
