"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createApiClient } from "@ppm/contracts";
import type { components } from "@ppm/contracts/schema";
import { Button, Field, Modal, ChartFrame } from "./ui";
import { RecordEditor } from "./delivery";
import type { Kind } from "./delivery-fields";

type S = components["schemas"];
type Snapshot = S["CommandSnapshot"];
type Metric = S["Metric"];
type Row = S["RecordView"];
type Dashboard = "Executive" | "Delivery" | "Risk" | "Resource";
const number = (v: string | number | null | undefined) =>
  v == null
    ? "Unknown"
    : Number(v).toLocaleString(undefined, { maximumFractionDigits: 2 });

export function CommandCenter({
  account,
  transport,
}: {
  account: S["AccountView"];
  transport: typeof fetch;
}) {
  const [start, setStart] = useState(
    new Date().toISOString().slice(0, 8) + "01",
  );
  const [end, setEnd] = useState(
    new Date(Date.now() + 28 * 86400000).toISOString().slice(0, 10),
  );
  const [portfolio, setPortfolio] = useState("");
  const [dashboard, setDashboard] = useState<Dashboard>("Executive");
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [portfolios, setPortfolios] = useState<Row[]>([]);
  const [views, setViews] = useState<Row[]>([]);
  const [viewName, setViewName] = useState("");
  const [selectedView, setSelectedView] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [evidence, setEvidence] = useState<Metric | null>(null);
  const [editor, setEditor] = useState<{
    kind: Kind;
    row: Row | null;
    projectId?: string;
  } | null>(null);
  const requestId = useRef(0);
  const client = useMemo(
    () => createApiClient(window.location.origin, transport),
    [transport],
  );
  const api = useCallback(
    async <T,>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const r = await transport(
        new Request(window.location.origin + "/api/v1" + path, {
          method,
          headers: {
            "content-type": "application/json",
            "idempotency-key": crypto.randomUUID(),
            ...(revision == null ? {} : { "if-match": String(revision) }),
          },
          body: body === undefined ? undefined : JSON.stringify(body),
        }),
      );
      if (!r.ok) {
        const e = await r.json().catch(() => null);
        throw new Error(
          e?.error?.message ||
            `Request failed (${r.status}). Refresh or sign in again.`,
        );
      }
      return r.json();
    },
    [transport],
  );
  const refresh = useCallback(async () => {
    const id = ++requestId.current;
    setBusy(true);
    setError("");
    setSnapshot(null);
    setEvidence(null);
    try {
      const query = new URLSearchParams({
        start,
        end,
        ...(portfolio ? { portfolio_id: portfolio } : {}),
      });
      const [data, p, v] = await Promise.all([
        api<Snapshot>("/command/snapshot?" + query),
        api<S["PageView"]>("/delivery/portfolios?limit=100"),
        api<S["PageView"]>("/delivery/saved_views?limit=100"),
      ]);
      if (id === requestId.current) {
        setSnapshot(data);
        setPortfolios(p.items);
        setViews(v.items);
      }
    } catch (e) {
      if (id === requestId.current) setError((e as Error).message);
    } finally {
      if (id === requestId.current) setBusy(false);
    }
  }, [api, start, end, portfolio]);
  useEffect(() => {
    void refresh();
    return () => {
      requestId.current++;
    };
  }, [refresh]);
  async function saveView(archive = false) {
    setError("");
    setNotice("");
    const row = views.find((v) => v.id === selectedView);
    try {
      if (archive && !row) return;
      const data =
        archive && row
          ? { ...row.data, archived: true }
          : {
              kind: "saved_views",
              name: viewName,
              user_id: account.id,
              portfolio_id: portfolio || null,
              start_date: start,
              end_date: end,
              dashboard,
            };
      await api(
        "/delivery/saved_views" + (archive && row ? "/" + row.id : ""),
        archive ? "PATCH" : "POST",
        data,
        archive ? row?.revision : undefined,
      );
      setNotice(archive ? "Saved view removed." : "Personal view saved.");
      setSelectedView("");
      await refresh();
    } catch (e) {
      setError((e as Error).message);
    }
  }
  async function exportSnapshot() {
    // Revalidate live authorization before generating the downloadable DTO.
    try {
      const query = new URLSearchParams({
        start,
        end,
        ...(portfolio ? { portfolio_id: portfolio } : {}),
      });
      const current = await api<Snapshot>("/command/snapshot?" + query);
      setSnapshot(current);
      const url = URL.createObjectURL(
        new Blob([JSON.stringify(current, null, 2)], {
          type: "application/json",
        }),
      );
      const a = document.createElement("a");
      a.href = url;
      a.download = "command-center.json";
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError((e as Error).message);
      setSnapshot(null);
    }
  }
  function metricsTable(ms: Metric[]) {
    return (
      <div
        className="table-scroll"
        tabIndex={0}
        role="region"
        aria-label="Metric data"
      >
        <table>
          <thead>
            <tr>
              <th>Metric / source</th>
              <th>Value / unit</th>
              <th>Period</th>
              <th>Quality / freshness</th>
              <th>Evidence</th>
            </tr>
          </thead>
          <tbody>
            {ms.map((m) => (
              <tr key={m.key}>
                <th scope="row">
                  {m.label}
                  <small>{m.source}</small>
                </th>
                <td>
                  {number(m.value)} {m.unit}
                </td>
                <td>{m.period}</td>
                <td>
                  {m.status} · {m.freshness}
                  <small>
                    {m.source_updated_at
                      ? new Date(m.source_updated_at).toLocaleString()
                      : "No source timestamp"}{" "}
                    · coverage {number(m.coverage_percent)}%
                  </small>
                </td>
                <td>
                  <Button onClick={() => setEvidence(m)}>
                    Inspect {m.label}
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  const names = new Map(snapshot?.projects.map((p) => [p.id, p.name]) || []);
  const editable = new Set(
    snapshot?.projects.filter((p) => p.can_edit).map((p) => p.id) || [],
  );
  const filteredRecords =
    snapshot?.records.filter((r) =>
      dashboard === "Risk"
        ? r.data.kind === "risks"
        : dashboard === "Delivery"
          ? ["milestones", "blockers", "dependencies"].includes(r.data.kind)
          : r.data.kind === "benefits",
    ) || [];
  return (
    <div className="command-workspace">
      <section className="page-heading">
        <div>
          <p className="eyebrow">PORTFOLIO INTELLIGENCE</p>
          <h1>Command center</h1>
          <p className="lead">
            Reported progress, supporting facts and the gaps that need
            attention.
          </p>
        </div>
        <Button onClick={() => void refresh()} disabled={busy}>
          Refresh
        </Button>
      </section>
      <section className="panel command-filters" aria-label="Dashboard filters">
        <Field label="From date">
          <input
            type="date"
            value={start}
            onChange={(e) => setStart(e.target.value)}
          />
        </Field>
        <Field label="To date (excluded)">
          <input
            type="date"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
          />
        </Field>
        <Field label="Portfolio">
          <select
            aria-label="Portfolio"
            value={portfolio}
            onChange={(e) => setPortfolio(e.target.value)}
          >
            <option value="">All authorized portfolios</option>
            {portfolios.map((p) => (
              <option key={p.id} value={p.id}>
                {p.data.name}
              </option>
            ))}
          </select>
        </Field>
        <Field label="Personal saved view">
          <select
            aria-label="Personal saved view"
            value={selectedView}
            onChange={(e) => {
              setSelectedView(e.target.value);
              const v = views.find((v) => v.id === e.target.value);
              if (v?.data.kind === "saved_views") {
                setStart(v.data.start_date);
                setEnd(v.data.end_date);
                setPortfolio(v.data.portfolio_id || "");
                setDashboard(v.data.dashboard || "Executive");
              }
            }}
          >
            <option value="">Select a view</option>
            {views.map((v) => (
              <option key={v.id} value={v.id}>
                {v.data.name}
              </option>
            ))}
          </select>
        </Field>
        <Field label="New view name">
          <input
            value={viewName}
            maxLength={160}
            onChange={(e) => setViewName(e.target.value)}
          />
        </Field>
        <Button
          disabled={!viewName.trim() || busy}
          onClick={() => void saveView()}
        >
          Save view
        </Button>
        <Button
          disabled={!selectedView || busy}
          onClick={() => void saveView(true)}
        >
          Remove view
        </Button>
        <small>
          Selectors list up to 100 authorized portfolios and personal views.
          Saved filters never grant access.
        </small>
      </section>
      <nav className="tabs" aria-label="Dashboard">
        {(["Executive", "Delivery", "Risk", "Resource"] as Dashboard[]).map(
          (d) => (
            <Button
              key={d}
              variant={dashboard === d ? "primary" : "secondary"}
              aria-pressed={dashboard === d}
              onClick={() => setDashboard(d)}
            >
              {d}
            </Button>
          ),
        )}
      </nav>
      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}
      {notice && <p role="status">{notice}</p>}
      {busy && <p role="status">Loading authorized source records…</p>}
      {snapshot && (
        <>
          <div className="section-heading">
            <p>
              {snapshot.projects.length} authorized projects ·{" "}
              {snapshot.timezone} · computed{" "}
              {new Date(snapshot.computed_at).toLocaleString()} ·{" "}
              {snapshot.metric_version}
            </p>
            <Button onClick={() => void exportSnapshot()}>
              Export metric DTO
            </Button>
          </div>
          {!snapshot.projects.length && (
            <section className="panel">
              <h2>No visible projects</h2>
              <p>
                Add a project or request project access. No portfolio health can
                be calculated yet.
              </p>
              <a href="/projects">Open projects</a>
            </section>
          )}
          {dashboard === "Executive" && (
            <>
              <ChartFrame
                title="Portfolio evidence health"
                description="Equal-weight covered active projects; higher health points are better. Missing projects remain unknown."
                table={metricsTable(
                  snapshot.totals.filter(
                    (m) => m.key === "health" || m.key === "alignment",
                  ),
                )}
              >
                <div className="command-bars">
                  {snapshot.projects.map((p) => {
                    const m = p.metrics.find((m) => m.key === "health");
                    return (
                      <div key={p.id}>
                        <span>
                          {p.name} · {number(m?.value)}
                        </span>
                        <div className="command-track">
                          <div style={{ width: `${Number(m?.value || 0)}%` }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </ChartFrame>
              <section className="panel">
                <h2>Financial and strategic measures</h2>
                {metricsTable(snapshot.totals)}
              </section>
            </>
          )}
          {(dashboard === "Executive" ||
            dashboard === "Risk" ||
            dashboard === "Delivery") &&
            snapshot.projects.map((p) => (
              <section className="panel" key={p.id}>
                <div className="section-heading">
                  <h2>
                    <a href={`/projects/${p.id}`}>{p.name}</a>
                  </h2>
                  <span>
                    Reported {p.reported_health} · Evidence {p.computed_health}
                  </span>
                </div>
                {p.discrepancy && (
                  <p className="command-discrepancy">
                    <strong>Health discrepancy</strong> — reported status
                    conflicts with delivery evidence. Inspect the critical
                    milestones and risk components below.
                  </p>
                )}
                {metricsTable(
                  p.metrics.filter((m) =>
                    dashboard === "Delivery"
                      ? ["variance", "critical"].includes(m.key) ||
                        m.key.startsWith("milestone_")
                      : dashboard === "Risk"
                        ? [
                            "risk",
                            "schedule_risk",
                            "financial_risk",
                            "capacity_risk",
                            "critical",
                          ].includes(m.key)
                        : ["health", "usage", "alignment", "critical"].includes(
                            m.key,
                          ),
                  ),
                )}
                {p.can_edit && (
                  <div className="button-row">
                    <Button
                      onClick={() =>
                        setEditor({
                          kind: dashboard === "Risk" ? "risks" : "benefits",
                          row: null,
                          projectId: p.id,
                        })
                      }
                    >
                      {dashboard === "Risk" ? "Record risk" : "Record benefit"}
                    </Button>
                    <a href={`/projects/${p.id}`}>
                      Edit sources and metric plan
                    </a>
                  </div>
                )}
              </section>
            ))}
          {dashboard === "Delivery" && (
            <section className="panel">
              <h2>Closed sprint velocity</h2>
              <p>
                Points at closure, grouped by team identity; no cross-team point
                ranking. Selected period: {snapshot.start} to {snapshot.end},
                end excluded.
              </p>
              <div
                className="table-scroll"
                tabIndex={0}
                role="region"
                aria-label="Velocity table"
              >
                <table>
                  <thead>
                    <tr>
                      <th>Sprint / team</th>
                      <th>Points</th>
                      <th>Closure date / source</th>
                    </tr>
                  </thead>
                  <tbody>
                    {snapshot.velocity.map((v) => (
                      <tr key={v.sprint_id}>
                        <th>
                          {v.name}
                          <small>Team {v.team_id}</small>
                        </th>
                        <td>{number(v.points)} points</td>
                        <td>
                          {v.end_date} · {v.freshness}
                          <small>
                            {v.policy} ·{" "}
                            {v.source_updated_at || "Closure snapshot missing"}
                          </small>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {!snapshot.velocity.length && (
                <p>No closed sprints in this period.</p>
              )}
            </section>
          )}
          {dashboard !== "Resource" && (
            <section className="panel">
              <h2>
                {dashboard === "Risk"
                  ? "Risk register and escalation readiness"
                  : dashboard === "Delivery"
                    ? "Milestones, blockers and dependencies"
                    : "Recorded business benefits"}
              </h2>
              {!filteredRecords.length && (
                <p>No matching records in this scope.</p>
              )}
              <div className="command-records">
                {filteredRecords.map((r) => {
                  const d = r.data;
                  return (
                    <article key={r.id}>
                      <h3>{d.name}</h3>
                      <p>
                        {"project_id" in d && d.project_id ? (
                          <a href={`/projects/${d.project_id}`}>
                            {names.get(d.project_id) ||
                              "Open authorized project"}
                          </a>
                        ) : null}
                      </p>
                      {d.kind === "risks" && (
                        <>
                          <p>
                            Severity {d.severity}/5 · Likelihood {d.likelihood}
                            /5 · {d.status}
                          </p>
                          <p>
                            Owner: {d.owner_id || "Unassigned"} · Review:{" "}
                            {d.review_on}
                          </p>
                          <p>Mitigation: {d.mitigation || "Missing"}</p>
                          <p>Resolution: {d.resolution || "Pending"}</p>
                          <strong>
                            {d.owner_id && d.mitigation
                              ? "Owner and mitigation recorded"
                              : "Escalation preparation incomplete"}
                            ; routing awaits workflow module.
                          </strong>
                        </>
                      )}
                      {d.kind === "benefits" && (
                        <p>
                          Target {number(d.target)} / realized{" "}
                          {number(d.realized)} {d.unit} · {d.period_start} to{" "}
                          {d.period_end} (end excluded)
                        </p>
                      )}
                      {d.kind === "milestones" && (
                        <p>
                          {d.critical ? "Critical" : "Standard"} · Due{" "}
                          {d.due_date} · Actual {d.actual_date || "Unfinished"}
                        </p>
                      )}
                      {d.kind === "blockers" && (
                        <p>
                          {d.status} · Owner {d.owner_id || "Unassigned"}
                        </p>
                      )}
                      {d.kind === "dependencies" && (
                        <p>
                          {names.get(d.project_id)} →{" "}
                          <a href={`/projects/${d.target_project_id}`}>
                            {names.get(d.target_project_id) ||
                              "Authorized dependency project"}
                          </a>
                          <small>
                            Predecessor → successor · source{" "}
                            {d.source_milestone_id ||
                              d.source_work_item_id ||
                              "project"}{" "}
                            · target{" "}
                            {d.target_milestone_id ||
                              d.target_work_item_id ||
                              "project"}
                          </small>
                        </p>
                      )}
                      <p>{d.description}</p>
                      <small>
                        Stored {d.kind} · updated{" "}
                        {new Date(r.updated_at).toLocaleString()} ·{" "}
                        {Date.now() - Date.parse(r.updated_at) >
                        snapshot.stale_days * 86400000
                          ? "stale"
                          : "fresh"}
                      </small>
                      {"project_id" in d &&
                        d.project_id &&
                        editable.has(d.project_id) && (
                          <Button
                            onClick={() =>
                              setEditor({
                                kind: d.kind,
                                row: r,
                                projectId: d.project_id!,
                              })
                            }
                          >
                            Edit {d.name}
                          </Button>
                        )}
                    </article>
                  );
                })}
              </div>
            </section>
          )}
          {dashboard === "Resource" && (
            <>
              <section className="panel">
                <h2>Assigned resource capacity</h2>
                <p>
                  {snapshot.start} to {snapshot.end} (end excluded). Source:
                  availability, calendars, leave, allocations and authorized
                  effort. Whole-resource scope is stated per row.
                </p>
                <div
                  className="table-scroll"
                  tabIndex={0}
                  role="region"
                  aria-label="Resource capacity table"
                >
                  <table>
                    <thead>
                      <tr>
                        <th>Resource / scope</th>
                        <th>Available</th>
                        <th>Allocated</th>
                        <th>Planned / actual utilization</th>
                        <th>Freshness / source</th>
                      </tr>
                    </thead>
                    <tbody>
                      {snapshot.resources.map(
                        ({ summary: r, freshness, source_updated_at }) => (
                          <tr key={r.resource_id}>
                            <th>
                              <a href="/resources">{r.resource_name}</a>
                              <small>{r.scope}</small>
                            </th>
                            <td>{number(r.available_hours)} h</td>
                            <td>{number(r.allocated_hours)} h</td>
                            <td>
                              {number(r.planned_percent)}% /{" "}
                              {number(r.actual_percent)}%
                              <small>
                                {r.effort_complete
                                  ? "Effort complete"
                                  : "Effort incomplete or restricted"}
                              </small>
                            </td>
                            <td>
                              {freshness}
                              <small>
                                {source_updated_at || "Missing source"} ·
                                capacity-v1
                              </small>
                            </td>
                          </tr>
                        ),
                      )}
                    </tbody>
                  </table>
                </div>
                {!snapshot.resources.length && (
                  <p>
                    No assigned resources in the selected interval or next four
                    weeks.
                  </p>
                )}
              </section>
              <section className="panel">
                <h2>Team workload support signals</h2>
                {snapshot.teams.map((t) => (
                  <article key={t.summary.team_id}>
                    <h3>{t.name}</h3>
                    <p>
                      {t.summary.status} · Planned{" "}
                      {number(t.summary.planned_percent)}% · Actual{" "}
                      {number(t.summary.actual_percent)}%
                    </p>
                    <p>
                      Sustained overload:{" "}
                      {t.summary.sustained_overload == null
                        ? "Unknown"
                        : t.summary.sustained_overload
                          ? "Yes"
                          : "No"}
                      . Overtime warning:{" "}
                      {t.summary.overtime_warning == null
                        ? "Unknown"
                        : t.summary.overtime_warning
                          ? "Yes"
                          : "No"}
                      .
                    </p>
                    <small>
                      Capacity-v1 · selected period · current team sources,
                      freshness shown in resource rows. Minimum five resources
                      every day; restricted evidence remains unknown.
                    </small>
                  </article>
                ))}
                {!snapshot.teams.length && (
                  <p>No reporting teams linked to the selected projects.</p>
                )}
              </section>
            </>
          )}
          <details className="panel">
            <summary>Metric rules and limitations</summary>
            <p>
              {snapshot.risk_rule} · Amber ≥{snapshot.amber}, Red ≥
              {snapshot.red} · stale after {snapshot.stale_days} days · policy
              revision {snapshot.policy_revision}
            </p>
            {snapshot.limitations.map((l) => (
              <p key={l}>{l}</p>
            ))}
            {account.role === "Admin" && (
              <a href="/organization">Configure metric policy</a>
            )}
          </details>
        </>
      )}
      <Modal
        open={!!evidence}
        title={evidence ? `${evidence.label} evidence` : "Evidence"}
        drawer
        onClose={() => setEvidence(null)}
      >
        {evidence && (
          <>
            <p>
              {number(evidence.value)} {evidence.unit} · {evidence.period}
            </p>
            <p>{evidence.explanation}</p>
            <p>
              Coverage {number(evidence.coverage_percent)}% ·{" "}
              {evidence.freshness} · source {evidence.source}
            </p>
            {!evidence.facts.length && (
              <p>No supporting records are available.</p>
            )}
            <ul>
              {evidence.facts.map((f, i) => (
                <li key={`${f.id}-${i}`}>
                  <strong>{f.name}</strong>
                  <p>{f.detail}</p>
                  <small>
                    {f.kind} · {f.id} ·{" "}
                    {new Date(f.updated_at).toLocaleString()}
                  </small>
                </li>
              ))}
            </ul>
          </>
        )}
      </Modal>
      <Modal
        open={!!editor}
        title={
          editor
            ? `${editor.row ? "Edit" : "Create"} ${editor.kind}`
            : "Edit record"
        }
        onClose={() => setEditor(null)}
      >
        {editor && (
          <RecordEditor
            kind={editor.kind}
            row={editor.row}
            projectId={editor.projectId}
            client={client}
            onClose={() => setEditor(null)}
            onSaved={() => {
              setEditor(null);
              void refresh();
            }}
          />
        )}
      </Modal>
    </div>
  );
}
