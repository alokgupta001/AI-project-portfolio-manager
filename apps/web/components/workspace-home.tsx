"use client";
import type { components } from "@ppm/contracts/schema";
import { Badge, MetricCard } from "./ui";
import { futureModules } from "./shell";
export function WorkspaceHome({
  account,
  sessionCount,
}: {
  account: components["schemas"]["AccountView"];
  sessionCount: number;
}) {
  const org = account.organizations.find(
    (o) => o.id === account.organization_id,
  );
  return (
    <>
      <section className="page-heading">
        <div>
          <p className="eyebrow">YOUR WORKSPACE, CONNECTED</p>
          <h1>Welcome, {account.name.split(" ")[0]}.</h1>
          <p className="lead">
            A clear starting point for your organization's people, projects and
            decisions.
          </p>
        </div>
        <Badge tone="success">Account connected</Badge>
      </section>
      <section className="welcome-banner">
        <div>
          <p className="eyebrow">{org?.name}</p>
          <h2>
            Set the foundation for
            <br />
            better delivery.
          </h2>
          <p>
            Your organization is connected. Plan projects, track delivery and
            preserve the decisions behind your portfolio.
          </p>
          <a className="button primary" href="/projects">
            Open your projects <span aria-hidden="true">↗</span>
          </a>
        </div>
        <div className="banner-art" aria-hidden="true">
          <span>ALIGN</span>
          <b>
            Plan.
            <br />
            Connect.
            <br />
            Deliver.
          </b>
          <span>ENTERPRISE PPM</span>
        </div>
      </section>
      <div className="metrics-grid">
        <MetricCard
          label="Your membership"
          value={account.role}
          detail="Permissions in the active organization"
        />
        <MetricCard
          label="Connected organizations"
          value={account.organizations.length}
          detail="Your active memberships"
        />
        <MetricCard
          label="Your active sessions"
          value={sessionCount}
          detail="Latest sessions returned by the service (up to 100)"
        />
      </div>
      <div className="home-grid">
        <section className="panel">
          <div className="section-heading">
            <h2>Start with your team</h2>
            <Badge>Available now</Badge>
          </div>
          <div className="action-row">
            <span className="action-icon" aria-hidden="true">
              ◎
            </span>
            <div>
              <h3>Profile & security</h3>
              <p>
                Keep your account details current and review signed-in devices.
              </p>
              <a href="/account#profile">Manage account →</a>
            </div>
          </div>
          {account.role === "Admin" ? (
            <div className="action-row">
              <span className="action-icon" aria-hidden="true">
                ♙
              </span>
              <div>
                <h3>Organization access</h3>
                <p>
                  Invite colleagues and give each member the access they need.
                </p>
                <a href="/account#members">Manage members →</a>
              </div>
            </div>
          ) : (
            <div className="action-row">
              <span className="action-icon" aria-hidden="true">
                ◇
              </span>
              <div>
                <h3>Your access is scoped</h3>
                <p>
                  Ask your organization Admin to manage membership and
                  invitations.
                </p>
              </div>
            </div>
          )}
        </section>
        <section className="panel">
          <p className="eyebrow">WHAT COMES NEXT</p>
          <h2>Your portfolio, in perspective.</h2>
          <p className="muted">
            Portfolios, project delivery, resource capacity and maturity
            assessments are available now. Computed intelligence follows in
            later modules.
          </p>
          <ol className="roadmap-list">
            {futureModules.slice(0, 4).map((m) => (
              <li key={m.name}>
                <span className="roadmap-number">{m.sprint}</span>
                <div>
                  <h3>{m.name}</h3>
                  <p>{m.detail}</p>
                </div>
              </li>
            ))}
          </ol>
        </section>
      </div>
    </>
  );
}
