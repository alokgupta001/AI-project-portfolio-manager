import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync, writeFileSync } from "node:fs";

test("command center reconciles facts, filters, saved views and evidence access", async ({
  page,
}) => {
  test.setTimeout(150000);
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
  async function create(kind: string, values: Record<string, unknown>) {
    const r = await page.request.post(`/api/v1/delivery/${kind}`, {
      headers: {
        origin: process.env.PPM_WEB_URL!,
        "x-csrf-token": csrf,
        "x-organization-id": f.command_org,
        "idempotency-key": crypto.randomUUID(),
      },
      data: { kind, name: kind, ...values },
    });
    expect(r.status(), await r.text()).toBe(201);
    return r.json();
  }
  await create("settings", { timezone: "Asia/Kolkata", currency: "INR" });
  const portfolio = await create("portfolios", {
    name: "Command acceptance portfolio",
  });
  const empty = await create("portfolios", { name: "Empty filter portfolio" });
  const p = await create("projects", {
    name: "DEMO — green release with missed gate",
    portfolio_id: portfolio.id,
    currency: "INR",
    status: "active",
    reported_health: "Green",
    ledger_complete: true,
  });
  await create("budget_lines", {
    project_id: p.id,
    amount: "100000",
    currency: "INR",
    approved: true,
  });
  await create("expenditures", {
    project_id: p.id,
    amount: "25000",
    currency: "INR",
    spent_on: "2026-10-05",
  });
  await create("milestones", {
    name: "Critical security gate",
    project_id: p.id,
    due_date: "2026-09-01",
    critical: true,
  });
  await create("benefits", {
    name: "Hours saved",
    project_id: p.id,
    unit: "hours",
    target: "100",
    realized: "20",
    period_start: "2026-10-01",
    period_end: "2026-11-01",
  });
  const started = Date.now();
  await page.goto("/command-center");
  await expect(
    page.getByText("Health discrepancy", { exact: true }),
  ).toBeVisible();
  const renderedMs = Date.now() - started;
  await page.getByLabel("From date", { exact: true }).fill("2026-10-01");
  await page
    .getByLabel("To date (excluded)", { exact: true })
    .fill("2026-11-01");
  await expect(
    page.getByRole("button", {
      name: "Inspect INR Recorded spend",
      exact: true,
    }),
  ).toBeVisible();
  await page
    .getByRole("button", {
      name: "Inspect Overdue critical milestones",
      exact: true,
    })
    .click();
  const drawer = page.getByRole("dialog");
  await expect(drawer).toContainText("Critical security gate");
  await expect(drawer).toContainText(
    "Critical milestone overdue since 2026-09-01",
  );
  await page.keyboard.press("Escape");
  await expect(
    page.getByRole("button", {
      name: "Inspect Overdue critical milestones",
      exact: true,
    }),
  ).toBeFocused();
  await page.getByLabel("Portfolio", { exact: true }).selectOption(empty.id);
  await expect(
    page.getByRole("heading", { name: "No visible projects" }),
  ).toBeVisible();
  await page
    .getByLabel("Portfolio", { exact: true })
    .selectOption(portfolio.id);
  await expect(
    page.getByText("Health discrepancy", { exact: true }),
  ).toBeVisible();
  await page.getByLabel("New view name").fill("Release review");
  await page.getByRole("button", { name: "Save view", exact: true }).click();
  await expect(
    page.getByText("Personal view saved.", { exact: true }),
  ).toBeVisible();
  await page.reload();
  await page
    .getByLabel("Personal saved view")
    .selectOption({ label: "Release review" });
  await expect(page.getByLabel("Portfolio", { exact: true })).toHaveValue(
    portfolio.id,
  );
  await page.getByRole("button", { name: "Risk", exact: true }).click();
  await page.getByRole("button", { name: "Record risk", exact: true }).click();
  const dialog = page.getByRole("dialog");
  await dialog.getByLabel("Name", { exact: true }).fill("Release exposure");
  await dialog.getByLabel("Review date", { exact: true }).fill("2026-10-20");
  await dialog
    .getByRole("button", { name: "Save record", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Release exposure" }),
  ).toBeVisible();
  await expect(
    page.getByText(/Escalation preparation incomplete/),
  ).toBeVisible();
  await page.getByRole("button", { name: "Delivery", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Critical security gate" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Resource", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Assigned resource capacity" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Executive", exact: true }).click();
  await page.getByText("View chart data table", { exact: true }).click();
  const download = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export metric DTO" }).click();
  const dto = JSON.parse(
    readFileSync((await (await download).path())!, "utf8"),
  );
  expect(
    dto.totals.find((m: { key: string }) => m.key === "INR_spend").value,
  ).toBe("25000.00");
  expect(dto.projects[0].discrepancy).toBe(true);
  const measurements: Record<string, unknown> = {
    renderedMs,
    computeMs: dto.compute_ms,
    projects: dto.projects.length,
    profile:
      "Local Docker production Next build; Playwright Chromium; tiny isolated fixture; no performance compliance claim",
    navigation: await page.evaluate(() =>
      performance.getEntriesByType("navigation").map((n) => n.toJSON()),
    ),
    paint: await page.evaluate(() =>
      performance.getEntriesByType("paint").map((n) => n.toJSON()),
    ),
  };
  for (const width of [1440, 768, 360]) {
    await page.setViewportSize({ width, height: 1000 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    const axe = await new AxeBuilder({ page }).analyze();
    expect(
      axe.violations.filter((v) =>
        ["serious", "critical"].includes(v.impact || ""),
      ),
    ).toEqual([]);
    await page.screenshot({
      path: `docs/verification/${process.env.PPM_VERIFICATION_PREFIX || "sprint-07"}-${width}.png`,
      fullPage: true,
    });
  }
  writeFileSync(
    `docs/verification/${process.env.PPM_VERIFICATION_PREFIX || "sprint-07"}-rendering.json`,
    JSON.stringify(measurements, null, 2),
  );
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(f.viewer_org);
  await expect(
    page.getByRole("heading", { name: "No visible projects" }),
  ).toBeVisible();
  await expect(
    page.getByText("Health discrepancy", { exact: true }),
  ).toHaveCount(0);
  await expect(
    page
      .getByLabel("Personal saved view")
      .getByRole("option", { name: "Release review" }),
  ).toHaveCount(0);
});
