import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

test("CSV preview, durable sync, live progress, repeat effects and revoked scope", async ({
  page,
}) => {
  test.setTimeout(180000);
  page.setDefaultTimeout(20000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  const fixture = JSON.parse(
    readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"),
  );
  await page.goto("/login");
  await page
    .getByLabel("Email address", { exact: true })
    .fill(fixture.integration_email);
  await page.getByLabel("Password", { exact: true }).fill(fixture.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(fixture.integration_org);
  await expect(
    page.getByRole("heading", { name: "Organization members" }),
  ).toBeVisible();
  const csrf = (await page.context().cookies()).find(
    (cookie) => cookie.name === "ppm_csrf",
  )!.value;
  const headers = {
    origin: process.env.PPM_WEB_URL!,
    "x-csrf-token": csrf,
    "x-organization-id": fixture.integration_org,
    "idempotency-key": crypto.randomUUID(),
  };
  async function create(kind: string, values: Record<string, unknown>) {
    const response = await page.request.post(`/api/v1/delivery/${kind}`, {
      headers: { ...headers, "idempotency-key": crypto.randomUUID() },
      data: { kind, name: kind, ...values },
    });
    expect(response.status(), await response.text()).toBe(201);
    return response.json();
  }
  await create("settings", { timezone: "Asia/Kolkata", currency: "INR" });
  const portfolio = await create("portfolios", {
    name: "Sprint 08 fixture portfolio",
  });
  const project = await create("projects", {
    name: "Sprint 08 import project",
    portfolio_id: portfolio.id,
    currency: "INR",
  });
  await page.goto("/integrations");
  await expect(
    page.getByRole("heading", { name: "Integrations & job activity" }),
  ).toBeVisible();
  await expect(
    page.getByText("No connections in your current scope."),
  ).toBeVisible();
  await page
    .getByLabel("Connection name", { exact: true })
    .fill("CSV browser fixture");
  await page
    .getByRole("combobox", { name: "Project", exact: true })
    .selectOption(project.id);
  const mapping = page.getByRole("textbox", {
    name: "Field mapping (target to source path)",
    exact: true,
  });
  const validMapping = await mapping.inputValue();
  await mapping.fill(
    JSON.stringify({
      external_id: "id",
      name: "id.title",
      source_updated_at: "updated_at",
    }),
  );
  const rejected = page.waitForResponse(
    (response) =>
      response.url().endsWith("/api/v1/integrations") &&
      response.request().method() === "POST",
  );
  await page
    .getByRole("button", { name: "Create connection", exact: true })
    .click();
  expect((await rejected).status()).toBe(422);
  await expect(
    page.getByRole("alert").filter({ hasText: "Request validation failed" }),
  ).toBeVisible();
  await expect(
    page.getByText("No connections in your current scope."),
  ).toBeVisible();
  await mapping.fill(validMapping);
  await page
    .getByRole("button", { name: "Create connection", exact: true })
    .click();
  await expect(
    page.getByRole("status").filter({ hasText: "Connection created" }),
  ).toBeVisible();
  const csv =
    "id,name,updated_at,status\n1,Imported release work,2026-10-09T00:00:00Z,backlog\n2,Invalid fixture row,2026-10-09T00:00:00Z,invalid";
  await page
    .getByRole("textbox", { name: "CSV source", exact: true })
    .fill(csv);
  const dashboard = await page.context().newPage();
  let snapshots = 0;
  dashboard.on("response", (response) => {
    if (response.url().includes("/command/snapshot") && response.ok())
      snapshots++;
  });
  await dashboard.goto("/command-center");
  await expect.poll(() => snapshots).toBeGreaterThan(0);
  const beforeSync = snapshots;
  await page.getByRole("button", { name: "Preview import" }).click();
  await expect(
    page.getByText("1 valid rows · 1 validation errors"),
  ).toBeVisible();
  await page.getByRole("button", { name: "Start sync" }).click();
  await expect(
    page.getByText("Processing finished", { exact: true }),
  ).toBeVisible({ timeout: 60000 });
  await expect(
    page.getByRole("region", { name: "Job progress" }),
  ).toContainText("partially succeeded");
  await expect(
    page.getByRole("list", { name: "Processing stages" }),
  ).toContainText("degraded");
  await expect
    .poll(() => snapshots, { timeout: 15000 })
    .toBeGreaterThan(beforeSync);
  await dashboard.close();
  const listing = await (
    await page.request.get("/api/v1/integrations/activity/jobs")
  ).json();
  const first = listing[0];
  const resumed = await page.request.get(
    `/api/v1/integrations/activity/jobs/${first.id}/events`,
    { headers: { "last-event-id": "1" } },
  );
  expect(resumed.status()).toBe(200);
  expect(await resumed.text()).not.toContain("id: 1\n");
  const repeated = await page.request.post(
    `/api/v1/integrations/${first.integration_id}/sync`,
    {
      headers: { ...headers, "idempotency-key": crypto.randomUUID() },
      data: { csv_text: csv },
    },
  );
  expect(repeated.status()).toBe(202);
  const repeatedId = (await repeated.json()).id;
  await expect
    .poll(
      async () =>
        (
          await (
            await page.request.get(
              `/api/v1/integrations/activity/jobs/${repeatedId}`,
            )
          ).json()
        ).status,
      { timeout: 60000 },
    )
    .toBe("partially_succeeded");
  const work = await (
    await page.request.get("/api/v1/delivery/work_items")
  ).json();
  expect(
    work.items.filter(
      (item: { data: { name: string } }) =>
        item.data.name === "Imported release work",
    ),
  ).toHaveLength(1);
  const sources = await (
    await page.request.get(
      `/api/v1/integrations/${first.integration_id}/sources`,
    )
  ).json();
  expect(sources).toHaveLength(1);
  expect(sources[0].source_updated_at).toContain("2026-10-09");
  for (const width of [1440, 768, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    const axe = await new AxeBuilder({ page }).analyze();
    expect(
      axe.violations.filter((violation) =>
        ["serious", "critical"].includes(violation.impact || ""),
      ),
    ).toEqual([]);
    await page.screenshot({
      path: `docs/verification/sprint-08-${width}.png`,
      fullPage: true,
    });
  }
  await page.getByLabel("Connection name", { exact: true }).focus();
  await page.keyboard.press("Tab");
  await expect(
    page.getByLabel("Source namespace", { exact: true }),
  ).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("searchbox", { name: "Find project", exact: true }),
  ).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("combobox", { name: "Project", exact: true }),
  ).toBeFocused();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(fixture.viewer_org);
  await expect(
    page.getByText("No connections in your current scope."),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Create connection", exact: true }),
  ).toHaveCount(0);
  expect(
    (
      await page.request.get(
        `/api/v1/integrations/activity/jobs/${first.id}/events`,
      )
    ).status(),
  ).toBe(404);
  expect(errors).toEqual([]);
});
