"use client";

import { FormEvent, useEffect, useState } from "react";
import { createApiClient } from "@ppm/contracts";
import type { components } from "@ppm/contracts/schema";

import { AuthFrame, Shell } from "../../components/shell";
import { PasswordField } from "../../components/password-field";
import { apiError } from "../../components/api-error";
import {
  PilotAccount,
  SetupChecklist,
  PersonalFeed,
} from "../../components/pilot";
import { WorkspaceHome } from "../../components/workspace-home";
import { Integrations } from "../../components/integrations";
import { AI } from "../../components/ai";
import { Agents } from "../../components/agents";
import { Documents } from "../../components/documents";
import { CommandCenter } from "../../components/command-center";
import { Assessments } from "../../components/assessments";
import { Capacity } from "../../components/capacity";
import { Delivery } from "../../components/delivery";
import { Gallery } from "../../components/gallery";
import {
  ConfirmDialog,
  DataTable,
  Skeleton,
  type Confirmation,
} from "../../components/ui";

type Account = components["schemas"]["AccountView"];
type Member = components["schemas"]["MemberView"];
type Session = components["schemas"]["SessionView"];
type Audit = components["schemas"]["AuditView"];
type Role = Member["role"];
let csrfToken = "";
let activeOrganization = "";
let refreshing: Promise<boolean> | null = null;
const transport: typeof fetch = async (input, init) => {
  const request = new Request(input, init);
  if (!csrfToken) {
    const response = await fetch("/api/v1/auth/csrf", { cache: "no-store" });
    if (!response.ok) throw new Error("Session verification is unavailable.");
    csrfToken = (await response.json()).csrf_token;
  }
  request.headers.set("x-csrf-token", csrfToken);
  if (activeOrganization)
    request.headers.set("x-organization-id", activeOrganization);
  const retry = request.clone();
  const result = await fetch(request);
  if (result.status === 401 && !request.url.endsWith("/auth/login")) {
    refreshing ??= fetch("/api/v1/auth/refresh", {
      method: "POST",
      headers: { "x-csrf-token": csrfToken },
    })
      .then((r) => r.ok)
      .finally(() => {
        refreshing = null;
      });
    if (await refreshing) return fetch(retry);
  }
  return result;
};
const api = () => createApiClient(window.location.origin, transport);
const messages: Record<number, string> = {
  400: "This link is invalid, expired or already used. Request a new one.",
  401: "Sign-in failed or your session expired. Check your credentials and sign in again.",
  403: "Permission or request verification failed. Reload and try again.",
  404: "The requested membership or session is not available.",
  409: "Reload to confirm your active organization. The final active admin cannot be removed.",
  412: "This member changed. Reload the list before saving.",
  422: "Check your fields. New passwords need at least 12 characters and at most 72 UTF-8 bytes.",
  429: "Too many attempts. Wait ten minutes before trying again.",
};
function checked<T>(result: {
  data?: T;
  error?: unknown;
  response: Response;
}): T {
  if (!result.response.ok)
    throw new Error(apiError(result.error, result.response.status));
  return result.data as T;
}

