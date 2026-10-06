"use client";
import { useEffect, useState } from "react";
import type { components } from "@ppm/contracts/schema";
import { createApiClient } from "@ppm/contracts";
import { ChangeDetails, RecordEditor, RelatedName } from "./delivery";
import {
  fields,
  immutable,
  labels,
  type DeliveryRecord,
  type Kind,
} from "./delivery-fields";
import {
  Badge,
  Button,
  Field,
  MetricCard,
  Modal,
  Skeleton,
  StatePanel,
} from "./ui";

type Client = ReturnType<typeof createApiClient>;
type Summary = components["schemas"]["CapacityView"];
function check<T>(r: { data?: T; response: Response; error?: unknown }): T {
  if (!r.response.ok) {
    const e = r.error as { error?: { message?: string } };
    throw new Error(
      e?.error?.message ||
        `Request failed (${r.response.status}). Reload and try again.`,
    );
  }
  return r.data as T;
}
const kinds: Kind[] = [
  "resources",
  "calendars",
  "availability",
  "resource_skills",
  "resource_teams",
  "allocations",
  "time_off",
  "effort",
  "effort_coverage",
  "resource_access",
  "capacity_snapshots",
];
const number = (v: string | number | null | undefined) =>
  v == null ? "Unknown" : Number(v).toFixed(2);

