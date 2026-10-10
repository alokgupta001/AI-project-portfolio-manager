import { createApiClient } from "@ppm/contracts";

export const dynamic = "force-dynamic";

async function getStatus() {
  const base = process.env.API_ORIGIN;
  if (!base)
    return {
      problem: "API_ORIGIN is not configured. See the local setup guide.",
    };
  try {
    const url = new URL(base);
    if (!["http:", "https:"].includes(url.protocol))
      throw new Error("Invalid origin");
    const client = createApiClient(base);
    const [ready, foundation] = await Promise.all([
      client.GET("/api/v1/health/ready", {
        signal: AbortSignal.timeout(5000),
        cache: "no-store",
      }),
      client.GET("/api/v1/foundation", {
        signal: AbortSignal.timeout(5000),
        cache: "no-store",
      }),
    ]);
    return { ready: ready.data ?? ready.error, foundation: foundation.data };
  } catch {
    return {
      problem:
        "The API is unavailable. Start the local stack, then refresh this page.",
    };
  }
}

export default async function Home() {
  const status = await getStatus();
  const healthy = status.ready?.status === "ready";
  return (
    <main>
      <header>
        <a href="/" className="brand">
          <span className="brand-mark">P</span> Enterprise PPM
        </a>
        <span className="environment">LOCAL FOUNDATION</span>
      </header>
      <section className="intro">
        <p className="eyebrow">OPERATIONAL PILOT / DEVELOPMENT WORKSPACE</p>
        <h1>
          A connected foundation.
          <br />
          <span>Ready for what comes next.</span>
        </h1>
        <p className="lead">
          The starting point for enterprise portfolio intelligence. This
          workspace connects the web application to its API, database, and local
          services.
        </p>
      </section>
      <section className="panel" aria-labelledby="status-heading">
        <div className="panel-heading">
          <div>
            <p className="eyebrow">LIVE CONNECTIONS</p>
            <h2 id="status-heading">Foundation status</h2>
          </div>
          <span className={healthy ? "badge success" : "badge warning"}>
            {healthy ? "Services ready" : "Setup required"}
          </span>
        </div>
        {status.problem ? (
          <p role="alert" className="notice">
            {status.problem}
          </p>
        ) : (
          <ul className="services">
            {status.ready?.dependencies.map((item) => (
              <li key={item.name}>
                <span className="service-name">{item.name}</span>
                <span
                  className={item.status === "ready" ? "state ready" : "state"}
                >
                  {item.status === "ready" ? "Connected" : "Unavailable"}
                </span>
              </li>
            ))}
          </ul>
        )}
        {status.foundation ? (
          <dl className="checkpoint">
            <div>
              <dt>Database checkpoint</dt>
              <dd data-testid="instance-id">{status.foundation.instance_id}</dd>
            </div>
            <div>
              <dt>Initialized in UTC</dt>
              <dd>{status.foundation.initialized_at}</dd>
            </div>
            <div>
              <dt>Schema revision</dt>
              <dd>{status.foundation.schema_revision}</dd>
            </div>
          </dl>
        ) : (
          <p className="notice">
            A database checkpoint will appear after the first migration
            succeeds.
          </p>
        )}
        <a className="refresh" href="/system">
          Refresh status <span aria-hidden="true">↗</span>
        </a>
      </section>
      <section className="next-step">
        <span className="step-number">02</span>
        <div>
          <h2>Identity and organization access</h2>
          <p>
            Sign in to manage delivery, resources, assessments and deterministic
            dashboards. AI features and live-provider acceptance remain
            unavailable or unverified.
          </p>
          <a
            className="refresh"
            href={`${process.env.PPM_WEB_ORIGIN || "http://localhost:3000"}/login`}
          >
            Open your workspace
          </a>
        </div>
      </section>
      <footer>
        Development environment · Existing organization data is preserved ·
        Service status is read from the API on every refresh
      </footer>
    </main>
  );
}
