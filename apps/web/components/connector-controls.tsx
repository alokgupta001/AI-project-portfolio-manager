"use client";
import { useCallback, useEffect, useState } from "react";
import type { components } from "@ppm/contracts/schema";
import { apiError } from "./api-error";
type S = components["schemas"];
export function ConnectorControls({
  integration,
  transport,
  refresh,
}: {
  integration: S["IntegrationView"];
  transport: typeof fetch;
  refresh: () => Promise<void>;
}) {
  const [authority, setAuthority] = useState<S["AuthorityView"] | null>(null);
  const [conflicts, setConflicts] = useState<S["ConflictView"][]>([]);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const api = useCallback(
    async <T,>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const response = await transport(
        new Request(
          window.location.origin +
            `/api/v1/integrations/${integration.id}` +
            path,
          {
            method,
            headers: {
              "content-type": "application/json",
              ...(revision == null ? {} : { "if-match": String(revision) }),
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
    [transport, integration.id],
  );
  const load = useCallback(async () => {
    const [a, c] = await Promise.all([
      api<S["AuthorityView"] | null>("/authority"),
      api<S["ConflictView"][]>("/conflicts"),
    ]);
    setAuthority(a);
    setConflicts(c);
  }, [api]);
  useEffect(() => {
    void load()
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [load]);
  async function act(work: () => Promise<void>) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await work();
      await load();
      await refresh();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section
      className="connector-controls"
      aria-label="Connector authority and conflict review"
    >
      <h3>Organization connector authority</h3>
      <p>
        {loading
          ? "Loading connector authority…"
          : authority
            ? `${authority.active ? "Active" : "Revoked"} · generation ${authority.generation} · revision ${authority.revision}`
            : "Session-delegated legacy connection. Approve a narrow connector principal for work after logout."}
      </p>
      <p>
        Approval permits only this connection’s project work/sprints. Rotation
        invalidates queued jobs; resubmit after rotation. Values below are
        server secret references, never keys.
      </p>
      {error && <p role="alert">{error}</p>}
      {notice && <p role="status">{notice}</p>}
      {loading && <p role="status">Loading connector authority…</p>}
      {!loading && (
        <form
          className="identity-form"
          key={`${integration.revision}:${authority?.revision || 0}`}
          onSubmit={(e) => {
            e.preventDefault();
            const form = new FormData(e.currentTarget);
            void act(async () => {
              await api(
                "/authority",
                "PUT",
                {
                  active: true,
                  interval_minutes: Number(form.get("interval")),
                  secret_ref: form.get("secret_ref") || "",
                  webhook_secret_ref: form.get("webhook_secret_ref") || "",
                },
                authority?.revision || 0,
              );
              setNotice(
                "Connector authority approved/rotated independently of your session.",
              );
            });
          }}
        >
          <label>
            Credential reference
            <input
              name="secret_ref"
              defaultValue={integration.config.secret_ref}
              maxLength={80}
            />
          </label>
          <label>
            Webhook credential reference
            <input
              name="webhook_secret_ref"
              defaultValue={integration.config.webhook_secret_ref}
              maxLength={80}
            />
          </label>
          <label>
            Polling interval (minutes; 0 disables schedule)
            <input
              name="interval"
              type="number"
              min={0}
              max={10080}
              defaultValue={authority?.interval_minutes || 0}
              disabled={integration.config.mode !== "live"}
            />
          </label>
          <button disabled={busy}>Approve / rotate connector authority</button>
        </form>
      )}
      <button
        disabled={busy || !authority?.active}
        onClick={() =>
          void act(async () => {
            await api(
              "/authority",
              "PUT",
              {
                active: false,
                interval_minutes: 0,
                secret_ref: integration.config.secret_ref || "",
                webhook_secret_ref: integration.config.webhook_secret_ref || "",
              },
              authority?.revision || 0,
            );
            setNotice(
              "Connector revoked. Queued and scheduled work is stopped.",
            );
          })
        }
      >
        Revoke connector authority
      </button>
      <h3>Source conflicts</h3>
      <button disabled={busy} onClick={() => void act(load)}>
        Refresh source conflicts
      </button>
      {!conflicts.length && <p>No source conflicts recorded.</p>}
      {conflicts.map((c) => (
        <article key={c.id}>
          <h4>
            Conflict {c.id.slice(0, 8)} · {c.status} · revision {c.revision}
          </h4>
          <p>
            Source version: {c.source_updated_at || "unknown"} · observed{" "}
            {c.source_observed_at}
          </p>
          <div
            className="table-scroll"
            tabIndex={0}
            role="region"
            aria-label="Source conflict comparison table"
          >
            <table>
              <caption>
                Current saved local values and proposed source values
              </caption>
              <thead>
                <tr>
                  <th>Field</th>
                  <th>Local</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {Object.keys(c.candidate).map((key) => (
                  <tr key={key}>
                    <td>{key}</td>
                    <td>{JSON.stringify(c.local[key] ?? null)}</td>
                    <td>{JSON.stringify(c.candidate[key])}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p>
            Review local revision <strong>{String(c.local.revision)}</strong>.
            Refresh source conflicts to inspect current local values. Changes
            made after this review are rejected until refreshed.
          </p>
          {c.status === "pending" &&
            (["keep_local", "accept_source"] as const).map((decision) => (
              <button
                key={decision}
                disabled={busy}
                onClick={() =>
                  void act(async () => {
                    await api(
                      `/conflicts/${c.id}/resolve`,
                      "POST",
                      {
                        decision,
                        local_revision: Number(c.local.revision),
                        source_fingerprint: c.fingerprint,
                      },
                      c.revision,
                    );
                    setNotice(
                      "Reviewed conflict resolved with source and local version checks.",
                    );
                  })
                }
              >
                {decision === "keep_local"
                  ? "Keep local edits"
                  : "Accept reviewed source"}
              </button>
            ))}
        </article>
      ))}
    </section>
  );
}
