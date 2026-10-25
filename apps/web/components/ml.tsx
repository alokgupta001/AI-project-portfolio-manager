"use client";
import { useCallback, useEffect, useState } from "react";
import type { components } from "@ppm/contracts/schema";
import { RecordSelect } from "./record-select";
import { apiError } from "./api-error";
type S = components["schemas"];
type History = S["MLHistoryView"];
type Dataset = S["DatasetView"];
type Run = S["RunView"];

export function ML({
  account,
  transport,
}: {
  account: S["AccountView"];
  transport: typeof fetch;
}) {
  const [histories, setHistories] = useState<History[]>([]);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [runs, setRuns] = useState<Run[]>([]);
  const [project, setProject] = useState("");
  const [history, setHistory] = useState("");
  const [dataset, setDataset] = useState("");
  const [target, setTarget] = useState<S["DatasetInput"]["target"]>("delay");
  const [source, setSource] = useState("");
  const [trainEnd, setTrainEnd] = useState("2025-03-01");
  const [validationEnd, setValidationEnd] = useState("2025-07-01");
  const [cutoff, setCutoff] = useState("2025-12-31");
  const [horizon, setHorizon] = useState(30);
  const [active, setActive] = useState<Run | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const admin = account.role === "Admin";
  const api = useCallback(
    async <T,>(path: string, method = "GET", body?: unknown): Promise<T> => {
      const result = await transport(
        new Request(window.location.origin + "/api/v1/ml" + path, {
          method,
          headers: {
            "content-type": "application/json",
            "idempotency-key": crypto.randomUUID(),
          },
          body: body === undefined ? undefined : JSON.stringify(body),
        }),
      );
      if (!result.ok)
        throw new Error(
          apiError(await result.json().catch(() => null), result.status),
        );
      return result.json();
    },
    [transport],
  );
  const refresh = useCallback(async () => {
    const [h, d, r] = await Promise.all([
      api<History[]>("/histories"),
      api<Dataset[]>("/datasets"),
      api<Run[]>("/runs"),
    ]);
    setHistories(h);
    setDatasets(d);
    setRuns(r);
  }, [api]);
  useEffect(() => {
    if (!admin) {
      setLoading(false);
      return;
    }
    void refresh()
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [admin, refresh]);
  useEffect(() => {
    if (!active || !["queued", "running"].includes(active.status)) return;
    const id = setTimeout(() => {
      void api<Run>(`/runs/${active.id}`)
        .then(setActive)
        .catch((e) => setError(e.message));
    }, 1500);
    return () => clearTimeout(id);
  }, [active, api]);
  async function action(work: () => Promise<void>) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await work();
      await refresh();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  const selected = datasets.find((d) => d.id === dataset);
  const candidateRows = Object.entries(active?.card.candidates || {}) as [
    string,
    {
      validation: Record<string, number>;
      test: Record<string, number>;
    },
  ][];
  const scoreKey =
    active?.card.target === "delay" || active?.card.target === "overrun"
      ? "mae"
      : "brier";
  const displayScore = (value: number | undefined) =>
    value == null ? "Unavailable" : value.toFixed(4);
  return (
    <div className="delivery-workspace ml-workspace">
      <section className="panel">
        <h1>History & baseline lab</h1>
        <p>
          Import dated evidence, freeze a dataset, and inspect a reproducible
          CPU baseline. Forecast serving belongs to Sprint 13.
        </p>
        <p className="muted">
          Synthetic metrics are demonstration only. Genuine labels and live
          connector acceptance are unavailable until supplied and verified.
          Broad AI accuracy AT17 remains BLOCKED.
        </p>
        <a href="/integrations">
          Review connections, source history & conflicts →
        </a>
        {error && <p role="alert">{error}</p>}
        {notice && <p role="status">{notice}</p>}
        {loading && <p role="status">Loading local research…</p>}
        {!admin && (
          <p role="alert">
            History and baseline research requires Admin in the active
            organization.
          </p>
        )}
        {admin && (
          <button disabled={busy} onClick={() => void action(refresh)}>
            Refresh lab
          </button>
        )}
      </section>
      {admin && (
        <>
          <section className="panel">
            <h2>1. Import history</h2>
            <p>
              Use aggregate numeric observations and genuine outcome facts from
              an authorized project. No raw notes or AI outputs. Each import
              creates an immutable version. Public real datasets require a
              separate license and target review.
            </p>
            <RecordSelect
              transport={transport}
              kind="projects"
              label="History project"
              name="history-project"
              value={project}
              onChange={setProject}
            />
            <label>
              Outcome target
              <select
                value={target}
                onChange={(e) => setTarget(e.target.value as typeof target)}
              >
                {["delay", "overrun", "risk", "failure", "sentiment"].map(
                  (t) => (
                    <option key={t}>{t}</option>
                  ),
                )}
              </select>
            </label>
            <button
              disabled={busy || !project}
              onClick={() =>
                void action(async () => {
                  const template = await api<{ history: unknown }>(
                    `/template?project_id=${project}&target=${target}`,
                  );
                  setSource(JSON.stringify(template.history, null, 2));
                  setNotice(
                    "Loaded 90 synthetic fixture records. Inspect or replace the JSON before importing.",
                  );
                })
              }
            >
              Load synthetic example
            </button>
            <label>
              History import JSON
              <textarea
                aria-label="History import JSON"
                rows={9}
                value={source}
                onChange={(e) => setSource(e.target.value)}
                placeholder="Load the example for the schema, or paste authorized numeric history."
              />
            </label>
            <button
              disabled={busy || !source}
              onClick={() =>
                void action(async () => {
                  const imported = await api<History>(
                    "/histories",
                    "POST",
                    JSON.parse(source),
                  );
                  setHistory(imported.id);
                  setNotice(
                    `Imported version ${imported.version}; ${imported.manifest.lineage} lineage.`,
                  );
                })
              }
            >
              Import history version
            </button>
            <h3>History versions</h3>
            {!histories.length && (
              <p>
                No historical outcomes imported. Real model evaluation is
                unavailable.
              </p>
            )}
            <div
              className="table-scroll"
              tabIndex={0}
              role="region"
              aria-label="History versions table"
            >
              <table>
                <caption>History provenance and permission status</caption>
                <thead>
                  <tr>
                    <th>Name/version</th>
                    <th>Lineage</th>
                    <th>Labels</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {histories.map((h) => (
                    <tr key={h.id}>
                      <td>
                        {h.name} v{h.version}
                      </td>
                      <td>{String(h.manifest.lineage)}</td>
                      <td>{String(h.manifest.label_verification)}</td>
                      <td>{h.withdrawn ? "Withdrawn" : "Active"}</td>
                      <td>
                        <button
                          disabled={busy || h.withdrawn}
                          onClick={() =>
                            void action(async () => {
                              await api(
                                `/histories/${h.id}/withdraw`,
                                "POST",
                                {},
                              );
                              setActive(null);
                              setNotice(
                                "History withdrawn. Dataset builds, runs and artifact access now reject its descendants.",
                              );
                            })
                          }
                        >
                          Withdraw {h.name} v{h.version}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
          <section className="panel">
            <h2>2. Freeze an as-of dataset</h2>
            <label>
              History version
              <select
                value={history}
                onChange={(e) => setHistory(e.target.value)}
              >
                <option value="">Select history</option>
                {histories
                  .filter((h) => !h.withdrawn)
                  .map((h) => (
                    <option key={h.id} value={h.id}>
                      {h.name} v{h.version} · {String(h.manifest.lineage)}
                    </option>
                  ))}
              </select>
            </label>
            <div className="form-grid">
              <label>
                Train boundary
                <input
                  type="date"
                  value={trainEnd}
                  onChange={(e) => setTrainEnd(e.target.value)}
                />
              </label>
              <label>
                Validation boundary
                <input
                  type="date"
                  value={validationEnd}
                  onChange={(e) => setValidationEnd(e.target.value)}
                />
              </label>
              <label>
                As-of cutoff
                <input
                  type="date"
                  value={cutoff}
                  onChange={(e) => setCutoff(e.target.value)}
                />
              </label>
              <label>
                Horizon (days)
                <input
                  type="number"
                  min={1}
                  max={366}
                  value={horizon}
                  onChange={(e) => setHorizon(Number(e.target.value))}
                />
              </label>
            </div>
            <p>
              Labels must be known by each boundary and outcomes must fall
              inside the horizon. Entities spanning splits are purged. Missing
              outcomes produce an explicit insufficient-data state.
            </p>
            <button
              disabled={busy || !history}
              onClick={() =>
                void action(async () => {
                  const d = await api<Dataset>("/datasets", "POST", {
                    history_id: history,
                    target,
                    horizon_days: horizon,
                    train_end: `${trainEnd}T00:00:00Z`,
                    validation_end: `${validationEnd}T00:00:00Z`,
                    cutoff: `${cutoff}T00:00:00Z`,
                  });
                  setDataset(d.id);
                  setNotice(`Dataset frozen: ${d.manifest.eligibility}.`);
                })
              }
            >
              Build dataset version
            </button>
            <label>
              Dataset version
              <select
                value={dataset}
                onChange={(e) => setDataset(e.target.value)}
              >
                <option value="">Select dataset</option>
                {datasets.map((d) => (
                  <option key={d.id} value={d.id}>
                    {String(d.manifest.target)} · {String(d.manifest.lineage)} ·{" "}
                    {d.digest.slice(0, 10)} · {String(d.manifest.eligibility)}
                  </option>
                ))}
              </select>
            </label>
            {selected && (
              <>
                <p>
                  Eligibility:{" "}
                  <strong>{String(selected.manifest.eligibility)}</strong> ·
                  Entity overlap: {String(selected.manifest.entity_overlap)}
                </p>
                <details>
                  <summary>Dataset manifest, splits & provenance</summary>
                  <pre
                    style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}
                  >
                    {JSON.stringify(selected.manifest, null, 2)}
                  </pre>
                </details>
              </>
            )}
          </section>
          <section className="panel">
            <h2>3. Run & review a baseline</h2>
            <p>
              Constant baseline, regularized linear model and 32-tree Random
              Forest. One CPU thread, fixed seed, training-only imputation. No
              AI API calls or model downloads.
            </p>
            <button
              disabled={busy || !dataset}
              onClick={() =>
                void action(async () => {
                  const run = await api<Run>("/runs", "POST", {
                    dataset_id: dataset,
                  });
                  setActive(run);
                  setNotice("Baseline queued in the existing worker.");
                })
              }
            >
              Run CPU baseline
            </button>
            {!runs.length && <p>No baseline runs yet.</p>}
            <label>
              Saved model card
              <select
                value={active?.id || ""}
                onChange={(e) =>
                  void action(async () =>
                    setActive(await api<Run>(`/runs/${e.target.value}`)),
                  )
                }
              >
                <option value="">Select run</option>
                {runs.map((r) => (
                  <option value={r.id} key={r.id}>
                    {r.id.slice(0, 8)} · {r.status} ·{" "}
                    {String(r.card.lineage || "pending")}
                  </option>
                ))}
              </select>
            </label>
            {active && (
              <div role="region" aria-label="Model card">
                <h3>Model card · {active.status}</h3>
                <p role="status">
                  {["queued", "running"].includes(active.status)
                    ? "Waiting for local worker evaluation…"
                    : `Eligibility: ${active.card.eligibility}`}
                </p>
                {active.card.lineage === "synthetic" && (
                  <p>
                    <strong>
                      SYNTHETIC DEMO ONLY — these metrics are not real-world
                      evidence.
                    </strong>
                  </p>
                )}
                <p>
                  {String(
                    active.card.promotion ||
                      "Promotion blocked pending evaluation and Sprint 13",
                  )}
                </p>
                {active.card.repeat_matches_previous != null && (
                  <p>
                    Reproduction matches previous result:{" "}
                    {String(active.card.repeat_matches_previous)}
                  </p>
                )}
                {candidateRows.length > 0 && (
                  <div
                    className="table-scroll"
                    tabIndex={0}
                    role="region"
                    aria-label="Model comparison table"
                  >
                    <table>
                      <caption>
                        Model comparison ·{" "}
                        {scoreKey === "mae"
                          ? `MAE (${active.card.target === "delay" ? "days" : "percentage points"})`
                          : "Brier score"}{" "}
                        · lower is better; selection uses validation
                      </caption>
                      <thead>
                        <tr>
                          <th>Candidate</th>
                          <th>Validation</th>
                          <th>Held-out test</th>
                          <th>Test PR-AUC</th>
                          <th>Test recall at .5</th>
                        </tr>
                      </thead>
                      <tbody>
                        {candidateRows.map(([name, values]) => (
                          <tr key={name}>
                            <td>
                              {name.replaceAll("_", " ")}
                              {active.card.selected === name
                                ? " (selected)"
                                : ""}
                            </td>
                            <td>{displayScore(values.validation[scoreKey])}</td>
                            <td>{displayScore(values.test[scoreKey])}</td>
                            <td>{displayScore(values.test.pr_auc)}</td>
                            <td>{displayScore(values.test.recall)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
                <details>
                  <summary>Metrics, lineage & limitations</summary>
                  <pre
                    style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}
                  >
                    {JSON.stringify(active.card, null, 2)}
                  </pre>
                </details>
                <button
                  disabled={busy || active.status === "queued"}
                  onClick={() =>
                    void action(async () => {
                      const output = await api(`/runs/${active.id}/artifacts`);
                      const url = URL.createObjectURL(
                        new Blob([JSON.stringify(output, null, 2)], {
                          type: "application/json",
                        }),
                      );
                      const link = document.createElement("a");
                      link.href = url;
                      link.download = `baseline-${active.id}.json`;
                      link.click();
                      URL.revokeObjectURL(url);
                    })
                  }
                >
                  Download model card & artifacts
                </button>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
