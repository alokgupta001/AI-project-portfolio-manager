import { test, expect, type Page } from "./test";
import AxeBuilder from "@axe-core/playwright";
import { mkdirSync, readFileSync } from "node:fs";
import type { components } from "@ppm/contracts/schema";

type S = components["schemas"];
type Snapshot = S["CommandSnapshot"];
const evidenceDirectory = "artifacts/local/frontend-redesign";
const widths = [360, 768, 1024, 1440, 1920];

test.beforeAll(() => mkdirSync(evidenceDirectory, { recursive: true }));
test.beforeEach(async ({ page }) => {
  // This suite tests the application beneath the independently tested welcome tour.
  await page.addInitScript(() => {
    const original = Storage.prototype.getItem;
    Storage.prototype.getItem = function (key: string) {
      return key.startsWith("ppm-tutorial-v1:")
        ? JSON.stringify({ version: 1, status: "completed", step: 7 })
        : original.call(this, key);
    };
  });
});

async function login(page: Page) {
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  await page.goto("/login");
  await page.getByLabel("Email address", { exact: true }).fill(f.command_email);
  await page.getByLabel("Password", { exact: true }).fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(f.command_org);
  await expect(
    page.getByRole("heading", { name: "Organization members" }),
  ).toBeVisible();
  const csrf = (await page.context().cookies()).find(
    (c) => c.name === "ppm_csrf",
  )!.value;
  const headers = {
    origin: process.env.PPM_WEB_URL!,
    "x-csrf-token": csrf,
    "x-organization-id": f.command_org,
  };
  return { f, headers };
}

function calendarDate(timeZone: string, offset = 0) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "numeric",
    day: "numeric",
  }).formatToParts(new Date());
  const part = (type: string) =>
    Number(parts.find((value) => value.type === type)?.value);
  return new Date(
    Date.UTC(part("year"), part("month") - 1, part("day") + offset),
  )
    .toISOString()
    .slice(0, 10);
}

async function theme(page: Page, value: "light" | "dark") {
  if ((await page.locator("html").getAttribute("data-theme")) !== value)
    await page
      .getByRole("button", { name: `Switch to ${value} theme` })
      .click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", value);
}

async function captureMatrix(page: Page, state: "populated" | "empty") {
  for (const color of ["light", "dark"] as const) {
    await theme(page, color);
    for (const width of widths) {
      await page.setViewportSize({ width, height: 1000 });
      expect(
        await page.evaluate(() => document.documentElement.scrollWidth),
      ).toBeLessThanOrEqual(width);
      const result = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
        .analyze();
      expect(
        result.violations.map((v) => ({
          id: v.id,
          nodes: v.nodes.map((n) => n.target),
        })),
      ).toEqual([]);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({
        path: `${evidenceDirectory}/home-${state}-${color}-${width}.png`,
        fullPage: true,
        animations: "disabled",
      });
    }
  }
}