export default function IdentityClient({
  mode,
}: {
  mode:
    | "signup"
    | "login"
    | "reset"
    | "complete"
    | "account"
    | "workspace"
    | "gallery"
    | "delivery"
    | "capacity"
    | "assessment"
    | "command"
    | "integrations"
    | "documents"
    | "ai"
    | "agents";
}) {
  const protectedMode = [
    "account",
    "workspace",
    "gallery",
    "delivery",
    "capacity",
    "assessment",
    "command",
    "integrations",
    "documents",
    "ai",
    "agents",
  ].includes(mode);
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null);
  const [memberFilter, setMemberFilter] = useState("");
  const [account, setAccount] = useState<Account | null>(null);
  const [members, setMembers] = useState<Member[]>([]);
  const [sessions, setSessions] = useState<Session[]>([]);
  const [events, setEvents] = useState<Audit[]>([]);
  const [cursor, setCursor] = useState<string | null>(null);
  const [auditCursor, setAuditCursor] = useState<string | null>(null);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(protectedMode);
  const [challenge, setChallenge] = useState("");
  const [completionAction, setCompletionAction] = useState("");
  async function load() {
    const user = checked(await api().GET("/api/v1/auth/me"));
    const nextSessions = checked(
      await api().GET("/api/v1/auth/sessions"),
    ).items;
    let nextMembers: Member[] = [];
    let nextEvents: Audit[] = [];
    let nextCursor: string | null = null;
    let nextAuditCursor: string | null = null;
    if (user.role === "Admin") {
      const list = checked(await api().GET("/api/v1/organization/members"));
      nextMembers = list.items;
      nextCursor = list.next_cursor ?? null;
      const history = checked(await api().GET("/api/v1/organization/audit"));
      nextEvents = history.items;
      nextAuditCursor = history.next_cursor ?? null;
    }
    activeOrganization = user.organization_id || "";
    setSessions(nextSessions);
    setMembers(nextMembers);
    setEvents(nextEvents);
    setCursor(nextCursor);
    setAuditCursor(nextAuditCursor);
    setAccount(user);
  }
  useEffect(() => {
    if (mode === "complete") {
      // Presentation hint only; the server validates the actual challenge kind.
      setCompletionAction(
        new URLSearchParams(window.location.search).get("action") || "",
      );
      setChallenge(
        new URLSearchParams(window.location.hash.slice(1)).get("token") || "",
      );
      window.history.replaceState(null, "", window.location.pathname);
    }
    if (
      [
        "account",
        "workspace",
        "gallery",
        "delivery",
        "capacity",
        "assessment",
        "command",
        "integrations",
        "documents",
        "ai",
        "agents",
      ].includes(mode)
    )
      load()
        .catch((e) => {
          if (e.message !== messages[401]) setError(e.message);
        })
        .finally(() => setLoading(false));
  }, [mode]);
  async function action(work: () => Promise<void>) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await work();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed.");
    } finally {
      setBusy(false);
    }
  }
  function form(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    return new FormData(event.currentTarget);
  }
  function text(data: FormData, key: string) {
    return String(data.get(key) || "");
  }
  const organizationControl = account ? (
    <label>
      Organization
      <select
        value={account.organization_id || ""}
        disabled={busy}
        onChange={(e) => {
          const id = e.target.value;
          void action(async () => {
            checked(
              await api().POST("/api/v1/auth/switch", {
                body: { organization_id: id },
              }),
            );
            await load();
            setNotice("Organization switched.");
          });
        }}
      >
        {!account.organization_id && (
          <option value="">Choose an accessible organization</option>
        )}
        {account.organizations.map((o) => (
          <option key={o.id} value={o.id}>
            {o.name} · {o.role} · {o.id.slice(0, 8)}
          </option>
        ))}
      </select>
    </label>
  ) : null;
  const content = (
    <div className="identity-page">
      {mode !== "workspace" &&
        mode !== "gallery" &&
        mode !== "delivery" &&
        mode !== "capacity" &&
        mode !== "assessment" &&
        mode !== "command" &&
        mode !== "integrations" &&
        mode !== "documents" &&
        mode !== "ai" &&
        mode !== "agents" && (
          <section className="intro">
            <p className="eyebrow">YOUR ENTERPRISE WORKSPACE</p>
            <h1>
              {mode === "signup"
                ? "Create your organization."
                : mode === "login"
                  ? "Welcome back."
                  : mode === "reset"
                    ? "Recover your account."
                    : mode === "complete"
                      ? completionAction === "reset"
                        ? "Reset your password."
                        : completionAction === "invite"
                          ? "Accept your invitation."
                          : "Complete your account request."
                      : "Your account. Your access."}
            </h1>
            <p className="lead">
              {mode === "complete"
                ? completionAction === "reset"
                  ? "Enter your display name and choose a new password. Resetting your password signs out existing sessions. Then sign in with your new password."
                  : completionAction === "invite"
                    ? "New members choose a display name and password. Existing verified members enter their current password to join the organization."
                    : "For signup or activation, choose a display name and password. For password recovery, choose a new password. For an invitation to an existing account, enter your current password."
                : "Secure access to the organizations you belong to. Your permissions follow your active membership."}
            </p>
          </section>
        )}
      {error && (
        <p role="alert" className="notice error">
          {error}
        </p>
      )}
      {mode === "complete" && error === messages[400] && (
        <p className="notice">
          For signup, <a href="/signup">request verification again</a>. For
          recovery, <a href="/account/reset">request a password reset</a>. For
          an invitation, ask the organization Admin to resend it, then open the
          latest message.
        </p>
      )}
      {notice && (
        <p role="status" className="notice">
          {notice}
        </p>
      )}
      {loading && <Skeleton label="Loading your account" />}
      {!protectedMode && (
        <form
          className="panel identity-form"
          onSubmit={(event) => {
            const data = form(event);
            void action(async () => {
              if (mode === "signup") {
                const r = await transport(
                  new Request(
                    window.location.origin + "/api/v1/auth/register",
                    {
                      method: "POST",
                      headers: { "content-type": "application/json" },
                      body: JSON.stringify({
                        email: text(data, "email"),
                        organization_name: text(data, "organization_name"),
                      }),
                    },
                  ),
                );
                if (!r.ok)
                  throw new Error(
                    messages[r.status] ||
                      "Registration unavailable. Try again.",
                  );
                setNotice((await r.json()).message);
              } else if (mode === "login") {
                checked(
                  await api().POST("/api/v1/auth/login", {
                    body: {
                      email: text(data, "email"),
                      password: text(data, "password"),
                    },
                  }),
                );
                window.location.assign("/account");
              } else if (mode === "reset") {
                setNotice(
                  checked(
                    await api().POST("/api/v1/auth/reset-request", {
                      body: { email: text(data, "email") },
                    }),
                  ).message,
                );
              } else {
                setNotice(
                  checked(
                    await api().POST("/api/v1/auth/complete", {
                      body: {
                        token: challenge,
                        password: text(data, "password"),
                        name: text(data, "name"),
                      },
                    }),
                  ).message,
                );
                setChallenge("");
              }
            });
          }}
        >
          {mode !== "complete" && (
            <label>
              Email address
              <input
                name="email"
                type="email"
                required
                autoComplete="email"
                maxLength={254}
              />
            </label>
          )}
          {mode === "complete" && (
            <>
              <label>
                One-time token
                <input
                  type="password"
                  value={challenge}
                  onChange={(e) => setChallenge(e.target.value)}
                  required
                  autoComplete="off"
                  maxLength={128}
                />
              </label>
              <label>
                Display name
                <input
                  name="name"
                  required
                  maxLength={120}
                  autoComplete="name"
                />
              </label>
            </>
          )}
          {mode === "signup" && (
            <label>
              Organization name
              <input name="organization_name" required maxLength={120} />
            </label>
          )}
          {mode !== "reset" && mode !== "signup" && (
            <PasswordField
              label={
                mode === "complete" ? "Password (12–72 bytes)" : "Password"
              }
              autoComplete={
                mode === "login" ? "current-password" : "new-password"
              }
              minLength={mode === "complete" ? 12 : 1}
            />
          )}
          <button disabled={busy}>
            {busy
              ? "Working…"
              : mode === "signup"
                ? "Send verification instructions"
                : mode === "login"
                  ? "Sign in"
                  : mode === "reset"
                    ? "Send recovery instructions"
                    : completionAction === "reset"
                      ? "Reset password"
                      : "Verify and continue"}
          </button>
          <nav aria-label="Account help">
            <a href="/signup">Create an account</a>
            <a href="/login">Sign in</a>
            <a href="/account/reset">Forgot password?</a>
          </nav>
        </form>
      )}
      {protectedMode && !loading && !account && (
        <a className="refresh" href="/login">
          Go to sign in
        </a>
      )}
      {account && !account.organization_id && (
        <section className="panel">
          <h2>Your account is active</h2>
          <p>
            {account.organizations.length
              ? "Select an organization above to continue."
              : "You have no active organization memberships. Ask an administrator to invite you or restore your membership. You can still manage your personal profile and sessions."}
          </p>
          <a href="/account">Account and access</a>
        </section>
      )}
      {account?.organization_id && mode === "workspace" && (
        <>
          <SetupChecklist transport={transport} />
          <WorkspaceHome account={account} sessionCount={sessions.length} />
          <PersonalFeed transport={transport} />
        </>
      )}
      {account && mode === "gallery" && <Gallery />}
      {account?.organization_id && mode === "ai" && (
        <AI
          key={account.organization_id}
          account={account}
          transport={transport}
        />
      )}
      {account?.organization_id && mode === "agents" && (
        <Agents
          key={account.organization_id}
          account={account}
          transport={transport}
        />
      )}
      {account?.organization_id && mode === "documents" && (
        <Documents
          key={account.organization_id}
          account={account}
          transport={transport}
        />
      )}
      {account?.organization_id && mode === "integrations" && (
        <Integrations
          key={account.organization_id}
          account={account}
          transport={transport}
        />
      )}
      {account?.organization_id && mode === "command" && (
        <CommandCenter
          key={account.organization_id}
          account={account}
          transport={transport}
        />
      )}
      {account?.organization_id && mode === "assessment" && (
        <Assessments
          key={account.organization_id}
          account={account}
          transport={transport}
        />
      )}
      {account?.organization_id && mode === "capacity" && (
        <Capacity
          transport={transport}
          key={account.organization_id}
          account={account}
          client={api()}
        />
      )}
      {account?.organization_id && mode === "delivery" && (
        <Delivery
          key={account.organization_id}
          account={account}
          client={api()}
        />
      )}
      {account?.organization_id && mode === "account" && (
        <PilotAccount
          key={account.organization_id}
          account={account}
          transport={transport}
        />
      )}
      {account && mode === "account" && (
        <div className="identity-grid">
          <section className="panel">
            <h2>Active organization</h2>
            <p className="badge">{account.role}</p>
            <p className="muted">{account.email}</p>
            <button
              disabled={busy}
              onClick={() =>
                void action(async () => {
                  checked(await api().POST("/api/v1/auth/logout"));
                  csrfToken = "";
                  window.location.assign("/login");
                })
              }
            >
              Sign out
            </button>
          </section>
          <section className="panel" id="profile">
            <h2>Profile & security</h2>
            <form
              className="identity-form"
              onSubmit={(e) => {
                const data = form(e);
                void action(async () => {
                  checked(
                    await api().PATCH("/api/v1/auth/profile", {
                      body: { name: text(data, "name") },
                    }),
                  );
                  await load();
                  setNotice("Profile saved.");
                });
              }}
            >
              <label>
                Display name
                <input
                  key={account.name}
                  name="name"
                  defaultValue={account.name}
                  required
                  maxLength={120}
                />
              </label>
              <button disabled={busy}>Save profile</button>
            </form>
            <a className="refresh" href="/account/reset">
              Reset password and revoke sessions
            </a>
          </section>
          <section className="panel wide">
            <h2>Active sessions</h2>
            <p className="muted">
              Revoke access immediately, including on another device.
            </p>
            <ul className="identity-list">
              {sessions.map((s) => (
                <li key={s.id}>
                  <span>
                    {s.current ? "This session" : "Other session"} ·{" "}
                    {new Date(s.created_at).toLocaleString()}
                  </span>
                  <button
                    disabled={busy}
                    onClick={() =>
                      setConfirmation({
                        title: "Revoke session?",
                        description: s.current
                          ? "You will be signed out on this device."
                          : "The selected device will lose access immediately.",
                        confirm: () =>
                          action(async () => {
                            checked(
                              await api().DELETE(
                                "/api/v1/auth/sessions/{session_id}",
                                { params: { path: { session_id: s.id } } },
                              ),
                            );
                            if (s.current) window.location.assign("/login");
                            else {
                              await load();
                              setNotice("Session revoked.");
                            }
                          }),
                      })
                    }
                  >
                    Revoke{s.current ? " current" : " session"}
                  </button>
                </li>
              ))}
            </ul>
          </section>
          {account.role === "Admin" ? (
            <>
              <section className="panel wide">
                <h2>Invite a member</h2>
                <p className="muted">
                  Invite a colleague to this organization with the role they
                  need. Ask them to check their inbox and spam folder; sending
                  progress appears under Pending invitations.
                </p>
                <form
                  className="identity-form inline-form"
                  onSubmit={(e) => {
                    const data = form(e);
                    void action(async () => {
                      setNotice(
                        checked(
                          await api().POST("/api/v1/organization/invitations", {
                            body: {
                              email: text(data, "email"),
                              role: text(data, "role") as Role,
                            },
                          }),
                        ).message,
                      );
                      await load();
                    });
                  }}
                >
                  <label>
                    Email address
                    <input name="email" type="email" required />
                  </label>
                  <label>
                    Role
                    <select name="role">
                      <option>Viewer</option>
                      <option>Project Manager</option>
                      <option>Admin</option>
                    </select>
                  </label>
                  <button disabled={busy}>Create invitation</button>
                </form>
              </section>
              <section className="panel wide" id="members">
                <h2>Organization members</h2>
                <p className="muted">
                  Changes use the current member revision. The final active
                  admin is protected.
                </p>
                <label>
                  Filter loaded members
                  <input
                    type="search"
                    value={memberFilter}
                    onChange={(e) => setMemberFilter(e.target.value)}
                    placeholder="Name, email or role"
                  />
                </label>
                {members.filter((m) =>
                  `${m.name} ${m.email} ${m.role}`
                    .toLowerCase()
                    .includes(memberFilter.toLowerCase()),
                ).length === 0 && <p>No matching loaded members.</p>}
                <ul className="identity-list">
                  {members
                    .filter((m) =>
                      `${m.name} ${m.email} ${m.role}`
                        .toLowerCase()
                        .includes(memberFilter.toLowerCase()),
                    )
                    .map((m) => (
                      <li key={`${m.user_id}-${m.revision}`}>
                        <div>
                          <strong>{m.name}</strong>
                          <p className="muted">
                            {m.email} · {m.active ? "Active" : "Inactive"}
                          </p>
                        </div>
                        <form
                          className="member-form"
                          onSubmit={(e) => {
                            const data = form(e);
                            const save = () =>
                              action(async () => {
                                checked(
                                  await api().PATCH(
                                    "/api/v1/organization/members/{user_id}",
                                    {
                                      params: {
                                        path: { user_id: m.user_id },
                                        header: {
                                          "if-match": String(m.revision),
                                        },
                                      },
                                      body: {
                                        role: text(data, "role") as Role,
                                        active: data.has("active"),
                                      },
                                    },
                                  ),
                                );
                                await load();
                                setNotice("Member updated.");
                              });
                            if (
                              !data.has("active") ||
                              text(data, "role") !== m.role
                            )
                              setConfirmation({
                                title: "Change member access?",
                                description: `Update access for ${m.email}. Removing access may revoke their sessions.`,
                                confirm: save,
                              });
                            else void save();
                          }}
                        >
                          <label>
                            Role for {m.email}
                            <select name="role" defaultValue={m.role}>
                              <option>Admin</option>
                              <option>Project Manager</option>
                              <option>Viewer</option>
                            </select>
                          </label>
                          <label className="checkbox">
                            <input
                              type="checkbox"
                              name="active"
                              defaultChecked={m.active}
                            />
                            Active
                          </label>
                          <button disabled={busy}>Save member</button>
                        </form>
                      </li>
                    ))}
                </ul>
                {cursor && (
                  <button
                    disabled={busy}
                    onClick={() =>
                      void action(async () => {
                        const result = checked(
                          await api().GET("/api/v1/organization/members", {
                            params: { query: { after: cursor } },
                          }),
                        );
                        setMembers([...members, ...result.items]);
                        setCursor(result.next_cursor ?? null);
                      })
                    }
                  >
                    Load more members
                  </button>
                )}
              </section>
              <section className="panel wide">
                <h2>Access audit</h2>
                <DataTable
                  key={account.organization_id}
                  rows={events}
                  rowKey={(e) => e.id}
                  caption="Access audit"
                  searchText={(e) => e.action}
                  columns={[
                    {
                      key: "action",
                      label: "Action",
                      sort: (e) => e.action,
                      render: (e) => e.action.replaceAll("_", " "),
                    },
                    {
                      key: "time",
                      label: "Time",
                      sort: (e) => e.created_at,
                      render: (e) => (
                        <time dateTime={e.created_at}>
                          {new Date(e.created_at).toLocaleString()}
                        </time>
                      ),
                    },
                  ]}
                />
                {auditCursor && (
                  <button
                    disabled={busy}
                    onClick={() =>
                      void action(async () => {
                        const list = checked(
                          await api().GET("/api/v1/organization/audit", {
                            params: { query: { after: auditCursor } },
                          }),
                        );
                        setEvents([...events, ...list.items]);
                        setAuditCursor(list.next_cursor ?? null);
                      })
                    }
                  >
                    Load more events
                  </button>
                )}
              </section>
            </>
          ) : (
            <section className="panel wide">
              <h2>Membership access</h2>
              <p>
                Your {account.role} membership lets you manage your own account.
                Organization membership changes require an Admin. Project access
                will require explicit scope when project modules are introduced.
              </p>
            </section>
          )}
        </div>
      )}
      <ConfirmDialog
        value={confirmation}
        onClose={() => setConfirmation(null)}
      />
    </div>
  );
  if (account && protectedMode)
    return (
      <Shell
        key={account.organization_id}
        transport={transport}
        name={account.name}
        role={account.role || "Account"}
        organizationControl={organizationControl}
      >
        {content}
      </Shell>
    );
  return (
    <AuthFrame>
      <main className="auth-main">
        {protectedMode && (
          <section className="intro">
            <p className="eyebrow">ENTERPRISE PPM</p>
            <h1>Your workspace awaits.</h1>
            <p className="lead">
              Sign in to manage your account and organization. Portfolio and
              intelligence modules are coming in later releases.
            </p>
          </section>
        )}
        {content}
      </main>
    </AuthFrame>
  );
}