function SavedPlan({ data }: { data: Record<string, unknown> }) {
  const days = Array.isArray(data.days) ? (data.days as Summary["days"]) : [];
  const sources = data.sources as
    { allocations?: Record<string, unknown>[] } | undefined;
  return (
    <>
      <h3>Captured daily plan</h3>
      <p>
        {String(data.start_date)} until {String(data.end_date)} (excluded).
        Local scheduled hours, including approved leave and holidays.
      </p>
      <div className="table-scroll">
        <table className="capacity-table">
          <caption>Preserved capacity in hours</caption>
          <thead>
            <tr>
              <th>Date</th>
              <th>Available</th>
              <th>Allocated</th>
              <th>Excess</th>
            </tr>
          </thead>
          <tbody>
            {days.map((d) => (
              <tr key={d.day}>
                <th>{d.day}</th>
                <td>{number(d.available_hours)}</td>
                <td>{number(d.allocated_hours)}</td>
                <td>{number(d.excess_hours)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <h3>Preserved allocations</h3>
      {sources?.allocations?.map((a) => (
        <p key={String(a.id)}>
          {String(a.name)} · {String(a.start_date)} until {String(a.end_date)} ·{" "}
          {String(a.hours_per_day)} hours per scheduled day · revision{" "}
          {String(a.revision)}
        </p>
      ))}
    </>
  );
}

export function Capacity({
  account,
  client,
}: {
  account: components["schemas"]["AccountView"];
  client: Client;
}) {
  const [kind, setKind] = useState<Kind>("resources");
  const [resources, setResources] = useState<DeliveryRecord[]>([]);
  const [resourceId, setResourceId] = useState("");
  const [skill, setSkill] = useState("");
  const [q, setQ] = useState("");
  const [start, setStart] = useState(new Date().toISOString().slice(0, 10));
  const [end, setEnd] = useState(
    new Date(Date.now() + 14 * 86400000).toISOString().slice(0, 10),
  );
  const [rows, setRows] = useState<DeliveryRecord[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [archived, setArchived] = useState(false);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [project, setProject] = useState("");
  const [projects, setProjects] = useState<DeliveryRecord[]>([]);
  const [teams, setTeams] = useState<DeliveryRecord[]>([]);
  const [teamId, setTeamId] = useState("");
  const [team, setTeam] = useState<
    components["schemas"]["TeamCapacityView"] | null
  >(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [refresh, setRefresh] = useState(0);
  const [editor, setEditor] = useState<{ row: DeliveryRecord | null } | null>(
    null,
  );
  const [history, setHistory] = useState<
    components["schemas"]["HistoryView"][] | null
  >(null);
  const [snapshot, setSnapshot] = useState<
    components["schemas"]["SnapshotView"] | null
  >(null);
  const [notice, setNotice] = useState("");
  useEffect(() => {
    let valid = true;
    void Promise.all(
      ["resources", "projects", "teams"].map(async (k) =>
        check(
          await client.GET("/api/v1/delivery/{kind}", {
            params: {
              path: { kind: k as Kind },
              query: { limit: 100, ...(k === "resources" ? { skill, q } : {}) },
            },
          }),
        ),
      ),
    )
      .then(([r, p, t]) => {
        if (!valid) return;
        setResources(r.items);
        setProjects(p.items);
        setTeams(t.items);
        if (resourceId && !r.items.some((x) => x.id === resourceId))
          setResourceId("");
      })
      .catch((e) => {
        if (valid) setError(String(e.message));
      });
    return () => {
      valid = false;
    };
  }, [client, refresh, skill, q, resourceId]);
  useEffect(() => {
    let valid = true;
    setLoading(true);
    setError("");
    setSummary(null);
    setTeam(null);
    setRows([]);
    void (async () => {
      try {
        const r = check(
          await client.GET("/api/v1/delivery/{kind}", {
            params: {
              path: { kind },
              query: {
                offset,
                limit: 20,
                archived,
                resource_id:
                  resourceId && !["resources", "calendars"].includes(kind)
                    ? resourceId
                    : undefined,
                ...(kind === "resources" ? { q, skill } : {}),
              },
            },
          }),
        );
        const s = resourceId
          ? check(
              await client.GET("/api/v1/capacity/resources/{rid}", {
                params: {
                  path: { rid: resourceId },
                  query: { start, end, project_id: project || undefined },
                },
              }),
            )
          : null;
        const t = teamId
          ? check(
              await client.GET("/api/v1/capacity/teams/{tid}", {
                params: { path: { tid: teamId }, query: { start, end } },
              }),
            )
          : null;
        if (valid) {
          setRows(r.items);
          setTotal(r.total);
          setSummary(s);
          setTeam(t);
        }
      } catch (e) {
        if (valid)
          setError(e instanceof Error ? e.message : "Unable to load staffing");
      } finally {
        if (valid) setLoading(false);
      }
    })();
    return () => {
      valid = false;
    };
  }, [
    client,
    kind,
    resourceId,
    start,
    end,
    project,
    teamId,
    refresh,
    offset,
    archived,
    q,
    skill,
  ]);
  const admin = account.role === "Admin";
  const sensitive = ["effort", "effort_coverage"].includes(kind);
  const canWrite =
    account.role !== "Viewer" &&
    (sensitive
      ? Boolean(summary?.can_effort)
      : [
            "resource_access",
            "calendars",
            "capacity_snapshots",
            "resources",
          ].includes(kind)
        ? admin
        : admin || Boolean(summary?.can_manage));
  async function showHistory(row: DeliveryRecord) {
    try {
      setHistory(
        check(
          await client.GET("/api/v1/delivery/history/{kind}/{id_}", {
            params: { path: { kind, id_: row.id } },
          }),
        ),
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : "History unavailable");
    }
  }
  return (
    <>
      <header className="page-heading">
        <div>
          <p className="eyebrow">People & delivery</p>
          <h1>Resource planning</h1>
          <p>
            Plan shared capacity across projects. Resource profiles can exist
            without a login.
          </p>
        </div>
      </header>
      {notice && (
        <p role="status" className="notice">
          {notice}
        </p>
      )}
      {error && (
        <StatePanel
          kind="error"
          title="Staffing could not load"
          children={error}
          action={
            <Button onClick={() => setRefresh((x) => x + 1)}>Reload</Button>
          }
        />
      )}
      <section className="panel">
        <h2>Staffing scope</h2>
        <div className="delivery-fields">
          <Field label="Find resources">
            <input
              value={q}
              onChange={(e) => {
                setQ(e.target.value);
                setOffset(0);
              }}
            />
          </Field>
          <Field label="Exact skill filter">
            <input
              value={skill}
              onChange={(e) => {
                setSkill(e.target.value);
                setOffset(0);
              }}
            />
          </Field>
          <Field label="Resource profile">
            <select
              value={resourceId}
              onChange={(e) => {
                setResourceId(e.target.value);
                setOffset(0);
              }}
            >
              <option value="">Choose a resource</option>
              {resources.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.data.name}
                </option>
              ))}
            </select>
          </Field>
          <Field label="From date">
            <input
              type="date"
              required
              value={start}
              onChange={(e) => setStart(e.target.value)}
            />
          </Field>
          <Field label="Until date (excluded)">
            <input
              type="date"
              required
              value={end}
              onChange={(e) => setEnd(e.target.value)}
            />
          </Field>
          <Field label="Project utilization slice">
            <select
              value={project}
              onChange={(e) => setProject(e.target.value)}
            >
              <option value="">All authorized projects</option>
              {projects.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.data.name}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Team utilization">
            <select value={teamId} onChange={(e) => setTeamId(e.target.value)}>
              <option value="">Choose a team</option>
              {teams.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.data.name}
                </option>
              ))}
            </select>
          </Field>
        </div>
        <p className="muted">
          Selectors show up to 100 authorized matches. Hours follow each
          resource’s local calendar; end dates are excluded. Refresh after
          access changes.
        </p>
      </section>
      {loading ? (
        <Skeleton label="Loading staffing" />
      ) : (
        summary && (
          <section className="panel">
            <h2>{summary.resource_name}: capacity heatmap</h2>
            <p>
              {summary.scope === "full_resource"
                ? "Full resource plan across projects"
                : "Partial project scope: full utilization and overload are unknown"}{" "}
              · {summary.metric_version} · As of{" "}
              {new Date(summary.as_of).toLocaleString()}
            </p>
            <div className="metrics-grid">
              <MetricCard
                detail="Selected date interval"
                label="Available hours"
                value={number(summary.available_hours)}
              />
              <MetricCard
                detail="Selected date interval"
                label="Allocated hours"
                value={number(summary.allocated_hours)}
              />
              <MetricCard
                detail="Selected date interval"
                label="Planned utilization %"
                value={number(summary.planned_percent)}
              />
              <MetricCard
                detail="Selected date interval"
                label="Excess hours"
                value={number(summary.excess_hours)}
              />
              <MetricCard
                detail="Selected date interval"
                label="Actual utilization %"
                value={number(summary.actual_percent)}
              />
            </div>
            <p>
              {summary.can_effort
                ? summary.effort_complete
                  ? "Complete timesheet coverage"
                  : "Partial timesheets: actual utilization is unknown"
                : "Sensitive effort is restricted"}
            </p>
            <div className="capacity-heatmap" aria-hidden="true">
              {summary.days.map((d) => (
                <span
                  key={d.day}
                  className={
                    d.available_hours == null
                      ? "capacity-unknown"
                      : Number(d.excess_hours) > 0
                        ? "capacity-over"
                        : "capacity-normal"
                  }
                >
                  {d.day.slice(5)}
                  <strong>
                    {number(d.allocated_hours)} / {number(d.available_hours)} h
                  </strong>
                  {Number(d.excess_hours) > 0
                    ? "Over capacity"
                    : d.planned_percent == null
                      ? "Unknown utilization"
                      : `${number(d.planned_percent)}%`}
                </span>
              ))}
            </div>
            <div className="table-scroll">
              <table className="capacity-table">
                <caption>
                  Weekly capacity reconciliation (Monday weeks, clipped to
                  selected dates)
                </caption>
                <thead>
                  <tr>
                    <th>From</th>
                    <th>Until (excluded)</th>
                    <th>Available h</th>
                    <th>Allocated h</th>
                    <th>Excess h</th>
                    <th>Planned %</th>
                  </tr>
                </thead>
                <tbody>
                  {summary.weeks.map((w) => (
                    <tr key={w.start_date}>
                      <th>{w.start_date}</th>
                      <td>{w.end_date}</td>
                      <td>{number(w.available_hours)}</td>
                      <td>{number(w.allocated_hours)}</td>
                      <td>{number(w.excess_hours)}</td>
                      <td>{number(w.planned_percent)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="table-scroll">
              <table className="capacity-table">
                <caption>
                  Daily capacity in hours — equivalent heatmap table
                </caption>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Timezone</th>
                    <th>Available</th>
                    <th>Allocated</th>
                    <th>Excess</th>
                    <th>Actual</th>
                    <th>Timesheet</th>
                  </tr>
                </thead>
                <tbody>
                  {summary.days.map((d) => (
                    <tr key={d.day}>
                      <th>{d.day}</th>
                      <td>{d.timezone || "Missing calendar"}</td>
                      <td>{number(d.available_hours)}</td>
                      <td>{number(d.allocated_hours)}</td>
                      <td>{number(d.excess_hours)}</td>
                      <td>{number(d.actual_hours)}</td>
                      <td>
                        {d.effort_complete ? "Complete" : "Unknown / partial"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )
      )}
      {team && (
        <section className="panel">
          <h2>Team workload support signals</h2>
          <p>{team.label}</p>
          <p>
            {team.resource_count} resources · {team.status.replaceAll("_", " ")}
          </p>
          {team.status === "available" && (
            <>
              <p>
                Available {number(team.available_hours)} h · Allocated{" "}
                {number(team.allocated_hours)} h · Planned{" "}
                {number(team.planned_percent)}% · Actual{" "}
                {number(team.actual_percent)}%
              </p>
              <p>
                Two consecutive full weeks over capacity:{" "}
                {team.sustained_overload == null
                  ? "Unknown"
                  : team.sustained_overload
                    ? "Yes — review staffing"
                    : "No"}
                . Overtime above 10%:{" "}
                {team.overtime_warning == null
                  ? "Unknown / restricted"
                  : team.overtime_warning
                    ? "Yes — offer support"
                    : "No"}
                .
              </p>
            </>
          )}
        </section>
      )}
      <section className="panel">
        <div className="actions">
          <Field label="Planning records">
            <select
              value={kind}
              onChange={(e) => {
                setKind(e.target.value as Kind);
                setOffset(0);
                setArchived(false);
              }}
            >
              {kinds
                .filter((k) => k !== "resource_access" || admin)
                .map((k) => (
                  <option key={k} value={k}>
                    {labels[k]}
                  </option>
                ))}
            </select>
          </Field>
          <label className="checkbox">
            <input
              type="checkbox"
              checked={archived}
              onChange={(e) => {
                setArchived(e.target.checked);
                setOffset(0);
              }}
            />
            Archived records
          </label>
          {canWrite && (
            <Button onClick={() => setEditor({ row: null })}>
              Create {labels[kind].toLowerCase()}
            </Button>
          )}
          <Button variant="secondary" onClick={() => setRefresh((x) => x + 1)}>
            Refresh staffing
          </Button>
        </div>
        <h2>{kind === "allocations" ? "Staffing matrix" : labels[kind]}</h2>
        {kind === "calendars" && (
          <p>
            Calendar versions are immutable. To change working hours, create a
            new calendar and assign dated availability.
          </p>
        )}
        {kind === "time_off" && (
          <p>
            Enter approved hours only. Do not record medical reasons or personal
            notes.
          </p>
        )}
        {sensitive && !summary?.can_effort && (
          <p>
            Choose a resource with an explicit sensitive effort grant to enter
            or amend timesheets.
          </p>
        )}
        {!loading && !rows.length && (
          <StatePanel
            kind="empty"
            title="No visible records"
            children="Create a record if permitted, or adjust the resource and archive filters."
          />
        )}
        <div className="table-scroll">
          <table className="capacity-table">
            <caption>
              {total} authorized records; page {Math.floor(offset / 20) + 1}
            </caption>
            <thead>
              <tr>
                <th>Name</th>
                <th>Details</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id}>
                  <th>
                    {r.data.kind === "resources" ? (
                      <button onClick={() => setResourceId(r.id)}>
                        {r.data.name}
                      </button>
                    ) : (
                      r.data.name
                    )}
                    <small className="capacity-revision">
                      Revision {r.revision}
                    </small>
                  </th>
                  <td>
                    {fields[kind].map((f) => {
                      const v = (r.data as unknown as Record<string, unknown>)[
                        f.key
                      ];
                      return v != null && v !== "" ? (
                        <div key={f.key}>
                          <span>{f.label}: </span>
                          {f.reference && f.reference !== "people" ? (
                            <RelatedName
                              client={client}
                              kind={f.reference}
                              id={String(v)}
                            />
                          ) : (
                            <span>
                              {typeof v === "boolean"
                                ? v
                                  ? "Yes"
                                  : "No"
                                : String(v)}
                            </span>
                          )}
                        </div>
                      ) : null;
                    })}
                  </td>
                  <td>
                    <div className="actions">
                      {(canWrite ||
                        (kind === "resources" &&
                          summary?.can_manage &&
                          resourceId === r.id)) &&
                        !immutable.includes(kind) && (
                          <Button
                            variant="secondary"
                            onClick={() => setEditor({ row: r })}
                          >
                            Edit
                          </Button>
                        )}
                      <Button
                        variant="secondary"
                        onClick={() => void showHistory(r)}
                      >
                        History
                      </Button>
                      {kind === "capacity_snapshots" && (
                        <Button
                          variant="secondary"
                          onClick={() => {
                            void client
                              .GET("/api/v1/capacity/snapshots/{id_}", {
                                params: { path: { id_: r.id } },
                              })
                              .then((x) => setSnapshot(check(x)))
                              .catch((e) => setError(e.message));
                          }}
                        >
                          View snapshot
                        </Button>
                      )}
                    </div>
                    {r.data.archived && <Badge>Archived</Badge>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="actions">
          <Button
            variant="secondary"
            disabled={offset === 0}
            onClick={() => setOffset((x) => Math.max(0, x - 20))}
          >
            Previous
          </Button>
          <Button
            variant="secondary"
            disabled={offset + 20 >= total}
            onClick={() => setOffset((x) => x + 20)}
          >
            Next
          </Button>
        </div>
      </section>
      <Modal
        open={!!editor}
        title={`${editor?.row ? "Edit" : "Create"} ${labels[kind]}`}
        onClose={() => setEditor(null)}
      >
        {editor && (
          <RecordEditor
            key={editor.row?.id || kind}
            kind={kind}
            row={editor.row}
            resourceId={resourceId || undefined}
            client={client}
            onClose={() => setEditor(null)}
            onSaved={() => {
              setNotice("Record saved. Capacity refreshed.");
              setRefresh((x) => x + 1);
            }}
          />
        )}
      </Modal>
      <Modal
        open={history !== null}
        title="Staffing change history"
        onClose={() => setHistory(null)}
      >
        {history?.length ? (
          history.map((h) => (
            <details key={h.id}>
              <summary>{new Date(h.created_at).toLocaleString()}</summary>
              <ChangeDetails before={h.before} after={h.after} />
            </details>
          ))
        ) : (
          <p>No visible history.</p>
        )}
      </Modal>
      <Modal
        open={snapshot !== null}
        title="Immutable allocation snapshot"
        onClose={() => setSnapshot(null)}
      >
        <p>
          Captured {snapshot && new Date(snapshot.created_at).toLocaleString()}.
          Later changes do not alter these planning inputs.
        </p>
        {snapshot && <SavedPlan data={snapshot.snapshot} />}
      </Modal>
    </>
  );
}
