"use client";
import { useCallback, useEffect, useState } from "react";
import { apiError } from "./api-error";
import type { components } from "@ppm/contracts/schema";

import { RecordSelect } from "./record-select";
type S = components["schemas"];
type Integration = S["IntegrationView"];
type Job = S["JobView"];
const terminal = ["succeeded", "partially_succeeded", "failed", "cancelled"];

export function Integrations({
  account,
  transport,
}: {
  account: S["AccountView"];
  transport: typeof fetch;
}) {
  const [items, setItems] = useState<Integration[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selected, setSelected] = useState("");
  const [active, setActive] = useState<Job | null>(null);
  const [stages, setStages] = useState<string[]>([]);
  const [connection, setConnection] = useState("");
  const [provider, setProvider] = useState<"csv" | "github" | "jira">("csv");
  const [statusMapping, setStatusMapping] = useState("{}");
  const [mapping, setMapping] = useState(
    '{"external_id":"id","name":"name","source_updated_at":"updated_at","status":"status"}',
  );
  const [source, setSource] = useState(
    "id,name,updated_at,status\nexample-1,Example work,2026-10-09T00:00:00Z,backlog",
  );
  const [evidence, setEvidence] = useState<S["SourceView"][]>([]);
  const [preview, setPreview] = useState<S["Preview"] | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState("");
  const admin = account.role === "Admin";
  const api = useCallback(
    async <T,>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const response = await transport(
        new Request(window.location.origin + "/api/v1/integrations" + path, {
          method,
          headers: {
            "content-type": "application/json",
            "idempotency-key": crypto.randomUUID(),
            ...(revision == null ? {} : { "if-match": String(revision) }),
          },
          body: body === undefined ? undefined : JSON.stringify(body),
        }),
      );
      if (!response.ok) {
        const result = await response.json().catch(() => null);
        throw new Error(apiError(result, response.status));
      }
      return response.json();
    },
    [transport],
  );
  const refresh = useCallback(async () => {
    const [integrations, activity] = await Promise.all([
      api<Integration[]>(""),
      api<Job[]>("/activity/jobs"),
    ]);
    setItems(integrations);
    setJobs(activity);
  }, [api]);
  useEffect(() => {
    let live = true;
    void (async () => {
      try {
        await refresh();
      } catch (e) {
        if (live) setError((e as Error).message);
      } finally {
        if (live) setLoading(false);
      }
    })();
    return () => {
      live = false;
    };
  }, [refresh, transport]);
  const activeId = active?.id;
  useEffect(() => {
    if (!activeId) return;
    const controller = new AbortController();
    let after = 0;
    setStages([]);
    void (async () => {
      while (!controller.signal.aborted) {
        try {
          setConnection(
            after ? "Reconnecting to retained progress…" : "Connecting…",
          );
          const response = await transport(
            new Request(
              window.location.origin +
                `/api/v1/integrations/activity/jobs/${activeId}/events`,
              {
                headers: { "last-event-id": String(after) },
                signal: controller.signal,
              },
            ),
          );
          if (!response.ok || !response.body)
            throw new Error("Progress access unavailable");
          setConnection("Live progress connected");
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let buffer = "";
          let resynced = false;
          let refreshedAt = 0;
          while (true) {
            const result = await reader.read();
            if (result.done) break;
            buffer += decoder.decode(result.value, { stream: true });
            let boundary;
            while ((boundary = buffer.indexOf("\n\n")) >= 0) {
              const block = buffer.slice(0, boundary);
              buffer = buffer.slice(boundary + 2);
              if (block.includes("event: access_revoked"))
                throw new Error(
                  "Progress access revoked; sign in or refresh scope.",
                );
              if (block.includes("event: resync_required")) {
                after = 0;
                resynced = true;
                setStages([]);
                setConnection("Progress expired; snapshot refreshed");
              }
              const data = block
                .split("\n")
                .find((line) => line.startsWith("data: "));
              if (block.includes("event: stage") && data) {
                const event: S["StageView"] = JSON.parse(data.slice(6));
                if (event.sequence > after) {
                  after = event.sequence;
                  if (Date.now() - refreshedAt > 1000) {
                    refreshedAt = Date.now();
                    setActive(await api<Job>(`/activity/jobs/${activeId}`));
                  }
                  setStages((previous) => [
                    ...previous.slice(-49),
                    `${event.sequence}. ${event.stage.replaceAll("_", " ")} · ${new Date(event.occurred_at).toLocaleTimeString()}`,
                  ]);
                }
              }
            }
          }
          const snapshot = await api<Job>(`/activity/jobs/${activeId}`);
          if (resynced) after = snapshot.sequence;
          setActive(snapshot);
          await refresh();
          if (terminal.includes(snapshot.status)) {
            setConnection("Processing finished");
            break;
          }
        } catch (e) {
          if (controller.signal.aborted) break;
          setConnection((e as Error).message);
          if ((e as Error).message.includes("access")) break;
        }
        await new Promise((resolve) => setTimeout(resolve, 1500));
      }
    })();
    return () => controller.abort();
  }, [activeId, api, refresh, transport]);
  async function action(fn: () => Promise<void>) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await fn();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  const integration = items.find((item) => item.id === selected);
  function input() {
    if (integration?.config.mode === "live") return {};
    return integration?.config.provider === "csv"
      ? { csv_text: source }
      : { records: JSON.parse(source) };
  }
  return (
    <div className="delivery-workspace">
      <section className="panel">
        <h1>Integrations & job activity</h1>
        <p className="muted">
          Import project work with source timestamps and provenance. Fixture
          connections are labelled; live credentials stay on the server.
        </p>
        {error && <p role="alert">{error}</p>}
        {notice && <p role="status">{notice}</p>}
        {loading && <p role="status">Loading integrations…</p>}
        <button disabled={busy} onClick={() => void action(refresh)}>
          Refresh activity
        </button>
        {!admin && (
          <p>
            Integration settings and sync actions require Admin. Job reads also
            require current project access.
          </p>
        )}
      </section>
      {admin && (
        <section className="panel">
          <h2>Create connection</h2>
          <form
            className="identity-form"
            onSubmit={(e) => {
              e.preventDefault();
              const f = new FormData(e.currentTarget);
              void action(async () => {
                const created = await api<Integration>("", "POST", {
                  name: f.get("name"),
                  provider,
                  mode: f.get("mode"),
                  project_id: f.get("project"),
                  resource: f.get("resource") || "",
                  jira_project: f.get("jira_project") || "",
                  entity: f.get("entity"),
                  board_id: f.get("board_id")
                    ? Number(f.get("board_id"))
                    : null,
                  team_id: f.get("team_id") || null,
                  secret_ref: f.get("secret_ref") || "",
                  webhook_secret_ref: f.get("webhook_secret_ref") || "",
                  mapping: JSON.parse(mapping),
                  status_map: JSON.parse(String(f.get("status_map") || "{}")),
                });
                await refresh();
                setSelected(created.id);
                setPreview(null);
                setNotice(
                  "Connection created. Preview fixture data before syncing.",
                );
              });
            }}
          >
            <label>
              Connection name
              <input name="name" required maxLength={160} />
            </label>
            <RecordSelect
              transport={transport}
              kind="projects"
              label="Project"
              name="project"
              required
            />
            <label>
              Provider
              <select
                value={provider}
                onChange={(e) => {
                  const next = e.target.value as typeof provider;
                  setProvider(next);
                  setStatusMapping(
                    next === "github"
                      ? '{"open":"backlog","closed":"done"}'
                      : next === "jira"
                        ? '{"To Do":"backlog","In Progress":"in_progress","Done":"done"}'
                        : "{}",
                  );
                  setMapping(
                    next === "jira"
                      ? '{"external_id":"id","name":"fields.summary","source_updated_at":"fields.updated","status":"fields.status.name"}'
                      : next === "github"
                        ? '{"external_id":"number","name":"title","source_updated_at":"updated_at","status":"state"}'
                        : '{"external_id":"id","name":"name","source_updated_at":"updated_at","status":"status"}',
                  );
                }}
              >
                <option>csv</option>
                <option>github</option>
                <option>jira</option>
              </select>
            </label>
            <label>
              Mode
              <select name="mode">
                <option value="fixture">
                  Contract fixture (no provider calls)
                </option>
                {provider !== "csv" && (
                  <option value="live">
                    Live (server credentials required)
                  </option>
                )}
              </select>
            </label>
            <label>
              Repository or Jira Cloud host
              <input
                name="resource"
                placeholder="owner/repository or tenant.atlassian.net"
              />
            </label>
            <label>
              Jira project key
              <input name="jira_project" />
            </label>
            <label>
              Entity
              <select
                name="entity"
                onChange={(e) => {
                  if (e.target.value === "sprints") {
                    setMapping(
                      '{"external_id":"id","name":"name","source_updated_at":"updated_at","status":"state","start_date":"startDate","end_date":"endDate"}',
                    );
                    setStatusMapping(
                      '{"future":"planned","active":"active","closed":"closed"}',
                    );
                  }
                }}
              >
                <option value="issues">Issues / work items</option>
                {provider === "github" && (
                  <option value="pulls">Pull requests</option>
                )}
                {provider === "jira" && (
                  <option value="sprints">Sprints</option>
                )}
              </select>
            </label>
            {provider === "jira" && (
              <>
                <label>
                  Board ID (sprints)
                  <input name="board_id" type="number" min="1" />
                </label>
                <label>
                  Local team UUID (sprints)
                  <input name="team_id" />
                </label>
              </>
            )}
            <label>
              Server secret reference
              <input
                name="secret_ref"
                placeholder={`PPM_CONNECTOR_${(account.organization_id || "").replaceAll("-", "").toUpperCase()}_${provider.toUpperCase()}_TOKEN`}
              />
            </label>
            <label>
              Webhook secret reference
              <input
                name="webhook_secret_ref"
                placeholder={`PPM_CONNECTOR_${(account.organization_id || "").replaceAll("-", "").toUpperCase()}_${provider.toUpperCase()}_WEBHOOK`}
              />
            </label>
            <label>
              Field mapping (target to source path)
              <textarea
                required
                value={mapping}
                onChange={(e) => setMapping(e.target.value)}
                rows={4}
              />
            </label>
            <label>
              Status mapping (JSON)
              <textarea
                name="status_map"
                value={statusMapping}
                onChange={(e) => setStatusMapping(e.target.value)}
                rows={2}
              />
            </label>
            <button disabled={busy}>Create connection</button>
          </form>
        </section>
      )}
      <section className="panel">
        <h2>Connections & sync history</h2>
        {!loading && !items.length && (
          <p>No connections in your current scope.</p>
        )}
        <label>
          Connection
          <select
            value={selected}
            onChange={(e) => {
              setSelected(e.target.value);
              setPreview(null);
            }}
          >
            <option value="">Select connection</option>
            {items.map((item) => (
              <option key={item.id} value={item.id}>
                {item.config.name} · {item.config.provider} · {item.config.mode}{" "}
                · {item.enabled ? "enabled" : "disabled"}
              </option>
            ))}
          </select>
        </label>
        {integration && (
          <>
            <p>Source cursor: {integration.cursor || "No completed sync"}</p>
            <button
              disabled={busy}
              onClick={() =>
                void action(async () =>
                  setEvidence(
                    await api<S["SourceView"][]>(`/${selected}/sources`),
                  ),
                )
              }
            >
              Inspect imported source evidence
            </button>
            {evidence.map((source) => (
              <p key={source.external_id}>
                Source {source.external_id} · {source.target_kind} revision{" "}
                {source.target_revision} · source timestamp{" "}
                {source.source_updated_at
                  ? new Date(source.source_updated_at).toLocaleString()
                  : "Unknown"}{" "}
                · observed{" "}
                {new Date(source.source_observed_at).toLocaleString()} ·{" "}
                <a href="/projects">Open project records</a>
              </p>
            ))}
            <p>
              Settings revision {integration.revision}. Source timestamps remain
              distinct from job processing time.
            </p>
            {admin && (
              <>
                {!!integration.config.webhook_secret_ref && (
                  <button
                    disabled={busy}
                    onClick={() =>
                      void action(async () => {
                        await api(
                          `/${selected}`,
                          "PATCH",
                          { enabled: integration.enabled },
                          integration.revision,
                        );
                        await refresh();
                        setNotice(
                          "Webhook authority renewed for your current session.",
                        );
                      })
                    }
                  >
                    Renew webhook authorization
                  </button>
                )}
                <button
                  disabled={busy}
                  onClick={() =>
                    void action(async () => {
                      await api(
                        `/${selected}`,
                        "PATCH",
                        { enabled: !integration.enabled },
                        integration.revision,
                      );
                      await refresh();
                    })
                  }
                >
                  {integration.enabled
                    ? "Disable connection"
                    : "Enable connection"}
                </button>
                {integration.config.mode === "fixture" && (
                  <label>
                    {integration.config.provider === "csv"
                      ? "CSV source"
                      : "Provider contract records (JSON array)"}
                    <textarea
                      value={source}
                      onChange={(e) => {
                        setSource(e.target.value);
                        setPreview(null);
                      }}
                      rows={6}
                    />
                  </label>
                )}
                <div className="actions">
                  {integration.config.mode === "fixture" && (
                    <button
                      disabled={busy}
                      onClick={() =>
                        void action(async () =>
                          setPreview(
                            await api<S["Preview"]>(
                              `/${selected}/preview`,
                              "POST",
                              input(),
                            ),
                          ),
                        )
                      }
                    >
                      Preview import
                    </button>
                  )}
                  <button
                    disabled={
                      busy ||
                      !integration.enabled ||
                      (integration.config.mode === "fixture" && !preview)
                    }
                    onClick={() =>
                      void action(async () => {
                        const job = await api<Job>(
                          `/${selected}/sync`,
                          "POST",
                          input(),
                        );
                        setActive(job);
                        await refresh();
                      })
                    }
                  >
                    Start sync
                  </button>
                </div>
                {preview && (
                  <div role="status">
                    <p>
                      {preview.valid} valid rows · {preview.errors.length}{" "}
                      validation errors
                    </p>
                    {preview.errors.map((err, i) => (
                      <p key={i}>
                        Row {String(err.row)}: {String(err.code)}
                      </p>
                    ))}
                    <details>
                      <summary>Mapped preview</summary>
                      <pre
                        style={{
                          whiteSpace: "pre-wrap",
                          overflowWrap: "anywhere",
                        }}
                      >
                        {JSON.stringify(preview.examples, null, 2)}
                      </pre>
                    </details>
                  </div>
                )}
              </>
            )}
          </>
        )}
        <ul>
          {jobs
            .filter((job) => !selected || job.integration_id === selected)
            .map((job) => (
              <li key={job.id}>
                <button onClick={() => setActive(job)}>
                  {job.status.replaceAll("_", " ")} · {job.accepted} accepted ·{" "}
                  {job.errors.length} errors ·{" "}
                  {new Date(job.created_at).toLocaleString()}
                </button>
              </li>
            ))}
        </ul>
        {!loading && !jobs.length && (
          <p>No jobs yet. A preview does not write project data.</p>
        )}
      </section>
      {active && (
        <section className="panel" aria-label="Job progress">
          <h2>Job progress & data quality</h2>
          <p role="status">{connection}</p>
          <p>
            {active.status.replaceAll("_", " ")} · attempt {active.attempt} ·{" "}
            {active.accepted} accepted
          </p>
          <p>
            Worker heartbeat:{" "}
            {active.heartbeat_at
              ? new Date(active.heartbeat_at).toLocaleString()
              : "Waiting for worker"}
          </p>
          <ol aria-label="Processing stages">
            {stages.map((s) => (
              <li key={s}>{s}</li>
            ))}
          </ol>
          {active.errors.map((err, i) => (
            <p key={i}>
              Page {String(err.page || 1)}, row {String(err.row || "—")}:{" "}
              {String(err.code)}
            </p>
          ))}
          {!!active.errors.length && (
            <p>
              Correct rejected source rows and submit another sync. Previously
              applied source versions are deduplicated; local edits require
              resolution.
            </p>
          )}
          {admin && !terminal.includes(active.status) && (
            <button
              disabled={busy || active.cancel_requested}
              onClick={() =>
                void action(async () =>
                  setActive(
                    await api<Job>(
                      `/activity/jobs/${active.id}/cancel`,
                      "POST",
                    ),
                  ),
                )
              }
            >
              Request cancellation
            </button>
          )}
        </section>
      )}
    </div>
  );
}
