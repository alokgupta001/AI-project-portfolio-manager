"use client";
import { useCallback, useEffect, useState } from "react";
import type { components } from "@ppm/contracts/schema";

type Account = components["schemas"]["AccountView"];
type Item = {
  id: string;
  name: string;
  href: string;
  kind?: string;
  due_date?: string;
  read?: boolean;
};
type Page = { items: Item[]; total: number; enabled?: boolean };
import { usePilotApi } from "./pilot-api";
export { usePilotApi } from "./pilot-api";
import { RecordSelect } from "./record-select";
export function RecordSearch({ transport }: { transport: typeof fetch }) {
  const api = usePilotApi(transport);
  const [q, setQ] = useState("");
  const [kind, setKind] = useState("");
  const [offset, setOffset] = useState(0);
  const [page, setPage] = useState<Page | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let live = true;
    setPage(null);
    setError("");
    const timer = setTimeout(() => {
      void api<Page>(
        "workspace/search?" +
          new URLSearchParams({
            q,
            offset: String(offset),
            ...(kind ? { kind } : {}),
          }),
      )
        .then((p) => {
          if (live) setPage(p);
        })
        .catch((e) => {
          if (live) setError(e.message);
        });
    }, 200);
    return () => {
      live = false;
      clearTimeout(timer);
    };
  }, [api, q, kind, offset]);
  return (
    <section aria-label="Search records">
      <label>
        Find a record
        <input
          type="search"
          maxLength={160}
          value={q}
          onChange={(e) => {
            setQ(e.target.value);
            setOffset(0);
          }}
        />
      </label>
      <label>
        Record type
        <select
          value={kind}
          onChange={(e) => {
            setKind(e.target.value);
            setOffset(0);
          }}
        >
          <option value="">All records</option>
          {["projects", "work_items", "risks", "assessments"].map((k) => (
            <option key={k} value={k}>
              {k.replaceAll("_", " ")}
            </option>
          ))}
        </select>
      </label>
      {error && <p role="alert">{error}</p>}
      {!error && !page && <p role="status">Searching…</p>}
      <nav className="command-results" aria-label="Matching records">
        {page?.items.map((i) => (
          <a href={i.href} key={i.kind + i.id}>
            {i.name}
            <small>{i.kind?.replaceAll("_", " ")}</small>
          </a>
        ))}
      </nav>
      {page && (
        <>
          <p>
            {page.total
              ? `${page.total} permitted matches`
              : "No permitted records match your search."}
          </p>
          <button disabled={!offset} onClick={() => setOffset(offset - 25)}>
            Previous records
          </button>
          <button
            disabled={offset + 25 >= page.total}
            onClick={() => setOffset(offset + 25)}
          >
            Next records
          </button>
        </>
      )}
    </section>
  );
}
export function PersonalFeed({
  transport,
  notifications = false,
}: {
  transport: typeof fetch;
  notifications?: boolean;
}) {
  const api = usePilotApi(transport);
  const [page, setPage] = useState<Page | null>(null);
  const [error, setError] = useState("");
  const [offset, setOffset] = useState(0);
  const load = useCallback(
    () =>
      api<Page>(
        `workspace/${notifications ? "notifications" : "my-work"}?offset=${offset}`,
      ).then(setPage),
    [api, notifications, offset],
  );
  useEffect(() => {
    let live = true;
    setPage(null);
    void load().catch((e) => {
      if (live) setError(e.message);
    });
    return () => {
      live = false;
    };
  }, [load]);
  return (
    <section className="panel">
      <h2>{notifications ? "Your notifications" : "My work"}</h2>
      {error && <p role="alert">{error}</p>}
      {!page && !error && <p role="status">Loading…</p>}
      {notifications && page && (
        <label>
          <input
            type="checkbox"
            checked={page.enabled}
            onChange={(e) =>
              void api("workspace/notification-preference", "PUT", {
                enabled: e.target.checked,
              })
                .then(load)
                .catch((e) => setError(e.message))
            }
          />
          Show in-app notifications
        </label>
      )}
      {page?.items.map((i) => (
        <div className="action-row" key={i.id}>
          <a href={i.href}>{i.name}</a>
          <span>
            {i.due_date ? `Due ${i.due_date}` : i.kind?.replaceAll("_", " ")}
          </span>
          {notifications && (
            <button
              disabled={i.read}
              onClick={() =>
                void api(`workspace/notifications/${i.id}/read`, "POST")
                  .then(load)
                  .catch((e) => setError(e.message))
              }
            >
              {i.read ? "Read" : "Mark read"}
            </button>
          )}
        </div>
      ))}
      {page && !page.items.length && (
        <p>
          {notifications
            ? "No eligible notifications. Assignment, review and import results appear here for 30 days while you have access."
            : "No permitted assigned work, open risks or active assessments. Ask your Admin about assignments and access."}
        </p>
      )}
      {page && (
        <>
          <button disabled={!offset} onClick={() => setOffset(offset - 25)}>
            Previous
          </button>
          <button
            disabled={offset + 25 >= page.total}
            onClick={() => setOffset(offset + 25)}
          >
            Next
          </button>
        </>
      )}
    </section>
  );
}
export function SetupChecklist({ transport }: { transport: typeof fetch }) {
  const api = usePilotApi(transport);
  const [steps, setSteps] = useState<
    { label: string; href: string; complete: boolean }[] | null
  >(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let live = true;
    void api<{ steps: NonNullable<typeof steps> }>("workspace/setup")
      .then((p) => {
        if (live) setSteps(p.steps);
      })
      .catch((e) => {
        if (live) setError(e.message);
      });
    return () => {
      live = false;
    };
  }, [api]);
  return (
    <section className="panel">
      <h2>Getting started</h2>
      <p>
        A login account controls access. A resource profile describes staffing
        and can exist without a login.
      </p>
      {error && <p role="alert">{error}</p>}
      {!steps && !error && <p role="status">Checking saved progress…</p>}
      <ul>
        {steps?.map((s) => (
          <li key={s.label}>
            {s.complete ? "✓ " : "○ "}
            <a href={s.href}>{s.label}</a>
            {s.complete ? " — saved" : " — next step"}
          </li>
        ))}
      </ul>
      <p>
        Examples are optional. Admins can preview the delivery sample in
        Organization setup and choose “Load sample data”. Sample names start
        with Demo; archive them through their existing forms when finished.
      </p>
    </section>
  );
}
type Invitation = {
  invitation_id: string;
  email: string;
  role: string;
  expires_at: string;
  delivery_status: string;
};
const deliveryLabels: Record<string, string> = {
  queued: "Waiting to send (or retry)",
  provider_accepted: "Accepted by email provider — inbox arrival unconfirmed",
  local_preview: "Local test message — no inbox email sent",
  failed: "Sending failed after retries — resend after fixing delivery",
  cancelled: "Sending stopped — resend for a new link",
  acceptance_unverified: "Earlier delivery — inbox arrival unconfirmed",
  legacy_delivery_unverified: "Earlier delivery — status unverified",
};
export function PilotAccount({
  account,
  transport,
}: {
  account: Account;
  transport: typeof fetch;
}) {
  const api = usePilotApi(transport);
  const [profile, setProfile] = useState<{
    name: string;
    revision: number;
    description: string | null;
    industry: string | null;
    website: string | null;
    created_at: string;
    administrators: { id: string; name: string }[];
    active_members: number;
    members: number;
    timezone: string | null;
    currency: string | null;
    setup_complete: boolean;
  } | null>(null);
  const [editingName, setEditingName] = useState(false);
  const [editingDetails, setEditingDetails] = useState(false);
  const [draftName, setDraftName] = useState("");
  const [details, setDetails] = useState({
    description: "",
    industry: "",
    website: "",
  });
  const [invites, setInvites] = useState<Invitation[]>([]);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const load = useCallback(async () => {
    setProfile(await api("organization/profile"));
    if (account.role === "Admin")
      setInvites(await api("organization/invitations"));
  }, [api, account]);
  useEffect(() => {
    void load().catch((e) => setError(e.message));
  }, [load]);
  async function act(fn: () => Promise<unknown>, success = "Saved.") {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await fn();
      await load();
      setNotice(success);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="panel" id="organization-profile">
      <h2>Organization profile</h2>
      {error && <p role="alert">{error}</p>}
      {notice && <p role="status">{notice}</p>}
      {profile && (
        <>
          <h3>{profile.name}</h3>
          {editingName ? (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (draftName.trim() === profile.name) {
                  setEditingName(false);
                  return;
                }
                void act(async () => {
                  await api(
                    "organization/profile",
                    "PATCH",
                    { name: draftName.trim() },
                    profile.revision,
                  );
                  setEditingName(false);
                }, "Organization name saved. Refresh other pages to see the updated name.");
              }}
            >
              <label>
                Organization name
                <input
                  autoFocus
                  required
                  maxLength={120}
                  value={draftName}
                  onChange={(e) => setDraftName(e.target.value)}
                />
              </label>
              <button
                disabled={
                  busy || !draftName.trim() || draftName.trim() === profile.name
                }
              >
                Save organization name
              </button>
              <button
                type="button"
                disabled={busy}
                onClick={() => {
                  setEditingName(false);
                  setError("");
                }}
              >
                Cancel name change
              </button>
            </form>
          ) : (
            account.role === "Admin" && (
              <button
                disabled={busy}
                onClick={() => {
                  setDraftName(profile.name);
                  setEditingName(true);
                  setNotice("");
                  setError("");
                }}
              >
                Edit name
              </button>
            )
          )}
          {profile.description && <p>{profile.description}</p>}
          {profile.industry && <p>Industry: {profile.industry}</p>}
          {profile.website && (
            <p>
              <a href={profile.website} target="_blank" rel="noreferrer">
                Organization website
              </a>
            </p>
          )}
          <p>
            Created {new Date(profile.created_at).toLocaleDateString()} ·{" "}
            {profile.active_members} active members of {profile.members}
          </p>
          <p>
            Administrators:{" "}
            {profile.administrators.map((a) => a.name).join(", ") ||
              "No active administrators"}
          </p>
          <p>
            {profile.setup_complete
              ? `Operating settings saved: ${profile.timezone} · ${profile.currency}`
              : "Operating settings required: configure timezone and currency to begin planning."}
          </p>
          <a href="/organization">
            {profile.setup_complete
              ? "Organization setup"
              : "Configure organization"}
          </a>
          {" · "}
          <a href="/resources">Resource planning and working calendars</a>
          {editingDetails ? (
            <form
              onSubmit={(e) => {
                e.preventDefault();
                void act(async () => {
                  await api(
                    "organization/profile",
                    "PATCH",
                    {
                      description: details.description.trim() || null,
                      industry: details.industry.trim() || null,
                      website: details.website.trim() || null,
                    },
                    profile.revision,
                  );
                  setEditingDetails(false);
                }, "Organization details saved.");
              }}
            >
              <label>
                Short description
                <textarea
                  maxLength={1000}
                  value={details.description}
                  onChange={(e) =>
                    setDetails({ ...details, description: e.target.value })
                  }
                />
              </label>
              <label>
                Industry
                <input
                  maxLength={120}
                  value={details.industry}
                  onChange={(e) =>
                    setDetails({ ...details, industry: e.target.value })
                  }
                />
              </label>
              <label>
                Website
                <input
                  type="url"
                  maxLength={500}
                  value={details.website}
                  onChange={(e) =>
                    setDetails({ ...details, website: e.target.value })
                  }
                />
              </label>
              <button
                disabled={
                  busy ||
                  (details.description.trim() === (profile.description || "") &&
                    details.industry.trim() === (profile.industry || "") &&
                    details.website.trim() === (profile.website || ""))
                }
              >
                Save organization details
              </button>
              <button
                type="button"
                disabled={busy}
                onClick={() => {
                  setEditingDetails(false);
                  setError("");
                }}
              >
                Cancel details change
              </button>
            </form>
          ) : (
            account.role === "Admin" && (
              <p>
                <button
                  disabled={busy}
                  onClick={() => {
                    setDetails({
                      description: profile.description || "",
                      industry: profile.industry || "",
                      website: profile.website || "",
                    });
                    setEditingDetails(true);
                    setError("");
                    setNotice("");
                  }}
                >
                  Edit organization details
                </button>
              </p>
            )
          )}
        </>
      )}
      {account.role === "Admin" && (
        <>
          <h3>Pending invitations</h3>
          <p>
            Resending replaces the old link. Cancellation prevents acceptance.
            Provider acceptance does not confirm inbox arrival. Refresh this
            list to check sending progress. Expired invitations can be resent.
          </p>
          <button
            disabled={busy}
            onClick={() => void act(async () => {}, "Invitations refreshed.")}
          >
            Refresh invitations
          </button>
          {!invites.length && <p>No pending invitations.</p>}
          {invites.map((i) => (
            <div key={i.invitation_id}>
              <p>
                {i.email} · {i.role} ·{" "}
                {deliveryLabels[i.delivery_status] ||
                  "Sending status unavailable"}{" "}
                · {new Date(i.expires_at) <= new Date() ? "expired" : "expires"}{" "}
                {new Date(i.expires_at).toLocaleString()}
              </p>
              {["resend", "cancel"].map((op) => (
                <button
                  disabled={busy}
                  key={op}
                  onClick={() =>
                    void act(() =>
                      api(
                        `organization/invitations/${i.invitation_id}/${op}`,
                        "POST",
                      ),
                    )
                  }
                >
                  {op === "resend" ? "Resend invitation" : "Cancel invitation"}
                </button>
              ))}
            </div>
          ))}
        </>
      )}
    </section>
  );
}
export function AssessmentAccess({
  transport,
  account,
  frameworkId,
  assessmentId,
}: {
  transport: typeof fetch;
  account: Account;
  frameworkId?: string;
  assessmentId?: string;
}) {
  const api = usePilotApi(transport);
  const [grants, setGrants] = useState<
    { user_id: string; id: string; name: string }[]
  >([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const scope = frameworkId
    ? { framework_id: frameworkId }
    : { assessment_id: assessmentId! };
  const scopeQuery = frameworkId
    ? `framework_id=${frameworkId}`
    : `assessment_id=${assessmentId}`;
  const load = useCallback(
    () => api<typeof grants>(`assessment/access?${scopeQuery}`).then(setGrants),
    [api, scopeQuery],
  );
  useEffect(() => {
    if (account.role === "Admin") void load().catch((e) => setError(e.message));
  }, [account.role, load]);
  async function grant(user: string, active: boolean) {
    setBusy(true);
    setError("");
    try {
      await api("assessment/access", "POST", {
        user_id: user,
        ...scope,
        active,
      });
      await load();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section aria-label="Assessment access">
      <h3>Access</h3>
      <p>
        Assignments allow eligible respondents and independent reviewers to work
        on an assessment. Completed-result grants share scores only. Framework
        editors must be active Project Managers; only Admin publishes. Ownership
        grants no additional access.
      </p>
      {error && <p role="alert">{error}</p>}
      {account.role === "Admin" && (
        <>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const user = new FormData(e.currentTarget).get("member");
              if (user) void grant(String(user), true);
            }}
          >
            <RecordSelect
              transport={transport}
              kind="people"
              label="Member"
              name="member"
              required
            />
            <button disabled={busy}>
              Grant {frameworkId ? "framework editing" : "result access"}
            </button>
          </form>
          {grants.map((g) => (
            <div key={g.id}>
              <span>{g.name || "Granted member"}</span>
              <button
                disabled={busy}
                onClick={() => void grant(g.user_id, false)}
              >
                Revoke access
              </button>
            </div>
          ))}
        </>
      )}
    </section>
  );
}

export function DepartmentComparison({
  transport,
  version,
}: {
  transport: typeof fetch;
  version: string;
}) {
  const api = usePilotApi(transport);
  const [start, setStart] = useState(
    new Date(Date.now() - 365 * 86400000).toISOString().slice(0, 10),
  );
  const [end, setEnd] = useState(new Date().toISOString().slice(0, 10));
  const [data, setData] = useState<{
    items: {
      department_id: string;
      name: string;
      score: string | null;
      count: number;
      scored_count: number;
    }[];
    count: number;
    coverage: string;
  } | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let live = true;
    setData(null);
    setError("");
    void api<NonNullable<typeof data>>(
      "workspace/comparison?" +
        new URLSearchParams({ framework_version_id: version, start, end }),
    )
      .then((d) => {
        if (live) setData(d);
      })
      .catch((e) => {
        if (live) setError(e.message);
      });
    return () => {
      live = false;
    };
  }, [api, version, start, end]);
  return (
    <section>
      <h3>Department comparison</h3>
      <p>
        Completed departmental results using exactly this published version,
        across the full permitted cohort. Period uses assessment creation dates
        in UTC.
      </p>
      <label>
        Comparison from
        <input
          type="date"
          required
          value={start}
          onChange={(e) => setStart(e.target.value)}
        />
      </label>
      <label>
        Comparison through
        <input
          type="date"
          required
          value={end}
          onChange={(e) => setEnd(e.target.value)}
        />
      </label>
      {error && <p role="alert">{error}</p>}
      {!data && !error && <p role="status">Loading full cohort…</p>}
      {data && (
        <>
          <p>
            {data.count} completed records · {data.coverage}
          </p>
          <div
            className="table-scroll"
            tabIndex={0}
            role="region"
            aria-label="Department comparison scores"
          >
            <table>
              <caption>Compatible departmental scores</caption>
              <thead>
                <tr>
                  <th>Department</th>
                  <th>Mean score / 100</th>
                  <th>Count</th>
                  <th>Scored count</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((d) => (
                  <tr key={d.department_id}>
                    <th>{d.name || "Department"}</th>
                    <td>
                      {d.score == null
                        ? "Unknown"
                        : Number(d.score).toLocaleString(undefined, {
                            maximumFractionDigits: 2,
                          })}
                    </td>
                    <td>{d.count}</td>
                    <td>{d.scored_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {!data.count && (
            <p>No completed compatible departmental results in this period.</p>
          )}
        </>
      )}
    </section>
  );
}
