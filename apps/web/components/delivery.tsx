"use client";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { apiError } from "./api-error";
import { createApiClient } from "@ppm/contracts";
import type { components } from "@ppm/contracts/schema";
import {
  Badge,
  Button,
  ConfirmDialog,
  DataTable,
  Field,
  MetricCard,
  Modal,
  Skeleton,
  StatePanel,
  type Confirmation,
} from "./ui";
import {
  fields,
  labels,
  immutable,
  type DeliveryInput,
  type DeliveryRecord,
  type FieldSpec,
  type Kind,
} from "./delivery-fields";

type Client = ReturnType<typeof createApiClient>;
type Account = components["schemas"]["AccountView"];
type Summary = components["schemas"]["SummaryView"];
function check<T>(r: { data?: T; error?: unknown; response: Response }): T {
  if (!r.response.ok) {
    throw new Error(apiError(r.error, r.response.status));
  }
  return r.data as T;
}
export function RelatedName({
  client,
  kind,
  id,
}: {
  client: Client;
  kind: Kind;
  id: string;
}) {
  const [name, setName] = useState("Loading reference…");
  useEffect(() => {
    let current = true;
    void client
      .GET("/api/v1/delivery/{kind}/{id_}", {
        params: { path: { kind, id_: id } },
      })
      .then((result) => {
        if (current) setName(check(result).data.name);
      })
      .catch(() => {
        if (current) setName("Unavailable reference");
      });
    return () => {
      current = false;
    };
  }, [client, kind, id]);
  return kind === "projects" ? (
    <a href={`/projects/${id}`}>{name}</a>
  ) : (
    <span>{name}</span>
  );
}
function Relationship({
  row,
  client,
}: {
  row: DeliveryRecord;
  client: Client;
}) {
  const d = row.data;
  if (d.kind === "dependencies")
    return (
      <span>
        <RelatedName client={client} kind="projects" id={d.project_id} />
        {d.source_milestone_id && (
          <>
            {" "}
            /{" "}
            <RelatedName
              client={client}
              kind="milestones"
              id={d.source_milestone_id}
            />
          </>
        )}
        {d.source_work_item_id && (
          <>
            {" "}
            /{" "}
            <RelatedName
              client={client}
              kind="work_items"
              id={d.source_work_item_id}
            />
          </>
        )}
        {" → "}
        <RelatedName client={client} kind="projects" id={d.target_project_id} />
        {d.target_milestone_id && (
          <>
            {" "}
            /{" "}
            <RelatedName
              client={client}
              kind="milestones"
              id={d.target_milestone_id}
            />
          </>
        )}
        {d.target_work_item_id && (
          <>
            {" "}
            /{" "}
            <RelatedName
              client={client}
              kind="work_items"
              id={d.target_work_item_id}
            />
          </>
        )}
        <small>Predecessor → successor</small>
      </span>
    );
  if (d.kind === "alignments")
    return (
      <span>
        <RelatedName client={client} kind="goals" id={d.goal_id} />
        <small>
          Weight {d.weight} · contribution {d.contribution}
        </small>
      </span>
    );
  return null;
}
function Reference({
  spec,
  value,
  onChange,
  client,
  projectId,
}: {
  spec: FieldSpec;
  value: string;
  onChange: (v: string) => void;
  client: Client;
  projectId?: string;
}) {
  const [query, setQuery] = useState("");
  const [choiceOffset, setChoiceOffset] = useState(0);
  const [choiceNext, setChoiceNext] = useState(false);
  const [options, setOptions] = useState<{ id: string; name: string }[]>([]);
  const [error, setError] = useState("");
  useEffect(() => {
    let valid = true;
    const timer = setTimeout(() => {
      void (async () => {
        try {
          let rows: { id: string; name: string }[] = [];
          if (spec.reference === "people")
            rows = check(
              await client.GET("/api/v1/delivery/people", {
                params: {
                  query: { q: query, offset: choiceOffset, limit: 25 },
                },
              }),
            );
          else {
            const scope = [
              "sprints",
              "work_items",
              "milestones",
              "expenditures",
            ].includes(spec.reference || "")
              ? projectId
              : undefined;
            const r = check(
              await client.GET("/api/v1/delivery/{kind}", {
                params: {
                  path: { kind: spec.reference as Kind },
                  query: {
                    q: query,
                    project_id: scope,
                    limit: 25,
                    offset: choiceOffset,
                  },
                },
              }),
            );
            setChoiceNext(choiceOffset + 25 < r.total);
            rows = r.items.map((x) => ({ id: x.id, name: x.data.name }));
            if (value && !rows.some((x) => x.id === value)) {
              const selected = await client.GET(
                "/api/v1/delivery/{kind}/{id_}",
                {
                  params: {
                    path: { kind: spec.reference as Kind, id_: value },
                  },
                },
              );
              if (selected.data)
                rows.push({ id: value, name: selected.data.data.name });
            }
          }
          if (valid) {
            if (spec.reference === "people") setChoiceNext(rows.length === 25);
            setOptions(rows);
            setError("");
          }
        } catch (e) {
          if (valid)
            setError(e instanceof Error ? e.message : "Choices unavailable");
        }
      })();
    }, 150);
    return () => {
      valid = false;
      clearTimeout(timer);
    };
  }, [spec.reference, value, query, projectId, client, choiceOffset]);
  return (
    <div className="reference-field">
      <button
        type="button"
        disabled={!choiceOffset}
        onClick={() => setChoiceOffset(choiceOffset - 25)}
      >
        Previous choices
      </button>
      <button
        type="button"
        disabled={!choiceNext}
        onClick={() => setChoiceOffset(choiceOffset + 25)}
      >
        Next choices
      </button>
      <Field label={`Find ${spec.label.toLowerCase()}`}>
        <input
          type="search"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setChoiceOffset(0);
          }}
          placeholder="Search available choices"
        />
      </Field>
      <Field label={spec.label}>
        <select
          required={spec.required}
          value={value}
          onChange={(e) => onChange(e.target.value)}
        >
          <option value="">{spec.required ? "Select…" : "None"}</option>
          {value && !options.some((o) => o.id === value) && (
            <option value={value}>
              {value.slice(0, 8)} (current reference)
            </option>
          )}
          {options.map((o) => (
            <option key={o.id} value={o.id}>
              {o.name} · {o.id.slice(0, 8)}
            </option>
          ))}
        </select>
      </Field>
      {error && <p role="alert">{error}</p>}
      <small className="muted">Up to 100 matching authorized choices.</small>
    </div>
  );
}
export function RecordEditor({
  kind,
  row,
  projectId,
  portfolioId,
  currency,
  resourceId,
  client,
  onSaved,
  onClose,
}: {
  kind: Kind;
  row: DeliveryRecord | null;
  projectId?: string;
  portfolioId?: string;
  currency?: string;
  resourceId?: string;
  client: Client;
  onSaved: () => void;
  onClose: () => void;
}) {
  const initial: Record<string, string | boolean> = {
    name: "",
    description: "",
    archived: false,
  };
  for (const f of fields[kind])
    initial[f.key] = f.default ?? (f.type === "checkbox" ? false : "");
  if (projectId && fields[kind].some((f) => f.key === "project_id"))
    initial.project_id = projectId;
  if (portfolioId && fields[kind].some((f) => f.key === "portfolio_id"))
    initial.portfolio_id = portfolioId;
  if (currency && fields[kind].some((f) => f.key === "currency"))
    initial.currency = currency;
  if (row)
    for (const [key, v] of Object.entries(row.data))
      initial[key] = v === null ? "" : typeof v === "boolean" ? v : String(v);
  if (resourceId && fields[kind].some((f) => f.key === "resource_id"))
    initial.resource_id = resourceId;
  const [values, setValues] = useState(initial);
  const [reason, setReason] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null);
  const [command] = useState(() => crypto.randomUUID());
  async function save() {
    setBusy(true);
    setError("");
    try {
      const body: Record<string, unknown> = {
        kind,
        name: values.name,
        description: values.description,
        archived: values.archived,
      };
      for (const f of fields[kind])
        body[f.key] =
          f.type === "checkbox"
            ? Boolean(values[f.key])
            : values[f.key] === "" && f.key !== "holidays" && !f.emptyString
              ? null
              : values[f.key];
      if (row)
        check(
          await client.PATCH("/api/v1/delivery/{kind}/{id_}", {
            params: {
              path: { kind, id_: row.id },
              header: { "if-match": row.revision, "x-change-reason": reason },
            },
            body: body as DeliveryInput,
          }),
        );
      else
        check(
          await client.POST("/api/v1/delivery/{kind}", {
            params: { path: { kind }, header: { "idempotency-key": command } },
            body: body as DeliveryInput,
          }),
        );
      onSaved();
      onClose();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unable to save");
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <form
        className="delivery-form"
        onSubmit={(e) => {
          e.preventDefault();
          if (
            row &&
            (values.archived !== row.data.archived ||
              kind === "grants" ||
              kind === "resource_access")
          )
            setConfirmation({
              title: "Confirm access or archive change?",
              description:
                "This change affects visibility or permissions. Existing history will be retained.",
              confirm: save,
            });
          else void save();
        }}
      >
        {error && (
          <p role="alert" className="notice error">
            {error} Your unsaved values are retained.
          </p>
        )}
        <Field label="Name">
          <input
            required
            maxLength={160}
            value={String(values.name)}
            onChange={(e) => setValues({ ...values, name: e.target.value })}
          />
        </Field>
        {kind !== "time_off" && (
          <Field
            label={kind === "baselines" ? "Baseline reason" : "Description"}
          >
            <textarea
              required={kind === "baselines"}
              maxLength={4000}
              value={String(values.description)}
              onChange={(e) =>
                setValues({ ...values, description: e.target.value })
              }
            />
          </Field>
        )}
        <div className="delivery-fields">
          {fields[kind]
            .filter(
              (f) =>
                !(projectId && f.key === "project_id") &&
                !(portfolioId && f.key === "portfolio_id"),
            )
            .map((f) => (
              <div key={f.key}>
                {f.reference ? (
                  <Reference
                    spec={f}
                    value={String(values[f.key] || "")}
                    client={client}
                    projectId={
                      f.key.startsWith("target_")
                        ? String(values.target_project_id || "")
                        : String(values.project_id || projectId || "")
                    }
                    onChange={(v) => setValues({ ...values, [f.key]: v })}
                  />
                ) : (
                  <Field label={f.label}>
                    {f.options ? (
                      <select
                        value={String(values[f.key] ?? "")}
                        onChange={(e) =>
                          setValues({ ...values, [f.key]: e.target.value })
                        }
                      >
                        {f.label.includes("(optional)") && (
                          <option value="">Unknown</option>
                        )}
                        {f.options.map((v) => (
                          <option key={v}>{v}</option>
                        ))}
                      </select>
                    ) : f.type === "checkbox" ? (
                      <input
                        type="checkbox"
                        checked={Boolean(values[f.key])}
                        onChange={(e) =>
                          setValues({ ...values, [f.key]: e.target.checked })
                        }
                      />
                    ) : (
                      <input
                        type={f.type || "text"}
                        required={f.required}
                        step={f.step}
                        value={String(values[f.key] ?? "")}
                        onChange={(e) =>
                          setValues({ ...values, [f.key]: e.target.value })
                        }
                      />
                    )}
                  </Field>
                )}
              </div>
            ))}
        </div>
        {row && (
          <>
            <Field label="Change reason (required when reopening)">
              <input
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                maxLength={1000}
              />
            </Field>
            {!immutable.includes(kind) && (
              <label className="checkbox">
                <input
                  type="checkbox"
                  checked={Boolean(values.archived)}
                  onChange={(e) =>
                    setValues({ ...values, archived: e.target.checked })
                  }
                />
                Archived
              </label>
            )}
            <p className="muted">
              Revision {row.revision}. A stale edit is rejected; close and
              reload to use the current revision.
            </p>
          </>
        )}
        <div className="actions">
          <Button disabled={busy}>{busy ? "Saving…" : "Save record"}</Button>
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancel
          </Button>
        </div>
      </form>
      <ConfirmDialog
        value={confirmation}
        onClose={() => setConfirmation(null)}
      />
    </>
  );
}
function Timeline({
  rows,
  baseline,
}: {
  rows: DeliveryRecord[];
  baseline?: components["schemas"]["BaselineView"];
}) {
  const dated = rows.flatMap((r) => {
    const d = r.data as unknown as Record<string, string>;
    const end = d.due_date || d.end_date || d.target_end_date;
    const start = d.start_date || end;
    return start && end ? [{ id: r.id, name: d.name, start, end }] : [];
  });
  const times = dated.flatMap((r) => [Date.parse(r.start), Date.parse(r.end)]);
  const first = Math.min(...times);
  const span = Math.max(86400000, Math.max(...times) - first);
  return (
    <section className="panel">
      <h2>Delivery timeline</h2>
      <p className="muted">
        Current milestones page and up to 100 work items, in calendar days.
        Forecast changes do not rewrite saved baselines.{" "}
        {baseline
          ? `Latest baseline: version ${baseline.version}.`
          : "No baseline captured yet."}
      </p>
      {dated.length ? (
        <>
          <div className="gantt" aria-hidden="true">
            {dated.map((r) => (
              <div className="gantt-row" key={r.id}>
                <span>{r.name}</span>
                <div className="gantt-track">
                  <b
                    style={{
                      marginLeft: `${((Date.parse(r.start) - first) / span) * 90}%`,
                      width: `${Math.max(1, ((Date.parse(r.end) - Date.parse(r.start)) / span) * 90)}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
          <div
            className="table-scroll"
            tabIndex={0}
            role="region"
            aria-label="Timeline dates"
          >
            <table>
              <caption>Timeline date alternative</caption>
              <thead>
                <tr>
                  <th scope="col">Item</th>
                  <th scope="col">Start</th>
                  <th scope="col">Finish</th>
                </tr>
              </thead>
              <tbody>
                {dated.map((r) => (
                  <tr key={r.id}>
                    <td>{r.name}</td>
                    <td>{r.start}</td>
                    <td>{r.end}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <StatePanel title="No dates to display">
          Add dated work or milestones to build the timeline.
        </StatePanel>
      )}
    </section>
  );
}
function PlanSnapshot({ data }: { data: Record<string, unknown> }) {
  const project = (data.project || {}) as Record<string, unknown>;
  const groups = (data.items || {}) as Record<
    string,
    Record<string, unknown>[]
  >;
  return (
    <div
      className="table-scroll"
      tabIndex={0}
      role="region"
      aria-label="Saved plan details"
    >
      <table>
        <caption>Saved plan — never overwritten by current edits</caption>
        <thead>
          <tr>
            <th scope="col">Item</th>
            <th scope="col">Planned start</th>
            <th scope="col">Planned finish / amount</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{String(project.name || "Project")}</td>
            <td>{String(project.start_date || "Not set")}</td>
            <td>
              {String(project.target_end_date || "Not set")} · Forecast{" "}
              {String(project.forecast_end_date || "Not set")}
            </td>
          </tr>
          {Object.entries(groups).flatMap(([kind, rows]) =>
            rows.map((r) => (
              <tr key={String(r.id)}>
                <td>
                  {String(r.name)} <small>({kind.replaceAll("_", " ")})</small>
                </td>
                <td>{String(r.start_date || "—")}</td>
                <td>
                  {String(r.due_date || r.end_date || r.amount || "—")}{" "}
                  {String(r.currency || "")}
                </td>
              </tr>
            )),
          )}
        </tbody>
      </table>
    </div>
  );
}
export function ChangeDetails({
  before,
  after,
}: {
  before: Record<string, unknown> | null;
  after: Record<string, unknown>;
}) {
  const keys = Object.keys(after).filter(
    (k) =>
      ![
        "id",
        "organization_id",
        "snapshot",
        "created_at",
        "updated_at",
      ].includes(k) && JSON.stringify(before?.[k]) !== JSON.stringify(after[k]),
  );
  return (
    <dl className="change-details">
      {keys.map((k) => (
        <div key={k}>
          <dt>{k.replaceAll("_", " ")}</dt>
          <dd>
            {before ? String(before[k] ?? "Not set") + " → " : ""}
            {String(after[k] ?? "Not set")}
          </dd>
        </div>
      ))}
    </dl>
  );
}

export function Delivery({
  account,
  client,
}: {
  account: Account;
  client: Client;
}) {
  const path = usePathname();
  const projectId = path.startsWith("/projects/")
    ? path.split("/")[2]
    : undefined;
  const top: Kind = path.startsWith("/portfolios")
    ? "portfolios"
    : path.startsWith("/organization")
      ? "settings"
      : "projects";
  const [kind, setKind] = useState<Kind>(projectId ? "work_items" : top);
  useEffect(() => {
    const target = new URLSearchParams(window.location.search).get("kind");
    if (projectId && ["work_items", "risks"].includes(target || ""))
      setKind(target as Kind);
  }, [projectId]);
  const [rows, setRows] = useState<DeliveryRecord[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [portfolio, setPortfolio] = useState<
    components["schemas"]["PortfolioSummary"] | null
  >(null);
  const [settings, setSettings] = useState<DeliveryRecord | null>(null);
  const [q, setQ] = useState("");
  useEffect(() => {
    const target = new URLSearchParams(window.location.search).get("record");
    if (!projectId || !target) return;
    let live = true;
    void client
      .GET("/api/v1/delivery/{kind}/{id_}", {
        params: { path: { kind, id_: target } },
      })
      .then((response) => {
        const record = check(response);
        if (
          live &&
          "project_id" in record.data &&
          record.data.project_id === projectId
        )
          setQ(record.data.name);
      })
      .catch(() => {
        if (live) setError("This record is unavailable in your current scope.");
      });
    return () => {
      live = false;
    };
  }, [client, kind, projectId]);
  const [status, setStatus] = useState("");
  const [industry, setIndustry] = useState("");
  const [sort, setSort] = useState<"name" | "updated">("name");
  const [archived, setArchived] = useState(false);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(true);
  const [editor, setEditor] = useState<{
    kind: Kind;
    row: DeliveryRecord | null;
  } | null>(null);
  const [history, setHistory] = useState<
    components["schemas"]["HistoryView"][] | null
  >(null);
  const [timeline, setTimeline] = useState<DeliveryRecord[]>([]);
  const [refresh, setRefresh] = useState(0);
  const [portfolioFilter, setPortfolioFilter] = useState("");
  useEffect(() => {
    setPortfolioFilter(
      new URLSearchParams(window.location.search).get("portfolio") || "",
    );
  }, []);
  useEffect(() => {
    let valid = true;
    setLoading(true);
    setError("");
    const timer = setTimeout(() => {
      void (async () => {
        try {
          const config = check(
            await client.GET("/api/v1/delivery/{kind}", {
              params: { path: { kind: "settings" } },
            }),
          );
          const list = check(
            await client.GET("/api/v1/delivery/{kind}", {
              params: {
                path: { kind },
                query: {
                  q,
                  sort,
                  ...(kind === "projects" && industry ? { industry } : {}),
                  status: status || undefined,
                  archived,
                  offset,
                  limit: 20,
                  project_id: projectId,
                  portfolio_id:
                    kind === "projects" && portfolioFilter
                      ? portfolioFilter
                      : undefined,
                },
              },
            }),
          );
          const details = projectId
            ? check(
                await client.GET("/api/v1/delivery/project-summary/{id_}", {
                  params: { path: { id_: projectId } },
                }),
              )
            : null;
          if (valid) {
            setRows(list.items);
            setTotal(list.total);
            setSettings(config.items[0] || null);
            setSummary(details);
            setTimeline([]);
          }
          if (projectId && kind === "milestones") {
            const work = check(
              await client.GET("/api/v1/delivery/{kind}", {
                params: {
                  path: { kind: "work_items" },
                  query: { project_id: projectId, limit: 100 },
                },
              }),
            );
            if (valid) setTimeline([...list.items, ...work.items]);
          }
        } catch (e) {
          if (valid) {
            setError(e instanceof Error ? e.message : "Could not load");
            setRows([]);
            setSummary(null);
          }
        } finally {
          if (valid) setLoading(false);
        }
      })();
    }, 150);
    return () => {
      valid = false;
      clearTimeout(timer);
    };
  }, [
    account.organization_id,
    projectId,
    kind,
    q,
    sort,
    status,
    archived,
    offset,
    refresh,
    portfolioFilter,
    client,
  ]);
  const canWrite =
    account.role === "Admin" ||
    (projectId
      ? Boolean(summary?.can_edit)
      : kind === "projects" && account.role === "Project Manager");
  const tabs: Kind[] = projectId
    ? [
        "work_items",
        "milestones",
        "sprints",
        "blockers",
        "risks",
        "benefits",
        "metric_plans",
        "dependencies",
        "budget_lines",
        "expenditures",
        "status_updates",
        "baselines",
        "alignments",
        ...(account.role === "Admin" ? ["grants" as Kind] : []),
      ]
    : top === "settings"
      ? [
          "settings",
          "metric_policies",
          "departments",
          "teams",
          "team_members",
          "goals",
          "programs",
          "grants",
        ]
      : top === "portfolios"
        ? ["portfolios", "programs", "alignments"]
        : ["projects"];
  function tab(k: Kind) {
    setKind(k);
    setOffset(0);
    setQ("");
    setStatus("");
    setArchived(false);
    setPortfolio(null);
  }
  async function audit(row: DeliveryRecord) {
    try {
      setHistory(
        check(
          await client.GET("/api/v1/delivery/history/{kind}/{id_}", {
            params: { path: { kind: row.data.kind, id_: row.id } },
          }),
        ),
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : "History unavailable");
    }
  }
  return (
    <>
      {kind === "grants" && (
        <section className="panel">
          <h2>Project access</h2>
          <p>
            Admin can grant read, edit or manage access here. Owners need an
            explicit grant. Portfolio read includes projects but does not allow
            project edits. To revoke, edit the grant and archive it; open tabs
            and searches recheck access.
          </p>
        </section>
      )}
      <section className="page-heading">
        <div>
          <p className="eyebrow">PORTFOLIO & DELIVERY</p>
          <h1>
            {projectId
              ? summary?.project.data.name || "Project workspace"
              : top === "settings"
                ? "Organization setup"
                : labels[top]}
          </h1>
          <p className="lead">
            {projectId
              ? "Manage delivery, preserve plans and trace every change."
              : "A shared system of record for goals, portfolios and project delivery."}
          </p>
        </div>
        <div className="actions">
          <a className="button secondary" href="/projects">
            Projects
          </a>
          <a className="button secondary" href="/portfolios">
            Portfolios
          </a>
          {account.role === "Admin" && (
            <a className="button secondary" href="/organization">
              Organization setup
            </a>
          )}
        </div>
      </section>
      {error && (
        <p role="alert" className="notice error">
          {error}{" "}
          <button onClick={() => setRefresh((v) => v + 1)}>Reload</button>
        </p>
      )}
      {notice && (
        <p role="status" className="notice">
          {notice}
        </p>
      )}
      {!loading && !settings && (
        <StatePanel
          title="Configure your organization first"
          action={
            account.role === "Admin" ? (
              <Button
                onClick={() => setEditor({ kind: "settings", row: null })}
              >
                Configure organization
              </Button>
            ) : undefined
          }
        >
          An Admin must set timezone and default currency before creating
          delivery records.
        </StatePanel>
      )}
      {summary && (
        <>
          <div className="metrics-grid">
            <MetricCard
              label="Reported health"
              value={
                summary.project.data.kind === "projects"
                  ? summary.project.data.reported_health
                  : "Unknown"
              }
              detail="Human-reported; computed health not available"
            />
            <MetricCard
              label="Approved budget"
              value={`${summary.money[0]?.currency} ${summary.money[0]?.approved_budget}`}
              detail="Approved, active budget lines"
            />
            <MetricCard
              label="Recorded expenditure"
              value={`${summary.money[0]?.currency} ${summary.money[0]?.recorded_spend}`}
              detail={
                summary.money[0]?.ledger_complete
                  ? "Ledger marked complete"
                  : "Partial ledger · recorded entries only"
              }
            />
          </div>
          <section className="panel project-overview">
            <div>
              <h2>Project overview</h2>
              <p>{summary.project.data.description || "No description yet."}</p>
              <p className="muted">
                Goal alignment:{" "}
                {summary.alignment_complete
                  ? `${summary.alignment_percent}%`
                  : "Incomplete — link goals with weights totaling 1"}
                .{" "}
                {summary.project.data.archived
                  ? "Archived · restore to edit."
                  : ""}
              </p>
            </div>
            <div className="actions">
              {summary.can_edit && (
                <Button
                  variant="secondary"
                  onClick={() =>
                    setEditor({ kind: "projects", row: summary.project })
                  }
                >
                  Edit project
                </Button>
              )}
              <Button
                variant="secondary"
                onClick={() => void audit(summary.project)}
              >
                Project history
              </Button>
            </div>
          </section>
        </>
      )}
      <nav className="delivery-tabs" aria-label="Delivery sections">
        {tabs.map((k) => (
          <Button
            key={k}
            variant={k === kind ? "primary" : "secondary"}
            onClick={() => tab(k)}
            aria-pressed={k === kind}
          >
            {labels[k]}
          </Button>
        ))}
      </nav>
      <section className="panel">
        <div className="section-heading">
          <h2>{labels[kind]}</h2>
          {canWrite && !(kind === "settings" && settings) && (
            <Button
              disabled={Boolean(summary?.project.data.archived)}
              onClick={() => setEditor({ kind, row: null })}
            >
              Create {labels[kind].toLowerCase()}
            </Button>
          )}
        </div>
        <div className="server-filters">
          <Field label="Search records">
            <input
              type="search"
              value={q}
              onChange={(e) => {
                setQ(e.target.value);
                setOffset(0);
              }}
            />
          </Field>
          {kind === "projects" && (
            <Field label="Industry filter">
              <select
                value={industry}
                onChange={(e) => {
                  setIndustry(e.target.value);
                  setOffset(0);
                }}
              >
                <option value="">All industries</option>
                {[
                  "unknown",
                  "fintech",
                  "technology",
                  "healthcare",
                  "public_sector",
                  "other",
                ].map((i) => (
                  <option key={i} value={i}>
                    {i === "unknown" ? "Unknown" : i.replaceAll("_", " ")}
                  </option>
                ))}
              </select>
            </Field>
          )}
          <Field label="Sort records">
            <select
              value={sort}
              onChange={(e) => {
                setSort(e.target.value as "name" | "updated");
                setOffset(0);
              }}
            >
              <option value="name">Name</option>
              <option value="updated">Recently updated</option>
            </select>
          </Field>
          {fields[kind].some((f) => f.key === "status") && (
            <Field label="Filter status">
              <select
                value={status}
                onChange={(e) => {
                  setStatus(e.target.value);
                  setOffset(0);
                }}
              >
                <option value="">All statuses</option>
                {fields[kind]
                  .find((f) => f.key === "status")
                  ?.options?.map((s) => (
                    <option key={s}>{s}</option>
                  ))}
              </select>
            </Field>
          )}
          <label className="checkbox">
            <input
              type="checkbox"
              checked={archived}
              onChange={(e) => {
                setArchived(e.target.checked);
                setOffset(0);
              }}
            />
            Show archived
          </label>
        </div>
        {loading ? (
          <Skeleton label="Loading delivery records" />
        ) : rows.length ? (
          <DataTable
            key={`${kind}-${account.organization_id}-${offset}`}
            caption={labels[kind]}
            rows={rows}
            rowKey={(r) => r.id}
            searchText={(r) => r.data.name}
            pageSize={20}
            external
            columns={[
              {
                key: "name",
                label: "Name",
                render: (r) => (
                  <div>
                    {r.data.kind === "projects" ? (
                      <a href={`/projects/${r.id}`}>{r.data.name}</a>
                    ) : (
                      <strong>{r.data.name}</strong>
                    )}
                    <small className="record-description">
                      {r.data.description}
                    </small>
                  </div>
                ),
              },
              {
                key: "state",
                label: "Details",
                render: (r) => (
                  <span>
                    <Relationship row={r} client={client} />
                    {[
                      "status",
                      "reported_health",
                      "amount",
                      "currency",
                      "due_date",
                      "weight",
                      "access",
                    ]
                      .filter((k) => k in r.data)
                      .map(
                        (k) =>
                          `${k.replaceAll("_", " ")}: ${String((r.data as unknown as Record<string, unknown>)[k])}`,
                      )
                      .join(" · ") || `Revision ${r.revision}`}
                  </span>
                ),
              },
              {
                key: "actions",
                label: "Actions",
                render: (r) => (
                  <div className="actions">
                    {canWrite && !immutable.includes(kind) && (
                      <Button
                        variant="secondary"
                        onClick={() => setEditor({ kind, row: r })}
                      >
                        Edit {r.data.name}
                      </Button>
                    )}
                    {kind === "portfolios" && (
                      <>
                        <a href={`/projects?portfolio=${r.id}`}>
                          View projects
                        </a>
                        <Button
                          variant="secondary"
                          onClick={() => {
                            void client
                              .GET("/api/v1/delivery/portfolio-summary/{id_}", {
                                params: { path: { id_: r.id } },
                              })
                              .then((result) => setPortfolio(check(result)))
                              .catch((e) => setError(e.message));
                          }}
                        >
                          Budget totals
                        </Button>
                      </>
                    )}
                    <Button variant="secondary" onClick={() => void audit(r)}>
                      History
                    </Button>
                  </div>
                ),
              },
            ]}
          />
        ) : (
          <StatePanel title="No matching records">
            {canWrite
              ? "Create the first record or change the filters."
              : "No records are available within your current scope."}
          </StatePanel>
        )}
        <div className="pagination">
          <span>
            {total} matching records · page {Math.floor(offset / 20) + 1}
          </span>
          <div className="actions">
            <Button
              variant="secondary"
              disabled={offset === 0 || loading}
              onClick={() => setOffset(Math.max(0, offset - 20))}
            >
              Previous records
            </Button>
            <Button
              variant="secondary"
              disabled={offset + 20 >= total || loading}
              onClick={() => setOffset(offset + 20)}
            >
              Next records
            </Button>
          </div>
        </div>
      </section>
      {projectId && kind === "work_items" && (
        <section className="panel">
          <h2>Work board</h2>
          <p className="muted">
            Current server page only. Open a card to update its status; invalid
            transitions and stale revisions are rejected.
          </p>
          <div className="work-board">
            {["backlog", "ready", "in_progress", "done"].map((s) => (
              <section key={s}>
                <h3>{s.replaceAll("_", " ")}</h3>
                {rows
                  .filter(
                    (r) => r.data.kind === "work_items" && r.data.status === s,
                  )
                  .map((r) => (
                    <button
                      disabled={!canWrite}
                      key={r.id}
                      className="work-card"
                      onClick={() => setEditor({ kind: "work_items", row: r })}
                    >
                      {r.data.name}
                      {r.data.kind === "work_items" && r.data.blocked && (
                        <Badge tone="warning">Blocked</Badge>
                      )}
                    </button>
                  ))}
              </section>
            ))}
          </div>
        </section>
      )}
      {projectId && kind === "milestones" && (
        <Timeline rows={timeline} baseline={summary?.baselines[0]} />
      )}{" "}
      {summary && kind === "baselines" && (
        <section className="panel">
          <h2>Immutable plan history</h2>
          {summary.baselines.length === 0 ? (
            <p>No baseline captured.</p>
          ) : (
            summary.baselines.map((b) => (
              <details key={b.id}>
                <summary>
                  Version {b.version} · {b.reason}
                </summary>
                <p>{new Date(b.created_at).toLocaleString()}</p>
                <PlanSnapshot data={b.snapshot} />
              </details>
            ))
          )}
        </section>
      )}
      {portfolio && (
        <section className="panel">
          <h2>{portfolio.portfolio.data.name}: authorized budget totals</h2>
          <p>
            {portfolio.visible_projects} visible projects. Currencies are never
            combined.
          </p>
          {portfolio.money.map((m) => (
            <p key={m.currency}>
              {m.currency} · Approved {m.approved_budget} · Recorded{" "}
              {m.recorded_spend} ·{" "}
              {m.ledger_complete ? "Complete ledger" : "Partial ledger"}
            </p>
          ))}
        </section>
      )}
      <Modal
        open={!!editor}
        onClose={() => setEditor(null)}
        title={
          editor
            ? `${editor.row ? "Edit" : "Create"} ${labels[editor.kind]}`
            : "Record"
        }
      >
        {editor && (
          <RecordEditor
            key={`${editor.kind}-${editor.row?.id || "new"}`}
            kind={editor.kind}
            row={editor.row}
            projectId={editor.kind === "projects" ? undefined : projectId}
            currency={
              summary?.money[0]?.currency ||
              (settings?.data.kind === "settings"
                ? settings.data.currency
                : undefined)
            }
            portfolioId={
              editor.kind === "projects" && portfolioFilter
                ? portfolioFilter
                : undefined
            }
            client={client}
            onClose={() => setEditor(null)}
            onSaved={() => {
              setNotice("Record saved.");
              setRefresh((v) => v + 1);
            }}
          />
        )}
      </Modal>
      <Modal
        open={history !== null}
        onClose={() => setHistory(null)}
        title="Change history"
        drawer
      >
        {history?.length ? (
          history.map((h) => (
            <details key={h.id}>
              <summary>{new Date(h.created_at).toLocaleString()}</summary>
              <ChangeDetails before={h.before} after={h.after} />
            </details>
          ))
        ) : (
          <p>No history visible in your scope.</p>
        )}
      </Modal>
    </>
  );
}