test("redesign: live snapshot, scoped filters, complete server pages and project deep links", async ({
  page,
}) => {
  test.setTimeout(180000);
  const { headers } = await login(page);
  async function create(kind: string, values: Record<string, unknown>) {
    const r = await page.request.post(`/api/v1/delivery/${kind}`, {
      headers: { ...headers, "idempotency-key": crypto.randomUUID() },
      data: { kind, name: `Redesign ${kind}`, ...values },
    });
    expect(r.status(), await r.text()).toBe(201);
    return r.json();
  }
  const settingsResponse = await page.request.get(
    "/api/v1/delivery/settings?limit=100",
    { headers },
  );
  expect(settingsResponse.ok()).toBe(true);
  const settings: S["PageView"] = await settingsResponse.json();
  const savedSettings = settings.items.find((s) => s.data.kind === "settings");
  const timezone =
    savedSettings?.data.kind === "settings"
      ? savedSettings.data.timezone
      : "Asia/Kolkata";
  if (!savedSettings) await create("settings", { timezone, currency: "INR" });
  const portfolio = await create("portfolios", {
    name: `Redesign verification ${crypto.randomUUID().slice(0, 8)}`,
  });
  const projects: { id: string }[] = [];
  for (let i = 1; i <= 7; i++)
    projects.push(
      await create("projects", {
        name: `Redesign project ${i}`,
        portfolio_id: portfolio.id,
        currency: "INR",
        status: "active",
      }),
    );
  await create("expenditures", {
    project_id: projects[0].id,
    amount: "125.00",
    currency: "INR",
    spent_on: calendarDate(timezone, -10),
  });
  await create("expenditures", {
    project_id: projects[0].id,
    amount: "375.00",
    currency: "INR",
    spent_on: calendarDate(timezone, -60),
  });
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Welcome,/ })).toBeVisible();
  await page
    .getByRole("combobox", { name: "Portfolio scope", exact: true })
    .selectOption(portfolio.id);
  await expect(
    page.getByRole("button", { name: /^Visible projects/ }).locator("strong"),
  ).toHaveText("7");
  await expect(
    page.getByRole("button", { name: /^Health coverage/ }).locator("strong"),
  ).toHaveText("0%");
  await expect(page.locator(".period-spend-value strong")).toHaveText(
    "125.00 INR",
  );
  await expect(page.locator(".snapshot-meta")).toContainText(
    `${calendarDate(timezone, -29)} to ${calendarDate(timezone, 1)} (end excluded)`,
  );
  await page
    .getByRole("button", { name: "Unknown health 7", exact: true })
    .click();
  await expect(page.locator("#projects-in-focus [role=status]")).toHaveText(
    "7 of 7 visible projects · Unknown health",
  );
  await page.getByLabel("Filter Projects in focus").fill("Redesign project 7");
  await expect(
    page.getByRole("link", { name: "Redesign project 7", exact: true }),
  ).toBeVisible();
  const updated = page.waitForResponse((response) => {
    const url = new URL(response.url());
    return (
      url.pathname === "/api/v1/command/snapshot" &&
      url.searchParams.get("portfolio_id") === portfolio.id &&
      url.searchParams.get("start") === calendarDate(timezone, -89) &&
      url.searchParams.get("end") === calendarDate(timezone, 1)
    );
  });
  await page
    .getByRole("combobox", { name: "Activity period", exact: true })
    .selectOption("90");
  const updatedResponse = await updated;
  expect(updatedResponse.ok()).toBe(true);
  const snapshot: Snapshot = await updatedResponse.json();
  expect(snapshot.projects).toHaveLength(7);
  expect(snapshot.projects.every((p) => p.computed_health === "Unknown")).toBe(
    true,
  );
  expect(snapshot.totals.find((m) => m.key === "INR_period_spend")?.value).toBe(
    "500.00",
  );
  await expect(page.locator(".period-spend-value strong")).toHaveText(
    "500.00 INR",
  );
  await expect(page.locator(".snapshot-meta")).toContainText(
    `${snapshot.start} to ${snapshot.end} (end excluded)`,
  );
  await page.setViewportSize({ width: 1440, height: 1000 });
  await theme(page, "light");
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: `${evidenceDirectory}/home-live-light-1440.png`,
    fullPage: true,
    animations: "disabled",
  });
  await page.goto("/projects");
  await page
    .getByRole("searchbox", { name: "Search records", exact: true })
    .fill("Redesign project");
  await expect(
    page.getByRole("cell", { name: "Redesign project 7", exact: true }),
  ).toBeVisible();
  await expect(page.locator(".data-table tbody tr")).toHaveCount(7);
  await page
    .getByRole("button", { name: "Create projects", exact: true })
    .click();
  const editor = page.getByRole("dialog", {
    name: "Create Projects",
    exact: true,
  });
  await editor
    .getByRole("textbox", { name: "Name", exact: true })
    .fill("Unsaved regression record");
  page.once("dialog", (dialog) => dialog.dismiss());
  await page.keyboard.press("Escape");
  await expect(editor).toBeVisible();
  await expect(
    editor.getByRole("textbox", { name: "Name", exact: true }),
  ).toHaveValue("Unsaved regression record");
  page.once("dialog", (dialog) => dialog.accept());
  await editor.getByRole("button", { name: "Cancel", exact: true }).click();
  await expect(editor).not.toBeVisible();
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: `${evidenceDirectory}/projects-list-live-light-1440.png`,
    fullPage: true,
    animations: "disabled",
  });
  await page.goto(`/projects/${projects[0].id}`);
  await expect(
    page
      .getByRole("navigation", { name: "Primary navigation" })
      .getByRole("link", { name: "Projects", exact: true }),
  ).toHaveAttribute("aria-current", "page");
  await expect(
    page.locator(".metric-card").filter({ hasText: "Approved budget" }),
  ).not.toContainText("undefined");
  await expect(
    page.getByRole("heading", { name: "Project overview", exact: true }),
  ).toBeVisible();
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: `${evidenceDirectory}/project-detail-live-light-1440.png`,
    fullPage: true,
    animations: "disabled",
  });
  expect(errors).toEqual([]);
});

