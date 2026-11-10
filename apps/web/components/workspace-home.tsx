"use client";
import { useEffect, useRef, useState } from "react";
import type { components } from "@ppm/contracts/schema";
import { Button, DataTable, Field, Skeleton, StatePanel } from "./ui";
import { Icon, type IconName } from "./icon";
import { usePilotApi } from "./pilot-api";

type S = components["schemas"];
const healthStates = ["Green", "Amber", "Red", "Unknown"] as const;
type Health = (typeof healthStates)[number];
type HealthFilter = Health | "All" | "Attention";
const healthOf = (project: S["ProjectMetrics"]): Health =>
  healthStates.includes(project.computed_health as Health)
    ? (project.computed_health as Health)
    : "Unknown";
function dateRange(days: number, timeZone: string) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(new Date());
  const part = (type: string) =>
    Number(parts.find((value) => value.type === type)?.value);
  // Calendar-day arithmetic stays independent of daylight-saving hour changes.
  const end = new Date(
    Date.UTC(part("year"), part("month") - 1, part("day") + 1),
  );
  const start = new Date(end);
  start.setUTCDate(start.getUTCDate() - days);
  return {
    start: start.toISOString().slice(0, 10),
    end: end.toISOString().slice(0, 10),
  };
}

export function WorkspaceHome({
  account,
  sessionCount,
  transport,
}: {
  account: S["AccountView"];
  sessionCount: number;
  transport: typeof fetch;
}) {
  const api = usePilotApi(transport);
  const [snapshot, setSnapshot] = useState<S["CommandSnapshot"] | null>(null);
  const [portfolios, setPortfolios] = useState<S["PageView"] | null>(null);
  const [portfolioError, setPortfolioError] = useState(false);
  const [portfolio, setPortfolio] = useState("");
  const [days, setDays] = useState(30);
  const [filter, setFilter] = useState<HealthFilter>("All");
  const [error, setError] = useState("");
  const [refresh, setRefresh] = useState(0);
  const timezone = useRef("UTC");
  useEffect(() => {
    let live = true;
    setPortfolios(null);
    setPortfolioError(false);
    void api<S["PageView"]>("delivery/portfolios?limit=100")
      .then((data) => {
        if (live) setPortfolios(data);
      })
      .catch(() => {
        if (live) setPortfolioError(true);
      });
    return () => {
      live = false;
    };
  }, [api, refresh]);
  useEffect(() => {
    let live = true;
    setSnapshot(null);
    setError("");
    async function load() {
      const range = dateRange(days, timezone.current);
      const request = (period: typeof range) =>
        api<S["CommandSnapshot"]>(
          "command/snapshot?" +
            new URLSearchParams({
              ...period,
              ...(portfolio ? { portfolio_id: portfolio } : {}),
            }),
        );
      let data = await request(range);
      if (!live) return;
      timezone.current = data.timezone;
      const organizationRange = dateRange(days, data.timezone);
      // The first snapshot discovers the organization's calendar. Correct its
      // period once when the UTC bootstrap date differs, without an effect loop.
      if (
        organizationRange.start !== range.start ||
        organizationRange.end !== range.end
      ) {
        data = await request(organizationRange);
        if (!live) return;
        timezone.current = data.timezone;
      }
      setSnapshot(data);
    }
    void load().catch((e: Error) => {
      if (live) setError(e.message);
    });
    return () => {
      live = false;
    };
  }, [api, portfolio, days, refresh]);
  const projects = snapshot?.projects || [];
  const periodSpend =
    snapshot?.totals.filter((metric) => metric.key.endsWith("_period_spend")) ||
    [];
  const counts = Object.fromEntries(
    healthStates.map((health) => [
      health,
      projects.filter((p) => healthOf(p) === health).length,
    ]),
  ) as Record<Health, number>;
  const coverage = projects.length
    ? Math.round(((projects.length - counts.Unknown) / projects.length) * 100)
    : null;
  const visible = projects.filter(
    (p) =>
      filter === "All" ||
      (filter === "Attention"
        ? ["Amber", "Red"].includes(healthOf(p))
        : healthOf(p) === filter),
  );
  const metrics: {
    label: string;
    value: number | string | null;
    detail: string;
    icon: IconName;
    filter: HealthFilter;
  }[] = [
    {
      label: "Visible projects",
      value: projects.length,
      detail: "Permission-scoped snapshot",
      icon: "overview",
      filter: "All",
    },
    {
      label: "Need attention",
      value: counts.Amber + counts.Red,
      detail: "Amber or Red computed health",
      icon: "warning",
      filter: "Attention",
    },
    {
      label: "Healthy projects",
      value: counts.Green,
      detail: "Green computed health",
      icon: "check",
      filter: "Green",
    },
    {
      label: "Health coverage",
      value: coverage == null ? null : `${coverage}%`,
      detail: "Known health / visible projects",
      icon: "coverage",
      filter: "Unknown",
    },
  ];
  return (
    <>
      <section className="page-heading home-heading">
        <div>
          <h1>Welcome, {account.name.split(" ")[0]}.</h1>
          <p className="lead">
            Your portfolio, with the next decision in view.
          </p>
        </div>
        <a className="text-action" href="/command-center">
          Open command center <Icon name="arrow" size={18} />
        </a>
      </section>
      <section
        className="panel portfolio-overview"
        aria-labelledby="portfolio-overview-title"
      >
        <div className="overview-toolbar">
          <div>
            <h2 id="portfolio-overview-title">Portfolio overview</h2>
            <p className="muted">
              Current project health · activity within the selected period.
            </p>
          </div>
          <div className="overview-filters">
            <Field label="Portfolio scope">
              <select
                value={portfolio}
                onChange={(e) => {
                  setPortfolio(e.target.value);
                  setFilter("All");
                }}
              >
                <option value="">All permitted portfolios</option>
                {portfolios?.items.map((p) => (
                  <option value={p.id} key={p.id}>
                    {p.data.name}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="Activity period">
              <select
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
              >
                <option value={30}>Last 30 days</option>
                <option value={90}>Last 90 days</option>
                <option value={365}>Last 365 days</option>
              </select>
            </Field>
            <Button
              variant="secondary"
              onClick={() => setRefresh((r) => r + 1)}
            >
              Refresh
            </Button>
          </div>
        </div>
        {(portfolioError ||
          (portfolios && portfolios.total > portfolios.items.length)) && (
          <p className="muted">
            {portfolioError
              ? "Portfolio choices are unavailable."
              : `Showing ${portfolios?.items.length} of ${portfolios?.total} permitted portfolio choices.`}{" "}
            Use the Command center for additional scope controls.
          </p>
        )}
        <div className="overview-metrics" aria-label="Portfolio statistics">
          {metrics.map((m) => (
            <button
              key={m.label}
              className="overview-metric"
              disabled={!snapshot}
              aria-pressed={filter === m.filter}
              onClick={() => {
                setFilter(m.filter);
                document
                  .getElementById("projects-in-focus")
                  ?.scrollIntoView({ block: "nearest" });
              }}
            >
              <span className="metric-symbol">
                <Icon name={m.icon} size={22} />
              </span>
              <span>
                <span className="metric-label">{m.label}</span>
                <strong>{snapshot ? (m.value ?? "Unavailable") : "—"}</strong>
                <small>
                  {m.detail}
                  {m.filter === "Unknown" ? " · View unknown" : ""}
                </small>
              </span>
            </button>
          ))}
        </div>
        {snapshot && (
          <section
            className="period-spend"
            aria-labelledby="period-spend-title"
          >
            <div className="period-spend-heading">
              <h3 id="period-spend-title">Recorded spend in period</h3>
              <p className="muted">
                Separate currency totals. Partial ledgers may omit spending;
                zero means no recorded spend.
              </p>
            </div>
            {periodSpend.length ? (
              <div className="period-spend-values">
                {periodSpend.map((metric) => (
                  <div className="period-spend-value" key={metric.key}>
                    <strong>
                      {metric.value == null
                        ? "Unavailable"
                        : Number(metric.value).toLocaleString(undefined, {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })}{" "}
                      {metric.unit}
                    </strong>
                    <small className="spend-quality">
                      {metric.status === "partial"
                        ? "Partial ledger"
                        : metric.status === "unknown"
                          ? "Unavailable"
                          : "Available"}{" "}
                      · Source {metric.freshness}
                    </small>
                  </div>
                ))}
              </div>
            ) : (
              <p className="muted">
                No financial totals are available in this scope. Recorded
                spending appears for permitted projects with a currency.
              </p>
            )}
          </section>
        )}
        {snapshot && (
          <p className="snapshot-meta">
            Snapshot{" "}
            {new Date(snapshot.computed_at).toLocaleString(undefined, {
              timeZone: snapshot.timezone,
            })}{" "}
            · {snapshot.timezone}. Health is current, not a historical trend.
            Activity: {snapshot.start} to {snapshot.end} (end excluded).
          </p>
        )}
      </section>
      {error && (
        <StatePanel
          title="Portfolio snapshot unavailable"
          kind="error"
          action={
            <div className="actions">
              <Button onClick={() => setRefresh((r) => r + 1)}>
                Retry snapshot
              </Button>
              <a className="button secondary" href="/command-center">
                Open scope controls
              </a>
            </div>
          }
        >
          {error} Narrow the portfolio scope if the snapshot exceeds service
          limits.
        </StatePanel>
      )}
      {!snapshot && !error && <Skeleton label="Loading portfolio snapshot" />}
      <div className="overview-grid">
        <section className="panel health-panel" aria-labelledby="health-title">
          <div className="section-heading">
            <div>
              <h2 id="health-title">Portfolio health</h2>
              <p className="muted">
                Select a health category to explore its projects.
              </p>
            </div>
            <span className="health-total">
              {snapshot ? projects.length : "—"}
              <small>visible projects</small>
            </span>
          </div>
          <div className="health-bars">
            {healthStates.map((health) => (
              <button
                className="health-bar"
                key={health}
                disabled={!snapshot}
                aria-pressed={filter === health}
                onClick={() => setFilter(filter === health ? "All" : health)}
                title={`${health}: ${snapshot ? counts[health] : "unavailable"} visible projects`}
              >
                <span>
                  <i className={`health-dot health-${health.toLowerCase()}`} />
                  {health === "Unknown" ? "Unknown health" : `${health} health`}
                </span>
                <span className="health-track">
                  <span
                    className={`health-fill health-${health.toLowerCase()}`}
                    style={{
                      transform: `scaleX(${snapshot && projects.length ? counts[health] / projects.length : 0})`,
                    }}
                  />
                </span>
                <b>{snapshot ? counts[health] : "—"}</b>
              </button>
            ))}
          </div>
          {snapshot && !projects.length && (
            <p className="muted">
              No permitted projects in this scope. Health coverage is
              unavailable until projects have evidence.
            </p>
          )}
          <details>
            <summary>View chart data table</summary>
            <div
              className="table-scroll"
              tabIndex={0}
              role="region"
              aria-label="Health distribution data"
            >
              <table>
                <caption>Computed health across visible projects</caption>
                <thead>
                  <tr>
                    <th scope="col">Category</th>
                    <th scope="col">Projects</th>
                  </tr>
                </thead>
                <tbody>
                  {healthStates.map((health) => (
                    <tr key={health}>
                      <th scope="row">{health}</th>
                      <td>{snapshot ? counts[health] : "Unavailable"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
          <a className="text-action" href="/projects">
            View underlying projects <Icon name="arrow" size={17} />
          </a>
        </section>
        <section className="panel access-panel">
          <h2>Workspace access</h2>
          <dl className="access-list">
            <div>
              <dt>
                <Icon name="account" size={18} />
                Account role
              </dt>
              <dd>{account.role}</dd>
            </div>
            <div>
              <dt>
                <Icon name="portfolios" size={18} />
                Connected organizations
              </dt>
              <dd>{account.organizations.length}</dd>
            </div>
            <div>
              <dt>
                <Icon name="monitor" size={18} />
                Active sessions
              </dt>
              <dd>{sessionCount}</dd>
            </div>
          </dl>
          <p className="muted">Sessions returned by the service, up to 100.</p>
          <a className="text-action" href="/account">
            Manage account <Icon name="arrow" size={17} />
          </a>
          {account.role === "Admin" && (
            <a className="text-action" href="/account#members">
              Manage members <Icon name="arrow" size={17} />
            </a>
          )}
        </section>
      </div>
      <section
        className="panel focus-projects"
        id="projects-in-focus"
        aria-labelledby="focus-title"
      >
        <div className="section-heading">
          <div>
            <h2 id="focus-title">Projects in focus</h2>
            <p className="muted" role="status">
              {snapshot
                ? `${visible.length} of ${projects.length} visible projects · ${filter === "All" ? "All health categories" : filter === "Attention" ? "Amber or Red health" : `${filter} health`}`
                : "Projects appear when your snapshot is available."}
            </p>
          </div>
          {filter !== "All" && (
            <Button variant="secondary" onClick={() => setFilter("All")}>
              Show all health categories
            </Button>
          )}
        </div>
        {snapshot && (
          <DataTable
            key={`${portfolio}-${filter}`}
            rows={visible}
            rowKey={(p) => p.id}
            caption="Projects in focus"
            searchText={(p) => `${p.name} ${healthOf(p)} ${p.reported_health}`}
            pageSize={5}
            columns={[
              {
                key: "name",
                label: "Project",
                sort: (p) => p.name,
                render: (p) => (
                  <a className="project-link" href={`/projects/${p.id}`}>
                    {p.name}
                    <Icon name="arrow" size={16} />
                  </a>
                ),
              },
              {
                key: "health",
                label: "Computed health",
                sort: (p) => healthOf(p),
                render: (p) => (
                  <span
                    className={`health-label health-label-${healthOf(p).toLowerCase()}`}
                  >
                    <i
                      className={`health-dot health-${healthOf(p).toLowerCase()}`}
                    />
                    {healthOf(p)}
                  </span>
                ),
              },
              {
                key: "evidence",
                label: "Evidence health",
                render: (p) => {
                  const m = p.metrics.find((m) => m.key === "health");
                  return (
                    <span title={m?.explanation}>
                      {m?.value == null
                        ? "Unavailable"
                        : `${Number(m.value).toLocaleString(undefined, { maximumFractionDigits: 1 })} ${m.unit}`}
                    </span>
                  );
                },
              },
              {
                key: "reported",
                label: "Reported health",
                render: (p) => (
                  <span>
                    {p.reported_health}
                    {p.discrepancy && (
                      <small className="discrepancy-note">
                        Review discrepancy
                      </small>
                    )}
                  </span>
                ),
              },
            ]}
          />
        )}
        <a className="text-action" href="/projects">
          View all projects <Icon name="arrow" size={17} />
        </a>
        {snapshot && (
          <details className="snapshot-notes">
            <summary>Sources & metric definitions</summary>
            <p>
              {snapshot.scope} Health categories use the server's versioned
              metric policy; the chart counts all visible projects. Coverage is
              the percentage with a known category. Unknown is not healthy or
              zero. Attention means Amber or Red.
            </p>
            {snapshot.limitations.map((note) => (
              <p key={note}>{note}</p>
            ))}
            <p>
              Metric version: {snapshot.metric_version} · Policy revision:{" "}
              {snapshot.policy_revision}
            </p>
            {snapshot.totals
              .filter((m) => m.key.endsWith("_period_spend"))
              .map((m) => (
                <p key={m.key}>
                  <strong>
                    {m.label}: {m.value ?? "Unavailable"} {m.unit}
                  </strong>{" "}
                  · {m.period} · {m.status} · {m.freshness}
                  <br />
                  {m.explanation}
                  <br />
                  Source: {m.source}
                </p>
              ))}
          </details>
        )}
      </section>
      <section className="panel quick-links" aria-labelledby="continue-title">
        <div>
          <h2 id="continue-title">Continue your work</h2>
          <p className="muted">Your next task, one step away.</p>
        </div>
        {(
          [
            ["Projects", "/projects", "projects", "Plan and track delivery"],
            [
              "Assessments",
              "/assessments",
              "assessments",
              "Continue an assessment",
            ],
            ["Documents", "/documents", "documents", "Find your evidence"],
            ["Resources", "/resources", "resources", "Review team capacity"],
          ] as const
        ).map(([label, href, icon, detail]) => (
          <a key={href} href={href}>
            <Icon name={icon} />
            <span>
              <b>{label}</b>
              <small>{detail}</small>
            </span>
            <Icon name="arrow" size={16} />
          </a>
        ))}
      </section>
    </>
  );
}
