import { test, expect, type Locator } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFileSync } from "node:fs";

test("resource planning preserves split capacity, snapshots, privacy and responsive access", async ({
  page,
}) => {
  test.setTimeout(120000);
  test.skip(!process.env.PPM_IDENTITY_FIXTURE, "Use isolated browser runner");
  const f = JSON.parse(readFileSync(process.env.PPM_IDENTITY_FIXTURE!, "utf8"));
  await page.goto("/login");
  await page
    .getByLabel("Email address", { exact: true })
    .fill(f.capacity_email);
  await page.getByLabel("Password", { exact: true }).fill(f.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(f.capacity_org);
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
        "x-organization-id": f.capacity_org,
        "idempotency-key": crypto.randomUUID(),
      },
      data: { kind, name: kind, ...values },
    });
    expect(r.status(), await r.text()).toBe(201);
    return r.json();
  }
  await create("settings", { timezone: "America/New_York", currency: "USD" });
  const portfolio = await create("portfolios", { name: "Capacity portfolio" });
  const project = await create("projects", {
    name: "North project",
    portfolio_id: portfolio.id,
    currency: "USD",
  });
  const second = await create("projects", {
    name: "South project",
    portfolio_id: portfolio.id,
    currency: "USD",
  });
  await page.goto("/resources");
  await expect(
    page.getByRole("heading", { name: "Resource planning", exact: true }),
  ).toBeVisible();
  async function editor(
    kind: string,
    label: string,
    name: string,
  ): Promise<Locator> {
    await page
      .getByRole("combobox", { name: "Planning records", exact: true })
      .selectOption(kind);
    await page
      .getByRole("button", {
        name: `Create ${label.toLowerCase()}`,
        exact: true,
      })
      .click();
    const dialog = page.getByRole("dialog", {
      name: `Create ${label}`,
      exact: true,
    });
    await dialog.getByLabel("Name", { exact: true }).fill(name);
    return dialog;
  }
  async function save(dialog: Locator) {
    await dialog
      .getByRole("button", { name: "Save record", exact: true })
      .click();
    await expect(dialog).not.toBeVisible();
  }
  let dialog = await editor(
    "resources",
    "Resource profiles",
    "Alex — capacity fixture",
  );
  await save(dialog);
  await page
    .getByRole("combobox", { name: "Resource profile", exact: true })
    .selectOption({ label: "Alex — capacity fixture" });
  await page.getByLabel("From date", { exact: true }).fill("2026-03-09");
  await page
    .getByLabel("Until date (excluded)", { exact: true })
    .fill("2026-03-16");
  dialog = await editor("calendars", "Working calendars", "Half time New York");
  await dialog
    .getByLabel("IANA timezone", { exact: true })
    .fill("America/New_York");
  for (const day of ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    await dialog.getByLabel(`${day} hours`, { exact: true }).fill("4");
  await save(dialog);
  dialog = await editor("availability", "Availability", "2026 schedule");
  await dialog.getByLabel("Start date", { exact: true }).fill("2026-01-01");
  await dialog
    .getByLabel("End date (excluded)", { exact: true })
    .fill("2027-01-01");
  const calendarChoice = dialog.getByRole("combobox", {
    name: "Calendar version",
    exact: true,
  });
  await expect(
    calendarChoice
      .getByRole("option")
      .filter({ hasText: "Half time New York" }),
  ).toHaveCount(1);
  await calendarChoice.selectOption({
    label: (await calendarChoice
      .getByRole("option")
      .filter({ hasText: "Half time New York" })
      .textContent())!,
  });
  await save(dialog);
  for (const [id, name] of [
    [project.id, "North allocation"],
    [second.id, "South allocation"],
  ]) {
    dialog = await editor("allocations", "Allocations", name);
    await dialog.getByLabel("Start date", { exact: true }).fill("2026-03-09");
    await dialog
      .getByLabel("End date (excluded)", { exact: true })
      .fill("2026-03-16");
    await dialog
      .getByRole("combobox", { name: "Project", exact: true })
      .selectOption(id);
    await dialog
      .getByLabel("Hours per scheduled day", { exact: true })
      .fill("3");
    await save(dialog);
  }
  const metric = (label: string) =>
    page
      .locator(".metric-card")
      .filter({ has: page.getByText(label, { exact: true }) })
      .locator("strong");
  await expect(metric("Available hours")).toHaveText("20.00");
  await expect(metric("Allocated hours")).toHaveText("30.00");
  await expect(metric("Planned utilization %")).toHaveText("150.00");
  await expect(
    page.getByText("Sensitive effort is restricted", { exact: true }),
  ).toBeVisible();
  dialog = await editor("time_off", "Approved time off", "Approved leave");
  await dialog.getByLabel("Start date", { exact: true }).fill("2026-03-11");
  await dialog
    .getByLabel("End date (excluded)", { exact: true })
    .fill("2026-03-13");
  await dialog.getByLabel("Hours per scheduled day", { exact: true }).fill("4");
  await save(dialog);
  await expect(metric("Available hours")).toHaveText("12.00");
  await expect(metric("Excess hours")).toHaveText("18.00");
  dialog = await editor(
    "capacity_snapshots",
    "Allocation snapshots",
    "Approved allocation plan",
  );
  await dialog.getByLabel("Start date", { exact: true }).fill("2026-03-09");
  await dialog
    .getByLabel("End date (excluded)", { exact: true })
    .fill("2026-03-16");
  await save(dialog);
  await page
    .getByRole("button", { name: "View snapshot", exact: true })
    .click();
  await expect(
    page.getByRole("dialog").getByText("Captured daily plan", { exact: true }),
  ).toBeVisible();
  await page.keyboard.press("Escape");
  await page
    .getByRole("combobox", { name: "Planning records", exact: true })
    .selectOption("allocations");
  await expect(
    page.getByRole("rowheader", { name: /^North allocation/ }),
  ).toBeVisible();
  await page.reload();
  await page
    .getByRole("combobox", { name: "Resource profile", exact: true })
    .selectOption({ label: "Alex — capacity fixture" });
  await page.getByLabel("From date", { exact: true }).fill("2026-03-09");
  await page
    .getByLabel("Until date (excluded)", { exact: true })
    .fill("2026-03-16");
  await page
    .getByRole("combobox", { name: "Planning records", exact: true })
    .selectOption("allocations");
  await expect(metric("Excess hours")).toHaveText("18.00");
  expect(
    (
      await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
        .analyze()
    ).violations.map((v) => v.id),
  ).toEqual([]);
  await page.screenshot({
    path: "artifacts/local/sprint05-resources-desktop.png",
    fullPage: true,
  });
  await page.setViewportSize({ width: 360, height: 800 });
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth),
  ).toBeLessThanOrEqual(360);
  await page.screenshot({
    path: "artifacts/local/sprint05-resources-mobile.png",
    fullPage: true,
  });
  await page
    .getByRole("combobox", { name: "Organization", exact: true })
    .selectOption(f.viewer_org);
  await expect(
    page.getByText("Alex — capacity fixture", { exact: true }),
  ).toHaveCount(0);
  await expect(page.getByRole("button", { name: /^Create / })).toHaveCount(0);
});
