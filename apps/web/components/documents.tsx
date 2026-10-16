"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import type { components } from "@ppm/contracts/schema";
import { apiError } from "./api-error";
import {
  Button,
  Field,
  StatePanel,
  ConfirmDialog,
  type Confirmation,
} from "./ui";
import { RecordSelect } from "./record-select";

type S = components["schemas"];
type Doc = S["DocumentView"];
type Version = S["VersionView"];
const categories = [
  "SRS",
  "BRD",
  "PRD",
  "MOM",
  "sprint_report",
  "risk_log",
  "charter",
  "policy",
] as const;

export function Documents({
  account,
  transport,
}: {
  account: S["AccountView"];
  transport: typeof fetch;
}) {
  const [items, setItems] = useState<Doc[]>([]);
  const [selected, setSelected] = useState<Doc | null>(null);
  const [active, setActive] = useState<Version | null>(null);
  const [preview, setPreview] = useState<S["ChunkView"][]>([]);
  const [hits, setHits] = useState<S["SearchHit"][]>([]);
  const [job, setJob] = useState<S["JobStatus"] | null>(null);
  const [references, setReferences] = useState<S["EvidenceReference"][]>([]);
  const [attachment, setAttachment] = useState("");
  const [focusChunk, setFocusChunk] = useState("");
  const [orphans, setOrphans] = useState<string[] | null>(null);
  const [q, setQ] = useState("");
  const [term, setTerm] = useState("");
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const [deleted, setDeleted] = useState(false);
  const [page, setPage] = useState(0);
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState<(typeof categories)[number]>("SRS");
  const [project, setProject] = useState("");
  const [newVersion, setNewVersion] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null);
  const generation = useRef(0);
  const selection = useRef(0);
  const viewer = account.role === "Viewer";
  const admin = account.role === "Admin";
  const api = useCallback(
    async <T,>(
      path: string,
      method = "GET",
      body?: unknown,
      revision?: number,
    ): Promise<T> => {
      const response = await transport(
        new Request(window.location.origin + "/api/v1/documents" + path, {
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
    const current = ++generation.current;
    const result = await api<S["DocumentPage"]>(
      `?${new URLSearchParams({ q, offset: String(offset), limit: "25", deleted: String(deleted) })}`,
    );
    if (current === generation.current) {
      setItems(result.items);
      setTotal(result.total);
    }
  }, [api, q, offset, deleted]);
  useEffect(() => {
    let live = true;
    setLoading(true);
    void refresh()
      .catch((e) => {
        if (live) setError(e.message);
      })
      .finally(() => {
        if (live) setLoading(false);
      });
    return () => {
      live = false;
      generation.current++;
    };
  }, [refresh]);

  async function choose(d: Doc, version?: Version) {
    const current = ++selection.current;
    setSelected(d);
    setActive(version || d.versions[0] || null);
    setPreview([]);
    setPage(0);
    setJob(null);
    setReferences([]);
    setFocusChunk("");
    setError("");
    const v = version || d.versions[0];
    if (v?.status === "ready" && !deleted) {
      try {
        const result = await api<S["ChunkView"][]>(`/versions/${v.id}/preview`);
        if (current === selection.current) setPreview(result);
        const links = await api<S["EvidenceReference"][]>(
          `/versions/${v.id}/assessment-links`,
        );
        if (current === selection.current) setReferences(links);
      } catch (e) {
        if (current === selection.current) setError((e as Error).message);
      }
    }
  }
  useEffect(() => {
    if (
      !selected ||
      !active ||
      !["queued", "processing"].includes(active.status)
    )
      return;
    let live = true;
    const timer = setInterval(() => {
      void (async () => {
        try {
          const [d, progress] = await Promise.all([
            api<Doc>(`/${selected.id}`),
            api<S["JobStatus"]>(`/versions/${active.id}/job`).catch(() => null),
          ]);
          if (!live) return;
          const v = d.versions.find((v) => v.id === active.id);
          const parsed =
            v?.status === "ready" && v.status !== active.status
              ? await api<S["ChunkView"][]>(`/versions/${v.id}/preview`)
              : null;
          if (!live) return;
          setSelected(d);
          setJob(progress);
          if (v && v.status !== active.status) {
            setActive(v);
            if (parsed) setPreview(parsed);
            await refresh();
          }
        } catch (e) {
          if (live) {
            setError((e as Error).message);
            setSelected(null);
            setNewVersion(false);
            setActive(null);
            setPreview([]);
            setHits([]);
          }
        }
      })();
    }, 1500);
    return () => {
      live = false;
      clearInterval(timer);
    };
  }, [api, selected, active, refresh]);

  async function perform(action: () => Promise<void>) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await action();
      await refresh();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function readFile(value: File) {
    if (value.size > 8 * 1024 * 1024 || value.size === 0)
      throw new Error("Choose a file from 1 byte to 8 MiB.");
    const bytes = new Uint8Array(await value.arrayBuffer());
    let binary = "";
    for (let i = 0; i < bytes.length; i += 8192)
      binary += String.fromCharCode(...bytes.subarray(i, i + 8192));
    return btoa(binary);
  }
  async function command(path: string, method = "POST", body?: unknown) {
    if (!selected) return;
    await api(path, method, body, selected.revision);
    selection.current++;
    setSelected(null);
    setNewVersion(false);
    setActive(null);
    setPreview([]);
    setHits([]);
    setNotice("Saved. Source access and retention are checked on the server.");
  }

  return (
    <div className="stack document-workspace">
      <header className="page-heading">
        <div>
          <p className="eyebrow">EVIDENCE & GOVERNANCE</p>
          <h1>Document library</h1>
          <p>
            Versioned sources with project access, safe processing and traceable
            locations.
          </p>
        </div>
      </header>
      {error && (
        <StatePanel
          title="Document action unavailable"
          kind="error"
          action={
            <Button variant="secondary" onClick={() => void perform(refresh)}>
              Retry library
            </Button>
          }
        >
          {error}
        </StatePanel>
      )}
      {notice && <p role="status">{notice}</p>}
      <section className="panel stack">
        <h2>Find sources</h2>
        <Field label="Filter document titles">
          <input
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setOffset(0);
            }}
            maxLength={160}
          />
        </Field>
        {admin && (
          <Field label="Retention view">
            <select
              value={String(deleted)}
              onChange={(e) => {
                setDeleted(e.target.value === "true");
                setOffset(0);
                setSelected(null);
                setNewVersion(false);
                setActive(null);
                setPreview([]);
              }}
            >
              <option value="false">Active sources</option>
              <option value="true">Deleted sources and legal holds</option>
            </select>
          </Field>
        )}
        {loading ? (
          <p role="status">Loading permitted sources…</p>
        ) : items.length === 0 ? (
          <StatePanel title="No sources in this view">
            Upload a source you are permitted to manage, or change the title
            filter.
          </StatePanel>
        ) : (
          <div
            className="table-scroll"
            role="region"
            aria-label="Permitted document list; scroll horizontally"
            tabIndex={0}
          >
            <table>
              <caption>{total} permitted sources</caption>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Category</th>
                  <th>Latest version</th>
                  <th>Status</th>
                  <th>Policy</th>
                  <th>Open</th>
                </tr>
              </thead>
              <tbody>
                {items.map((d) => (
                  <tr key={d.id}>
                    <td>{d.title}</td>
                    <td>{d.category}</td>
                    <td>{d.versions[0]?.number ?? "Unknown"}</td>
                    <td>{d.versions[0]?.status ?? "Unknown"}</td>
                    <td>{d.policy_label || "Not registered"}</td>
                    <td>
                      <Button
                        variant="secondary"
                        disabled={busy || loading}
                        onClick={() => void choose(d)}
                      >
                        Open {d.title}
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <div className="actions">
          <Button
            variant="secondary"
            disabled={offset === 0 || loading}
            onClick={() => setOffset((v) => Math.max(0, v - 25))}
          >
            Previous sources
          </Button>
          <span>Page {offset / 25 + 1}</span>
          <Button
            variant="secondary"
            disabled={offset + 25 >= total || loading}
            onClick={() => setOffset((v) => v + 25)}
          >
            Next sources
          </Button>
        </div>
      </section>
      {!viewer && (
        <section className="panel stack">
          <h2>Upload evidence</h2>
          <p>
            PDF, Word, UTF-8 text, CSV, XLSX, PNG or JPEG; maximum 8 MiB. Scans
            use English OCR. Quarantined files cannot be previewed, retrieved or
            downloaded. Do not upload restricted workforce notes.
          </p>
          <form
            className="stack"
            onSubmit={(e) => {
              e.preventDefault();
              void perform(async () => {
                if (!file) throw new Error("Choose a source file.");
                if (newVersion && !selected)
                  throw new Error("Open a document before adding a version.");
                const d = newVersion ? selected : null;
                const result = await api<S["Accepted"]>(
                  "",
                  "POST",
                  {
                    title: d?.title || title,
                    category: d?.category || category,
                    project_id: d?.project_id || project || null,
                    document_id: d?.id || null,
                    filename: file.name,
                    content_base64: await readFile(file),
                  },
                  d?.revision,
                );
                await choose(
                  result.document,
                  result.document.versions.find(
                    (v) => v.id === result.version_id,
                  ),
                );
                setNotice(
                  result.duplicate
                    ? "Identical version already exists."
                    : "Upload stored. Processing will report scanning and extraction status.",
                );
              });
            }}
          >
            <Field label="Add version to open document">
              <input
                type="checkbox"
                checked={newVersion}
                onChange={(e) => setNewVersion(e.target.checked)}
                disabled={!selected || deleted}
              />
            </Field>
            {!newVersion && (
              <>
                <Field label="Document title">
                  <input
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    maxLength={160}
                  />
                </Field>
                <Field label="Document category">
                  <select
                    value={category}
                    onChange={(e) =>
                      setCategory(e.target.value as typeof category)
                    }
                  >
                    {categories.map((c) => (
                      <option key={c}>{c}</option>
                    ))}
                  </select>
                </Field>
                <RecordSelect
                  transport={transport}
                  kind="projects"
                  label="Document project"
                  value={project}
                  onChange={setProject}
                  required={category !== "policy"}
                />
                <p className="muted">
                  An organization policy may omit the project; only Admin can
                  manage it.
                </p>
              </>
            )}
            <Field label="Source file">
              <input
                type="file"
                accept=".txt,.csv,.pdf,.docx,.xlsx,.png,.jpg,.jpeg"
                required
                onChange={(e) => setFile(e.target.files?.[0] || null)}
              />
            </Field>
            <Button disabled={busy}>Store and process source</Button>
          </form>
        </section>
      )}
      <section className="panel stack">
        <h2>Search source text</h2>
        <p>
          This view uses keyword search. Budgeted hybrid retrieval is available
          through AI operations when a provider is authorized. Extracted
          findings remain unavailable.
        </p>
        <form
          className="actions"
          onSubmit={(e) => {
            e.preventDefault();
            void perform(async () => {
              const result = await api<S["Retrieval"]>(
                `/search?q=${encodeURIComponent(term)}`,
              );
              setHits(result.items);
              setNotice(
                result.items.length
                  ? `${result.items.length} permitted keyword matches.`
                  : "No permitted source text matches these words.",
              );
            });
          }}
        >
          <Field label="Source keywords">
            <input
              required
              value={term}
              onChange={(e) => setTerm(e.target.value)}
              maxLength={160}
            />
          </Field>
          <Button disabled={busy}>Search text</Button>
        </form>
        {hits.map((h) => (
          <article className="panel" key={h.id}>
            <h3>
              {h.title} · version {h.version_number}
            </h3>
            <p>
              {h.location} · {h.method} ·{" "}
              {h.confidence === null
                ? "Confidence unknown"
                : `OCR confidence ${Math.round(h.confidence * 100)}%`}
            </p>
            <p style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}>
              {h.text}
            </p>
            <Button
              variant="secondary"
              onClick={() =>
                void perform(async () => {
                  const c = await api<S["ChunkView"]>(`/citations/${h.id}`);
                  const d = await api<Doc>(`/${h.document_id}`);
                  await choose(
                    d,
                    d.versions.find((v) => v.id === h.version_id),
                  );
                  setPreview([c]);
                  setFocusChunk(c.id);
                })
              }
            >
              Open source location
            </Button>
          </article>
        ))}
      </section>
      {selected && (
        <section className="panel stack">
          <h2>{selected.title}</h2>
          <p>
            Document revision {selected.revision}.{" "}
            {selected.legal_hold ? "Legal hold active." : "No legal hold."}{" "}
            Retain through {new Date(selected.retain_until).toLocaleString()}.
          </p>
          <Field label="Source version">
            <select
              value={active?.id || ""}
              onChange={(e) =>
                void choose(
                  selected,
                  selected.versions.find((v) => v.id === e.target.value),
                )
              }
            >
              {selected.versions.map((v) => (
                <option key={v.id} value={v.id}>
                  Version {v.number} · {v.filename} · {v.status}
                </option>
              ))}
            </select>
          </Field>
          {active && (
            <>
              <p role="status">
                Processing: {active.status}
                {active.diagnostic ? ` · ${active.diagnostic}` : ""}
                {job
                  ? ` · attempt ${job.attempt} · ${job.stages.join(" → ")}`
                  : ""}
              </p>
              <p className="muted" style={{ overflowWrap: "anywhere" }}>
                SHA-256: {active.sha256} · {active.size} bytes ·{" "}
                {active.parser_version} · scanner{" "}
                {active.scanner || "not confirmed"}
              </p>
              {active.status === "ready" && !deleted && (
                <Button
                  variant="secondary"
                  disabled={busy}
                  onClick={() =>
                    void perform(async () => {
                      const ticket = await api<S["DownloadTicket"]>(
                        `/versions/${active.id}/download-ticket`,
                        "POST",
                      );
                      const response = await transport(
                        new Request(
                          `${window.location.origin}/api/v1/documents/versions/${active.id}/download?token=${encodeURIComponent(ticket.token)}`,
                        ),
                      );
                      if (!response.ok)
                        throw new Error(
                          apiError(
                            await response.json().catch(() => null),
                            response.status,
                          ),
                        );
                      const url = URL.createObjectURL(await response.blob());
                      const link = document.createElement("a");
                      link.href = url;
                      link.download = active.filename;
                      link.click();
                      setTimeout(() => URL.revokeObjectURL(url), 1000);
                    })
                  }
                >
                  Download verified original
                </Button>
              )}
              {preview.map((c) => (
                <article key={c.id} className="panel">
                  <h3>{c.location}</h3>
                  <p>
                    {c.method} ·{" "}
                    {c.confidence === null
                      ? "Confidence unknown"
                      : `OCR confidence ${Math.round(c.confidence * 100)}%`}
                  </p>
                  <pre
                    style={{ whiteSpace: "pre-wrap", overflowWrap: "anywhere" }}
                  >
                    {focusChunk === c.id ? <mark>{c.text}</mark> : c.text}
                  </pre>
                </article>
              ))}
              {active.status === "ready" && !deleted && (
                <div className="actions">
                  <Button
                    variant="secondary"
                    disabled={page === 0 || busy}
                    onClick={() =>
                      void perform(async () => {
                        setPreview(
                          await api(
                            `/versions/${active.id}/preview?offset=${Math.max(0, page - 25)}`,
                          ),
                        );
                        setPage((v) => Math.max(0, v - 25));
                      })
                    }
                  >
                    Previous locations
                  </Button>
                  <Button
                    variant="secondary"
                    disabled={preview.length < 25 || busy}
                    onClick={() =>
                      void perform(async () => {
                        setPreview(
                          await api(
                            `/versions/${active.id}/preview?offset=${page + 25}`,
                          ),
                        );
                        setPage((v) => v + 25);
                      })
                    }
                  >
                    Next locations
                  </Button>
                </div>
              )}
              {selected.can_manage && !deleted && (
                <div className="actions">
                  <Button
                    variant="secondary"
                    disabled={
                      busy ||
                      ["queued", "processing", "purged"].includes(active.status)
                    }
                    onClick={() =>
                      void perform(async () => {
                        const result = await api<S["Accepted"]>(
                          `/versions/${active.id}/reprocess`,
                          "POST",
                          undefined,
                          selected.revision,
                        );
                        await choose(
                          result.document,
                          result.document.versions.find(
                            (v) => v.id === active.id,
                          ),
                        );
                      })
                    }
                  >
                    Reprocess version
                  </Button>
                  <Button
                    variant="secondary"
                    disabled={
                      busy || !["queued", "processing"].includes(active.status)
                    }
                    onClick={() =>
                      void perform(() =>
                        command(`/versions/${active.id}/cancel`),
                      )
                    }
                  >
                    Cancel processing
                  </Button>
                </div>
              )}
            </>
          )}
          {admin && (
            <form
              key={`${selected.id}-${selected.revision}`}
              className="stack"
              onSubmit={(e) => {
                e.preventDefault();
                const data = new FormData(e.currentTarget);
                void perform(async () => {
                  const policy =
                    selected.category === "policy" && data.get("owner")
                      ? {
                          owner_id: data.get("owner"),
                          version_id: active?.id,
                          applicability: data.get("applicability"),
                          state: data.get("state"),
                          effective_date: data.get("effective"),
                          review_date: data.get("review"),
                        }
                      : null;
                  await command(`/${selected.id}/governance`, "PATCH", {
                    legal_hold: data.get("hold") === "on",
                    retain_until: new Date(
                      String(data.get("retention")),
                    ).toISOString(),
                    policy,
                  });
                });
              }}
            >
              <h3>Policy and retention</h3>
              <Field label="Legal hold">
                <input
                  name="hold"
                  type="checkbox"
                  defaultChecked={selected.legal_hold}
                />
              </Field>
              <Field label="Retain until (local time)">
                <input
                  required
                  type="datetime-local"
                  name="retention"
                  defaultValue={new Date(
                    new Date(selected.retain_until).getTime() -
                      new Date().getTimezoneOffset() * 60000,
                  )
                    .toISOString()
                    .slice(0, 16)}
                />
              </Field>
              {selected.category === "policy" && (
                <>
                  <PolicyOwner
                    transport={transport}
                    initial={selected.policy?.owner_id || ""}
                  />
                  <Field label="Policy applicability">
                    <input
                      name="applicability"
                      maxLength={500}
                      defaultValue={selected.policy?.applicability || ""}
                    />
                  </Field>
                  <Field label="Policy state">
                    <select
                      name="state"
                      defaultValue={selected.policy?.state || "draft"}
                    >
                      <option>draft</option>
                      <option>current</option>
                      <option>superseded</option>
                    </select>
                  </Field>
                  <Field label="Effective date">
                    <input
                      name="effective"
                      type="date"
                      defaultValue={selected.policy?.effective_date || ""}
                    />
                  </Field>
                  <Field label="Review date">
                    <input
                      name="review"
                      type="date"
                      defaultValue={selected.policy?.review_date || ""}
                    />
                  </Field>
                  <p>
                    Registers the selected ready source version. Approval
                    workflow is pending Sprint 15.
                  </p>
                </>
              )}
              <Button disabled={busy}>Save governance</Button>
            </form>
          )}
          {selected.can_manage && (
            <Button
              variant="danger"
              disabled={busy}
              onClick={() =>
                setConfirmation({
                  title: deleted ? "Purge retained source?" : "Delete source?",
                  description: deleted
                    ? "Permanently removes original bytes and derived text after retention expires. Legal holds block this action."
                    : "Immediately removes retrieval and download access. Retention and legal holds preserve the original bytes.",
                  confirm: () =>
                    perform(() =>
                      command(
                        `/${selected.id}${deleted ? "/purge" : ""}`,
                        deleted ? "POST" : "DELETE",
                      ),
                    ),
                })
              }
            >
              {deleted ? "Purge expired source" : "Delete source"}
            </Button>
          )}
        </section>
      )}
      {selected && active?.status === "ready" && !deleted && (
        <section className="panel stack">
          <h2>Assessment evidence references</h2>
          <p>
            Only private evidence you can access is listed. Linking an identical
            released attachment preserves all saved scores.
          </p>
          {references.length === 0 ? (
            <p>No permitted assessment references.</p>
          ) : (
            references.map((r) => (
              <p key={r.attachment_id}>
                <a href={`/assessments?assessment=${r.assessment_id}`}>
                  {r.assessment_name}
                </a>
              </p>
            ))
          )}
          {selected.can_manage && (
            <form
              className="stack"
              onSubmit={(e) => {
                e.preventDefault();
                void perform(async () => {
                  await api(
                    `/versions/${active.id}/assessment-link`,
                    "POST",
                    { attachment_id: attachment },
                    selected.revision,
                  );
                  setReferences(
                    await api(`/versions/${active.id}/assessment-links`),
                  );
                  setNotice(
                    "Released assessment attachment linked; assessment scores are unchanged.",
                  );
                });
              }}
            >
              <Field label="Released assessment attachment reference">
                <input
                  required
                  value={attachment}
                  onChange={(e) => setAttachment(e.target.value)}
                  pattern="[a-fA-F0-9-]{36}"
                />
              </Field>
              <p>
                Copy the reference shown beside the released attachment in
                Assessments.
              </p>
              <Button disabled={busy}>Link released attachment</Button>
            </form>
          )}
        </section>
      )}
      {admin && deleted && (
        <section className="panel stack">
          <h2>Orphan cleanup</h2>
          <p>
            Preview up to 100 unreferenced objects at least 30 days old.
            Referenced versions, other organizations and legal holds are
            excluded.
          </p>
          <Button
            variant="secondary"
            disabled={busy}
            onClick={() =>
              void perform(async () =>
                setOrphans(
                  (await api<S["OrphanPage"]>("/retention/orphans")).keys,
                ),
              )
            }
          >
            Preview eligible orphans
          </Button>
          {orphans && (
            <p role="status">{orphans.length} eligible orphan objects.</p>
          )}
          {!!orphans?.length && (
            <Button
              variant="danger"
              disabled={busy}
              onClick={() =>
                setConfirmation({
                  title: "Purge eligible orphans?",
                  description:
                    "Permanently removes the previewed old, unreferenced objects after another hold and reference check.",
                  confirm: () =>
                    perform(async () => {
                      await api("/retention/orphans/purge", "POST", {
                        keys: orphans,
                      });
                      setOrphans(null);
                      setNotice("Eligible orphans purged.");
                    }),
                })
              }
            >
              Purge previewed orphans
            </Button>
          )}
        </section>
      )}
      <ConfirmDialog
        value={confirmation}
        onClose={() => setConfirmation(null)}
      />
    </div>
  );
}

function PolicyOwner({
  transport,
  initial,
}: {
  transport: typeof fetch;
  initial: string;
}) {
  const [owner, setOwner] = useState(initial);
  return (
    <RecordSelect
      transport={transport}
      kind="people"
      label="Policy owner"
      name="owner"
      value={owner}
      onChange={setOwner}
    />
  );
}