test("redesign: snapshot categories reconcile, accessible filters and recoverable unavailable/empty states", async ({
  page,
}) => {
  test.setTimeout(300000);
  await page.clock.setFixedTime(new Date("2026-10-29T19:00:00Z"));
  const { f } = await login(page);
  // These complete, explicitly synthetic browser fixtures are independent of the
  // preceding live test. Only browser responses are mocked; no tenant records change.
  const stamp = "2026-10-29T19:00:00Z";
  const portfolio: S["RecordView"] = {
    id: "synthetic-portfolio",
    organization_id: f.command_org,
    revision: 1,
    created_at: stamp,
    updated_at: stamp,
    data: {
      kind: "portfolios",
      name: "Example browser scope",
      archived: false,
      description: "Synthetic browser fixture only",
    },
  };
  const synthetic: Snapshot = {
    amber: "30",
    red: "60",
    compute_ms: 0,
    computed_at: stamp,
    start: "2026-10-01",
    end: "2026-10-31",
    limitations: [
      "Synthetic browser state only; no organization records changed.",
    ],
    metric_version: "command-v1",
    risk_rule: "risk-rule-v1",
    policy_revision: 1,
    portfolio_id: null,
    scope: "Synthetic browser-only permitted project scope",
    stale_days: 7,
    timezone: "Asia/Kolkata",
    records: [],
    resources: [],
    teams: [],
    totals: [],
    velocity: [],
    projects: ["Green", "Amber", "Red", "Unknown"].map((health, i) => ({
      id: `synthetic-${i}`,
      name: `Example ${health} project`,
      portfolio_id: portfolio.id,
      computed_health: health,
      reported_health: health,
      discrepancy: false,
      can_edit: false,
      metrics: [
        {
          key: "health",
          label: "Evidence health",
          value: ["90", "50", "20", null][i],
          unit: "health points",
          period: "Current snapshot 2026-10-30",
          source: "Synthetic browser fixture only",
          source_updated_at: health === "Unknown" ? null : stamp,
          freshness: health === "Unknown" ? "missing" : "fresh",
          status: health === "Unknown" ? "unknown" : "available",
          coverage_percent: health === "Unknown" ? "0" : "100",
          explanation: "Browser-only category state; no inference or live data",
          facts: [],
        },
      ],
    })),
  };
  let mode: "populated" | "error" | "empty" = "populated";
  const queries: URLSearchParams[] = [];
  await page.route("**/api/v1/delivery/portfolios?*", async (route) => {
    const viewer =
      route.request().headers()["x-organization-id"] === f.viewer_org;
    const data: S["PageView"] = {
      as_of: stamp,
      items: viewer ? [] : [portfolio],
      limit: 100,
      offset: 0,
      total: viewer ? 0 : 1,
    };
    await route.fulfill({ json: data });
  });
  await page.route("**/api/v1/command/snapshot?*", async (route) => {
    const query = new URL(route.request().url()).searchParams;
    queries.push(query);
    const viewer =
      route.request().headers()["x-organization-id"] === f.viewer_org;
    if (mode === "error" && !viewer) {
      await route.fulfill({
        status: 503,
        json: { detail: "Snapshot temporarily unavailable" },
      });
      return;
    }
    const empty = mode === "empty" || viewer;
    const period = `${query.get("start")} to ${query.get("end")} (end excluded)`;
    const days =
      (Date.parse(query.get("end")!) - Date.parse(query.get("start")!)) /
      86400000;
    const totals: S["Metric"][] = ["INR", "USD"].map((currency) => ({
      key: `${currency}_period_spend`,
      label: `${currency} Period recorded spend`,
      value:
        currency === "INR"
          ? days === 90
            ? "500.00"
            : "125.00"
          : days === 90
            ? "100.00"
            : "25.00",
      unit: currency,
      period,
      source: "Synthetic browser fixture only",
      source_updated_at: stamp,
      freshness: currency === "INR" ? "fresh" : "stale",
      status: currency === "INR" ? "available" : "partial",
      coverage_percent: "100",
      explanation: "No FX conversion; browser-only example",
      facts: [],
    }));
    const data: Snapshot = {
      ...synthetic,
      start: query.get("start")!,
      end: query.get("end")!,
      portfolio_id: query.get("portfolio_id"),
      projects: empty ? [] : synthetic.projects,
      totals: empty ? [] : totals,
    };
    await route.fulfill({ json: data });
  });
  await page.goto("/");
  const stats = page.locator(".overview-metric strong");
  await expect(stats).toHaveText(["4", "2", "1", "75%"]);
  expect(queries.at(-1)?.get("start")).toBe("2026-10-01");
  expect(queries.at(-1)?.get("end")).toBe("2026-10-31");
  await expect(page.locator(".snapshot-meta")).toContainText("10/30/2026");
  await expect(page.locator(".period-spend-value strong")).toHaveText([
    "125.00 INR",
    "25.00 USD",
  ]);
  await expect(page.locator(".spend-quality")).toHaveText([
    "Available · Source fresh",
    "Partial ledger · Source stale",
  ]);
  await page
    .getByRole("combobox", { name: "Activity period", exact: true })
    .selectOption("90");
  await expect(page.locator(".period-spend-value strong")).toHaveText([
    "500.00 INR",
    "100.00 USD",
  ]);
  expect(queries.at(-1)?.get("start")).toBe("2026-08-02");
  expect(queries.at(-1)?.get("end")).toBe("2026-10-31");
  await page
    .getByRole("combobox", { name: "Portfolio scope", exact: true })
    .selectOption(portfolio.id);
  await expect(
    page.getByRole("button", { name: /^Visible projects/ }).locator("strong"),
  ).toHaveText("4");
  await page.getByRole("button", { name: /^Need attention/ }).click();
  await expect(page.locator("#projects-in-focus tbody tr")).toHaveCount(2);
  await expect(
    page.getByRole("link", { name: "Example Amber project" }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Unknown health 1", exact: true })
    .click();
  await expect(page.locator("#projects-in-focus tbody tr")).toHaveCount(1);
  await page
    .getByRole("button", { name: "Show all health categories" })
    .click();
  await page.getByText("View chart data table", { exact: true }).click();
  await expect(
    page
      .getByRole("region", { name: "Health distribution data" })
      .locator("tbody tr"),
  ).toHaveCount(4);
  await captureMatrix(page, "populated");
  mode = "error";
  await page.getByRole("button", { name: "Refresh", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Portfolio snapshot unavailable" }),
  ).toBeVisible();
  await expect(stats).toHaveText(["—", "—", "—", "—"]);
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.screenshot({
    path: `${evidenceDirectory}/home-unavailable-dark-1920.png`,
    fullPage: true,
    animations: "disabled",
  });
  mode = "empty";
  await page.getByRole("button", { name: "Retry snapshot" }).click();
  await expect(stats).toHaveText(["0", "0", "0", "Unavailable"]);
  await expect(
    page.getByText("No permitted projects in this scope.", { exact: false }),
  ).toBeVisible();
  await expect(
    page.getByText("No financial totals are available in this scope.", {
      exact: false,
    }),
  ).toBeVisible();
  await captureMatrix(page, "empty");
  // A genuine organization switch must remount all scope, period and health state.
  mode = "populated";
  await page.getByRole("button", { name: "Refresh", exact: true }).click();
  await expect(stats).toHaveText(["4", "2", "1", "75%"]);
  await page
    .getByRole("button", { name: "Unknown health 1", exact: true })
    .click();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(f.viewer_org);
  await expect(page.locator(".access-list")).toContainText("Viewer");
  await expect(
    page.getByRole("combobox", { name: "Portfolio scope", exact: true }),
  ).toHaveValue("");
  await expect(
    page.getByRole("combobox", { name: "Activity period", exact: true }),
  ).toHaveValue("30");
  await expect(stats).toHaveText(["0", "0", "0", "Unavailable"]);
  await expect(page.locator("#projects-in-focus [role=status]")).toHaveText(
    "0 of 0 visible projects · All health categories",
  );
  await expect(
    page.getByRole("link", { name: /^Example .* project$/ }),
  ).toHaveCount(0);
  await expect(
    page
      .getByRole("combobox", { name: "Portfolio scope", exact: true })
      .locator("option"),
  ).toHaveCount(1);
});
